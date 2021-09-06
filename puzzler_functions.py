"""CSC108/CSCA08: Fall 2020 -- Assignment 1: Phrase Puzzler

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Mario Badr, Jennifer Campbell, Tom Fairgrieve,
Diane Horton, Michael Liut, Jacqueline Smith, and Anya Tafliovich.

"""

from constants import (CONSONANT_POINTS, VOWEL_PRICE, CONSONANT_BONUS,
                       PLAYER_ONE, PLAYER_TWO, CONSONANT, VOWEL,
                       SOLVE, QUIT, HUMAN, HUMAN_HUMAN,
                       HUMAN_COMPUTER, EASY, HARD, ALL_CONSONANTS,
                       ALL_VOWELS, PRIORITY_CONSONANTS, HIDDEN)


# We provide this function as an example.
def is_win(puzzle: str, view: str) -> bool:
    """Return True if and only if puzzle and view are a winning
    combination. That is, if and only if puzzle and view are the same.

    >>> is_win('banana', 'banana')
    True
    >>> is_win('apple', 'a^^le')
    False
    >>> is_win('apple', 'app')
    False
    """

    return puzzle == view


# We provide this function as an example of using a function as a helper.
def is_game_over(puzzle: str, view: str, move: str) -> bool:
    """Return True if and only if puzzle and view are a winning
    combination or move is QUIT.

    >>> is_game_over('apple', 'a^^le', 'V')
    False
    >>> is_game_over('apple', 'a^^le', 'Q')
    True
    >>> is_game_over('apple', 'apple', 'S')
    True
    """

    return move == QUIT or is_win(puzzle, view)


# We provide the header and docstring of this function as an example
# of where and how to use constants in the docstring.
def is_human(current_player: str, game_type: str) -> bool:
    """Return True if and only if current_player represents a human in a
    game of type game_type.

    current_player is PLAYER_ONE or PLAYER_TWO.
    game_type is HUMAN, HUMAN_HUMAN, or HUMAN_COMPUTER.

    In a HUMAN game or a HUMAN_HUMAN game, a player is always
    human. In a HUMAN_COMPUTER game, PLAYER_ONE is human and
    PLAYER_TWO is computer.

    >>> is_human('Player One', 'H-')
    True
    >>> is_human('Player One', 'HH')
    True
    >>> is_human('Player Two', 'HH')
    True
    >>> is_human('Player One', 'HC')
    True
    >>> is_human('Player Two', 'HC')
    False
    """
    
    if game_type == HUMAN or game_type == HUMAN_HUMAN:
        return True
    # If the game is HUMAN_COMPUTER True will be returned 
    # only if the player is PLAYER_ONE
    else: 
        return current_player == PLAYER_ONE
        
 
# Helper.
def half_revealed(view: str) -> bool:
    """Return True if and only if at least half of the alphabetic
    characters in view are revealed.

    >>> half_revealed('')
    True
    >>> half_revealed('x')
    True
    >>> half_revealed('^')
    False
    >>> half_revealed('a^,^c!')
    True
    >>> half_revealed('a^b^^e ^c^d^^d')
    False
    """

    num_hidden = view.count(HIDDEN)
    num_alphabetic = 0
    for char in view:
        if char.isalpha():
            num_alphabetic += 1
    return num_alphabetic >= num_hidden


def is_one_player_game(game_type: str) -> bool:
    """Return True if and only if game_type represents a one player game.
    
    game_type is HUMAN, HUMAN_HUMAN, or HUMAN_COMPUTER.
    
    Only in a HUMAN game can there be one player, in a HUMAN_HUMAN game and 
    a HUMAN_COMPUTER game there are two players.
    
    >>> is_one_player_game('H-')
    True
    >>> is_one_player_game('HH')
    False
    >>> is_one_player_game('HC')
    False
    """
    
    # Returns True only if game is HUMAN
    return game_type == HUMAN


def current_player_score(player_one_score: int, player_two_score: int, 
                         current_player: str) -> int:
    """Return the score of current_player, if current_player is Player One, 
    return player_one_score, and return player_two_score if current_player 
    is Player Two.
    
    current_player is either PLAYER_ONE or PLAYER_TWO.
    
    >>> current_player_score(4, 6, 'Player One')
    4
    >>> current_player_score(3, 7, 'Player Two')
    7
    """
    
    if current_player == PLAYER_ONE:
        return player_one_score
    else:
        return player_two_score
    
       
def is_bonus_letter(letter: str, phrase_puzzle: str, 
                    current_view: str) -> bool:
    """Return True if and only if the consonant, letter, is a character 
    in phrase_puzzle, and is hidden in current_view, at the time when the 
    player wishes to solve phraze_puzzle.
    
    Precondition: letter must be a consonant.
    
    >>> is_bonus_letter('j', 'pajama top', 'pa^ama top')
    True
    >>> is_bonus_letter('r', 'sorority sisters', 's^r^rity sisters')
    False
    >>> is_bonus_letter('r', 'pajama top', 'paja^a ^^^')
    False
    """
    
    return letter in phrase_puzzle and letter not in current_view
            
    
