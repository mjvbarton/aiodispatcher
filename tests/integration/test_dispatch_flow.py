from dataclasses import dataclass
from typing import Literal

from aiodispatcher import Event, EventDispatcher


@dataclass(frozen=True)
class UserContext:
    """A simple user context dataclass for testing purposes."""

    user_id: int
    username: str


class UserCreatedEvent(Event[UserContext]):
    """An event that represents the creation of a user, carrying a UserContext."""

    def __init__(self, context: UserContext) -> None:
        super().__init__(context=context)


type UserEvents = Literal["user.created", "user.updated", "user.deleted"]


async def test_dispatch_with_custom_context(
    dispatcher: EventDispatcher,
) -> None:
    event_name = "user_created"
    received_contexts: list[UserContext] = []

    @dispatcher.listen(event_name)
    async def user_created_listener(event: Event[UserContext]) -> None:
        received_contexts.append(event.context)

    user_id = 123
    username = "test_user"
    event = UserCreatedEvent(context=UserContext(user_id=user_id, username=username))
    await dispatcher.dispatch(event_name, event)

    assert len(received_contexts) == 1
    assert received_contexts[0].user_id == user_id
    assert received_contexts[0].username == username


async def test_dispatch_with_literal_event_names() -> None:
    dispatcher = EventDispatcher[UserEvents]()
    received_events: list[str] = []

    @dispatcher.listen("user.created")
    async def user_created_listener(event: Event[UserContext]) -> None:
        received_events.append("user.created")

    @dispatcher.listen("user.updated")
    async def user_updated_listener(event: Event[UserContext]) -> None:
        received_events.append("user.updated")

    @dispatcher.listen("user.deleted")
    async def user_deleted_listener(event: Event[UserContext]) -> None:
        received_events.append("user.deleted")

    await dispatcher.dispatch(
        "user.created", UserCreatedEvent(context=UserContext(1, "user1"))
    )
    await dispatcher.dispatch(
        "user.updated", UserCreatedEvent(context=UserContext(1, "user1_updated"))
    )
    await dispatcher.dispatch(
        "user.deleted", UserCreatedEvent(context=UserContext(1, "user1_deleted"))
    )
