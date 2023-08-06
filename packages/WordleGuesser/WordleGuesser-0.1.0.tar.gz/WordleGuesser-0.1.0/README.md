# WordleGuesser
WordleGuesser is a package to determine the best guesses in Wordle.

## Installation
You can install this package using
```
pip install WordleGuesser
```

## Usage
```python
>>> from WordleGuesser import Solver

# Initialize with first guess 
>>> ws = Solver('roate', 'BBYBG')
45 possible answers left

# Get best guess
>>> ws.get_best_guess()
Best guess is mauls, with an average of 3.22 words remaining

# Add new guess
>>> ws.add_guess('mauls', 'BGGBY')
3 possible answers left: 
['pause', 'cause', 'sauce']

# View remaining possible answers
>>> ws.possible_answers
['pause', 'cause', 'sauce']

# View answer bank
>>> ws.answer_words

# View all possible guesses
>>> ws.valid_guesses
```

## Notes
* The matches arguement for add_guess() must be five digits long and must consist of only three unique characters representing the color of the tiles.  
	* Green ('G'): The letter is in the word and in the correct spot.
	* Yellow ('Y'): The letter is in the word but in the wrong spot.
	* Black ('B'): The letter is not in the word.

* get_best_guess() determines the best guess by evaluating the average number of answers remaining if that word is guessed. 'roate' is the best first guess because on average there are 60.4 possible answers left if it is guessed first, which is the lowest of any guess word. 