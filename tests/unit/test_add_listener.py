import pytest

from aiodispatcher import EventDispatcher, EventListener


def test_add_listener_adds_one_listener_for_one_event(
    dispatcher: EventDispatcher, passing_listener_1: EventListener
) -> None:
    event_name = "test_event"
    dispatcher.add_listener(event_name, passing_listener_1)

    assert len(dispatcher._listeners) == 1
    assert dispatcher._listeners[event_name][0] == passing_listener_1


def test_add_listener_adds_multiple_listeners_for_one_event(
    dispatcher: EventDispatcher,
    passing_listener_1: EventListener,
    passing_listener_2: EventListener,
) -> None:
    event_name = "test_event"
    dispatcher.add_listener(event_name, passing_listener_1)
    dispatcher.add_listener(event_name, passing_listener_2)

    assert len(dispatcher._listeners[event_name]) == 2
    assert passing_listener_1 in dispatcher._listeners[event_name]
    assert passing_listener_2 in dispatcher._listeners[event_name]


def test_add_listener_adds_multiple_listeners_for_multiple_events(
    dispatcher: EventDispatcher,
    passing_listener_1: EventListener,
    passing_listener_2: EventListener,
) -> None:
    event_name_1 = "test_event_1"
    event_name_2 = "test_event_2"
    dispatcher.add_listener(event_name_1, passing_listener_1)
    dispatcher.add_listener(event_name_1, passing_listener_2)
    dispatcher.add_listener(event_name_2, passing_listener_2)

    assert len(dispatcher._listeners) == 2
    assert passing_listener_1 in dispatcher._listeners[event_name_1]
    assert passing_listener_2 in dispatcher._listeners[event_name_1]
    assert passing_listener_1 not in dispatcher._listeners[event_name_2]
    assert passing_listener_2 in dispatcher._listeners[event_name_2]


def test_add_listener_raises_error_for_non_callable_listener(
    dispatcher: EventDispatcher, sync_listener: EventListener
) -> None:
    with pytest.raises(TypeError):
        dispatcher.add_listener("test_event", sync_listener)


def test_add_listener_raises_error_for_duplicate_listener(
    dispatcher: EventDispatcher, passing_listener_1: EventListener
) -> None:
    event_name = "test_event"
    dispatcher.add_listener(event_name, passing_listener_1)
    with pytest.raises(ValueError):
        dispatcher.add_listener(event_name, passing_listener_1)
