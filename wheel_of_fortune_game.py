"""File for the game wheel of fortune."""

import os
import subprocess
import pickle
from random import choice, randint
from time import sleep as wait

from colorama import Fore, Back, Style


class Settings:
    """Represents the settings of the game."""

    def __init__(self, name):
        """Initialise the default settings.

        Args:
            name(str): The name of the settings preset.
        Attributes:
            name(str): The name of the settings preset.
            phrases(list[str]): The phrases that can be selected to guess.
            widgets(list[str]): The widgets on the wheel that can be spun.
            wheel(obj): The wheel that is spun on each turn.
            round_count_limit(int): The amount of rounds the players play to.
        """
        self.name = name

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Load the default phrases
        phrases_path = os.path.join(script_dir, 'phrases.txt')
        with open(phrases_path, 'r') as f:
            self.phrases = [line.strip() for line in f]

        # Load the default wheel and its widgets
        widgets_path = os.path.join(script_dir, 'wheel_widgets.txt')
        with open(widgets_path, 'r') as f:
            default_widgets = [line.strip() for line in f]

        # Initialise the wheel
        self.wheel = Wheel('Default Wheel', default_widgets)

        self.round_limit = 3

    def set_name(self):
        """Set the name of the settings preset the player is editing."""
        clear_shell()
        print(style('NAME OF SETTINGS', 'bright'))

        valid_input = False
        while not valid_input:
            print('\nInput the new setting name')
            inputted_name = input('> ')
            if len(inputted_name) < 3:
                print(style(
                    'Name too short! Name must be over 3 characters long',
                    'red'
                ))
                wait(2)
            elif len(inputted_name) > 20:
                print(style(
                    'Name too long! Name must be under 20 characters long',
                    'red'
                ))
            else:
                valid_input = True
                self.name = inputted_name

    def change_round_limit(self):
        """Change the amount of rounds that are played during the game."""
        valid_input = False
        while not valid_input:
            try:
                print(style('SET ROUND LIMIT', 'bright'))
                print('Input the new round limit')
                new_round_limit_input = int(input('> '))
                if new_round_limit_input not in range(1, 11):
                    print(style(
                        'Round limit must be a whole number from 1-10',
                        'red'
                    ))
                    wait(3)
                    clear_shell()
                # If the input is valid then break the loop and continue
                # editing other settings
                else:
                    self.round_limit = new_round_limit_input
                    valid_input = True
            except ValueError:
                print(style(
                    'Round limit must be a whole integer from 1-10',
                    'red'
                ))
                wait(3)
                clear_shell()

    def export_settings(self):
        """Export the current settings to a file in the settings_presets 
        folder.
        """
        presets_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'settings_presets'
        )
        os.makedirs(presets_dir, exist_ok=True)

        file_name = f'{self.name}.pkl'
        file_path = os.path.join(presets_dir, file_name)

        with open(file_path, 'wb') as file:
            pickle.dump(self, file)
        print(style(f'Settings exported successfully to {file_path}.',
                    'green'))

    @staticmethod
    def import_settings():
        """Import settings from a file in the settings_presets folder."""
        presets_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'settings_presets'
        )

        files = [f for f in os.listdir(presets_dir) if f.endswith('.pkl')]
        if not files:
            print(style('No files found in the settings_presets folder.',
                        'red'))
            return None

        print(style('Available settings files:', 'bright'))
        for i, file in enumerate(files, start=1):
            print(f'{i}. {file}')

        # Show the user what files are available for import and get them
        # to select one
        try:
            file_choice = int(
                input('Enter the number of the file to import: '))
            if file_choice < 1 or file_choice > len(files):
                print(style('Invalid choice. Try a number corresponding '
                            'to the file you want to import', 'red'))
                wait(2)
                return None  # Send the user out of the menu

            # Import the selected file
            file_path = os.path.join(presets_dir, files[file_choice - 1])
            with open(file_path, 'rb') as file:
                imported_settings = pickle.load(file)

            print(style(f'Settings imported successfully from {file_path}.',
                        'green'))
            wait(2)
            return imported_settings

        # Exceptions
        except ValueError:
            print(style('Invalid input. Please enter a valid number.', 'red'))
            wait(2)
        except FileNotFoundError:
            print(style('File not found. Please check the file name and try '
                        'again.', 'red'))
            wait(2)
        return None


