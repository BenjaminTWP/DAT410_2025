import numpy as np
import random
import math
from TicTacToe import TicTacToe

class MCTSNode:
    def __init__(self, state, parent=None):
        self.moves_not_tested = state.get_allowed_moves()
        self.state = state # a current instance of the game
        self.parent = parent
        self.node_score = 0
        self.children = []
        self.visits = 0
        
    def is_fully_expanded(self):
        return len(self.moves_not_tested) == 0

    def find_best_child(self, exploration_weight=11.5):
        best_child = None
        best_node_score = -float("inf")

        for child in self.children:
            exploitation = child.node_score / (child.visits + 0.000001)
            exploration = exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 0.000001))
            score = exploitation + exploration

            if score > best_node_score:
                best_node_score = score
                best_child = child
        
        return best_child
    
    def expand(self):
        if self.moves_not_tested:
            move = self.moves_not_tested.pop() 
            new_state = TicTacToe()           
            new_state.board = np.copy(self.state.board)
            new_state.place_checker(1, move[0], move[1])  
            child_node = MCTSNode(new_state, parent=self) 
            self.children.append(child_node)
            return child_node
        return None

    def backpropagate(self, result):
        self.visits += 1
        self.node_score += result
        if self.parent != None:
            self.parent.backpropagate(-result)


def simulate_random_playout_from_state(state):
    current_player = 1
    while not state.is_full() and state.evaluate_board_win() == 0:
        possible_moves = state.get_allowed_moves()
        move = random.choice(possible_moves)
        state.place_checker(current_player, move[0], move[1])
        current_player *= -1
    return state.evaluate_board_win()


def mcts_search(root, iterations=20000, explor_w=11.5):
    for _ in range(iterations):
        node = root
        while node.is_fully_expanded() and node.children:
            node = node.find_best_child()
        
        if not node.is_fully_expanded():
            node = node.expand()
        
        result = simulate_random_playout_from_state(node.state)
        node.backpropagate(result)
    
    best_child_found = root.find_best_child(exploration_weight=explor_w)
    
    return best_child_found.state


def best_mcts_move(board, explore_weight=11.5):

    # before doing any sort of search, try to find moves
    # that oculd either end up into a direct loss or direct win
    winning_move = board.find_winning_move(1)
    if winning_move != None:
        return winning_move
    
    blocking_move = board.find_winning_move(-1)
    if blocking_move != None:
        return blocking_move
    
    root = MCTSNode(board)
    best_state = mcts_search(root, iterations=20000, explor_w=explore_weight)
    
    for move in board.get_allowed_moves():
        test_state = TicTacToe()
        test_state.board = np.copy(board.board)
        test_state.place_checker(1, move[0], move[1])
        if np.array_equal(test_state.board, best_state.board):
            return move
        
    if board.get_allowed_moves() != None:
        return random.choice(board.get_allowed_moves())
    else:
        None


def play_game(weight):
    game = TicTacToe(3)
    human_player = -1
    ai_player = 1
    
    while True:
        game.print_board()
        if game.is_full() or game.evaluate_board_win() != 0:
            break
        
        print("Human player turn:")
        game.place_checker(human_player)
        
        if game.is_full() or game.evaluate_board_win() != 0:
            break
    
        print("AI player turn:")
        move = best_mcts_move(game, explore_weight=weight)
        if move != None:
            row, col = move
            game.place_checker(ai_player, row, col)
    
    game.print_board()
    winner = game.evaluate_board_win()
    if winner == ai_player:
        print("AI wins!")
    elif winner == human_player:
        print("You win!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game(11.5)