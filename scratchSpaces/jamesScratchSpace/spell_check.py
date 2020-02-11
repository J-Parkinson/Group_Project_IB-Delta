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


def best_guess(word, dictionary):
    guesses = one_different(word)
    for guess in guesses:
        if guess in dictionary:
            return guess


test = "fest"
test_dict = get_dictionary('./scratchSpaces/jamesScratchSpace/dict.txt')
print(f'Dictionary: {test_dict}')
print(f'Correcting \'rest\' to \'{best_guess("rest", test_dict)}\'')
