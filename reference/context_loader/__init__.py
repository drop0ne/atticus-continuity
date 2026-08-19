"""Provider-neutral ATTICUS continuity hydration reference implementation."""

from .adapter import (
    AdapterLoadResult,
    FilesystemMetadataAdapter,
    MetadataAdapterError,
    MetadataSource,
)
from .checkpoint import CheckpointWritePlan, CheckpointWriteReceipt, CheckpointWriter
from .loader import (
    CheckpointValidator,
    Diagnostic,
    HydrationPlan,
    MappingRepository,
    PortableContextLoader,
    ValidationResult,
)

__all__ = [
    "AdapterLoadResult",
    "CheckpointValidator",
    "CheckpointWritePlan",
    "CheckpointWriteReceipt",
    "CheckpointWriter",
    "Diagnostic",
    "FilesystemMetadataAdapter",
    "HydrationPlan",
    "MappingRepository",
    "MetadataAdapterError",
    "MetadataSource",
    "PortableContextLoader",
    "ValidationResult",
]