class Player_Settings:
    def __init__(self):
        self.initialise_players()
        self.player_count = len(Player.player_list)

    def initialise_players(self):
        """Get the amount of players and get them to input their names."""
        clear_shell()
        valid_input = False
        while not valid_input:
            try:
                print('Select how many players (Min. 2, Max. 7)')
                player_count_input = int(input('>'))
                if (2 <= player_count_input <= 7):
                    valid_input = True
                    self.player_count = player_count_input
                else:
                    # Tell the player about the short error
                    print(style(
                        'Player count must be a whole number from 2-7',
                        'red'
                    ))
                    wait(2)
            except ValueError:
                # Tell the player about the error
                print(style(
                    'Player count must be a whole number from 2-7',
                    'red'
                ))
                wait(2)
        # Initialiate players and add them to the list for the game turn loops
        for i in range(1, player_count_input + 1):
            valid_input = False
            while not valid_input:
                print(f'Player {i}, input your name.')
                this_players_name = input('> ')
                # Catch names that are too short (includes empty).
                if len(this_players_name) < 3:
                    print(style(
                        'Name too short! Name must be over 3 characters long',
                        'red'
                    ))
                    wait(2)

                # Catch names that are too long.
                elif len(this_players_name) >= 15:
                    print(style(
                        'Name too long! Name must be under 15 characters long',
                        'red'
                    ))
                    wait(2)

                elif (
                    this_players_name.casefold()
                    in (
                        player.name.casefold()
                        for player in Player.player_list
                    )
                ):
                    print(style(
                        'Name cannot be identical to another!',
                        'red'
                    ))
                    wait(2)
                else:
                    # Intialise the current player
                    Player(this_players_name)
                    # Show the players that have been added so far
                    print(style('\nCurrent players:', 'bright'))
                    for n, player in enumerate(Player.player_list):
                        print(f'{n + 1}. {player.name}')
                    print()
                    valid_input = True

    def set_player_count(self):
        valid_input = False
        while not valid_input:
            try:
                print('Select how many players (Min. 2, Max. 7)')
                player_count_input = int(input('>'))
                if player_count_input > self.player_count:
                    for i in range(len(Player.player_list),
                                   player_count_input):
                        clear_shell()
                        Player.add_player()
                        self.player_count = len(Player.player_list)
                    valid_input = True
                elif player_count_input < self.player_count:
                    valid_input = True
                    clear_shell()
                    Player.remove_players()
                else:
                    print(f'Player count is the same! ({player_count_input}')
                    wait(2)
            except ValueError:
                print(style('Error! Input a whole number'))


class Player():
    """Represents a player who can play the game."""

    player_list = []

    def __init__(self, name):
        """Initialise the player and add itself into the class player list.

        Args:
            name (str): The player's name.

        Attributes:
            name (str): The player's name.
            this_rounds_money (int): The money the player has earned for the
                current round being played.
            total_money (int): The money the player has earned throughout
                all of the rounds played.
            rounds_won (int): The rounds the player has won.
        """
        self.name = name
        self.this_rounds_money = 0
        self.total_money = 0
        self.rounds_won = 0
        Player.player_list.append(self)

    @staticmethod
    def remove_players():
        """Remove players from the game."""
        # Prevent removing players if fewer than 2 players remain
        if len(Player.player_list) <= 2:
            print(style(
                'Error: You must have at least 2 players in the game.',
                'red'
            ))
            wait(2)
            return

        finished_removing = False

        while not finished_removing:
            player_dic = {}
            for i, player in enumerate(Player.player_list):
                player_dic[i + 1] = player
            try:
                for key in player_dic:
                    print(key, player_dic[key].name)
                print(
                    'Input the number corresponding to the player you want to '
                    'remove.\nInput 0 to exit'
                )
                remove_input = int(input('> '))
                if remove_input == 0:
                    finished_removing = True
                elif remove_input in player_dic:
                    Player.player_list.remove(player_dic[remove_input])
                    # Check if fewer than 2 players remain after removal
                    if len(Player.player_list) < 2:
                        print(style(
                            'Error: You cannot have fewer than 2 players.',
                            'red'
                        ))
                        Player.player_list.append(
                            player_dic[remove_input])
                        wait(2)
            except ValueError:
                print(style(
                    'Input was not a number - Input must be numeric '
                    'such as \'1, 2, 3...\'',
                    'red'
                ))
                wait(2)

    @staticmethod
    def add_player():
        """Add a player to the game"""
        valid_input = False
        while not valid_input:
            print('New player: Please enter your name...')
            this_players_name = input('> ')
            # Catch names that are too short (includes empty).
            if len(this_players_name) < 3:
                print(style(
                    'Name too short! Name must be over 3 characters long',
                    'red'
                ))
                wait(2)

            # Catch names that are too long.
            elif len(this_players_name) >= 15:
                print(style(
                    'Name too long! Name must be under 15 characters long',
                    'red'
                ))
                wait(2)

            elif (
                this_players_name.casefold()
                in (
                    player.name.casefold() for player in Player.player_list
                )
            ):
                print(style(
                    'Name cannot be identical to another!',
                    'red'
                ))
                wait(2)
            else:
                # Intialise the current player
                Player(this_players_name)
                # Show the players that have been added so far
                print(style('\nCurrent players:', 'bright'))
                for n, player in enumerate(Player.player_list):
                    print(f'{n + 1}. {player.name}')
                print()
                valid_input = True

    @classmethod
    def view_players(cls):
        clear_shell()
        for i, player in enumerate(cls.player_list):
            print(f'{i + 1}. {player.name}')

        print('\nPress enter to continue...')
        input('> ')


