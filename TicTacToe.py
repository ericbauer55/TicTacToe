import random
from typing import List, Dict


class TicTacToe:
    def __init__(self):
        self._player: Dict[str, str] = {'marker': ''}
        self._computer: Dict[str, str] = {'marker': '', 'play_style': 'random'}
        self._board: Dict[str, str] = {'top-L': ' ', 'top-M': ' ', 'top-R': ' ',
                                       'mid-L': ' ', 'mid-M': ' ', 'mid-R': ' ',
                                       'bot-L': ' ', 'bot-M': ' ', 'bot-R': ' '}
        self._VALID_MARKERS: List[str] = ['X', 'O']  # only these markers are allowed
        self._valid_moves: List[str] = list(self._board.keys())  # all moves are valid at the start
        self._next_move: str = random.choice(['player', 'computer'])
        self.turn_number: int = 1  # restricted to be between 1 and 9

    @property
    def winner(self) -> str:
        """
        This property checks who the winner of the game is.
        :return: only returns one of the following strings {'undecided', 'draw', 'computer', 'player'}
        """
        if self._turn_number < 5:
            # game cannot possibly be won until the first player has gone at least 3 times. This happens by turn 5
            # until then, don't bother checking win conditions
            return 'undecided'
        # TODO: create the win logic to check if someone has won, or the game is a draw
        return 'undecided'

    def __str__(self):
        """Over ride the string magic method to print the game board"""
        print('{0}|{1}|{2}'.format(self._board['top-L'], self._board['top-M'], self._board['top-R']))
        print('-+-+-')
        print('{0}|{1}|{2}'.format(self._board['mid-L'], self._board['mid-M'], self._board['mid-R']))
        print('-+-+-')
        print('{0}|{1}|{2}'.format(self._board['bot-L'], self._board['bot-M'], self._board['bot-R']))

    @staticmethod
    def get_valid_input(input_prompt: str, valid_input_list: List[str]) -> str:
        """
        This generically prompts the user to input a string that is in the discrete valid list
        :param input_prompt: string to prompt the user to input with
        :param valid_input_list: discrete list of valid string inputs
        :return: returns a valid item from the valid_input_list parameter
        """
        x = input(input_prompt)
        if x in valid_input_list:
            return x
        else:
            print("Input {0} is invalid.\nExpected: ".format(x))
            print("".join(['{0},\t'.format(vin) for vin in valid_input_list]))
            return TicTacToe.get_valid_input(input_prompt, valid_input_list)  # try again

    def set_player_marker(self) -> None:
        """This function prompts the user to choose X's or O's for their game"""
        self._player['marker'] = TicTacToe.get_valid_input('Choose your marker ("X" or "O"): ', self._VALID_MARKERS)

    def get_player_move(self) -> None:
        """This function prompts the user to choose a move from the valid list of moves. Then that move is marked on
        the game board and the chosen board area is removed from the list of valid moves"""
        prompt: str = "Choose move from: " + "".join(['{0},\t'.format(vin) for vin in self._valid_moves])
        board_area: str = TicTacToe.get_valid_input(prompt, self._valid_moves)
        self._board[board_area] = self._player['marker']  # fill in the chosen board area with player's marker
        self._valid_moves.remove(board_area)  # remove the chosen area from the list of valid moves
        self._next_move = 'computer'

    def get_computer_move(self) -> None:
        """This function generates a move from the computer based on the computer player's strategy. Then that move
        is marked on the game board and the chosen board area is removed from the list of valid moves"""
        if self._computer['strategy'] == 'random':
            board_area: str = random.choice(self._valid_moves)
            self._board[board_area] = self._computer['marker']  # fill in the chosen board area with computer's marker
            self._valid_moves.remove(board_area)  # remove the chosen area from the list of valid moves
        elif self._computer['strategy'] == 'optimal':
            # TODO: implement minimax strategy
            pass
        print('Computer chose to move into "{0}" area'.format(board_area))
        self._next_move = 'player'

if __name__ == '__main__':
    pass