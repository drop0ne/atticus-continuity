import hashlib, json, tempfile, unittest
from pathlib import Path
from reference.source_integrity.verify import VerificationError, sha256_file, verify_file, verify_manifest
class SourceIntegrityTests(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def _write(self,rel,data):
        p=self.root/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data); return p
    def test_sha256_file_known_bytes(self):
        p=self._write("a.bin",b"abc"); d,s=sha256_file(p,chunk_size=2); self.assertEqual(d,hashlib.sha256(b"abc").hexdigest()); self.assertEqual(s,3)
    def test_verify_file_pass(self):
        data=b"ATTICUS\x00PAC"; p=self._write("source.bin",data); r=verify_file(p,hashlib.sha256(data).hexdigest(),len(data)); self.assertTrue(r.ok); self.assertTrue(r.sha256_match); self.assertTrue(r.size_match)
    def test_verify_file_hash_mismatch_fails(self):
        p=self._write("source.bin",b"x"); r=verify_file(p,"0"*64,1); self.assertFalse(r.ok); self.assertFalse(r.sha256_match); self.assertTrue(r.size_match)
    def test_verify_file_size_mismatch_fails(self):
        data=b"xyz"; p=self._write("source.bin",data); r=verify_file(p,hashlib.sha256(data).hexdigest(),4); self.assertFalse(r.ok); self.assertTrue(r.sha256_match); self.assertFalse(r.size_match)
    def test_missing_file_fails_closed(self):
        r=verify_file(self.root/"missing.bin","0"*64); self.assertFalse(r.ok); self.assertEqual(r.status,"FAIL")
    def test_invalid_digest_rejected(self):
        p=self._write("a",b"a")
        with self.assertRaises(VerificationError): verify_file(p,"not-a-digest")
    def test_manifest_pass(self):
        self._write("files/a",b"a"); self._write("files/b",b"bb")
        m={"schema_version":"1.0","artifacts":[{"path":"files/a","sha256":hashlib.sha256(b"a").hexdigest(),"size_bytes":1},{"path":"files/b","sha256":hashlib.sha256(b"bb").hexdigest(),"size_bytes":2}]}; mp=self.root/"manifest.json"; mp.write_text(json.dumps(m)); s=verify_manifest(mp); self.assertEqual(s["status"],"PASS"); self.assertEqual(s["passed"],2)
    def test_manifest_detects_failure(self):
        self._write("a",b"a"); mp=self.root/"manifest.json"; mp.write_text(json.dumps({"schema_version":"1.0","artifacts":[{"path":"a","sha256":"0"*64,"size_bytes":1}]})); s=verify_manifest(mp); self.assertEqual(s["status"],"FAIL"); self.assertEqual(s["failed"],1)
    def test_manifest_path_escape_rejected(self):
        outside=self.root.parent/"outside-source-integrity-test"; outside.write_bytes(b"x")
        try:
            mp=self.root/"manifest.json"; mp.write_text(json.dumps({"schema_version":"1.0","artifacts":[{"path":"../outside-source-integrity-test","sha256":hashlib.sha256(b"x").hexdigest()}]}))
            with self.assertRaises(VerificationError): verify_manifest(mp)
        finally: outside.unlink(missing_ok=True)
    def test_manifest_duplicate_path_rejected(self):
        self._write("a",b"a"); d=hashlib.sha256(b"a").hexdigest(); mp=self.root/"manifest.json"; mp.write_text(json.dumps({"schema_version":"1.0","artifacts":[{"path":"a","sha256":d},{"path":"a","sha256":d}]}))
        with self.assertRaises(VerificationError): verify_manifest(mp)
if __name__=="__main__": unittest.main()