class Wheel():
    """Represents the wheel that is spun on each turn."""

    def __init__(self, name, widgets):
        """Initialise the wheel to be spun on each player's turn.

        Args:
            name (str): The name of the wheel.
            widgets (list[str]: The widgets that are able to be landed on when
                the wheel is spun.
        Attributes:
            name (str): The name of the wheel to be shown in settings.
            widgets (list[str]): The widgets that are able to be landed on when
                the wheel is spun.
            spun_widget (str): The last widget that was spun
        """
        self.name = name
        self.widgets = widgets
        self.spun_widget = None

    def spin(self):
        """Spin the wheel and return the widget that it lands on.

        Returns:
            str: The wheel widget that was spun
        """
        print(style('Press enter to spin the wheel!', 'bright'))
        input('> ')
        wait(0.5)
        clear_shell()
        print('Spinning....')
        # Choose the wheel widget and validate the widget spun on for
        # later comparison
        wheel_widget_spun = choice(self.widgets).strip().upper()
        self.spun_widget = wheel_widget_spun
        return wheel_widget_spun


def get_case_matched_character(guessed_character, hidden_character):
    """Return the matched case of guessed character to the hidden character.

    Args:
        guessed_character (str): The character that has been guessed.
        hidden_character (str): The character in the same position in the
            hidden phrase to be case-matched to.

    Returns:
        str: The guessed character with the matched case to the hidden
            character.
    """
    if guessed_character.lower() == hidden_character:
        case_matched_character = guessed_character.lower()
    elif guessed_character.upper() == hidden_character:
        case_matched_character = guessed_character.upper()
    return case_matched_character


def get_display_phrase(hidden_phrase):
    """Return the inputted phrase but hidden with selected letters shown.

    Args:
        hidden_phrase (str): The phrase that will be hidden for the players to
            guess.

    Returns:
        str: The phrase with the disallowed characters hidden (alphabetic).
    """
    characters_to_display = [' ', '\'', '?', '!', ',', '-']

    display_phrase = ''

    for i in range(0, len(hidden_phrase)):
        # Hide characters not in the allowed list
        if hidden_phrase[i] not in characters_to_display:
            display_phrase += '-'
        # Keep the allowed characters displayed
        elif hidden_phrase[i] in characters_to_display:
            display_phrase += hidden_phrase[i]
    return display_phrase


def style(phrase, colour):
    """Return the inputted phrase coloured to the selected colour.

    Args:
        phrase (str): The phrase to be coloured.
        colour (str): The colour to apply to the phrase. Options are:
            - 'red': Applies red colouring.
            - 'green': Applies green colouring.
            - 'bright': Applies bold and white styling.

    Returns:
        str: The phrase with coloured changes applied
    """
    phrase = str(phrase)
    # Colour checks sorted by rainbow, then brightness (high to low)
    if colour == 'red':
        phrase = Fore.RED + phrase + Style.RESET_ALL
    elif colour == 'green':
        phrase = Fore.GREEN + phrase + Style.RESET_ALL
    elif colour == 'bright':
        phrase = Style.BRIGHT + phrase + Style.RESET_ALL
    elif colour == 'dim':
        phrase = Style.DIM + phrase + Style.RESET_ALL

    return phrase


