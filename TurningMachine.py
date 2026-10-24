"""
    sort = compare + swap
    fixed-width from a[i] to b[i] where i is 0 is 17 steps - hex is 16 digits and , separates numbers
    
    Swap (no markers):
        read a[i] -> remember in STATE -> travel fixed-width to b[i] -> write a[i] to b[i] -> travel fixed-width back to a[i] 
        STATE:
            goR_L#_move'n' where # is the number at a[i] and n is the moves still needed to reach b[i]
            goL_R#_move'n' where # is the number at b[i] and n is the moves still needed to reach a[i]
            
    Compare:
        a[i] = b[i] -> skip to a[i+1]
        a[i] < b[i] -> stop, move to next pair
        a[i] > b[i] -> swap a[i] and b[i]
        
        if a[i] =< b[i] -> stop and go to a[i+1] 
        if a[i] > b[i] -> first difference found, swap a[i] and b[i] and swap the rest
        
        
    Halting:
        if all pairs are clean and ] is reached, go to cell 0 and accept
        if there are dirty pairs, go to cell 0 and repeat the process
        
    States:
    where...
    - i is the index
    - a and b are the hex digits being compared
    - C = clean
    - D = dirty
    - n = the number of moves still needed to travel to the other cell
    
        ⎆ = initial state
        
        Compare (clean):
            read_pos{i}_clean = in a[i] read a
            goR_L{a}_pos{i}_clean_{n}m = carry a 
            cmp_L{a}_pos{i}_clean = in b[i] read b and compare to a
            back_pos{i}_clean_{n}m = (if a[i] = b[i]) go back to a[i+1]
            (cmp ends if a[i] < b[i] or all digits are equal)
            next_pair_clean = scan right to ',' separator i.e. end of word b
            to_b_start_clean = scans left to the start of b
            rewind_clean = scans left to cell 0, and accepts 
            
        Compare (dirty):
            read_pos{i}_dirty = in a[i] read a
            goR_L{a}_pos{i}_dirty_{n}m = carry a 
            cmp_L{a}_pos{i}_dirty = in b[i] read b and compare to a
            back_pos{i}_dirty_{n}m = (if a[i] = b[i]) go back to a[i+1]
            (cmp ends if a[i] < b[i] or all digits are equal)
            next_pair_dirty = scan right to ',' separator i.e. end of word b
            to_b_start_dirty = scans left to the start of b
            rewind_dirty = scans left to cell 0, and begins new pass
            
        Swap:
            swap_read_pos{i} = in a[i] read a
            goR_L{a}_pos{i}_{n}m = carry a
            write_L{a}_pos{i} = in b[i] write a, read b
            goL_R{b}_pos{i}_{n}m = carry b
            write_R{b}_pos{i} = in a[i] write b
            next_pair_swap = moves to start of b to begin next comparison       
            
    Paths: 
    starts clean, finds a swap, turns dirty, reaches ], rewinds, starts next pass clean
    if list is sorted, reaches ] while clean and accepts
    
        Difference found:
            compare_clean() [a>b]
                cmp_L{a}_pos{i}_clean = writes a[i] to b[i] and carries b[i] to a[i]
                (first exchange complete in compare_clean)
            
            swap()
                goL_R{b}_pos{i}_{n}m = carries b[i] to a[i]
                write_R{b}_pos{i} = writes b[i] to a[i] 
                cont. swap till pos{15}
                next_pair_swap = goes to start of b 
                --> next_pair_dirty 
                
            compare_dirty() 
                next_pair_dirty = finds end of b
                to_b_start_dirty = goes to start of b
                read_pos{0}_dirty = begins next pair comparison
        
        Equal:
            compare_clean() goes to a[i+1] and does next comparison
        
        a < b:
            move to next pair and stay clean
        
        ] reached while clean:
            go to cell 0 and accept
        
        difference found while dirty:
            compare_dirty() uses same swap states and goes back to compare_dirty() for next pair at next_pair_dirty
        
        ] reached while dirty:
            go to cell 0 and repeat the process at read_pos{0}_clean
"""

import csv

hexadecimal = '0123456789ABCDEF'
width = 16
gap = width + 1    # a[i] to b[i] is 16 bits + 1 comma

blank = '·'
initial_state = '⎆'
error_state = '❗'
accept_state = '✔'
move_right = '→'
move_left = '←'
halt = '⏹'

rules = []

def rule(curr_state, curr_symbol, move, nxt_symbol, nxt_state):
    rules.append((curr_state, curr_symbol, move, nxt_symbol, nxt_state))
        
def skip(curr_state, symbols, move, nxt_state):
    """
    moves over symbols without changing symbol --> used for travel() and for states next_pair, to_b_start, and rewind
    adds one rule per symbol 
    moves, writes the same symbol back (unchanged) and goes to the next state    
    """
    for symbol in symbols:
        rule(curr_state, symbol, move, symbol, nxt_state)
    
def travel(state, move, steps, nxt_state, end_state=None):
    """
    move right or left over symbols without changing symbol --> used for swap and compare
    builds a chain of states that counts moves in the state names
         state_{n}m -> state_{n-1}m -> ... -> state_{1}m -> next_state
    special case: if a list only has one number, it reads ']' where it expected to find any other number or comma as there's no other entry to compare to
    --> in that case, leave the chain and go to end_state
    """
    for n in range(steps, 0, -1):
        now = f"{state}_{n}m"                                   # current state
        after = nxt_state if n == 1 else f"{state}_{n-1}m"      # next countdown state, unless n == 1 where it is nxt_state
        skip(now, hexadecimal + ',', move, after)               # add 17 rows for each state (hex + comma) -- leaves symbol unchanged, moves one cell, and goes to after (only state name changes)
        if end_state:                                           # for special case, reaches ']' at cell 17
            rule(now, ']', move_left, ']', end_state)

def compare_clean():
    pass

def compare_dirty():
    pass

def swap():
    pass

# Initial state rule - starts at '[' then begins reading in the clean state 
rule (initial_state, '[', move_right, '[', 'read_pos0_clean')

#export tsv
with open('TurningMachine.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter="\t", lineterminator="\n")
    for row in rules:
        writer.writerow(row)