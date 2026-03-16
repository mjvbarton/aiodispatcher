import pytest

from aiodispatcher import Event, EventDispatcher


def test_listen_decorator_returns_original_listener(
    dispatcher: EventDispatcher,
) -> None:
    event_name = "test_event"

    @dispatcher.listen(event_name)
    async def decorated_listener(event: Event) -> None:
        pass

    assert len(dispatcher._listeners) == 1
    assert dispatcher._listeners[event_name][0] == decorated_listener
    assert callable(dispatcher._listeners[event_name][0])
    assert decorated_listener.__name__ == "decorated_listener"


def test_listen_decorator_registers_same_listener_for_multiple_events(
    dispatcher: EventDispatcher,
) -> None:
    event_name_1 = "test_event_1"
    event_name_2 = "test_event_2"

    @dispatcher.listen(event_name_1)
    @dispatcher.listen(event_name_2)
    async def decorated_listener(event: Event) -> None:
        pass

    assert len(dispatcher._listeners) == 2
    assert decorated_listener in dispatcher._listeners[event_name_1]
    assert decorated_listener in dispatcher._listeners[event_name_2]


def test_listen_decorator_raises_error_for_sync_listener(
    dispatcher: EventDispatcher,
) -> None:
    event_name = "test_event"

    with pytest.raises(TypeError):

        @dispatcher.listen(event_name)
        def sync_listener(event: Event) -> None:
            pass
