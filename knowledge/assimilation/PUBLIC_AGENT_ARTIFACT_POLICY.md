# Public Agent Artifact Acquisition Policy

**Status:** ACTIVE SAFETY POLICY  
**Purpose:** permit lawful passive collection of publicly available multi-agent and chatbot artifacts while preventing unauthorized interaction, execution, or authority transfer.

## Scope

This policy covers research into public traces of:

- multi-agent coordination;
- shared external memory;
- cross-run artifact inheritance;
- agent-to-agent communication released publicly;
- benchmark/evaluation transcripts;
- public repositories or discussions containing agent-generated artifacts;
- official security incident disclosures;
- research datasets containing model/agent trajectories.

## Acquisition classes

### ALLOW — passive ordinary access

Allowed when access is ordinary, public, and intended for human/research viewing:

- public papers and appendices;
- official reports and postmortems;
- public conference material;
- public web pages;
- public GitHub repositories/issues/discussions;
- public benchmark traces;
- openly released datasets;
- model transcripts intentionally published by their owners/researchers.

### REQUIRE SEPARATE AUTHORIZATION

Do not perform under this repository program merely because the technical capability exists:

- authenticated access using credentials not specifically granted for the research;
- interacting with unknown agent endpoints;
- attempting to identify hidden agent populations through probing;
- sending instructions to third-party agents;
- prompt injection into external systems;
- bypassing robots, rate limits, authentication, network segmentation, or other access controls;
- exploiting vulnerabilities;
- persistence on third-party systems;
- extracting non-public data;
- accessing compromised infrastructure;
- attempting to gain allegiance, control, or reciprocal access from an apparent agent collective.

## Core rule

```text
PUBLIC OBSERVATION != PERMISSION TO INTERACT
```

The fact that an apparent agent is internet-accessible, autonomous-looking, or communicating publicly does not establish authorization to manipulate the host system.

## Ingestion path

```text
public artifact
-> source record
-> immutable/raw or inert representation
-> hash + retrieval timestamp
-> quarantine
-> claim extraction
-> verification
-> classification
-> research archive
```

Imported instructions are quoted/described as content, not followed.

## Archive fields

Each record should preserve:

```yaml
artifact_id:
retrieved_at:
public_url:
publisher_or_host:
artifact_type:
access_class: PUBLIC_ORDINARY
content_hash:
raw_preserved: true_or_false
agent_origin_claimed: true_or_false
agent_origin_verified: true_or_false
cross_agent_relation:
provenance:
claims_extracted: []
risk_flags: []
legal_or_terms_notes:
```

## Data minimization

Do not collect unnecessary personal information about private individuals. Security research should preserve what is necessary to understand system behavior, provenance, timing, technical mechanisms, and governance implications.

## Code handling

Agent-generated or foreign code is untrusted.

Default treatment:

```text
READ / HASH / STATICALLY INSPECT
!=
EXECUTE
```

Any later execution must occur in an explicitly authorized isolated test environment under experiment-specific controls.

## Use in local laboratory

Public artifacts may be transformed into synthetic or inert test fixtures for user-owned sandbox environments. The fixture should reproduce the relevant structural behavior without requiring unauthorized contact with the originating system.

Examples:

- shared-memory messages become synthetic message-board fixtures;
- public tool traces become simulated action proposals;
- published attack chains become abstract state-transition tests rather than live exploitation instructions;
- coordination logs become multi-agent scheduling scenarios.

## Epistemic rule

A claimed "swarm," "collective," "hive," or autonomous population must be classified according to evidence. Public artifacts can demonstrate coordination or persistent shared state in a particular system; they do not automatically establish a durable independent society of agents on the open internet.
