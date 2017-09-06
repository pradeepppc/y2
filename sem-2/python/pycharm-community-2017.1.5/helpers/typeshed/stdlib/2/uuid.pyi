from typing import Any, Tuple, Optional

_int = int

class UUID:
    def __init__(self, hex: Optional[str] = ..., bytes: Optional[str] = ...,
                 bytes_le: Optional[str] = ...,
                 fields: Optional[Tuple[int, int, int, int, int, int]] = ...,
                 int: Optional[int] = ...,
                 version: Optional[int] = ...) -> None: ...
    int = ...  # type: _int
    def get_bytes(self) -> _int: ...
    bytes = ...  # type: str
    def get_bytes_le(self) -> str: ...
    bytes_le = ...  # type: str
    def get_fields(self) -> Tuple[_int, _int, _int, _int, _int, _int]: ...
    fields = ...  # type: Tuple[_int, _int, _int, _int, _int, _int]
    def get_time_low(self) -> _int: ...
    time_low = ...  # type: _int
    def get_time_mid(self) -> _int: ...
    time_mid = ...  # type: _int
    def get_time_hi_version(self) -> _int: ...
    time_hi_version = ...  # type: _int
    def get_clock_seq_hi_variant(self) -> _int: ...
    clock_seq_hi_variant = ...  # type: _int
    def get_clock_seq_low(self) -> _int: ...
    clock_seq_low = ...  # type: _int
    def get_time(self) -> _int: ...
    time = ...  # type: _int
    def get_clock_seq(self) -> _int: ...
    clock_seq = ...  # type: _int
    def get_node(self) -> _int: ...
    node = ...  # type: _int
    def get_hex(self) -> str: ...
    hex = ...  # type: str
    def get_urn(self) -> str: ...
    urn = ...  # type: str
    def get_variant(self) -> _int: ...
    variant = ...  # type: _int
    def get_version(self) -> _int: ...
    version = ...  # type: _int

RESERVED_NCS = ...  # type: int
RFC_4122 = ...  # type: int
RESERVED_MICROSOFT = ...  # type: int
RESERVED_FUTURE = ...  # type: int

def getnode() -> int: ...
def uuid1(node: int = ..., clock_seq: int = ...) -> UUID: ...
def uuid3(namespace: UUID, name: str) -> UUID: ...
def uuid4() -> UUID: ...
def uuid5(namespace: UUID, name: str) -> UUID: ...

NAMESPACE_DNS = ...  # type: UUID
NAMESPACE_URL = ...  # type: UUID
NAMESPACE_OID = ...  # type: UUID
NAMESPACE_X500 = ...  # type: UUID