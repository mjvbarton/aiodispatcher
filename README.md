# aiodispatcher

[![PyPI version](https://img.shields.io/pypi/v/aiodispatcher)](https://pypi.org/project/aiodispatcher/)
[![Python version](https://img.shields.io/pypi/pyversions/aiodispatcher)](https://pypi.org/project/aiodispatcher/)
[![License](https://img.shields.io/github/license/mjvbarton/aiodispatcher)](https://github.com/mjvbarton/aiodispatcher/blob/main/LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/mjvbarton/aiodispatcher/ci.yml?label=CI)](https://github.com/mjvbarton/aiodispatcher/actions)

A lightweight Python library for concurrent async event dispatching.

## Requirements

- Python 3.14+

## Installation

```bash
pip install aiodispatcher
```

Or with `uv`:

```bash
uv add aiodispatcher
```

## Quick Start

```python
import asyncio
from aiodispatcher import Event, Signal, EventDispatcher

dispatcher = EventDispatcher()

@dispatcher.listen("user.created")
async def on_user_created(event: Event) -> None:
    print(f"User created: {event.context}")

async def main() -> None:
    await dispatcher.dispatch("user.created", Event({"user_id": "123"}))

asyncio.run(main())
```

## Core Concepts

### Events

Events are objects that carry a context payload. They are passed to all registered listeners when dispatched.

```python
from aiodispatcher import Event, Signal

# Event with context
class UserCreatedEvent(Event[dict]):
    pass

event = UserCreatedEvent({"user_id": "123", "email": "test@test.com"})
print(event.context)  # {"user_id": "123", "email": "test@test.com"}

# Signal — event with no context
signal = Signal()
print(signal.context)  # None
```

### Event Names

By default, event names are strings. You can use `enum.StrEnum` for type-safe event names:

```python
from enum import StrEnum
from aiodispatcher import EventDispatcher

class UserEvent(StrEnum):
    CREATED = "user.created"
    DELETED = "user.deleted"

dispatcher: EventDispatcher[UserEvent] = EventDispatcher()

@dispatcher.listen(UserEvent.CREATED)
async def on_user_created(event: Event) -> None:
    ...
```

You can also use `typing.Literal` for a fixed set of event names:

```python
from typing import Literal
from aiodispatcher import EventDispatcher

EventName = Literal["user.created", "user.deleted"]
dispatcher: EventDispatcher[EventName] = EventDispatcher()

@dispatcher.listen("user.created")
async def on_user_created(event: Event) -> None:
    ...
```

### Event Listeners

Event listeners are async functions that take an `Event` as their only argument:

```python
from aiodispatcher import Event, EventListener

async def on_user_created(event: Event) -> None:
    print(f"User created: {event.context}")
```

### EventDispatcher

The `EventDispatcher` class manages event listeners and dispatches events to them concurrently using `asyncio.gather`.

```python
from aiodispatcher import EventDispatcher, Event, Signal

dispatcher = EventDispatcher()

# Register a listener using the decorator
@dispatcher.listen("user.created")
async def on_user_created(event: Event) -> None:
    ...

# Or register manually
async def on_user_deleted(event: Event) -> None:
    ...

dispatcher.add_listener("user.deleted", on_user_deleted)

# Check if listeners are registered
dispatcher.has_listeners("user.created")  # True

# Get all listeners for an event
dispatcher.get_listeners("user.created")  # [on_user_created]

# Remove a listener
dispatcher.remove_listener("user.created", on_user_created)

# Dispatch an event
await dispatcher.dispatch("user.created", Signal())
```

## Error Handling

If any listener raises an exception during dispatching, an `EventDispatcherException` is raised **after all listeners have completed**. This ensures that all listeners are always invoked, even if some fail.

```python
from aiodispatcher import EventDispatcher, EventDispatcherException, Signal

dispatcher = EventDispatcher()

@dispatcher.listen("user.created")
async def failing_listener(event: Event) -> None:
    raise ValueError("Something went wrong")

@dispatcher.listen("user.created")
async def another_listener(event: Event) -> None:
    print("This will still be called!")

try:
    await dispatcher.dispatch("user.created", Signal())
except EventDispatcherException as exc:
    for listener_name, error in exc.errors.items():
        print(f"{listener_name}: {error}")
```

Output:

```bash
This will still be called!
failing_listener: Something went wrong
```

## API Reference

### `Event[Context]`

| Member              | Type      | Description                                |
|---------------------|-----------|--------------------------------------------|
| `context`           | `Context` | The event payload                          |
| `__init__(context)` | `None`    | Creates a new event with the given context |

### `Signal`

A special event with no context (`Event[None]`). Use for simple notifications.

### `EventDispatcher[TEventName]`

| Method | Description |
|---|---|
| `add_listener(event_name, listener)` | Registers a listener. Raises `TypeError` if not async, `ValueError` if already registered |
| `remove_listener(event_name, listener)` | Unregisters a listener. Raises `ValueError` if not registered |
| `has_listeners(event_name)` | Returns `True` if listeners exist for the event name |
| `get_listeners(event_name)` | Returns list of listeners. Raises `ValueError` if none registered |
| `listen(event_name)` | Decorator for registering listeners |
| `dispatch(event_name, event)` | Dispatches event to all listeners concurrently |

### `EventDispatcherException`

| Member | Type | Description |
|---|---|---|
| `errors` | `dict[str, Exception]` | Maps listener names to their exceptions |

## Type Aliases

| Alias | Type | Description |
|---|---|---|
| `EventListener` | `Callable[[Event], Coroutine[Any, Any, None]]` | An async event listener function |
| `EventListenerMap` | `dict[str, list[EventListener]]` | Maps event names to their listeners |
| `ListenerErrors` | `dict[str, Exception]` | Maps listener names to their exceptions |
| `TEventName` | `str` | Type alias for event names |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

All notable changes to this project will be documented in the [CHANGELOG.md](CHANGELOG.md) file.
