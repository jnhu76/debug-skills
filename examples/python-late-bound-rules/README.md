# python-late-bound-rules

## Run

```bash
python main.py
```

## Intended behavior

Bonus tiers:
- balance >= 1000 => +100
- balance >= 2000 => +300

So:
- `bob` with 1200 should receive `100`
- `carol` with 2500 should receive `400`

## Actual behavior

The program runs, but `bob` gets `0` and `carol` gets `600`.
The bug involves how rule functions are created and what values they capture.
