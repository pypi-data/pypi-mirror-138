import random
import string

import phrasehunter.phrase

class Game:
    def __init__(self, phrase=None):
        self.missed = 0
        self.phrases = [phrasehunter.phrase.Phrase('there is a cat'),
                        phrasehunter.phrase.Phrase('pizza is delicious'),
                        phrasehunter.phrase.Phrase('eat chocolate for breakfast'),
                        phrasehunter.phrase.Phrase('there are many patterns in life'),
                        phrasehunter.phrase.Phrase('save the world')]
        self.active_phrase = phrase
        self.guesses = set()


    def start(self):
        """Game.start()

        Calls the welcome method,
        """
        self.welcome()
        self.get_random_phrase()
        """creates the game loop,"""
        while self.missed < 5:
            """calls the get_guess method,"""
            guess = self.get_guess()
            """adds the user's guess to guesses,"""
            self.guesses.add(guess)

            """increments the number of missed by one if the guess is incorrect,"""
            if not self.active_phrase.check_letter(guess):
                self.missed += 1
                print(f'You have {5 - self.missed} out of 5 lives remaining!')

            if self.active_phrase.check_complete():
                break

        """calls the game_over method"""
        self.game_over()


    def get_random_phrase(self):
        if self.active_phrase is None:
            self.active_phrase = random.choice(self.phrases)

        return self.active_phrase


    def welcome(self):
        print("""Welcome to the Phrase Hunter game
        By Renee Louise Brinkman
        """)


    def get_guess(self):
        while True:
            self.active_phrase.display()
            letter = input('Guess a letter: ').lower()

            if len(letter) > 1 or letter not in string.ascii_lowercase:
                print('Invalid input. Please try again. Must be a letter')
            else:
                return letter
                break


    def game_over(self):
        """Game.game_over()

        this method displays a friendly win or loss message and ends the game.
        """
        if self.active_phrase.check_complete():
            print('Congratulations! You win!!!')
            print(self.active_phrase)
        else:
            print('Thank you for playing! The game is over. Sadly, you did not win.')

        play_again = input('\nDo you want to play again? (yes/no) ')

        if play_again.lower() == 'yes':
            self.newgame = Game()
            self.newgame.start()
        elif play_again.lower() == 'no':
            print('Thank you for playing!')
        else:
            print('\nInvalid response. Try again')
            self.game_over()
