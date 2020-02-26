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
    no_clash = 1
    just_first = 2
    just_last = 3
    all = 4


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

# ----------------------------------------------------------------------------------------------------------------
#   split_col :         no return value         mutates table
#   table: list         list String             expected to contain the field headers in the first row
#   field_name :        String                  specifying the name of the field to split on, expected in be in table[0]
#   new_cols:           list String             specifies the field names for the new fields (order matters)
#   which_words:        list String             (optional) specifies which word indices the new fields correspond to
#   separator:          String                  (optional) specifies the string used to split the string in the column
#   resolution_type:    Enum (ResolutionType)   (optional) specifies how word index clashes are resolved
#   joiner:             String                  (optional) specifies the string used to join words together

def split_col(table, field_index, new_cols, which_words=None, separator=' ', resolution_type=ResolutionType.no_clash,
              joiner=' '):
    for row_index, row in enumerate(table):
        if row_index != 0:
            words = row[field_index].split(separator)
            if len(words) == len(new_cols) and which_words is None:
                row += words
            elif which_words is not None and len(which_words) == len(new_cols):
                wildcard_found = False
                wildcard_index = -1
                indices = dict()
                for new_col_index, word_index in enumerate(which_words):
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

                row_string = [joiner.join(col) for col in row_addition]
                row += row_string

            else:
                raise Exception(f'number of words and columns provided not equal at index {row_index}')
        else:
            row += new_cols


def matrix_to_csv(table, path):
    with open(path, mode='w') as outfile:
        out = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        out.writerows(table)


def matrix_to_standard(table, field_map, field_consts, header=STANDARD_HEADER):
    # the field map will map the standard field headers to table's field headers
    result = [["" for _ in range(len(header[0]))] for _ in range(len(table) - 1)]

    for std_field_index in field_map:
        table_fields, joiner = field_map[std_field_index]
        for table_field_index in table_fields:
            for row_num, row in enumerate(result):
                if row[std_field_index] == '':
                    row[std_field_index] = table[row_num + 1][table_field_index]
                else:
                    row[std_field_index] += joiner + table[row_num + 1][table_field_index]

    for std_field_index in field_consts:
        for row in result:
            row[std_field_index] = field_consts[std_field_index]

    return result

# ----------------------------------------------------------------------------------------------------------------
#   matrix_to_standard_csv:     No return value             Outputs to a file specified by path
#   table:                      list list String            expected to contain field headers in first row
#   path:                       String                      specifies the output path for the generated CSV
#   field_map:                  dict<int, (list int,  maps a standard field header to a list of our field headers
#                                             String)>
#   field_consts                dict<int, String>        maps a standard field header to a constant string
#   header                      list list String            (optional atm) may consist of multiple rows

def matrix_to_standard_csv(table, path, field_map, field_consts={}, header=STANDARD_HEADER):
    with open(path, mode='w') as outfile:
        out = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        out.writerows(STANDARD_HEADER)
        out.writerows(matrix_to_standard(table, field_map, field_consts, header))


def read_csv(path):
    with open(path, mode='r') as infile:
        reader = csv.reader(infile, delimiter=',')
        table = []
        for row in reader:
            table.append(row)
        return table

