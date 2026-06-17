# Modeling FunctionCallback: Coordinator vs ExecutionState

## Context and Problem Statement

`FunctionCallback` in `SchemaCrawler-AI` bridges the MCP request-handling layer and the
SchemaCrawler command-execution layer. It holds a `Catalog` and an `ERModel` (pre-loaded at
startup via Spring injection) and receives a `DatabaseConnectionSource` freshly on every call
via a service locator (`DatabaseConnectionService`).

`ExecutionState` is the established SchemaCrawler pattern for commands. The inheritance chain is:

```
ExecutionState (interface)
  └─ AbstractExecutionState (abstract)
       └─ AbstractCommand<P>
            └─ AbstractFunctionExecutor<P>
                 └─ Concrete per-function executors
```

Commands extend `AbstractExecutionState` — each command IS its own state container. The pipeline
loads the catalog and ER model, then calls `transferState(command)` to push state into the command
before executing it. The command holds all three: `catalog`, `erModel`, and `connectionSource`.

The question is whether `FunctionCallback` should also implement `ExecutionState` to align with
this pattern.


## Considered Options

1. **Keep `FunctionCallback` as a standalone coordinator** — no change to the current design.
2. **Have `FunctionCallback` extend `AbstractExecutionState`** — align it with the command pattern
   so it can use `transferState(executor)` instead of calling individual setters.


## Decision Outcome

**Option 1 — keep `FunctionCallback` as a standalone coordinator.**

Reasons:

- **`FunctionExecutor` already IS the `ExecutionState`.** `AbstractFunctionExecutor` extends
  `AbstractCommand`, which extends `AbstractExecutionState`. The state belongs to the executor.
  `FunctionCallback` is the agent that creates and wires the executor, not a state holder itself.

- **`ExecutionState` is for pipeline participants.** The pattern is designed for the loader
  pipeline: the loader fills its own catalog/erModel, then transfers state to commands.
  `FunctionCallback` is not part of that pipeline; it is a bridge between MCP request handling
  and SchemaCrawler command execution.

- **The lifecycle split is intentional.** `FunctionCallback` deliberately separates stable
  pre-loaded state (catalog, erModel — unchanged across calls) from per-call state
  (connectionSource — retrieved fresh per request). `ExecutionState` holds all three together.
  Merging them would require holding a `connectionSource` permanently, which breaks the
  connection-per-request design of the MCP server.

- **No clarity gain from `transferState()`.** The manual setters in `FunctionCallback.executeFunction()`
  already replicate `transferState()` exactly, including the `usesConnection()` guard. Using
  `transferState()` would require `FunctionCallback` to carry a `connectionSource` field — adding
  complexity without simplifying the call site.

- **`FunctionCallback` is `final`.** Extending `AbstractExecutionState` would require removing
  `final`, which currently prevents unintended subclassing. There is no benefit that justifies
  this trade-off.
