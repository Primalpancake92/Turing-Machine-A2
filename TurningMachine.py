"""
    sort = compare + swap
    fixed-width from a[i] to b[i] where i is 0 is 17 steps - hex is 16 digits and , separates numbers
    
    Swap (no markers):
        read a[i] -> remember in STATE -> travel fixed-width to b[i] -> write a[i] to b[i] -> travel fixed-width back to a[i] 
        STATE:
            goR_L#_move'n' where # is the number at a[i] and n is the number of digits to b[i] x k
            goL_R#_move'n' where # is the number at b[i] and n is the number of digits to a[i] x k
            
    Compare:
        a[i] = b[i] -> skip to a[i+1]
        a[i] < b[i] -> stop, move to next pair
        a[i] > b[i] -> swap a[i] and b[i]
        
        if a[i] =< b[i] -> stop and go to a[i+1] 
        if a[i] > b[i] -> first difference found, swap a[i] and b[i] and swap the rest
        
    Flags:
        C = clean
        D = dirty (has been swapped)
        
    Halting:
        if all pairs are clean and ] is reached, go to cell 0 and accept
        if there are dirty pairs, go to cell 0 and repeat the process
        
    States:
    where...
    - i is the index
    - a and b are the hex digits being compared
    - C = clean
    - D = dirty
    - n = the number of digits to travel to the other cell
    
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
"""



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
    
def travel():
    pass

def compare_clean():
    pass

def compare_dirty():
    pass

def swap():
    pass

