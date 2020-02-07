import csv

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


def split_words(table, field_name, new_cols):
    field_index = table[0].index(field_name)
    for row_index, row in enumerate(table):
        if row_index != 0:
            words = row[field_index].split()
            row += words
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
          'Forest Hill Marlborough', 'Paten', '']]
std_test = [['Invertebrates; Insects', 'Object', 'Present', 'I.2019.2147', '', '', '', 'Hesperiidae', 'Thymelicus',
             'lineola', 'Hesperiidae', 'Thymelicus', 'lineola', '', 'Essex Skipper', 'Yes', '', 'Dry', '1',
             'Pinned whole\nDorsal', 'Male', 'Adult', '', 'Fair',
             'Right antenna missing\nSlight discolouration on left forewing', '[England, U.K.]', '[Essex]',
             'Shoeburyness', '', '20/07/[18]90', '', '[Adkin ?]', '[R ?]', '', 'W.H. Ballett Fletcher',
             'Ex coll W. H. Ballett Fletcher 1941:1\nShoeburyness\n20.7.90\n[R. Adkin ?] 6.11.90\n\n', 'Insect Room',
             'Lower', 'Cab 1', 'Drawer 40.02', 'Column 1 Row 1', '']]

matrix_to_csv(test, './jamesScratchSpace/test.csv')
matrix_to_csv(test2, './jamesScratchSpace/test2.csv')


split_words(test2, 'Present Determination', ['Genus', 'Species'])
matrix_to_standard_csv(test2, './jamesScratchSpace/std_test.csv', {'Current Genus': 'Genus',
                                                                   'Current species': 'Species'})
