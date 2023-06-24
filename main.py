from boggle_solver import solve_board, TEST_BOARD, LOOP, RECURSIVE, load_word_list, solve_one, clean_dict
import time
start_time = time.time()


def test():
    solve_board(TEST_BOARD) 
    print("--- %s seconds ---" % (time.time() - start_time))
    exit()

def main():

   

    run = True
    load_word_list() 
    done = ""   
    while run:
        if done != "R":
            board = [
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.']
            ] 

            print("Ready to solve board. Please capture letters")
            for i in range (4):
                for j in range (4):
                    board[i][j] = '?'
                    print(board[0])
                    print(board[1])
                    print(board[2])
                    print(board[3])
                    board[i][j] = input("Enter value: \n > ")

        if done == "R":
            load_word_list() 

        print(board[0])
        print(board[1])
        print(board[2])
        print(board[3])

        run_game = input("Run board (Y/N): > ")
        if run_game == "Y" or run_game == "y":
            
            solve_board(board) 
        
        done = input("(N)ew board, (R)eload words and run again or (Q)uit: \n > ")
        if done == "Q" or done == "q":
            run = False
            continue
        

    
if __name__ == "__main__":
    #main()
    test()
    #clean_dict()