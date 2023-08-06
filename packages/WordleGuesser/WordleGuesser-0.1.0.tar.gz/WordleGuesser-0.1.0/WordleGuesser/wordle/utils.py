def check_match_format(matches):
    matches = matches.upper()
    
    if len(matches) != 5:
        raise Exception("Matches must be 5 characters long!")
    
    for letter in matches:
        if letter not in ['Y', 'G', 'B']:
            raise Exception ("Unrecognizable match format: Matches can only contain 'B', 'G', 'Y'!")
            
            
    return matches


def format_guess(guess_word, matches):
    matches = check_match_format(matches)
    
    spot_matches = ''
    letter_matches = ''
    
    for ii in range(0,5):
        if matches[ii] == 'G':
            spot_matches += guess_word[ii]
            letter_matches += guess_word[ii]
        else:
            spot_matches += '_'
            
        if matches[ii] == 'Y':
            letter_matches += guess_word[ii]
            
    return spot_matches, letter_matches
  
def auto_elimination(guess, answer, possible_words):
    pwords = tuple(possible_words)
    
    for ii in range(0,5):
        letter = guess[ii]
        
        if letter == answer[ii]:
            pwords = place_elimination(ii, letter, pwords, True)
        
        elif letter in answer:
            pwords = letter_elimination(letter, pwords, True)
            pwords = place_elimination(ii, letter, pwords, False)
        
        else:
            pwords = letter_elimination(letter, pwords, False)
        
        pwords = multi_letter_elimination(guess, answer, pwords)
        
    return len(pwords)

def place_elimination(place, letter, pwords, positive_match):
    if positive_match:
        pwords = [word for word in pwords if word[place] == letter]
    else:
        pwords = [word for word in pwords if word[place] != letter]
        
    return pwords
    
def letter_elimination(letter, pwords, positive_match):
    if positive_match:
        pwords = [word for word in pwords if letter in word]
    else:
        pwords = [word for word in pwords if letter not in word]
    
    return pwords


def multi_letter_elimination(guess_word, letter_matches, pwords):
    multi = ''.join({letter for letter in guess_word if guess_word.count(letter) > 1})
    
    if not multi:
        return pwords
    
    for letter in multi:
        gcount = guess_word.count(letter)
        acount = letter_matches.count(letter)
        
        if acount == 0:
            continue
        
        elif gcount > acount:
            pwords = [word for word in pwords if word.count(letter) == acount]

        else:
            pwords = [word for word in pwords if word.count(letter) >= gcount]
    
    return pwords