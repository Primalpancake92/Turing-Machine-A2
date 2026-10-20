    """
    sort = compare + swap
    fixed-width from a[i] to b[i] where i is 0 is 17 steps - hex is 16bits and , separates numbers
    
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
        if a[i] > b[i] -> first difference found, return to pos 1 and swap a and b
        
    Flags:
        C = clean
        D = dirty (has been swapped)
        
    Halting:
        if all pairs are clean and ] is reached, go to cell 0 and accept
        if there are dirty pairs, go to cell 0 and repeat the process
    """

import unicodedata

hex = '123456789ABCDEF'
width = 16

blank = '·'
initial_state = '⎆'
error_state = '❗'
accept_state = '✔'
move_right = '→'
move_left = '←'
halt = '⏹'

rule = []

def rule(curr_state, curr_symbol, move, nxt_symbol, nxt_state):

