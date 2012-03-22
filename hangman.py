import random
import inspect, os
HANGMANPICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

#Build dictionary
filename = os.path.dirname(os.path.abspath(__file__)) + '/Dictionary.txt' 
words = open(filename, 'r').read().split()

def getRandomWord(word_list):
	"""Returns a random string from the passed list of strings"""
	word_index = random.randint(0, len(word_list) - 1)
	return word_list[word_index]

def displayBoard(HANGMANPICS, missed_letters, correct_letters, secret_word):
	print(HANGMANPICS[len(missed_letters)])
	print()

	print('Missed letters:', end= ' ')
	for letter in missed_letters:
		print(letter, end=' ')
	print()

	blanks = '_' * len(secret_word)

	for i in range(len(secret_word)):
		if secret_word[i] in correct_letters:
			blanks = blanks[:i] + secret_word[i] + blanks[i+1:]
	
	for letters in blanks:
		print(letter, end=' ')
	print()

def getGuess(already_guessed):
	"""Returns the letter the player entered.
	Makes sure the player entered a single letter and not something else."""
	while True:
		print('Guess a letter.')
		guess = input()
		guess = guess.lower()
		if len(guess) != 1:
			print('Please enter a single letter.')
		elif guess in already_guessed:
			print('You have already guessed that letter. Choose again.')
		elif guess not in 'abcdefghijklmnopqrstuvwxyz':
			print('Please enter a LETTER.')
		else
			return guess

def playAgain():
	"""Returns True if the player wants to play again, otherwise it returns False."""
	print('Do you want to play again? (yes or no)')
	return input().lower().startswith('y')

print('H A N G M A N')
missed_letters = ''
correct_letters = ''
secret_word = getRandomWord(words)
game_is_done = False

while True:
	displayBoard(HANGMANPICS, missed_letters, correct_letters, secret_word)

	#Let the player type in a letter.
	guess = getGuess(missed_letters + correct_letters)
	
	if guess in secret_word:
		correct_letters += guess

		#Check if the player has won
		found_all_letters = True
		for i in range(len(secret_word)):
			if secret_word[i] not in correct_letters:
				found_all_letters = False
				break
			if found_all_letters:
				print('Yes! The secret word is "' + secret_word + '"! You have won!')
				game_is_done = True


