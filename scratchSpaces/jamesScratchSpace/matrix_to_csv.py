import csv
import re
from enum import Enum, auto

STANDARD_HEADER = [['', '', '', 'Summary Data', '', '', '', 'Taxonomy', '', '', '', '', '', '', '', '', 'Description',
                    '', '', '', '', '', '', '', '', 'Collection Location Data', '', '', '', '', '', 'Collector',
                    '', '', 'Collection', 'Label Data', 'Storage Location', '', '', '', '',
                    'Additional Notes (if additional notes become consistent, consider a new separate column'],
                   ['', '', '', 'UI Number', 'Other Number', 'Other number type', 'Type status', 'Label Family',
                    'Label Genus', 'Label species', 'Current Family', 'Current Genus', 'Current species', 'Subspecies',
                    'Common Name', '', 'Variety', 'Preservation', 'Number of specimens', 'Description', 'Sex',
                    'Stage/Phase', '', 'Condition Rating (Good, Fair, Poor, Unacceptable)',
                    'Condition details (eg wing fallen off)', 'Level 1 eg.Country', 'Level 2 - eg.County',
                    'Level 3 - eg.Town/City/Village', 'Level 4 (eg.Nearest named place)', 'Date (DD/MM/YYYY)',
                    'Bred or not (B if bred/ blank if caught on wing)', 'Surname', 'First name', 'Middle Names',
                    'Name', 'Verbatum label data', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5 +6', ''],
                   ['ColCollection', 'ColTypeOfItem', 'ColObjectStatus', 'ColObjectNumber', 'ColOtherNumbers_tab',
                    'ColOtherNumbersType_tab', "IdeTypeStatus_tab(+ group='1')",
                    "TaxTaxonomyRef_tab(+ group='2').ClaFamily", "TaxTaxonomyRef_tab(+ group='2').ClaGenus",
                    "TaxTaxonomyRef_tab(+ group='2').ClaSpecies", "TaxTaxonomyRef_tab(+ group='1').ClaFamily",
                    "TaxTaxonomyRef_tab(+ group='1').ClaGenus", "TaxTaxonomyRef_tab(+ group='1').ClaSpecies",
                    "TaxTaxonomyRef_tab(+ group='1').ClaSubspecies", "TaxTaxonomyRef_tab(+ group='1').ComName_tab",
                    "IdePreferredName_tab(+ group='1')", 'SpeVariety', 'SpePreservation', 'SpeNumberSpecimens',
                    'ColPhysicalDescription', 'SpeSex', 'SpeStage', 'ConDateChecked', 'ConConditionStatus',
                    'ConConditionDetails', 'SitSiteRef_tab.LocCountry_tab', 'SitSiteRef_tab.LocDistrictCountyShire_tab',
                    'SitSiteRef_tab.LocTownship_tab', 'SitSiteRef_tab.LocNearestNamedPlace_tab',
                    'ColCollectionDatesText_tab', 'ColCollectionMethod', 'ColCollectorsRef_tab.NamLast',
                    'ColCollectorsRef_tab.NamFirst', 'ColCollectorsRef_tab.NamMiddle',
                    'ColSumAssociatedCollections_tab', 'EntLabVerbatimLabelData0', 'LocCurrentLocationRef.LocLevel1',
                    'LocCurrentLocationRef.LocLevel2', 'LocCurrentLocationRef.LocLevel3',
                    'LocCurrentLocationRef.LocLevel4', 'LocMovementNotes', 'NotNotes']]


class ResolutionType(Enum):
    no_clash = auto()
    just_first = auto()
    just_last = auto()
    all = auto()


def add_to_indices(word_index, col_index, indices, resolution_type, num_words):
    if word_index >= num_words or word_index < 0:
        raise Exception('index in optional parameter out of range')
    elif word_index in indices:
        if resolution_type == ResolutionType.no_clash:
            raise Exception('repeated index in optional parameter,'
                            ' consider changing resolution type')
        elif resolution_type == ResolutionType.just_last:
            # overwrite the last one
            indices[word_index] = [col_index]
        elif resolution_type == ResolutionType.all:
            indices[word_index].append(col_index)
    else:
        indices[word_index] = [col_index]


def split_col(table, field_name, new_cols, optional=None, separator=' ', resolution_type=ResolutionType.no_clash):
    # can extend by allowing slices and lists of indices as column to word mappings, and possibly additional wildcards
    field_index = table[0].index(field_name)
    for row_index, row in enumerate(table):
        if row_index != 0:
            words = row[field_index].split(separator)
            if len(words) == len(new_cols) and optional is None:
                row += words
            elif optional is not None and len(optional) == len(new_cols):
                wildcard_found = False
                wildcard_index = -1
                indices = dict()
                for new_col_index, word_index in enumerate(optional):
                    if word_index == '*':
                        if wildcard_found:
                            raise Exception('multiple wildcards passed in optional parameter')
                        else:
                            wildcard_found = True
                            wildcard_index = new_col_index
                    elif re.match('-?\\d+ *: *-?\\d+', word_index):
                        # match a slice
                        start = int(re.search('(-?\\d+) *:', word_index).group(1))
                        end = int(re.search(': *(-?\\d*)', word_index).group(1))
                        if start < 0:
                            start = len(words) + start
                        if end < 0:
                            end = len(words) + end
                        if start >= len(words) or end >= len(words) or start < 0 or end < 0:
                            raise Exception('index in optional parameter out of range')
                        for i in range(start, end + 1):
                            add_to_indices(i, new_col_index, indices, resolution_type, len(words))
                    elif re.match('\\[-?\\d+(, ?-?\\d)*\\]', word_index):
                        # match a list of indices
                        word_indices = re.findall('-?\\d+', word_index)
                        for w in word_indices:
                            index = int(w)
                            if index < 0:
                                index = len(words) + index
                            add_to_indices(index, new_col_index, indices, resolution_type, len(words))
                    elif re.match('\\d+', word_index):
                        add_to_indices(int(word_index), new_col_index, indices, resolution_type, len(words))
                    elif re.match('-\\d+', word_index):
                        index = len(words) + int(word_index)
                        add_to_indices(index, new_col_index, indices, resolution_type, len(words))
                    else:
                        raise Exception('Failed to match optional parameter')

                row_addition = [[] for _ in range(len(new_cols))]
                for word_index, word in enumerate(words):
                    if word_index in indices:
                        for col_index in indices[word_index]:
                            row_addition[col_index].append(word)
                    elif wildcard_found:
                        row_addition[wildcard_index].append(word)
                    # else we discard that word

                row_string = [' '.join(col) for col in row_addition]
                row += row_string

            else:
                raise Exception(f'number of words and columns provided not equal at index {row_index}')
        else:
            row += new_cols


def matrix_to_csv(table, path):
    with open(path, mode='w') as outfile:
        out = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        out.writerows(table)


def matrix_to_standard(table, field_map):
    # the field map will map the standard field headers to table's field headers
    result = [["" for _ in range(len(STANDARD_HEADER[0]))] for _ in range(len(table) - 1)]
    for field in STANDARD_HEADER[1]:
        if field in field_map:
            std_field_index = STANDARD_HEADER[1].index(field)
            table_field_index = table[0].index(field_map[field])
            for row_num, row in enumerate(result):
                row[std_field_index] = table[row_num + 1][table_field_index]
    for field in STANDARD_HEADER[2]:
        if field in field_map:
            std_field_index = STANDARD_HEADER[2].index(field)
            table_field_index = table[0].index(field_map[field])
            for row_num, row in enumerate(result):
                row[std_field_index] = table[row_num + 1][table_field_index]
    return result


def matrix_to_standard_csv(table, path, field_map):
    with open(path, mode='w') as outfile:
        out = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        out.writerows(STANDARD_HEADER)
        out.writerows(matrix_to_standard(table, field_map))


test = [[f'({x} {y})' for x in range(10)] for y in range(10)]
test2 = [['Accessor No.', 'Specimen No.', 'Present Determination', 'Determined By', 'Date Determined', 'Collection',
          'Original Determination', 'Date', 'Location', 'Collector', 'Other data'],
         ['', '00133', 'Euclidia glyphica', 'M. Hellier', '24/4/87', '', 'glyphica', '23/6/18',
          'Forest Hill Marlborough', 'Paten', ''],
         ['', '11504', 'Eurodryas aurinia', 'J. B. Beeson', '30.1.95', '', 'Melitaea aurinia', '1905',
          'Dartmoor Devon', 'J. Peed', '']]
std_test = [['Invertebrates; Insects', 'Object', 'Present', 'I.2019.2147', '', '', '', 'Hesperiidae', 'Thymelicus',
             'lineola', 'Hesperiidae', 'Thymelicus', 'lineola', '', 'Essex Skipper', 'Yes', '', 'Dry', '1',
             'Pinned whole\nDorsal', 'Male', 'Adult', '', 'Fair',
             'Right antenna missing\nSlight discolouration on left forewing', '[England, U.K.]', '[Essex]',
             'Shoeburyness', '', '20/07/[18]90', '', '[Adkin ?]', '[R ?]', '', 'W.H. Ballett Fletcher',
             'Ex coll W. H. Ballett Fletcher 1941:1\nShoeburyness\n20.7.90\n[R. Adkin ?] 6.11.90\n\n', 'Insect Room',
             'Lower', 'Cab 1', 'Drawer 40.02', 'Column 1 Row 1', '']]

matrix_to_csv(test, './jamesScratchSpace/test.csv')
matrix_to_csv(test2, './jamesScratchSpace/test2.csv')
matrix_to_csv(STANDARD_HEADER + std_test, './jamesScratchSpace/test3.csv')

split_col(test2, 'Present Determination', ['Genus', 'Species'])
split_col(test2, 'Determined By', ['First name', 'Middle Names', 'Surname'], optional=['0', '*', '-1'])
split_col(test2, 'Location', ['Town', 'Place'], optional=['-1', '0 : -1'], resolution_type=ResolutionType.just_first)
matrix_to_standard_csv(test2, './jamesScratchSpace/std_test.csv', {'Current Genus': 'Genus',
                                                                   'Current species': 'Species',
                                                                   'First name': 'First name',
                                                                   'Middle Names': 'Middle Names',
                                                                   'Surname': 'Surname',
                                                                   'Level 3 - eg.Town/City/Village': 'Town',
                                                                   'Level 4 (eg.Nearest named place)': 'Place'})
