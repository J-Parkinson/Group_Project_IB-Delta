from unittest import TestCase
from .. import matrix_to_csv


class TestAddToIndices(TestCase):
    def test_add_to_indices_out_of_range(self):
        # Assume
        indices = {}
        num_words = 4
        col_index = 2
        word_index1 = -1
        word_index2 = 4
        resolution_type = matrix_to_csv.ResolutionType.no_clash

        # Action & Assert
        with self.assertRaises(Exception):
            matrix_to_csv.add_to_indices(word_index1, col_index, indices,
                                         resolution_type, num_words)

        with self.assertRaises(Exception):
            matrix_to_csv.add_to_indices(word_index2, col_index, indices,
                                         resolution_type, num_words)

    def test_add_to_indices_clash(self):
        # Assume
        indices = {0: [2]}
        num_words = 4
        col_index = 3
        word_index1 = 0
        word_index2 = 1
        resolution_type = matrix_to_csv.ResolutionType.no_clash

        # Action & Assert
        with self.assertRaises(Exception):
            matrix_to_csv.add_to_indices(word_index1, col_index, indices, resolution_type, num_words)

        matrix_to_csv.add_to_indices(word_index2, col_index, indices, resolution_type, num_words)
        self.assertDictEqual(indices, {0: [2], 1: [3]}, 'failed to avoid a clash for different word indices')

    def test_add_to_indices_pick_first_type(self):
        # Assume
        indices = {0: [2]}
        num_words = 4
        col_index = 3
        word_index = 0
        resolution_type = matrix_to_csv.ResolutionType.just_first

        # Action
        matrix_to_csv.add_to_indices(word_index, col_index, indices, resolution_type, num_words)

        # Assert
        self.assertDictEqual(indices, {0: [2]})

    def test_add_to_indices_pick_last_type(self):
        # Assume
        indices = {0: [2]}
        num_words = 4
        col_index = 3
        word_index = 0
        resolution_type = matrix_to_csv.ResolutionType.just_last

        # Action
        matrix_to_csv.add_to_indices(word_index, col_index, indices, resolution_type, num_words)

        # Assert
        self.assertDictEqual(indices, {0: [3]})

    def test_add_to_indices_all_type(self):
        # Assume
        indices = {0: [2]}
        num_words = 4
        col_index = 3
        word_index = 0
        resolution_type = matrix_to_csv.ResolutionType.all

        # Action
        matrix_to_csv.add_to_indices(word_index, col_index, indices, resolution_type, num_words)

        # Assert
        self.assertDictEqual(indices, {0: [2, 3]}, 'failed to correctly add index to dictionary in all type')
