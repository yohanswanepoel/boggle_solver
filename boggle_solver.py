import duckdb
LOOP = 1
RECURSIVE = 2

TEST_BOARD = [
    ['s', 's', 'm', 'h'],
    ['o', 'y', 'i', 's'],
    ['e', 'b', 'l', 'l'],
    ['h', 'l', 'c', 'e']
]

words_found = []
non_words = []
score = 0

def load_word_list():
    duckdb.read_csv('wordlist.csv',header=False) 

def list_words(word):
    return duckdb.sql("SELECT column0 FROM \"wordlist.csv\" WHERE column0 like '{value}%'".format(value=word)).fetchall()

# Useful method for debugging
def solve_one(board, row, col):
    tree_history = "({0}{1})".format(row, col)
    value = board[row][col]
    print(value)
    word_len = len(value)
    which_way(board, row, col, word_len, value, -1, -1, 0, 0, tree_history)
    print("Score: {score}".format(score=score))
    print(words_found)

def solve_board(board):
    # Looking for words
    print("Looking for words")
    print("================================================")
    global score
    global words_found
    word_len = 0
    word = ""
    row_i = 0
    col_i = 0
    words_found = []
    score = 0
    # Loop picks starting points
    for row_i in range(0,4):
        for col_i in range(0,4):
            value = board[row_i][col_i]
            word_len = len(value)
            tree_history = "({0}{1})".format(row_i, col_i)
            which_way(board, row_i, col_i, word_len, value, -1, -1, 0, 0, tree_history)
            col_i += 1
        row_i += 1

    print("================================================")
    print("> Score: {score}".format(score=score))
    print("# Words: {count}".format(count=len(words_found)))

def which_way(board, start_row, start_col, word_len, word, previous_row, previous_col, dir_row, dir_col, tree_history):
    right = False
    left = False
    up = False
    down = False

    if start_col < 3: # right
        right = True
        walk_board(board, start_row, start_col, word_len, word, previous_row, previous_col, 0, 1, tree_history)

    if start_row < 3: # down
        down = True
        walk_board(board, start_row, start_col, word_len, word, previous_row, previous_col, 1, 0, tree_history)

    if start_col > 0: # left
        left = True
        walk_board(board, start_row, start_col, word_len, word, previous_row, previous_col, 0, -1, tree_history)

    if start_row > 0: # up
        up = True
        walk_board(board, start_row, start_col, word_len, word, previous_row, previous_col, -1, 0, tree_history)

    if right and up:
        walk_board(board, start_row, start_col, word_len, word, previous_row, previous_col, -1, 1, tree_history)

    if right and down:
        walk_board(board, start_row, start_col, word_len, word, previous_row, previous_col, 1, 1, tree_history)
    
    if left and up:
        walk_board(board, start_row, start_col, word_len, word, previous_row, previous_col, -1, -1, tree_history)
    
    if left and down:
        walk_board(board, start_row, start_col, word_len, word, previous_row, previous_col, 1, -1, tree_history)

def valid_move(tree_history, row, col):
    return tree_history[row][col] == 0  

def continue_score(word):
    global score
    global words_found
    global non_words
    if word in non_words:
        return False
    found = list_words(word)
    if len(found) > 0:
        if found[0][0] == word and word not in words_found:
            print(word)
            words_found.append(word) # 3 letters = 1 point, every letter after that is one 1 more e.g. 4 = 2 points
            score += len(word) - 2
    else: 
        non_words.append(word)
    return len(found) > 0

def walk_board(board, start_row, start_col, word_len, word, previous_row, previous_col, dir_row, dir_col, tree_history):
    global score
    global words_found
    
    next_col = start_col + dir_col
    next_row = start_row + dir_row
    track = "({0}{1})".format(next_row, next_col)
    if track in tree_history: # Do not backtrack or walk over same tiles in tree
        return
    new_history = tree_history + track
    
    value = word + board[next_row][next_col]
    if not word_logic(value, word_len):
        return
    which_way(board, next_row, next_col, word_len, value, start_row, start_col, dir_row, dir_col, new_history)           

def word_logic(value, word_len):
    if len(value) > 2:
        return continue_score(value)
    return True

def clean_dict():
    load_word_list()
    duckdb.sql("COPY(SELECT column0 FROM \"wordlist.csv\" where (LEN(column0) >2 and LEN(column0) < 17)) TO 'output.csv'")