def update_char_view(phrase_puzzle: str, current_view: str, 
                     update_index: int, guess_char: str) -> str:
    """Return the character at index, update_index, of phrase_puzzle, 
    if and only if, guess_char is in phrase_puzzle, guess_char 
    is not in current_view and if guess_char is the same as the character 
    at update_index of phrase_puzzle.
    
    >>> update_char_view('pajama top', 'paja^a top', 4, 'm')
    'm'
    >>> update_char_view('sorority sisters', 'sorority sist^rs', -3, 'u')
    '^'
    >>> update_char_view('pajama top', '^^j^m^ to^', 0, 'p')
    'p'
    """
    
    if (guess_char in phrase_puzzle and guess_char not in current_view and 
            guess_char == phrase_puzzle[update_index]):
        return phrase_puzzle[update_index]
    else: 
        return current_view[update_index]


def calculate_score(current_score: int, num_of_occurences: int, 
                    current_move: str) -> int:
    """Return the score of the current player, current_score, with the 
    addition of num_of_occurences multiplied by CONSONANT_POINTS, if and only 
    if current_move is guessing a consonant, or return the current_score 
    with VOWEL_PRICE subtracted, if and only if current_move is buying vowels.
    
    current_move is either VOWEL or CONSONANT.
    
    VOWEL_PRICE is the price to guess a vowel. CONSONANT_POINTS is the 
    number of points received for one correct consonant guessed.
    
    >>> calculate_score(3, 2, 'C')
    5
    >>> calculate_score(5, 1, 'V')
    4
    >>> calculate_score(4, 0, 'C')
    4
    >>> calculate_score(5, 3, 'V')
    4
    >>> calculate_score(5, 0, 'V')
    4
    """
    
    if current_move == CONSONANT:
        return current_score + (num_of_occurences * CONSONANT_POINTS)
    else:
        return current_score - VOWEL_PRICE
    
    
def next_player(current_player: str, num_of_occurences: int, 
                game_type: str) -> str:
    """Return the player to play next, if game_type is a two player game,
    return current_player if num_of_occurences is greater than zero, otherwise 
    return the other player. If game_type is a one player game always 
    return Player One.
    
    game_type is HUMAN, HUMAN_HUMAN or HUMAN_COMPUTER
    
    current_player is either PLAYER_ONE or PLAYER_TWO.
    
    >>> next_player('Player One', 2, 'HC')
    'Player One'
    >>> next_player('Player One', 2, 'HH')
    'Player One'
    >>> next_player('Player One', 0, 'HH')
    'Player Two'
    >>> next_player('Player One', 0, 'HC')
    'Player Two'
    >>> next_player('Player One', 0, 'H-')
    'Player One'
    >>> next_player('Player One', 4, 'H-')
    'Player One'
    """
    
    # This outer if statement is for HUMAN_HUMAN or HUMAN_COMPUTER game types
    if game_type == HUMAN_HUMAN or game_type == HUMAN_COMPUTER:
        if num_of_occurences > 0:
            return current_player
        elif current_player == PLAYER_ONE:
            return PLAYER_TWO
        else: 
            return PLAYER_ONE
    else: # This is done if the game is HUMAN
        return PLAYER_ONE
        
    
def is_hidden(index_of_char: int, phrase_puzzle: str, 
              current_view: str) -> bool:
    """Return True if and only if the character produced by the index,
    index_of_char, of phrase_puzzle, is hidden in current_view for all 
    occurences of the character.
    
    >>> is_hidden(4, 'pajama top', 'paja^a top')
    True
    >>> is_hidden(0, 'pajama top', 'pajama t^p')
    False
    >>> is_hidden(1, 'pajama top', 'p^j^m^ top')
    True
    >>> is_hidden(1, 'pajama top', '^ajama top')
    False
    """
    
    return phrase_puzzle[index_of_char] not in current_view
    
    
def computer_chooses_solve(current_view: str, game_difficulty: str, 
                           consonants_not_guessed: str) -> bool:
    """Return True if game_difficulty is hard and if either current_view is 
    half revealed, or consonants_not_guessed is an empty string. If 
    game_difficulty is easy and consonants_not_guessed is an empty string 
    return True.
    
    game_difficulty is either HARD or EASY.
    
    >>> computer_chooses_solve('^a^a^a ^o^', 'H', 'bcdjmpt')
    False
    >>> computer_chooses_solve('paja^a ^^p', 'H', 'cdlmtn')
    True
    >>> computer_chooses_solve('p^j^m^ top', 'H', '')
    True
    >>> computer_chooses_solve('p^j^m^ t^p', 'H', '')
    True
    >>> computer_chooses_solve('pa^a^a ^op', 'E', 'cdjlmnt')
    False
    >>> computer_chooses_solve('p^j^m^ top', 'E', '')
    True
    """
    
    return ((game_difficulty == HARD and half_revealed(current_view)) or 
            ((game_difficulty == HARD or game_difficulty == EASY) 
             and consonants_not_guessed == ''))
    
    
def erase(str_of_letters: str, remove_index: int) -> str:
    """Return the given string, str_of_letters, with the character at index, 
    remove_index, removed, if and only if remove_index is an index in 
    str_of_letters, if not return str_of_letters unchanged.
    
    Precondition: remove_index must be a positive integer.
    
    >>> erase('dialogue', 1)
    'dalogue'
    >>> erase('wild boar', 9)
    'wild boar'
    >>> erase('wild boar', 8)
    'wild boa'
    """
    
    if  0 < remove_index < len(str_of_letters):
        return (str_of_letters[:remove_index] 
                + str_of_letters[remove_index + 1:])
    else:
        return str_of_letters
    
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
