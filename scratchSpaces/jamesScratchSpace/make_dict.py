# list of names starts on line 60


def make_dict(path):
    dictionary = set()
    with open(path, 'r') as infile:
        text = infile.read().splitlines()
        skipping = False
        for line_num, line in enumerate(text):
            if skipping:
                skipping = check_skipping(line)
            if line_num >= 59 and not skipping:
                if line_num >= 55743:
                    return dictionary
                skip, name = get_name(line)
                if not skip and name != '':
                    for word in name.split():
                        dictionary.add(word)
                else:
                    skipping = True


def get_name(line):
    if line.startswith(' '):
        # just contains = with a name
        split = line.split('=')
        if split[0][-1] == 'S':
            return False, split[1]
        else:
            return False, ''
    else:
        # contains other info, so check it is a eukaryote
        if line[6] == 'E':
            name_part = line.split('=')[1]
            if ' (' in name_part:
                return False, name_part.split(' (')[0]
            else:
                return False, name_part
        else:
            return True, ''


def check_skipping(line):
    if line.startswith(' '):
        return True
    return False


with open('./scratchSpaces/jamesScratchSpace/species_dict.txt', 'w') as outfile:
    names = make_dict('./scratchSpaces/jamesScratchSpace/speclist.txt')
    for name in names:
        outfile.write(name + '\n')
    outfile.write('\n')
    outfile.flush()
