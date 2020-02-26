from unittest import TestCase
import pathlib
from utils.csv import spell_check


class TestSpellCheck(TestCase):
    def setUp(self):
        test_dir = pathlib.Path(__file__).parent
        self.test_dict1 = spell_check.get_dictionary(test_dir / 'dict.txt')
        self.test_dict2 = spell_check.get_dictionary(test_dir / 'dict2.txt')
        self.test_full_dict = spell_check.get_dictionary(test_dir / 'NHM_butterfly_dict.txt')

    def test_correct_words_sub(self):
        # Assume
        test = "fest"

        # Action
        corrected = spell_check.correct_words(test, self.test_dict1)

        # Assert
        self.assertEqual(corrected, 'test')

    def test_correct_words_del(self):
        # Assume
        test = 'thiss'

        # Action
        corrected = spell_check.correct_words(test, self.test_dict1)

        # Assert
        self.assertEqual(corrected, 'this')

    def test_correct_words_ins(self):
        # Assume
        test = 'tet'

        # Action
        corrected = spell_check.correct_words(test, self.test_dict1)

        # Assert
        self.assertEqual(corrected, 'test')

    def test_correct_words_sub_priority(self):
        # Assume
        test = 'cloan'

        # Action
        corrected = spell_check.correct_words(test, self.test_dict2)

        # Assert
        self.assertEqual(corrected, 'clean')

    def test_correct_words_multiple_two_mistakes(self):
        # Assume
        test = "evclidla glyphjce"

        # Action
        corrected = spell_check.correct_words(test, self.test_full_dict)

        # Assert
        self.assertEqual(corrected, 'euclidia glyphica')

