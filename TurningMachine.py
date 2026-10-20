hex = '123456789ABCDEF'
blank = '·'
rule = []

def rule(curr_state, curr_symbol, move, nxt_symbol, nxt_state):
    rule.append((curr_state, curr_symbol, move, nxt_symbol, nxt_state))
