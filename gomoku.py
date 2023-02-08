"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 28, 2022
"""

'''
Notes:
" " square is empty
"b" black stone
"w" white stone
square stored at board[y][x]

Sequences
(0, 1) left-to-right
(1, 0) top-to-bottom
(1, 1) upper-left to lower-right
(1, -1) upper-right to lower-left
'''


def is_empty(board):
    # This function returns True iff there are no stones on the board board.
    x_size = len(board[0])
    y_size = len(board)
    if (x_size == 0 or y_size == 0):
        return True
    for i in range(y_size):
        for j in range(x_size):
            if (board[i][j] != " "):
                return False
    return True


def is_full(board):
    # helper function for checking for a draw
    # returns True iff the board is full
    x_size = len(board[0])
    y_size = len(board)
    if (x_size == 0 or y_size == 0):
        return True
    for i in range(y_size):
        for j in range(x_size):
            if (board[i][j] == " "):
                return False
    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    # The func- tion returns "OPEN" if the sequence is open, "SEMIOPEN" if the sequence if semi-open, and "CLOSED" if the sequence is closed.
    x_size = len(board[0])
    y_size = len(board)
    x_begin = x_end - length*d_x
    y_begin = y_end - length*d_y
    beginning_bounded = True
    end_bounded = True
    colour = board[y_end][x_end] # colour of the sequence

    x_past_begin = x_begin
    y_past_begin = y_begin
    x_past_end = x_end + d_x
    y_past_end = y_end + d_y

    if(x_past_begin < 0 or y_past_begin < 0 or x_past_begin >= x_size or y_past_begin >= y_size):
        beginning_bounded = True
    elif(board[y_past_begin][x_past_begin] == " "): # if space, unbounded
        beginning_bounded = False
    if(x_past_end < 0 or y_past_end < 0 or x_past_end >= x_size or y_past_end >= y_size):
        end_bounded = True
    elif(board[y_past_end][x_past_end] == " "): # if space, unbounded
        end_bounded = False

    #print(beginning_bounded, end_bounded)

    if (beginning_bounded + end_bounded == 0): # both are false
        return "OPEN"
    elif (beginning_bounded + end_bounded == 1): # one is true
        return "SEMIOPEN"
    elif (beginning_bounded + end_bounded == 2): # both are true
        return "CLOSED"
    return "ERROR" #none of the above cases true is a problem


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    x_size = len(board[0])
    y_size = len(board)
    cur_x = x_start
    cur_y = y_start
    count = 0
    while(cur_x >= 0 and cur_x < x_size and cur_y >= 0 and cur_y < y_size):
        if (board[cur_y][cur_x] == col):
            count += 1
        else:
            count = 0
        if (count == length):
            next_y = cur_y + d_y
            next_x = cur_x + d_x
            if (next_x < 0 or next_x >= x_size or next_y < 0 or next_y >= y_size or board[next_y][next_x] != col): # check for no subsequence
                #print("sequence found at: ", cur_y, cur_x)
                sequence_type = is_bounded(board, cur_y, cur_x, length, d_y, d_x)
                if (sequence_type == "OPEN"):
                    open_seq_count += 1
                elif (sequence_type == "SEMIOPEN"):
                    semi_open_seq_count += 1
            else: # if we are in subsequence, fast forward to the end
                while(cur_x+d_x >= 0 and cur_x+d_x < x_size and cur_y+d_y >= 0 and cur_y+d_y < y_size and board[cur_y+d_y][cur_x+d_x] == col):
                    #print("fast forwarding: ", cur_y, cur_x)
                    cur_x += d_x
                    cur_y += d_y
            count = 0 # reset the count because length was reached
        cur_x += d_x
        cur_y += d_y


    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):
    '''
    Reminder of Sequences
    (0, 1) left-to-right
    (1, 0) top-to-bottom
    (1, 1) upper-left to lower-right
    (1, -1) upper-right to lower-left
    '''
    open_seq_count, semi_open_seq_count = 0, 0
    x_size = len(board[0])
    y_size = len(board)

    # check left-to-right sequences
    for i in range(y_size):
        cur_open, cur_semiopen = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += cur_open
        semi_open_seq_count += cur_semiopen

    # check top-to-bottom sequences
    for i in range(x_size):
        cur_open, cur_semiopen = detect_row(board, col, 0, i, length, 1, 0)
        open_seq_count += cur_open
        semi_open_seq_count += cur_semiopen

    # check upper-left to lower-right sequences
    for i in range(y_size): # go down leftmost column
        cur_open, cur_semiopen = detect_row(board, col, i, 0, length, 1, 1)
        open_seq_count += cur_open
        semi_open_seq_count += cur_semiopen
    for i in range(1, x_size): # go across rightmost column, excluding (0, 0)
        cur_open, cur_semiopen = detect_row(board, col, 0, i, length, 1, 1)
        open_seq_count += cur_open
        semi_open_seq_count += cur_semiopen

    # check upper-right to lower-left sequences
    for i in range(y_size): # go down rightmost column
        cur_open, cur_semiopen = detect_row(board, col, i, x_size - 1, length, 1, -1)
        open_seq_count += cur_open
        semi_open_seq_count += cur_semiopen
    for i in range(x_size-1): # go across rightmost column, excluding (y_size, x_size)
        cur_open, cur_semiopen = detect_row(board, col, 0, i, length, 1, -1)
        open_seq_count += cur_open
        semi_open_seq_count += cur_semiopen

    return open_seq_count, semi_open_seq_count


def detect_row_win(board, col, y_start, x_start, length, d_y, d_x):
    # helper function for checking win
    # return True if any sequence of the length is found in the row, regardless of openness
    x_size = len(board[0])
    y_size = len(board)
    cur_x = x_start
    cur_y = y_start
    count = 0
    while(cur_x >= 0 and cur_x < x_size and cur_y >= 0 and cur_y < y_size):
        if (board[cur_y][cur_x] == col):
            count += 1
        else:
            count = 0
        if (count == length):
            # print("Win found for: ", col, y_start, x_start, length, d_y, d_x)
            return True
        cur_x += d_x
        cur_y += d_y
    return False


def detect_rows_win(board, col, length):
    # helper function for checking win
    # return True if any sequence of the length is found on the board, regardless of openness
    '''
    Reminder of Sequences
    (0, 1) left-to-right
    (1, 0) top-to-bottom
    (1, 1) upper-left to lower-right
    (1, -1) upper-right to lower-left
    '''
    x_size = len(board[0])
    y_size = len(board)

    # check left-to-right sequences
    for i in range(y_size):
        if (detect_row_win(board, col, i, 0, length, 0, 1)):
            return True

    # check top-to-bottom sequences
    for i in range(x_size):
        if (detect_row_win(board, col, 0, i, length, 1, 0)):
            return True

    # check upper-left to lower-right sequences
    for i in range(y_size): # go down leftmost column
        if (detect_row_win(board, col, i, 0, length, 1, 1)):
            return True
    for i in range(1, x_size): # go across rightmost column, excluding (0, 0)
        if (detect_row_win(board, col, 0, i, length, 1, 1)):
            return True

    # check upper-right to lower-left sequences
    for i in range(y_size): # go down rightmost column
        if (detect_row_win(board, col, i, x_size - 1, length, 1, -1)):
            return True
    for i in range(x_size-1): # go across rightmost column, excluding (y_size, x_size)
        if (detect_row_win(board, col, 0, i, length, 1, -1)):
            return True
    return False


def search_max(board):
    move_y = 0
    move_x = 0
    max_score = -1000000 # current maximum score found
    x_size = len(board[0])
    y_size = len(board)
    if (x_size == 0 or y_size == 0):
        return move_y, move_x

    for i in range(y_size):
        for j in range(x_size):
            if (board[i][j] == " "):
                board[i][j] = "b"
                cur_score = score(board)
                #print(i, j, cur_score)
                if (cur_score > max_score):
                    max_score = cur_score
                    move_y = i
                    move_x = j
                board[i][j] = " "

    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    # Returns one of: ["White won", "Black won", "Draw", "Continue playing"]

    # start by checking for a win
    win_length = 5 # 5 stones in a row wins the game
    white_status = detect_rows_win(board, "w", win_length)
    black_status = detect_rows_win(board, "b", win_length)
    if (white_status):
        return "White won"
    if (black_status):
        return "Black won"
    if (is_full(board)):
        return "Draw"
    return "Continue Playing"


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


def my_test1():
    board = make_empty_board(3)
    print("Who won?", is_win(board))

    y = 0; x = 0; d_x = 0; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    y = 0; x = 1; d_x = 0; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")

    y = 0; x = 0; d_x = 1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")

    y = 0; x = 2; d_x = 0; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    print_board(board)
    analysis(board)
    print("Who won?", is_win(board))


def my_test2():
    board = make_empty_board(5)
    print("Who won?", is_win(board))

    y = 0; x = 0; d_x = 0; d_y = 1; length = 5
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    y = 0; x = 1; d_x = 0; d_y = 1; length = 4
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")

    print_board(board)
    analysis(board)
    print("Who won?", is_win(board))


if __name__ == '__main__':
    #play_gomoku(8)

    '''
    Testing ideas:
    -make boards as in my_test1() and mytest2() and check if results are as expected
    -play_gomoku(8) against the computer and see if row counts are as expected, also checking for no errors thrown
    '''

    pass