def highlighted(phrase, colour):
    """Return the inputted phrase highlighted to the selected colour.

    This function can be used alongside the colour text function to apply
    multiple styles to text, e.g. red text with a yellow highlight.

    Args:
        phrase (str): The phrase to be highlighted.
        colour (str): The colour to highlight the phrase. Options are:
            - 'red': Applies red highlighting.
            - 'yellow': Applies yellow highlighting.
            - 'green': Applies green highlighting.

    Returns:
        str: The phrase with the highlight changes applied
    """
    phrase = str(phrase)
    # Colour checks
    if colour == 'red':
        phrase = Back.RED + phrase + Style.RESET_ALL
    elif colour == 'yellow':
        phrase = Back.YELLOW + phrase + Style.RESET_ALL
    elif colour == 'green':
        phrase = Back.GREEN + phrase + Style.RESET_ALL

    return phrase


def clear_shell():
    """Clear the shell."""
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)


def get_new_display_phrase(guess_made, hidden_phrase, display_phrase):
    """Return a new display phrase that reveals characters that were guessed.

    If the phrase is guessed correctly, return the full hidden phrase.

    Args:
        guess_made (str): The guess the player made.
        hidden_phrase (str): The phrase the player is trying to guess.
        display_phrase (str): The hidden and revealed characters of the hidden
            phrase.

    Returns:
        str: The updated display phrase with the character that was guessed
            revealed or the whole phrase revealed if it was guessed correctly.
    """
    skipped_characters = [' ', '\'', '?', '!', ',', '-']

    # Remove skipped characters from both the guess and the hidden phrase
    filtered_guess = ''.join(
        char for char in guess_made if char not in skipped_characters
    )
    filtered_hidden_phrase = ''.join(
        char for char in hidden_phrase if char not in skipped_characters
    )

    # Check letter guesses
    if len(filtered_guess.strip()) == 1:
        if filtered_guess.casefold() in filtered_hidden_phrase.casefold():
            # Create mutable display phrase object
            new_display_phrase = [character for character in display_phrase]
            # Check every position in the hidden phrase for a match to the
            # guessed character
            for i, character in enumerate(new_display_phrase):
                if filtered_guess.casefold() == hidden_phrase[i].casefold():
                    revealed_character = get_case_matched_character(
                        guess_made, hidden_phrase[i])
                    # Reveal the character and modify the display phrase
                    new_display_phrase[i] = revealed_character
            # Make the display phrase list object into a string
            display_phrase = ''.join(new_display_phrase)
    # Check if guess was the hidden phrase (ignoring skipped characters)
    elif filtered_guess.casefold() == filtered_hidden_phrase.casefold():
        display_phrase = hidden_phrase  # Checked outside of function for win
    return display_phrase


def get_changed_characters_count(old_phrase, new_phrase):
    """Return how many characters have changed between 2 phrases.

    Args:
        old_phrase (str): The original phrase before characters have been
            changed, i.e. revealed.
        new_phrase (str): The new phrase with characters that have been
            changed, i.e. revealed.
    Returns:
        int: The sum of characters that are different between the phrases.
    """
    # Make the phrases mutable objects
    old_phrase = [character for character in old_phrase]
    new_phrase = [character for character in new_phrase]

    new_character_index = 0

    for i, character in enumerate(old_phrase):
        if new_phrase[i] != old_phrase[i]:
            new_character_index += 1
    return new_character_index


