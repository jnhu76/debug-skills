# java-detached-account

## Run

```bash
javac Main.java && java Main
```

## Intended behavior

After reloading the store, applying the VIP bonus should update the account currently stored in the repository.
So the stored account with id=2 should end at balance=3000.

## Actual behavior

The program runs, but the stored account still ends at balance=2000.
A detached object gets modified instead of the live one.
