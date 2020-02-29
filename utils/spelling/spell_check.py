# ----------------------------------------------------------------------------------------------------------------
#   Computes all possible words formed by deleting a character from the given word

def get_deletions(word):
    result = []
    for i, c in enumerate(word):
        if c != ' ':
            result.append((word[0:i] + word[i + 1:len(word)], 'del'))
    return result

# ----------------------------------------------------------------------------------------------------------------
#   Computes all possible words formed by substituting a character from the given word

def get_substitutions(word):
    result = []
    for i, c in enumerate(word):
        if c != ' ':
            for j in range(26):
                result.append((word[0:i] + chr(j + 97) + word[i + 1:len(word)], 'sub'))
    return result

# ----------------------------------------------------------------------------------------------------------------
#   Computes all possible words formed by inserting a new character into the given word

def get_insertions(word):
    result = []
    for i in range(len(word) + 1):
        for j in range(26):
            result.append((word[0:i] + chr(j + 97) + word[i:len(word)], 'ins'))
    return result

# ----------------------------------------------------------------------------------------------------------------
#   returns all words at a Levenshtein distance of 1 from the given word

def one_different(word):
    return get_deletions(word) + get_substitutions(word) + get_insertions(word)

# ----------------------------------------------------------------------------------------------------------------
#   reads in a dictionary of words from the given file path and stores them in a hashset

def get_dictionary(path):
    dictionary = set()
    with open(path, 'r') as infile:
        words = infile.read().splitlines()
        for word in words:
            dictionary.add(word)
    return dictionary

# ----------------------------------------------------------------------------------------------------------------
#   checks whether the first character of a word is upper case

def first_char_is_upper(word):
    first_char = ord(word[0])
    return 65 <= first_char <= 90

# ----------------------------------------------------------------------------------------------------------------
#   converts the first character of a word to upper case

def first_char_to_upper(word):
    new_word = chr(ord(word[0]) - 32) + word[1:]
    return new_word

# ----------------------------------------------------------------------------------------------------------------
#   Splits a string into multiple words and tries to correct each word using the dictionary, preserving
#   capitalisation of the first letter of the word

def correct_words(s, dictionary):
    corrected = ''
    words = s.split()
    for word in words:
        if '"' not in word:
            upper = first_char_is_upper(word)
            guess = best_guess(word.lower(), dictionary)
            if guess is not None:
                if upper:
                    corrected += first_char_to_upper(guess) + ' '
                else:
                    corrected += guess + ' '
            else:
                corrected += word + ' '
        else:
            return None
    return corrected[0:len(corrected) - 1]

# ----------------------------------------------------------------------------------------------------------------
#   Attempts to match a given word to a closest match in the given dictionary

def best_guess(word, dictionary):
    if word in dictionary:
        return word
    guesses = one_different(word)
    possible = []
    for guess, tag in guesses:
        if guess in dictionary:
            if tag == 'sub':
                return guess
            else:
                possible.append((guess, [tag]));

    if len(possible) > 0:
        return pick_guess(possible)

    for guess, tag in guesses:
        new_guesses = one_different(guess)
        for new_guess, new_tag in new_guesses:
            if new_guess in dictionary:
                if tag == 'sub' and new_tag == 'sub':
                    return new_guess
                else:
                    possible.append((new_guess, [tag, new_tag]))

    if len(possible) > 0:
        return pick_guess(possible)

    print('failed')
    return None

# ----------------------------------------------------------------------------------------------------------------
#   selects which of the given corrections is best (favouring substitutions)

def pick_guess(guesses):
    best_tags = None
    best_word = ''
    for word, tags in guesses:
        if best_tags is None or is_better(tags, best_tags):
            best_word = word
            best_tags = tags

    return best_word

# ----------------------------------------------------------------------------------------------------------------
#   A comparator to prioritise substitutions over insertions and deletions

def is_better(tags1, tags2):
    return tags1.count('sub') > tags2.count('sub')

# ----------------------------------------------------------------------------------------------------------
#   correct_table:      No return value         Mutates table
#   table:              list list String        expected to contain column headers in first row
#   column_dicts        dict<int, Path>         Maps column indices to path for that column's dictionary

def correct_table(table, column_dicts):
    for col_index in column_dicts:
        dictionary = get_dictionary(column_dicts[col_index])
        for row_index in range(1, len(table)):
            result = correct_words(table[row_index][col_index], dictionary)
            if result is not None:
                table[row_index][col_index] = result
