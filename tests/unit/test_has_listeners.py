from aiodispatcher import EventDispatcher, EventListener


def test_has_listeners_returns_false_for_nonexistent_event_name(
    dispatcher: EventDispatcher,
) -> None:
    assert not dispatcher.has_listeners("non_existent_event")


def test_has_listeners_returns_false_for_event_name_with_no_listeners(
    dispatcher: EventDispatcher,
) -> None:
    event_name = "test_event"
    dispatcher._listeners[
        event_name
    ] = []  # Manually add an event name with no listeners

    assert not dispatcher.has_listeners(event_name)


def test_has_listeners_returns_true_for_event_name_with_listeners(
    dispatcher: EventDispatcher,
    passing_listener_1: EventListener,
) -> None:
    event_name = "test_event"
    dispatcher._listeners[event_name] = [passing_listener_1]

    assert dispatcher.has_listeners(event_name)
