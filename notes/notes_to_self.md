The Turing machine contains two mechanisms, which is swapping and comparing.

The tape is defined by an array of different hexidecimal characters, and they
are stored in an unsorted fashion. Each of these strings are 16 characters long.
The gap is defined by the 16 characters with the one comma that is between the 
two adjacent string values.

```python
rules = []

def rule(curr_state, curr_symbol, move, write_symbol, next_state):
    rules.append((current_symbol, current_state, move, write_symbol, next_state))
```
The rule is a definition of the transition rule in the table. It defines the 
transition row, which is defined by the following relation: 

\delta(q,a)=(q',b,D)

This defines a transition, which consists of the current_state, current_symbol
being read, the next_state, the symbol being written to the tape, and where the
head is moving.

```python 
def skip(curr_state, symbols, move, next_state):
    for symbol in symbols:
        rule(curr_state, symbol, move, symbol, next_state)
```

This is just a function that moves the header across the strip without changing
the current letter.

```python 
def travel(state, move, steps, next_state, end_state=None):
    for n in range(steps, 0, -1):
        now = f"{state}_{n}m"
        after = nxt_state if n == 1 else f"{state}_{n-1}m"
        skip(now, hexadecimal + ',', move, after)
        if end_state:
            rule(now, ']', move_left, ']', end_state)
```

This generates the state countdowns from 16m to the final state which is
cmp_LA_pos0_clean

compare_clean():