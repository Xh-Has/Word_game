import math
from random import choice
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 8

SCRABBLE_LETTER_VALUES = {
    '*':0,'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = ".\words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish. 
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

# word_list = load_words()

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	
# print(get_frequency_dict('worlddd'))
# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    score = 0
    for x in word:
        score += SCRABBLE_LETTER_VALUES[x.lower()]

    if 7*len(word)-3*(n-len(word))>1:
        score *= (7*len(word)-3*(n-len(word)))
    else:
        score *=1

    return score
# print(get_word_score('bAll', 7))

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    displayHand = ''
    for letter in hand.keys():
        for j in range(hand[letter]):
            displayHand = displayHand +letter + ' '
    return displayHand         
# print(display_hand({'a':1, 'x':2, 'l':3, 'e':1}))

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#Update: it was modified for Problem #4.
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))-1 #-1 because of the problem #4 request, the '*' replaced a vowel

    for i in range(num_vowels):
        x = choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    hand['*'] = 1     # '*'added as a replacement of a vowel
    
    for i in range(num_vowels+1, n):    
        x = choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand
# print(deal_hand(8))

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand:dict, word) -> dict:
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    # """
    dict_word = get_frequency_dict(word)
    hand_copy = hand.copy()
    
    # subtract, for the same letter, the values of the dict_word and hand_copy
    # Letters that appear in word more time  than in hand_copy are deleted from the hand
    for letter_hand,freq_letter_hand in hand.items(): 
        for letter_word,freq_letter_word in dict_word.items(): 
            if letter_hand.lower() == letter_word.lower() and freq_letter_word >= freq_letter_hand:   
                del hand_copy[letter_hand]
            elif letter_hand.lower() == letter_word.lower():
                hand_copy[letter_hand] = freq_letter_hand - freq_letter_word
    return hand_copy 
# print(update_hand( {'n': 1, '*': 1, 'y': 1, 'd':1, 'w':1, 'e': 2},"h*neyy"))

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    hand_copy = hand.copy()
    word = word.lower()
   #checks if letters in word are available in the hand
    for letter in word:
        if letter in hand.keys() and hand_copy[letter] != 0 :
            hand_copy[letter] -= 1
            continue
        else:
            return False 
    potential_words = [ x for x in word_list if\
                    ((word[0] == x[0] or word[0] == '*') and len(x) == len(word))] 
    # it checks if the word is contained in the potential_list (sublist of word_list)
    lista = []
    for guess in potential_words:
        for i in range(1,len(word)): # it checks if the letters are the same from the second letter and after (the first letter is checked in potential_words)
            if word[i] == guess[i]:
                lista += [True]
                if len(lista) == (len(word)-1) and all(lista): #(len(word)-1) because it is checked from the second letter
                    return True 
                else:
                    continue
            if word[i] == '*' and guess[i] in VOWELS:
                lista += [True]
                if len(lista) == (len(word)-1) and all(lista):   
                    return True 
                else:
                    continue 
            else:
                lista = []
                break 
    print(hand_copy)         
    if len(lista) != (len(word)-1) and all(lista):   
        return False        
    return True  
# print(is_valid_word("h*ney", {'n': 1, 'h': 1, '*': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}, word_list))

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    somma = sum(hand.values())
    return somma
# print(calculate_handlen({'n': 1, 'h': 1, '*': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}))

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    print(display_hand(hand))

    score = 0
    while calculate_handlen(hand)!=0:
        word_earned = 0 # scores of every word
        word = input('Enter word, or "!!" to indicate that you are finished: \n')
        if word == '!!':
            print('Total score:', score)
            break
        elif is_valid_word(word, hand, word_list):
            word_earned = get_word_score(word, calculate_handlen(hand))
            score += word_earned
            print(f'{word} earned {word_earned} points. Total: {score} points.')
            hand = update_hand(hand, word)
        else :  
            print('The word is invalid!')   
            hand = update_hand(hand, word)

        if len(hand)>0:
            print(hand)  

    if  calculate_handlen(hand)==0:
        print('U finished the letters!')    
    return score     
# play_hand({'a':1, 'x':1, 'l':2, 'e':1, 'y':1, 'b':1,'*':1},word_list)

#
# Problem #6: Playing a game
# procedure you will use to substitute a letter in a hand
#
def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    alphabet = VOWELS + CONSONANTS + '*'
    excluded_letters = hand.keys()
    possible_choices = [x for x in alphabet if x not in excluded_letters]
    new_letter = choice(possible_choices)
    #obtain the value of the letter the user wants to replace and fix it
    # as the value of the new letter chosen randomly
    letter_value = hand[letter]
    del hand[letter]
    hand[new_letter] = letter_value
    return hand
# print(substitute_hand({'h':1, 'e':1, 'l':2, 'u':1}, 'l'))
 
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    hands = int(input('Input a total number of hands: '))
    
    total_score = 0
    for x in range(hands):
        hand = deal_hand(HAND_SIZE)
        print(display_hand(hand))
        
        change = input('Would you like to substitute a letter? Type \'Yes\' or \'No\': ').lower()
        
        if change not in ['yes','no']:
            print('U didn\'t choose between yes or no')
        elif change == 'yes':
            letter_change  = input('Which letter would you like to replace: ')
            hand = substitute_hand(hand, letter_change)
            print(hand)

        score = play_hand(hand, word_list )       
        replay_hand = input('Would you like to replay the hand? Type \'Yes\' or \'No\': ').lower()

        if replay_hand == 'yes':
            score2 = play_hand(hand, word_list ) 
            if score2 > score:
                score = score2

        print('Total score  for this hand :', score)
        print('-------------------------------------------------')    
        total_score += score
    print('Total score over all hands:', total_score)
    return total_score
#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
