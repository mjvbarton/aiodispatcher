import pytest

from aiodispatcher import EventDispatcher, EventListener


def test_get_listeners_raises_error_for_nonexistent_event_name(
    dispatcher: EventDispatcher,
) -> None:
    with pytest.raises(ValueError):
        dispatcher.get_listeners("non_existent_event")


def test_get_listeners_raises_error_for_event_name_with_no_listeners(
    dispatcher: EventDispatcher,
) -> None:
    event_name = "test_event"
    dispatcher._listeners[
        event_name
    ] = []  # Manually add an event name with no listeners

    with pytest.raises(ValueError):
        dispatcher.get_listeners(event_name)


def test_get_listeners_returns_list_of_listeners_for_event_name(
    dispatcher: EventDispatcher,
    passing_listener_1: EventListener,
    passing_listener_2: EventListener,
) -> None:
    event_name = "test_event"
    dispatcher._listeners[event_name] = [passing_listener_1, passing_listener_2]

    listeners = dispatcher.get_listeners(event_name)

    assert len(listeners) == 2
    assert passing_listener_1 in listeners
    assert passing_listener_2 in listeners
