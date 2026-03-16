import pytest

from aiodispatcher import (
    Event,
    EventDispatcher,
    EventDispatcherException,
    EventListener,
    Signal,
)


async def test_dispatch_calls_all_listeners_and_aggregates_results(
    dispatcher: EventDispatcher,
    signal: Signal,
) -> None:
    event_name = "test_event"
    result_set: set[str] = set()

    @dispatcher.listen(event_name)
    async def listener_1(_: Event) -> None:
        result_set.add("listener_1")

    @dispatcher.listen(event_name)
    async def listener_2(_: Event) -> None:
        result_set.add("listener_2")

    @dispatcher.listen("not_dispatched_event")
    async def listener_3(_: Event) -> None:
        result_set.add("listener_3")

    await dispatcher.dispatch(event_name, signal)
    assert "listener_1" in result_set
    assert "listener_2" in result_set
    assert "listener_3" not in result_set


async def test_dispatch_raises_aggregated_exception_for_failed_listeners(
    dispatcher: EventDispatcher,
    passing_listener_1: EventListener,
    passing_listener_2: EventListener,
    failing_listener_1: EventListener,
    failing_listener_2: EventListener,
    signal: Signal,
) -> None:
    event_name = "test_event"
    dispatcher.add_listener(event_name, passing_listener_1)
    dispatcher.add_listener(event_name, failing_listener_1)
    dispatcher.add_listener(event_name, passing_listener_2)
    dispatcher.add_listener(event_name, failing_listener_2)

    with pytest.raises(EventDispatcherException) as exc_info:
        await dispatcher.dispatch(event_name, signal)

    assert len(exc_info.value.errors) == 2
    assert "failing_listener_1" in exc_info.value.errors
    assert "failing_listener_2" in exc_info.value.errors
    assert isinstance(exc_info.value.errors["failing_listener_1"], ValueError)
    assert isinstance(exc_info.value.errors["failing_listener_2"], RuntimeError)


async def test_dispatch_raises_error_for_nonexistent_event_name(
    dispatcher: EventDispatcher,
    signal: Signal,
) -> None:
    with pytest.raises(ValueError):
        await dispatcher.dispatch("non_existent_event", signal)


async def test_dispatch_raises_error_for_event_name_with_no_listeners(
    dispatcher: EventDispatcher,
    signal: Signal,
) -> None:
    event_name = "test_event"
    dispatcher._listeners[
        event_name
    ] = []  # Manually add an event name with no listeners

    with pytest.raises(ValueError):
        await dispatcher.dispatch(event_name, signal)
