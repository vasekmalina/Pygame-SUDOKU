import random
import copy

base  = 3
side  = base*base
#remove = 10
removed = []

# pattern for a baseline valid solution
def pattern(r,c): 
    return (base*(r%base)+r//base+c)%side

# randomize rows, columns and numbers (of valid base pattern)
def shuffle(s): 
    return random.sample(s,len(s)) 


def generate(remove):
    r_base = range(base) 

    rows  = [ g*base + r for g in shuffle(r_base) for r in shuffle(r_base) ] 
    cols  = [ g*base + c for g in shuffle(r_base) for c in shuffle(r_base) ]

    nums  = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

    r_board = copy.deepcopy(board)
    
    #handle repetition
    r_list = []
    while len(r_list) != remove:
        for i in range(remove - len(r_list)):
            tup = (random.randrange(0,9), random.randrange(0,9))

            if tup not in r_list:
                r_list.append(tup)

    for i, j in r_list:
        r_board[i][j] = 0

    return board, r_board

