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
                cmp_L{a}_pos{i}_clean_{n}m = writes a[i] to b[i] and carries b[i] to a[i]
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
    """
    starts on a[0] in state read_pos0_clean
    read a[i] -> remember in STATE -> carry to b[i] -> compare -> travel back to a[i + 1] (if equal)
    
    """
    for i in range(width):
        read = f"read_pos{i}_clean"                     # state at a[i] reading a
        
        for a in hexadecimal:                           # set of states for all possible digits in a[i]
            carry = f"goR_L{a}_pos{i}_clean"            # state carrying a to b[i]
            cmp = f"cmp_L{a}_pos{i}_clean"              # state at b[i] comparing b to a
            
            # move 1 of 17, so the chain adds the 16 left
            rule(read, a, move_right, a, f'{carry}_{gap - 1}m' )                # read a, write it back, and move right
            # for special case of only one number
            travel(carry, move_right, gap - 1, cmp, end_state='rewind_clean')   # carry a to b[i] and compare to b[i], if ']' is reached (special case of only one number), go to rewind_clean
            
            for b in hexadecimal:                       # set of states at b[i], reading b, and comparing it to a
                if b < a:                               # first difference 
                    rule(cmp, b, move_left, a, f'goL_R{b}_pos{i}_{gap - 1}m')    # if b < a, move left and carry b to a[i], then go into swap()
                elif b > a:                             # already in right order
                    rule(cmp, b, move_left, b, 'next_pair_clean')                # if b > a, move left and go to next pair
            if i < width - 1:                           # move 1 of 16, so the chain adds the 15 left
                rule(cmp, a, move_left, a, f'back_pos{i}_clean_{gap - 2}m')      # if a == b and not at last digit, go back to a[i + 1]
            else:                                       # all 16 digits are equal
                rule(cmp, a, move_right, a, 'next_pair_clean')                   # if a == b and at last digit, go to next pair
        
        if i < width - 1:                               # moving from b[i] to a[i + 1]
            travel(f'back_pos{i}_clean', move_left, gap - 2, f'read_pos{i + 1}_clean')  # go back to a[i + 1] and read it
            
    # next pair - in number b
    skip('next_pair_clean', hexadecimal, move_right, 'next_pair_clean')         # scan over digits to the either the separator ',' or end ']'     
    rule('next_pair_clean', ',', move_left, ',', 'to_b_start_clean')            # another number
    rule('next_pair_clean', ']', move_left, ']', 'rewind_clean')                # end of pass
    # if not at the end of list
    skip('to_b_start_clean', hexadecimal, move_left, 'to_b_start_clean')        # scan backwards through b 
    rule('to_b_start_clean', ',', move_right, ',', 'read_pos0_clean')           # when separator ',' is reached, go to b[0] and start comparison with b as a
    
    # rewind (accept)
    skip('rewind_clean', hexadecimal + ',' +']', move_left, 'rewind_clean')         # scan left to [ in cell 0
    rule('rewind_clean', '[', halt, '[', accept_state)                          # when in cell 0, halt and accept
    
    # special case: empty list
    rule('read_pos0_clean', ']', move_left, ']', 'rewind_clean')
    
    
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