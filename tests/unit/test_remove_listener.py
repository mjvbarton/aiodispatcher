import pytest

from aiodispatcher import EventDispatcher, EventListener


def test_remove_listener_removes_only_specified_listener(
    dispatcher: EventDispatcher,
    passing_listener_1: EventListener,
    passing_listener_2: EventListener,
) -> None:
    event_name = "test_event"
    dispatcher.add_listener(event_name, passing_listener_1)
    dispatcher.add_listener(event_name, passing_listener_2)

    dispatcher.remove_listener(event_name, passing_listener_1)

    assert len(dispatcher._listeners) == 1
    assert dispatcher._listeners[event_name][0] == passing_listener_2
    assert passing_listener_1 not in dispatcher._listeners[event_name]


def test_remove_listener_cleans_up_empty_event_name(
    dispatcher: EventDispatcher,
    passing_listener_1: EventListener,
) -> None:
    event_name = "test_event"
    dispatcher.add_listener(event_name, passing_listener_1)

    dispatcher.remove_listener(event_name, passing_listener_1)
    assert event_name not in dispatcher._listeners


def test_remove_listener_raises_error_for_nonexistent_listener(
    dispatcher: EventDispatcher,
    passing_listener_1: EventListener,
    passing_listener_2: EventListener,
) -> None:
    event_name = "test_event"
    dispatcher.add_listener(event_name, passing_listener_1)

    with pytest.raises(ValueError):
        dispatcher.remove_listener(event_name, passing_listener_2)


def test_remove_listener_raises_error_for_nonexistent_event_name(
    dispatcher: EventDispatcher,
    passing_listener_1: EventListener,
) -> None:
    event_name = "test_event"
    non_existent_event_name = "non_existent_event"
    dispatcher.add_listener(event_name, passing_listener_1)

    with pytest.raises(ValueError):
        dispatcher.remove_listener(non_existent_event_name, passing_listener_1)
