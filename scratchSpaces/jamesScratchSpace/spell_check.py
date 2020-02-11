def get_deletions(word):
    result = []
    for i, c in enumerate(word):
        if c != ' ':
            result.append(word[0:i] + word[i + 1:len(word)])
    return result


def get_substitutions(word):
    result = []
    for i, c in enumerate(word):
        if c != ' ':
            for j in range(26):
                result.append(word[0:i] + chr(j + 97) + word[i + 1:len(word)])
    return result


def get_insertions(word):
    result = []
    for i in range(len(word) + 1):
        for j in range(26):
            result.append(word[0:i] + chr(j + 97) + word[i:len(word)])
    return result


def one_different(word):
    return get_deletions(word) + get_substitutions(word) + get_insertions(word)


def get_dictionary(path):
    dictionary = set()
    with open(path, 'r') as infile:
        words = infile.read().splitlines()
        for word in words:
            dictionary.add(word)
    return dictionary


def correct_latin_name(s, dictionary):
    corrected = ''
    words = s.split()
    for word in words:
        guess = best_guess(word, dictionary)
        if guess is not None:
            corrected += guess + ' '
        else:
            corrected += word + ' '
    return corrected[0:len(corrected) - 1]


def best_guess(word, dictionary):
    if word in dictionary:
        return word
    guesses = one_different(word)
    possible = []
    for guess in guesses:
        if guess in dictionary:
            possible.append(guess);

    if len(possible) > 0:
        return pick_guess(possible)
    for guess in guesses:
        new_guesses = one_different(guess)
        for new_guess in new_guesses:
            if new_guess in dictionary:
                possible.append(new_guess)

    if len(possible) > 0:
        return pick_guess(possible)

    print('failed')
    return None


def pick_guess(guesses):
    return guesses[0]


test = "fest"
test_dict = get_dictionary('./scratchSpaces/jamesScratchSpace/dict.txt')
print(f'Correcting \'{test}\' to \'{best_guess(test, test_dict)}\'')

test = "Lycaene phlaeees"
test_dict = get_dictionary('./scratchSpaces/jamesScratchSpace/species_dict.txt')
print(f'Correcting \'{test}\' to \'{correct_latin_name(test, test_dict)}\'')

