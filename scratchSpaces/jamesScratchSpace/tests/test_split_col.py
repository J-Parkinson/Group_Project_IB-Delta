from unittest import TestCase
from .. import matrix_to_csv


class TestSplitCol(TestCase):
    def test_split_col_no_options(self):
        # Assume
        table = [['Full Name'],
                 ['Joe Bloggs']]
        field_name = 'Full Name'
        new_cols = ['First Name', 'Last Name']

        # Action
        try:
            matrix_to_csv.split_col(table, field_name, new_cols)
        except Exception:
            self.fail()

        # Assert
        self.assertEqual(table, [['Full Name', 'First Name', 'Last Name'],
                                 ['Joe Bloggs', 'Joe', 'Bloggs']])

    def test_split_col_separator(self):
        # Assume
        table = [['List'],
                 ['1, 2, 3, 4']]
        field_name = 'List'
        new_cols = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        separator = ', '

        # Action
        try:
            matrix_to_csv.split_col(table, field_name, new_cols, separator=separator)
        except Exception:
            self.fail()

        # Assert
        self.assertEqual(table, [['List', 'Item 1', 'Item 2', 'Item 3', 'Item 4'],
                                 ['1, 2, 3, 4', '1', '2', '3', '4']])

    def test_split_col_joiner(self):
        # Assume
        table = [['List'],
                 ['1, 2, 3, 4']]
        field_name = 'List'
        new_cols = ['Item 1', 'Item 2', 'Others']
        optional = ['0', '1', '*']
        separator = ', '
        joiner = ', '

        # Action
        try:
            matrix_to_csv.split_col(table, field_name, new_cols, optional=optional, separator=separator, joiner=joiner)
        except Exception:
            self.fail()

        # Assert
        self.assertEqual(table, [['List', 'Item 1', 'Item 2', 'Others'],
                                 ['1, 2, 3, 4', '1', '2', '3, 4']])

    def test_split_col_options_single_indices(self):
        # Assume
        table = [['Items'],
                 ['1 2 3 4']]
        field_name = 'Items'
        new_cols = ['Item 2', 'Item 4', 'Item 1', 'Item 3']
        options = ['1', '-1', '0', '2']

        # Action
        try:
            matrix_to_csv.split_col(table, field_name, new_cols, optional=options)
        except Exception:
            self.fail()

        # Assert
        table_index = dict()
        for new_col in new_cols:
            self.assertIn(new_col, table[0])
            table_index[new_col] = table[0].index(new_col)

        self.assertIn('1', table[1])
        self.assertEqual(table[1].index('1'), table_index['Item 1'])
        self.assertIn('2', table[1])
        self.assertEqual(table[1].index('2'), table_index['Item 2'])
        self.assertIn('3', table[1])
        self.assertEqual(table[1].index('3'), table_index['Item 3'])
        self.assertIn('4', table[1])
        self.assertEqual(table[1].index('4'), table_index['Item 4'])

    def test_split_col_options_wildcard(self):
        # Assume
        table = [['Full Name'],
                 ['Joe M. Bloggs']]
        field_name = 'Full Name'
        new_cols = ['First Name', 'Middle Name(s)', 'Last Name']
        options = ['0', '*', '-1']

        # Action
        try:
            matrix_to_csv.split_col(table, field_name, new_cols, optional=options)
        except Exception:
            self.fail()

        # Assert
        table_index = dict()
        for new_col in new_cols:
            self.assertIn(new_col, table[0])
            table_index[new_col] = table[0].index(new_col)

        self.assertIn('Joe', table[1])
        self.assertEqual(table[1].index('Joe'), table_index['First Name'])
        self.assertIn('M.', table[1])
        self.assertEqual(table[1].index('M.'), table_index['Middle Name(s)'])
        self.assertIn('Bloggs', table[1])
        self.assertEqual(table[1].index('Bloggs'), table_index['Last Name'])

    def test_split_col_options_list(self):
        # Assume
        table = [['List'],
                 ['1, 2, 3, 4']]
        field_name = 'List'
        new_cols = ['1st & 4th', '2nd & 3rd']
        options = ['[0, 3]', '[1,2]']
        separator = ', '
        joiner = ', '

        # Action
        try:
            matrix_to_csv.split_col(table, field_name, new_cols, optional=options, separator=separator, joiner=joiner)
        except Exception:
            self.fail()

        # Assert
        table_index = dict()
        for new_col in new_cols:
            self.assertIn(new_col, table[0])
            table_index[new_col] = table[0].index(new_col)

        self.assertIn('1, 4', table[1])
        self.assertEqual(table[1].index('1, 4'), table_index['1st & 4th'])
        self.assertIn('2, 3', table[1])
        self.assertEqual(table[1].index('2, 3'), table_index['2nd & 3rd'])

    def test_split_col_options_range(self):
        # Assume
        table = [['List'],
                 ['1, 2, 3, 4, 5']]
        field_name = 'List'
        new_cols = ['1 - 3', 'Last']
        options = ['0 : 2', '-1']
        separator = ', '
        joiner = ', '

        # Action
        try:
            matrix_to_csv.split_col(table, field_name, new_cols, optional=options, separator=separator, joiner=joiner)
        except Exception:
            self.fail()

        # Assert
        table_index = dict()
        for new_col in new_cols:
            self.assertIn(new_col, table[0])
            table_index[new_col] = table[0].index(new_col)

        self.assertIn('1, 2, 3', table[1])
        self.assertEqual(table[1].index('1, 2, 3'), table_index['1 - 3'])
        self.assertIn('5', table[1])
        self.assertEqual(table[1].index('5'), table_index['Last'])

    def test_split_col_multiple_wildcards(self):
        # Assume
        table = [['Full Name'],
                 ['Joe M. Bloggs']]
        field_name = 'Full Name'
        new_cols = ['First Name', 'Middle Name(s)', 'Last Name']
        options = ['0', '*', '*']

        # Action & Assert
        with self.assertRaises(Exception):
            matrix_to_csv.split_col(table, field_name, new_cols, optional=options)

    def test_split_col_words_and_cols_mismatch(self):
        # Assume
        table = [['Full Name'],
                 ['Joe M. Bloggs']]
        field_name = 'Full Name'
        new_cols = ['First Name', 'Last Name']

        # Action & Assert
        with self.assertRaises(Exception):
            matrix_to_csv.split_col(table, field_name, new_cols)

    def test_split_col_option_invalid(self):
        # Assume
        table = [['List'],
                 ['1, 2, 3, 4']]
        field_name = 'List'
        new_cols = ['1 - 2', '3 - 4']
        options1 = ['0:', '2:3']
        options2 = ['[0, 1]', '[2, 3']
        separator = ', '
        joiner = ', '

        # Action & Assert
        with self.assertRaises(Exception):
            matrix_to_csv.split_col(table, field_name, new_cols, optional=options1, separator=separator, joiner=joiner)

        with self.assertRaises(Exception):
            matrix_to_csv.split_col(table, field_name, new_cols, optional=options2, separator=separator, joiner=joiner)

    def test_split_col_just_first_resolution(self):
        # Assume
        table = [['List'],
                 ['1, 2, 3, 4']]
        field_name = 'List'
        new_cols = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        options = ['0', '0:1', '0:2', '0:3']
        resolution_type = matrix_to_csv.ResolutionType.just_first
        separator = ', '

        # Action
        try:
            matrix_to_csv.split_col(table, field_name, new_cols, optional=options, separator=separator,
                                    resolution_type=resolution_type)
        except Exception:
            self.fail()

        # Assert
        table_index = dict()
        for new_col in new_cols:
            self.assertIn(new_col, table[0])
            table_index[new_col] = table[0].index(new_col)

        self.assertIn('1', table[1])
        self.assertEqual(table[1].index('1'), table_index['Item 1'])
        self.assertIn('2', table[1])
        self.assertEqual(table[1].index('2'), table_index['Item 2'])
        self.assertIn('3', table[1])
        self.assertEqual(table[1].index('3'), table_index['Item 3'])
        self.assertIn('4', table[1])
        self.assertEqual(table[1].index('4'), table_index['Item 4'])

    def test_split_col_just_last_resolution(self):
        # Assume
        table = [['List'],
                 ['1, 2, 3, 4']]
        field_name = 'List'
        new_cols = ['Item 4', 'Item 3', 'Item 2', 'Item 1']
        options = ['0:3', '0:2', '0:1', '0']
        resolution_type = matrix_to_csv.ResolutionType.just_last
        separator = ', '

        # Action
        try:
            matrix_to_csv.split_col(table, field_name, new_cols, optional=options, separator=separator,
                                    resolution_type=resolution_type)
        except Exception:
            self.fail()

        # Assert
        table_index = dict()
        for new_col in new_cols:
            self.assertIn(new_col, table[0])
            table_index[new_col] = table[0].index(new_col)

        self.assertIn('1', table[1])
        self.assertEqual(table[1].index('1'), table_index['Item 1'])
        self.assertIn('2', table[1])
        self.assertEqual(table[1].index('2'), table_index['Item 2'])
        self.assertIn('3', table[1])
        self.assertEqual(table[1].index('3'), table_index['Item 3'])
        self.assertIn('4', table[1])
        self.assertEqual(table[1].index('4'), table_index['Item 4'])

    def test_split_col_all_resolution(self):
        # Assume
        table = [['List'],
                 ['1, 2, 3, 4']]
        field_name = 'List'
        new_cols = ['Item 1', 'Items 1-2', 'Items 1-3']
        options = ['0', '0:1', '0:2']
        resolution_type = matrix_to_csv.ResolutionType.all
        separator = ', '
        joiner = ', '

        # Action
        try:
            matrix_to_csv.split_col(table, field_name, new_cols, optional=options, separator=separator,
                                    resolution_type=resolution_type, joiner=joiner)
        except Exception:
            self.fail()

        # Assert
        table_index = dict()
        for new_col in new_cols:
            self.assertIn(new_col, table[0])
            table_index[new_col] = table[0].index(new_col)

        self.assertIn('1', table[1])
        self.assertEqual(table[1].index('1'), table_index['Item 1'])
        self.assertIn('1, 2', table[1])
        self.assertEqual(table[1].index('1, 2'), table_index['Items 1-2'])
        self.assertIn('1, 2, 3', table[1])
        self.assertEqual(table[1].index('1, 2, 3'), table_index['Items 1-3'])