def get_guess(display_phrase, response_dic, player):
    """Get the player to input a guess and error catch it until it is valid.

    Args:
        display_phrase(str): The revealed characters of the hidden phrase the
            players are trying to guess.
        response_dic(dic): A dictionary of variants of yes and no.
        player(obj): The player who is making the guess.
    Returns:
        str: The validated guess that the player has made
    """
    valid_input = False
    vowel_list = ['a', 'e', 'i', 'o', 'u']
    skipped_characters = [' ', '\'', '?', '!', ',', '-']

    while not valid_input:
        print('\nInput a letter or the phrase if you know it')
        guess_made = input('>')

        # Catch invalid guesses that contain numbers
        if any(i in guess_made for i in '1234567890'):
            print(style('Numbers are not allowed in guesses!', 'red'))
            wait(2)
        # Consonant guesses
        elif (len(guess_made) == 1 and
                guess_made.casefold() not in vowel_list):
            valid_input = True
        # Vowel guesses - user has to purchase a vowel for $250.
        elif (len(guess_made) == 1 and
                guess_made.casefold() in vowel_list):
            print('\nWould you like to buy a vowel? ($250)')
            print('\nPress enter to exit.')
            buy_a_vowel_input = input('> ')
            if buy_a_vowel_input in response_dic[True]:  # Yes
                if player.this_rounds_money >= 250:
                    player.this_rounds_money -= 250
                    valid_input = True
                else:
                    wait(0.5)
                    print('\nSorry, you don\'t have enough money...')
                    wait(2)

        # Provide a range of error of 3 characters for user.
        # guessing phrases before errors are displayed.
        elif (len(display_phrase) - 3) < len(guess_made) < \
                (len(display_phrase) + 3):
            valid_input = True
        # Empty guesses
        elif len(guess_made) == 0:
            print(style('Cannot accept empty answers!', 'red'))
            wait(1)
        # Invalid length guesses
        elif (len(guess_made) < (len(display_phrase) - 3)):
            print(style('Guessed phrase too short!', 'red'))
        elif (len(guess_made)) > (len(display_phrase) + 3):
            print(style('Guessed phrase too long!', 'red'))

    return guess_made


def show_guess_result(guess, display_phrase, old_display_phrase, widget_spun,
                      player):
    """Show the result of the guess the player made.

    Args:
        guess (str): The guess the player made.
        display_phrase (str): The hidden phrase as it has been displayed.
        old_display_phrase (str): The display phrase before a guess.
        widget_spun (int): The widget the player has spun.
        player (Player): The player whose turn it is.
    """
    wait(0.5)
    money_from_turn = 0

    # Display for character guesses
    if len(guess) == 1:
        print(f'\nIs \'{guess.upper()}\' in the phrase?')
    # Display for phrase guesses
    else:
        print(f'\nIs \'{guess}\' the phrase?')
    wait(1)
    # The character was not in the phrase
    if old_display_phrase == display_phrase:
        print(style('No', 'red'))
        print(display_phrase)
    # The character was in the phrase
    else:
        print(style('Yes', 'green'))
        print(display_phrase)
        # Find the multiplier (characters found) and get the amount of money
        # from the widget the player landed on multiplied by how many
        # characters were found with the guess the player made
        m = get_changed_characters_count(old_display_phrase, display_phrase)
        money_from_turn += (widget_spun * m)
        # Add the money to the sum of the rounds money
        player.this_rounds_money += money_from_turn

        # Display how much money the player got from the turn
        print('That gave you...')
        print(style(
            f'+ ${money_from_turn} (${widget_spun} * {m})',
            'green'
        ))
    # Display player balance
    print('Balance:', style(f'${player.this_rounds_money}', 'bright'))

    wait(4)  # Time at the end of the turn to read turn results


def handle_bankrupt(player):
    """Handle when the player lands on the BANKRUPT widget.
    Args:
        player (Player): The okayer who landed on BANKRUPT
    """
    if player.this_rounds_money > 0:
        wait(1)
        print('You\'re going from...')
        wait(0.5)
        print(style(f'${player.this_rounds_money}', 'green'))
        wait(1)
        print('to...')
        wait(1)
        player.this_rounds_money = 0
        print(style('$0!', 'bright'))
        wait(4)  # Time for player to cry about going bankrupt
    else:
        wait(1)
        print(
            'You landed on',
            f"{style('BANKRUPT', 'dim')}.",
            'However, because you have no money, your turn will',
            'be skipped.'
        )
        wait(3)


