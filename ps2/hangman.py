# Problem Set 2, hangman.py
# Name: Bhargav Acharya
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
      if letter in letters_guessed:
        continue
      else:
        return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    output_list = ""
    for letter in secret_word:
      if letter in letters_guessed:
        output_list += letter
      else:
        output_list += "_ "

    return output_list


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    all_letters = string.ascii_lowercase
    output_string = ""
    for letter in all_letters:
      if letter not in letters_guessed:
        output_string += letter
      else:
        pass
    return output_string

def check_input(guess):
  '''
  guess : The guess character 
  returns: True if the guess is valid 
  '''
  if guess.isalpha():
    return True
  return False

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    total_guesses = 6 
    wrong_guesses = 0
    warnings = 3
    guessed_letters = []
    print("Welcome to Hangman")
    print(f"I am thinking of a word that is {len(secret_word)} letters long")
    #main game loop 
    while((not is_word_guessed(secret_word,guessed_letters)) and not (wrong_guesses >= 6) ):
      print("------------------")
      print(f"you have {total_guesses - wrong_guesses} left")
      print("Available Letters:",get_available_letters(guessed_letters) )
      guess = input("Please guess a letter:")
      #check if it is valid input
      if not check_input(guess):
        if warnings>0:
          warnings-=1
          print(f"Opps! Thats not a valid letter. You have {warnings} warnings left:",get_guessed_word(secret_word,guessed_letters))
          #Ask for a new input
          continue
        else:
          wrong_guesses+=1
          print(f"Opps! Thats not a valid letter. You have {total_guesses-wrong_guesses} warnings left:",get_guessed_word(secret_word,guessed_letters))
          continue
      #check if the letter is already guessed 
      if guess in guessed_letters:
        if warnings>0:
          warnings-=1
          print(f"{guess} has already been guessed. You have {warnings} warnings left:",get_guessed_word(secret_word,guessed_letters))
        else:
          wrong_guesses+=1
          print(f"Opps! Thats not a valid letter. You have {total_guesses-wrong_guesses} warnings left:",get_guessed_word(secret_word,guessed_letters))
          continue
      #update guessed words if it is a valid input
      guessed_letters.extend(guess)
      if guess in secret_word:
        print("Good Guess", get_guessed_word(secret_word,guessed_letters) )
        continue
      else:
        if guess in "aeiou":
          print("Opps! That letter is not in the word:",get_guessed_word(secret_word,guessed_letters))
          wrong_guesses += 2
        else:
          print("Opps! That letter is not in the word:",get_guessed_word(secret_word,guessed_letters))
          wrong_guesses += 1
     
    
    if wrong_guesses>=6:
      print("Sorry you ran out of guesses. The word was ", secret_word)
    elif is_word_guessed(secret_word,guessed_letters):
      print("Congratulations!You won.\nYour score is ", (total_guesses-wrong_guesses)*len(set(secret_word)))




def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    word = my_word.replace(" ", "")
    word_length = len(word)
    if len(other_word) != word_length:
      return False
    for index, letter in enumerate(word):
      if letter != "_":
        if letter == other_word[index]:
          continue
        else:
          return False
    return True

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    for word in line.split():
      if match_with_gaps(my_word, word):
        print(word,end="\t")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    total_guesses = 6 
    wrong_guesses = 0
    warnings = 3
    guessed_letters = []
    print("Welcome to Hangman")
    print(f"I am thinking of a word that is {len(secret_word)} letters long")
    #main game loop 
    while((not is_word_guessed(secret_word,guessed_letters)) and not (wrong_guesses >= 6) ):
      print("------------------")
      print(f"you have {total_guesses - wrong_guesses} left")
      print("Available Letters:",get_available_letters(guessed_letters) )
      guess = input("Please guess a letter:")
      if guess == "*":
        show_possible_matches(get_guessed_word(secret_word,guessed_letters))
      #check if it is valid input
      if not check_input(guess):
        if warnings>0:
          warnings-=1
          print(f"Opps! Thats not a valid letter. You have {warnings} warnings left:",get_guessed_word(secret_word,guessed_letters))
          #Ask for a new input
          continue
        else:
          wrong_guesses+=1
          print(f"Opps! Thats not a valid letter. You have {total_guesses-wrong_guesses} warnings left:",get_guessed_word(secret_word,guessed_letters))
          continue
      #check if the letter is already guessed 
      if guess in guessed_letters:
        if warnings>0:
          warnings-=1
          print(f"{guess} has already been guessed. You have {warnings} warnings left:",get_guessed_word(secret_word,guessed_letters))
          continue
        else:
          wrong_guesses+=1
          print(f"Opps! Thats not a valid letter. You have {total_guesses-wrong_guesses} warnings left:",get_guessed_word(secret_word,guessed_letters))
          continue
      #update guessed words if it is a valid input
      guessed_letters.extend(guess)
      if guess in secret_word:
        print("Good Guess", get_guessed_word(secret_word,guessed_letters) )
        continue
      else:
        if guess in "aeiou":
          print("Opps! That letter is not in the word:",get_guessed_word(secret_word,guessed_letters))
          wrong_guesses += 2
        else:
          print("Opps! That letter is not in the word:",get_guessed_word(secret_word,guessed_letters))
          wrong_guesses += 1
     
    
    if wrong_guesses>=6:
      print("Sorry you ran out of guesses. The word was ", secret_word)
    elif is_word_guessed(secret_word,guessed_letters):
      print("Congratulations!You won.\nYour score is ", (total_guesses-wrong_guesses)*len(set(secret_word)))





if __name__ == "__main__":

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
