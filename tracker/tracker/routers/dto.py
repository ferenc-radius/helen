from datetime import datetime
from pydantic import BaseModel, Field, IPvAnyAddress


def IpField(**kwargs) -> Field:
    return Field(title="IP address ipv4 or ipv6", **kwargs)


def PortField(**kwargs) -> Field:
    return Field(title="Port number", ge=1024, le=49151, **kwargs)


class NodeResponse(BaseModel):
    uid: str
    ip: IPvAnyAddress = IpField()
    port: int = PortField()
    last_seen: datetime


class NodeRequestBody(BaseModel):
    ip: IPvAnyAddress = IpField()
    port: int = PortField()


class VersionInfoResponse(BaseModel):
    version: str


class StatusResponse(BaseModel):
    status: str
