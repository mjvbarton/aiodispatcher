# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-16

### Added

- `Event[Context]` — generic base class for events with typed context
- `Signal` — a context-free event for simple notifications
- `EventDispatcher[TEventName]` — generic async event dispatcher
  - `add_listener` — registers an async listener with duplicate detection
  - `remove_listener` — unregisters a listener with empty list cleanup
  - `has_listeners` — checks if listeners exist for an event name
  - `get_listeners` — returns all listeners for an event name
  - `listen` — decorator for registering listeners
  - `dispatch` — dispatches events to all listeners concurrently
- `EventDispatcherException` — aggregates all listener errors after dispatch
- Support for custom event names via `enum.StrEnum` or `typing.Literal`
- Support for custom event context via generics

[0.1.0]: https://github.com/mjvbarton/aiodispatcher/releases/tag/v0.1.0
