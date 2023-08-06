from .words import answer_words, just_guess_words
from .utils import *

class Solver:
    def __init__(self, guess_word, matches):
        self.answer_words = answer_words
        self.just_guess_words = just_guess_words
        self.valid_guesses = answer_words + just_guess_words
        self.possible_answers = answer_words
        
        self.add_guess(guess_word, matches)
        
    def add_guess(self, guess_word, matches):
        """
        Eliminates words from possible answers based on entered guess word and matches 
        
        Parameters
        ----------
        guess_word : str
            The guessed word
        matches : str
            The color of each letter in guess word

        Returns
        -------
        None
        
        
        Examples
        -------
        >>> ws.add_guess('roate', 'BBGYB')
        
        '52 possible answers left'
        """
        spot_matches, letter_matches = format_guess(guess_word, matches)
        
        self.eliminate_words(guess_word, spot_matches, letter_matches)
        
        answers_left = len(self.possible_answers)
        
        if answers_left == 1:
            print(f"The answer is {self.possible_answers[0]}")
        
        elif answers_left <= 10:
            print(f'{answers_left} possible answers left: \n{self.possible_answers}')
        
        else:
            
            print(f"{answers_left} possible answers left")
        
    def eliminate_words(self, guess_word, spot_matches, letter_matches):
        pwords = tuple(self.possible_answers)
        
        for ii in range(0,5):
            letter = guess_word[ii]
            spot = spot_matches[ii]
            
            if letter == spot:
                pwords = place_elimination(ii, letter, pwords, True)
            
            elif letter in letter_matches:
                pwords = letter_elimination(letter, pwords, True)
                pwords = place_elimination(ii, letter, pwords, False)
            
            else:
                pwords = letter_elimination(letter, pwords, False)
            
        pwords = multi_letter_elimination(guess_word, letter_matches, pwords)
            
    
        self.possible_answers = pwords
        
    def get_best_guess(self, all_guess_words = True, return_dict = False):
        """
        Calculates the average number of remaining answers for every possible guess word.
        

        Parameters
        ----------
        all_guess_words : bool, optional
            Use all guess words or just answer words. The default is True.
            
        return_dict: dictionary, optional 
            Return dictionary guess words and average word left. The default is False
            
        Returns
        -------
        dict
            dictionary of all possible guesses and average number of remaining words.

        """
        wl_dict = dict()
        
        if len(self.possible_answers) == 2315:
            if all_guess_words:
                print(f"The best first guess is 'roate'")
                return 'roate'
            
            else:
                print(f"The best first guess is 'raise'")
                return 'raise'
            
        if len(self.possible_answers) == 1:
            print(f"The answer is {self.possible_answers[0]}")
        
        if all_guess_words:
            words_to_guess = self.valid_guesses
        else:
            words_to_guess = self.answer_words
        
        possible_answers_len = len(self.possible_answers)
        
        for guess in words_to_guess:
            counter = 0
            for answer in self.possible_answers:
                counter += auto_elimination(guess, answer, self.possible_answers)
                
            wl_dict[guess] = counter/possible_answers_len
        
        best_guess = min(wl_dict, key = wl_dict.get)
        
        for word in self.possible_answers:
            if wl_dict.get(word) == wl_dict.get(best_guess):
                best_guess = word
                break
        
        print(f'Best guess is {best_guess}, with an average of {wl_dict[best_guess]:.2f} words remaining')
        
        if return_dict:    
            return wl_dict    
        else:
            return
             
    