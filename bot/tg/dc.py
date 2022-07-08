from dataclasses import field

from marshmallow import EXCLUDE
from marshmallow_dataclass import dataclass


@dataclass
class MessageFrom:
    id: int
    first_name: str
    last_name: str | None = None
    username: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class Char:
    id: int
    type: str
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    title: str | None = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    message_id: int
    from_: MessageFrom = field(metadata={'date_key': 'from'})
    char: Char
    text: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: list[UpdateObj]

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE
