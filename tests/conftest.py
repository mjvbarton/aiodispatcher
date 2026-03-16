import pytest

from aiodispatcher import Event, EventDispatcher, EventListener, Signal


@pytest.fixture
def dispatcher() -> EventDispatcher:
    """A fixture that provides a fresh instance of `EventDispatcher` for each test."""

    return EventDispatcher()


@pytest.fixture
def signal() -> Signal:
    """A fixture that provides a simple `Signal` instance for testing."""

    return Signal()


@pytest.fixture
def passing_listener_1() -> EventListener:
    """A simple valid event listener that can be used in tests."""

    async def listener(event: Event) -> None:
        print("Listener 1 received event:", event)

    listener.__name__ = "passing_listener_1"
    return listener


@pytest.fixture
def passing_listener_2() -> EventListener:
    """A simple valid event listener that can be used in tests."""

    async def listener(event: Event) -> None:
        print("Listener 2 received event:", event)

    listener.__name__ = "passing_listener_2"
    return listener


@pytest.fixture
def failing_listener_1() -> EventListener:
    """A simple event listener that raises an exception to simulate a failure."""

    async def listener(event: Event) -> None:
        raise ValueError("Listener 1 failed")

    listener.__name__ = "failing_listener_1"
    return listener


@pytest.fixture
def failing_listener_2() -> EventListener:
    """A simple event listener that raises an exception to simulate a failure."""

    async def listener(event: Event) -> None:
        raise RuntimeError("Listener 2 failed")

    listener.__name__ = "failing_listener_2"
    return listener


@pytest.fixture
def sync_listener() -> EventListener:
    """
    A simple event listener that raises an exception synchronously to simulate a
    failure.
    """

    def listener(event: Event) -> None:
        raise Exception("Synchronous listener failed")

    listener.__name__ = "sync_listener"
    return listener  # type: ignore[return-value]
