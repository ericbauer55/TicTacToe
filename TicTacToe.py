import random
from typing import List, Dict, Tuple


class TicTacToe:
    def __init__(self):
        self._player: Dict[str, str] = {'marker': ''}
        self._computer: Dict[str, str] = {'marker': '', 'strategy': 'random'}
        self._board: Dict[str, str] = {'top-L': ' ', 'top-M': ' ', 'top-R': ' ',
                                       'mid-L': ' ', 'mid-M': ' ', 'mid-R': ' ',
                                       'bot-L': ' ', 'bot-M': ' ', 'bot-R': ' '}
        self._VALID_MARKERS: List[str] = ['X', 'O']  # only these markers are allowed
        self._valid_moves: List[str] = list(self._board.keys())  # all moves are valid at the start
        self._next_move: str = random.choice(['player', 'computer'])
        self._turn_number: int = 1  # restricted to be between 1 and 9

    @property
    def _winner(self) -> str:
        """
        This property checks who the winner of the game is.
        :return: only returns one of the following strings {'undecided', 'draw', 'computer', 'player'}
        """
        if self._turn_number < 5:
            # game cannot possibly be won until the first player has gone at least 3 times. This happens by turn 5
            # until then, don't bother checking win conditions
            return 'undecided'
        else:
            if self._has_three_in_a_row('player'):
                return 'player'
            if self._has_three_in_a_row('computer'):
                return 'computer'
            if self._turn_number == 9:
                return 'draw' # the game has ended
            return 'undecided'


    def _has_three_in_a_row(self, player_name: str) -> bool:
        """This checks every sequence of 3 in the game board to see if :param player_name has won"""
        three_in_a_row: bool = False  # assume it isn't true to start
        marker: str = self._player['marker'] if player_name == 'player' else self._computer['marker']
        # Establish all sequences to check
        seqs: Dict[str, Tuple[str, str, str]] = {   # check columns
                                                    'col-L': ('top-L', 'mid-L', 'bot-L'),
                                                    'col-M': ('top-M', 'mid-M', 'bot-M'),
                                                    'col-R': ('top-R', 'mid-R', 'bot-R'),
                                                    # check rows
                                                    'row-top': ('top-L', 'top-M', 'top-R'),
                                                    'row-mid': ('mid-L', 'mid-M', 'mid-R'),
                                                    'row-bot': ('bot-L', 'bot-M', 'bot-R'),
                                                    # check diagonals
                                                    'diag-1': ('bot-L', 'mid-M', 'top-R'),
                                                    'diag-2': ('top-L', 'mid-M', 'bot-R')}
        # Iterate through each sequence to check if those 3 areas are equal to marker
        for seq in seqs.values():
            area_markers = [self._board[area] for area in seq]  # retrieve a list of the area markers in that sequence
            if "".join(area_markers) == marker * 3:  # if all area markers are = 'XXX' or 'OOO' then that is a success
                three_in_a_row = True
                break

        return three_in_a_row

    def __str__(self) -> str:
        """Over ride the string magic method to print the game board"""
        rows =['{0}|{1}|{2}'.format(self._board['top-L'], self._board['top-M'], self._board['top-R']),
                '-+-+-',
                '{0}|{1}|{2}'.format(self._board['mid-L'], self._board['mid-M'], self._board['mid-R']),
                '-+-+-',
                '{0}|{1}|{2}'.format(self._board['bot-L'], self._board['bot-M'], self._board['bot-R'])]
        return '\n'.join(rows)

    @staticmethod
    def _get_valid_input(input_prompt: str, valid_input_list: List[str]) -> str:
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
            print("Input {0} is invalid.".format(x))
            return TicTacToe._get_valid_input(input_prompt, valid_input_list)  # try again

    def _set_player_marker(self) -> None:
        """This function prompts the user to choose X's or O's for their game"""
        chosen_marker = TicTacToe._get_valid_input('Choose your marker ("X" or "O"):\n>', self._VALID_MARKERS)
        self._player['marker'] = chosen_marker
        self._computer['marker'] = set(self._VALID_MARKERS).difference(chosen_marker).pop()  # get the other one

    def _get_player_move(self) -> None:
        """This function prompts the user to choose a move from the valid list of moves. Then that move is marked on
        the game board and the chosen board area is removed from the list of valid moves"""
        prompt: str = "Choose move from: " + ", ".join(['{0}'.format(vin) for vin in self._valid_moves]) + '\n>'
        board_area: str = TicTacToe._get_valid_input(prompt, self._valid_moves)
        self._board[board_area] = self._player['marker']  # fill in the chosen board area with player's marker
        self._valid_moves.remove(board_area)  # remove the chosen area from the list of valid moves
        self._next_move = 'computer'

    def _get_computer_move(self) -> None:
        """This function generates a move from the computer based on the computer player's strategy. Then that move
        is marked on the game board and the chosen board area is removed from the list of valid moves"""
        board_area: str = ''
        if self._computer['strategy'] == 'random':
            board_area = random.choice(self._valid_moves)
            self._board[board_area] = self._computer['marker']  # fill in the chosen board area with computer's marker
            self._valid_moves.remove(board_area)  # remove the chosen area from the list of valid moves
        elif self._computer['strategy'] == 'optimal':
            # TODO: implement minimax strategy
            pass
        print('Computer chose to move into "{0}" area'.format(board_area))
        self._next_move = 'player'

    def play(self) -> None:
        """Implements the main game setup and loop"""
        # SETUP
        print(self)
        self._set_player_marker()
        print('The {0} will be going first...'.format(self._next_move))
        # LOOP
        for i in range(1, 10):
            self._turn_number = i
            print('=' * 15 + '[Turn {}]'.format(i) + '=' * 15)
            if self._next_move == 'player':
                self._get_player_move()
            else:  # self._next_move == 'computer'
                self._get_computer_move()
            print(self)  # print game board before winner is checked
            if self._winner != 'undecided':
                break
        print('=' * 39)
        print('The winner of the game is...{}!'.format(self._winner))


if __name__ == '__main__':
    game = TicTacToe()
    game.play()
