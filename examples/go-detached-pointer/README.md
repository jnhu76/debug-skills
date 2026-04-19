# go-detached-pointer

## Run

```bash
go run .
```

## Intended behavior

After reloading the store, applying the VIP bonus should update the account now stored in the slice.
So the stored account with id=2 should end at balance=3000.

## Actual behavior

The program runs, but the stored account still ends at balance=2000.
A pointer into stale slice storage gets updated instead of the current store entry.
