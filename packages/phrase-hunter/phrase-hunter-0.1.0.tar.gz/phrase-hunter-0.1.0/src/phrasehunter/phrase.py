class Phrase:
    def __init__(self, phrase):
        self.phrase = phrase

        self.phrase_guessed = []

        for letter in self.phrase:
            if letter == ' ':
                self.phrase_guessed.append(' ')
            else:
                self.phrase_guessed.append(False)


    def __str__(self):
        output = ' '

        for index, letter_guessed in enumerate(self.phrase_guessed):
            if letter_guessed:
                output += self.phrase[index]
            else:
                output += '_ '

            if letter_guessed == ' ':
                output += '  '

        return output


    def display(self):
        """Phrase.display()

        this prints out the phrase to the console with guessed letters visibile
        and unguessed letters as underscores. For example, if the current phrase
        is "hello world" and the user has guessed the letter "o", the output
        should look like this: _ _ _ _ o    _ o _ _ _
        """

        print(self)


    def check_letter(self, guess):
        """Phrase.check_letter(guess)

        checks to see if the letter selected by the user matches a letter in the
        phrase
        """
        retvalue = False
        for index, letter in enumerate(self.phrase):
            if guess == letter:
                self.phrase_guessed[index] = True
                retvalue = True
        return retvalue


    def check_complete(self):
        """Phrase.check_complete()

        checks to see if the whole phrase has been guessed
        """
        for letter_guessed in self.phrase_guessed:
            if not letter_guessed:
                return False

        return True
