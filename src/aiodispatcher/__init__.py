import asyncio
import inspect
from abc import ABC
from collections.abc import Callable, Coroutine
from typing import Any


class Event[Context = Any](ABC):
    """
    A generic event class that can carry any type of context.

    This allows for flexible event definitions where the context can be of any type,
    such as a dictionary, a custom dataclass, or any other Python object.
    """

    context: Context

    def __init__(self, context: Context) -> None:
        self.context = context


class Signal(Event[None]):
    """
    A special type of event that does not carry any context. It can be used for simple
    signals or notifications where no additional data is needed.
    """

    def __init__(self) -> None:
        super().__init__(context=None)


type EventListener = Callable[[Event], Coroutine[Any, Any, None]]
"""
A type alias for event listener functions. An event listener is a callable that takes an
event as an argument and returns a coroutine that performs the handling logic.
"""

type TEventName = str
"""
A type alias for event names. This allows for type-safe event name definitions
in the dispatcher.

By default, event names are expected to be strings, but this can be extended to other
types if needed such as `enum.Enum` or `typing.Literal` for more structured
event naming.
"""

type EventListenerMap = dict[str, list[EventListener]]
"""
A type alias for the mapping of event names to their corresponding listeners. This
dictionary maps each event name (as a string) to a list of event listeners that should
be invoked when that event is dispatched.
"""

type ListenerErrors = dict[str, Exception]
"""
A type alias for a dictionary that maps listener names to exceptions. This is used to
store information about which listeners failed during event dispatching and their
respective exceptions. This allows for detailed error reporting when multiple listeners
fail.
"""


class EventDispatcherException(Exception):
    """
    An exception class for handling errors that occur during event dispatching.

    If any of the listeners raise an exception while handling an event, an instance of
    this class is raised containing details about which listeners failed and their
    respective exceptions.
    """

    errors: ListenerErrors
    """
    A dictionary mapping listener names to the exceptions they raised during event
    handling. This allows for detailed error reporting when multiple listeners fail.
    """

    def __init__(self, errors: ListenerErrors) -> None:
        self.errors = errors
        formatted_errors = "\n".join(
            f" - {listener}: ({type(error).__name__}) {error}"
            for listener, error in errors.items()
        )
        super().__init__(f"One or more event listeners failed:\n{formatted_errors}")

    @staticmethod
    def handle_dispatcher_results(
        listeners: list[EventListener], results: list[Any]
    ) -> None:
        """
        A helper method to process the results of dispatched event listeners.

        It checks the results for any exceptions and raises an
        `EventDispatcherException` if any listeners failed.

        Args:
            listeners (list[EventListener]): The list of listeners that were invoked.
            results (list[Any]): The list of results returned by the listeners, which
            may include exceptions if any listener failed.

        Raises:
            EventDispatcherException: If any of the listeners raised an exception, this
            method will raise an `EventDispatcherException` containing details about
            the failures.
        """
        errors: ListenerErrors = {}
        for listener, result in zip(listeners, results, strict=True):
            if isinstance(result, Exception):
                errors[listener.__name__] = result
        if errors:
            raise EventDispatcherException(errors)


class EventDispatcher[TEventName: str = str]:
    """
    A class responsible for managing event listeners and dispatching events to them.
    It allows for adding, removing, and checking listeners for specific event names,
    as well as dispatching events to all registered listeners for a given event name.
    """

    _listeners: EventListenerMap

    def __init__(self) -> None:
        self._listeners: EventListenerMap = {}

    def add_listener(self, event_name: TEventName, listener: EventListener) -> None:
        """
        Registers a new event listener for a specific event name.

        Args:
            event_name (TEventName): The name of the event to listen for.
            listener (EventListener): The async function that will be called when the
            event is dispatched.

        Raises:
            TypeError: If the provided listener is not an async function.
            ValueError: If the listener is already registered for the specified event
            name.
        """
        if not inspect.iscoroutinefunction(listener):
            raise TypeError(f"Listener {listener} must be an async function")
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        if listener in self._listeners[event_name]:
            raise ValueError(
                f"Listener {listener} is already registered for event '{event_name}'"
            )
        self._listeners[event_name].append(listener)

    def remove_listener(self, event_name: TEventName, listener: EventListener) -> None:
        """
        Unregisters an event listener from a specific event name.

        Args:
            event_name (TEventName): The name of the event to stop listening for.
            listener (EventListener): The async function that will no longer be called
            when the event is dispatched.
        """
        if event_name in self._listeners and listener in self._listeners[event_name]:
            self._listeners[event_name].remove(listener)
            if not self._listeners[event_name]:  # Clean up empty listener lists
                del self._listeners[event_name]
        else:
            raise ValueError(
                f"Listener {listener} is not registered for event '{event_name}'"
            )

    def has_listeners(self, event_name: TEventName) -> bool:
        """
        Checks if there are any listeners registered for a specific event name.

        Args:
            event_name (TEventName): The name of the event to check for listeners.

        Returns:
            bool: `True` if there are listeners registered for the event name,
            `False` otherwise.
        """
        return event_name in self._listeners and bool(self._listeners[event_name])

    def get_listeners(self, event_name: TEventName) -> list[EventListener]:
        """
        Retrieves the list of listeners registered for a specific event name.

        Args:
            event_name (TEventName): The name of the event to retrieve listeners for.

        Returns:
            list[EventListener]: A list of event listeners registered for the
            event name.

        Raises:
            ValueError: If the specified event name does not exist in the dispatcher.
        """
        if event_name not in self._listeners or not self._listeners[event_name]:
            raise ValueError(f"No listeners registered for event '{event_name}'")
        return self._listeners.get(event_name, [])

    def listen(self, event_name: TEventName) -> Callable[..., EventListener]:
        """
        A decorator method for registering event listeners. This allows for a more
        convenient syntax when defining event listeners.

        Args:
            event_name (TEventName): The name of the event to listen for.

        Returns:
            Callable[..., EventListener]: A decorator function that takes an event
            listener and registers it for the specified event name.
        """

        def decorator(listener: EventListener) -> EventListener:
            self.add_listener(event_name, listener)
            return listener

        return decorator

    async def dispatch(self, event_name: TEventName, event: Event) -> None:
        """
        Dispatches an event to all registered listeners for a specific event name.

        Args:
            event_name (TEventName): The name of the event to dispatch.
            event (Event): The event object to pass to the listeners.

        Raises:
            ValueError: If there are no listeners for the specified event name.
            EventDispatcherException: If any of the listeners raise an exception during
            event handling, an `EventDispatcherException` will be raised containing
            details about which listeners failed and their respective exceptions.
        """
        listeners = self.get_listeners(event_name)

        results = await asyncio.gather(
            *(listener(event) for listener in listeners),
            return_exceptions=True,
        )
        EventDispatcherException.handle_dispatcher_results(listeners, results)


__all__ = [
    "Event",
    "Signal",
    "EventListener",
    "EventListenerMap",
    "ListenerErrors",
    "TEventName",
    "EventDispatcherException",
    "EventDispatcher",
]
