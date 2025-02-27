import numpy as np

class TicTacToe:
    def __init__(self, dimension=3):
        self.board = np.zeros((dimension, dimension))
        self.dim = dimension

    def place_checker(self, player, row=None, col=None):
        if row is None or col is None:  
            while True:
                row = int(input(f"Player {player} enter row: ")) - 1
                col = int(input(f"Player {player} enter column: ")) - 1

                if row >= self.dim or row < 0 or col < 0 or col >= self.dim:
                    print("Move outside of matrix. Try again.")
                    continue
                if self.board[row, col] == 0:
                    self.board[row, col] = player
                    break
                else:
                    print("Spot taken, try again")
        else:  
            self.board[row, col] = player

    def get_allowed_moves(self):
        allowed_moves = []
        
        for row in range(self.dim):
            for col in range(self.dim):
                if self.board[row, col] == 0:
                    allowed_moves.append((row,col))

        return allowed_moves

    def evaluate_board_win(self):
        # this loop checks for row wins
        for row in range(self.dim):                     
            if abs(sum(self.board[row])) == self.dim:
                return np.sign(sum(self.board[row]))
            
        # this loop for colum wins 
        for col in range(self.dim):                     
            if abs(sum(self.board[:, col])) == self.dim:
                return np.sign(sum(self.board[:, col]))
            
        # this check for diagnoal wins
        if abs(sum(self.board.diagonal())) == self.dim: 
            return np.sign(sum(self.board.diagonal()))

        #other diagonal 
        if abs(sum(np.fliplr(self.board).diagonal())) == self.dim:  
            return np.sign(sum(np.fliplr(self.board).diagonal()))
        
        return 0  

    def is_full(self):
        return not np.any(self.board == 0)

    def print_board(self):
        print(self.board)

    def find_winning_move(self, player):
        for move in self.get_allowed_moves():
            temp_board = np.copy(self.board)
            temp_board[move[0], move[1]] = player
            temp_game = TicTacToe()
            temp_game.board = temp_board
            if temp_game.evaluate_board_win() == player:
                return move
        return None
    
if __name__ == "__main__":
    game = TicTacToe()
    player = 1

    while True:
        game.print_board()

        if game.is_full() or game.evaluate_board_win() != 0:
            break
        game.place_checker(player)

        player *= -1

    winner = game.evaluate_board_win()
    
    if winner == -1:
        print("Player -1 wins the game")
        
    elif winner == 1:
        print("Player 1 wins the game")
    else:
        print("Draw")