def start_turn(player, wheel, turn_count, round_count, settings):
    """Display to the round information and spin the wheel
    Args:
        player (Player): The player whose turn it is.
        wheel (Wheel): The wheel object that is spun during the turn.
        turn_count (int): The current turn number in the round.
        round_count (int): The current round number in the game.
        settings (Settings): The game settings, including round limits.
    """
    print(style(
        f'Turn {turn_count} | Round {round_count} of {settings.round_limit}',
        'bright'
    ))
    print()
    print('─'*50)
    print(f'{player.name}, it is your turn\n')

    # Display the money once every player has had a turn.
    if turn_count > len(Player.player_list):
        print(f'You have... ${player.this_rounds_money}')

    # Spin the wheel
    wheel.spin()
    wait(randint(3, 5))
    print('\nYou landed on...')
    wait(1)

    if wheel.spun_widget in ['BANKRUPT', 'LOSE A TURN']:
        print(style(wheel.spun_widget, 'dim'))
    else:
        print(style(f"\n${str(wheel.spun_widget)}", 'green'))


def handle_lose_a_turn():
    """Handle when the player lands on the LOSE A TURN widget."""
    print(style('\nYou lost a turn!', 'dim'))
    wait(2)


def victory(player, hidden_phrase, round_count, settings, money_from_turn=0):
    """Display the player won the round and then move onto the next round.

    Args:
        player (Player): The player who won the round.
        hidden_phrase (str): The phrase that was guessed correctly.
        round_count (int): The current round count.
        settings (Settings): The game settings.
        money_from_turn (int): The money earned from the final guess.

    Returns:
        bool: False if all rounds complete, True otherwise.
    """
    # Add the money from the final guess to the winner's total
    player.this_rounds_money += money_from_turn

    # Display who won the phrase and the phrase itself
    print(style(f'\n{player.name} guessed the phrase correctly!', 'bright'))
    print(style(f'The phrase was: {hidden_phrase}', 'green'))

    # Add statistics to the round winner's object
    player.rounds_won += 1

    # Add all players' round money to their total money
    for p in Player.player_list:
        p.total_money += p.this_rounds_money
        p.this_rounds_money = 0  # Reset round money for the next round

    wait(2)

    print(style(f'Round {round_count} is over!', 'bright'))
    wait(2)

    # Check if the game should continue
    if round_count >= settings.round_limit:
        print(style('Game Over!', 'bright'))

        # Find the players with the most rounds won
        max_rounds_won = max(p.rounds_won for p in Player.player_list)
        winners = [
            p for p in Player.player_list if p.rounds_won == max_rounds_won
        ]

        # Display the winners if there was a draw
        if len(winners) > 1:
            print(style('It\'s a draw!', 'bright'))
            print('The following players have the most rounds won:')
            for winner in winners:
                print(f'- {winner.name} with {winner.rounds_won} rounds won')
        # Display the singular winner
        else:
            winner = winners[0]
            print(
                f'The winner is {winner.name} with {winner.rounds_won} '
                'rounds won!'
            )

        # Display the leaderboard for total money
        print(style('\nLeaderboard (Total Money Earned):', 'bright'))
        # Calculate and sort the players by how much money they earned in total
        sorted_players = sorted(
            Player.player_list, key=lambda p: p.total_money, reverse=True
        )
        # Display the ranking of the players and how much money they earned
        for rank, p in enumerate(sorted_players, start=1):
            print(f'{rank}. {p.name} - ${p.total_money}')

        game_continuing = False
    else:
        print(style(f'Starting Round {round_count + 1}...', 'bright'))
        wait(2)
        game_continuing = True

    return game_continuing


