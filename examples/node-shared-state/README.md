# node-shared-state

## Run

```bash
node main.js
```

## Intended behavior

Each customer should have an independent monthly summary object.
Recording an order for bob should update only bob.

## Actual behavior

The program runs, but alice, bob, and carol all show the same total and order count.
The bug is about shared runtime state, not a syntax error.