def main():
    """Start the playable game.

    This function initialises the game by selecting the wheel options and
    the phrases that can be guessed. The game is managed in player turns. Each
    turn consists of the player spinning the wheel, guessing the phrase (in
    either characters or guessing a phrase), and getting a cash reward for any
    letters they find. A round ends once the phrase has been guessed correctly.

    The game will continue for how many rounds have been selected in the start
    menu.
    """
    # Put the player in the start menu
    in_start_menu = True

    # Gives flexibility for the user to answer input questions with a range
    # of answers
    response_dic = {
        True: ['y', 'ye', 'yes', 'yup', 'yu', 'yuh', 'yea', 'yeah', 'ya'],
        False: ['n', 'no', 'nop', 'nope', 'na', 'nah']
    }

    # Load the players
    player_settings = Player_Settings()

    # Load the default settings and setting variables that can be changed.
    # This includes the default phrases and round lengths.
    settings = Settings('Default Settings')
    wheel = settings.wheel

    # Start menu section - players can add and remove players, change their
    # names, the player count and the round count
    while in_start_menu:
        clear_shell()

        # All settings and player settings functions and their corresponding
        # input number
        player_settings_dic = {
            1: Player_Settings.set_player_count,
        }
        settings_dic = {
            2: Settings.change_round_limit,
            3: Settings.set_name,
            4: lambda _: Player.view_players(),
            8: lambda _: Settings.import_settings(),
            9: lambda _: settings.export_settings()
        }
        # Input validation
        valid_input = False

        # Settings selection
        while not valid_input:
            try:
                clear_shell()

                # Settings menu displays the setting preset name and the
                # different settings that they can change, alongside
                # import and export functions for setting preset files
                print(style(settings.name, 'bright'))

                # Normal settings
                print(
                    f'1. Set Player Count ({player_settings.player_count})\n'
                    f'2. Change Round Limit ({settings.round_limit})\n'
                    f'3. Change settings preset name\n'
                    f'4. View players'
                )
                # Export/import settings
                print(style('8. Import Settings', 'dim'))
                print(style('9. Export Settings', 'dim'))
                # Play the game input
                print(style('0. Play Game', 'green'))

                # Instructions for the player for the settings.
                print(style(
                    'Input the number of the setting you want to change',
                    'bright'
                ))

                # Get the setting that the user wants to change
                settings_input = int(input('> '))

            except ValueError:  # e.g. 'aaaaaa' or empty.
                print(style(
                    'Error! Please input the number correlating to the '
                    'setting you want to change.\nThese numbers must be '
                    'numerical only - \'1234567890\'.',
                    'red'
                ))
                wait(3)

            # Do the setting function that the user inputted.
            # Change the correlating gameplay setting
            if settings_input in settings_dic:
                settings_dic[settings_input](settings)
            # Change the correlating player setting
            elif settings_input in player_settings_dic:
                player_settings_dic[settings_input](player_settings)

            # Break the input loop
            else:
                valid_input = True

        # Start the game by changing the status of in menu to break the loop
        in_start_menu = False

    round_count = 1
    game_active = True

    # === CUT OFF FOR GAMEPLAY ROUNDS ===

    while game_active:
        # Get the hidden phrase
        hidden_phrase = choice(settings.phrases)
        # Hide the hidden phrase
        display_phrase = get_display_phrase(hidden_phrase)

        # Set round variables for the start of the round.
        round_over = False
        turn_count = 0

        while not round_over:  # Loop for every player's turn
            for player in Player.player_list:
                clear_shell()
                turn_count += 1

                start_turn(player, settings.wheel, turn_count, round_count,
                           settings)

                wait(2)  # Time for the player to see what widget was spun

                # Special visual for seeing the hidden phrase at first.
                if turn_count == 1:
                    print(style('\nThe phrase is...\n', 'bright'))
                    wait(1)
                    print(f'{display_phrase}\n\n')
                    wait(3)

                if wheel.spun_widget not in ['BANKRUPT', 'LOSE A TURN']:
                    # Make the landed option numeric for adding to players
                    # balance.
                    wheel.spun_widget = int(wheel.spun_widget)

                    if turn_count > 1:
                        print(f'\n{display_phrase}')
                        wait(1)

                    # Get the current player's guess for the turn
                    guess_made = get_guess(
                        display_phrase, response_dic, player)

                    # Used to check if display phrase is changed later - if the
                    # player made an incorrect guess or not
                    old_display_phrase = display_phrase

                    # Change the display phrase by revealing the characters
                    # that were correctly guessed or the phrase itself.
                    display_phrase = get_new_display_phrase(
                        guess_made, hidden_phrase, display_phrase
                    )

                    # Check if the player has revealed the phrase completely
                    # (changing the display phrase to the phrase) and then
                    # finish the round
                    if display_phrase == hidden_phrase:
                        if not victory(
                                player, hidden_phrase, round_count, settings):
                            game_active = False
                        else:
                            round_count += 1
                        round_over = True
                        break  # Exit the turn loop to start a new round

                    # Process non-winning guesses
                    else:
                        show_guess_result(
                            guess_made, display_phrase, old_display_phrase,
                            wheel.spun_widget, player
                        )

                # Handle the special widgets
                elif wheel.spun_widget == 'LOSE A TURN':
                    handle_lose_a_turn()
                elif wheel.spun_widget == 'BANKRUPT':
                    handle_bankrupt(player)

            if round_over:
                break  # Exit the player loop when the round is over


if __name__ == '__main__':
    main()
