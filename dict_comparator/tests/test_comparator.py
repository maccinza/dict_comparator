# -*- coding: utf-8 -*-
from __future__ import absolute_import

from unittest import TestCase
from collections import OrderedDict

from dict_comparator.exceptions import UsageError
from dict_comparator.comparator import assert_dicts_equal


class TestDictsComparison(TestCase):

    def test_usage_error(self):
        """Should raise UsageError when arguments are not an especialization of MutableMapping"""

        expected_msg = ('Both objects being compared must be instances of '
                        'dictionaries')
        obj_1 = obj_2 = [1, 2, 3, 4, 5]
        with self.assertRaises(UsageError) as raised:
            assert_dicts_equal(obj_1, obj_2)
        self.assertEqual(raised.exception.message, expected_msg)

    def test_successfully_compare_identical_simple_dicts(self):
        """Should successfully compare simple identical dictionaries that do not contain any inner dictionaries as one of their values"""

        obj_1 = obj_2 = {
            'first-key': 'first-value',
            'second-key': 2,
            'third-key': [3, 2, 1]
        }

        assert_dicts_equal(obj_1, obj_2)

    def test_successfully_compare_simple_dicts_different_key_types(self):
        """Should successfully compare simple dictionaries with keys of different types, and do not contain any inner dictionaries as one of their values and raise an AssertionError"""

        obj_1 = {
            'first-key': 'one'
        }

        obj_2 = {
            'first-key': 1
        }

        expected_msg = ("Value in path ['first-key'] is of type 'str' with value "
                        "'one' in first dict and it is of type 'int' with "
                        "value '1' in second dict")
        with self.assertRaises(AssertionError) as raised:
            assert_dicts_equal(obj_1, obj_2)
        self.assertEqual(raised.exception.message, expected_msg)

    def test_successfully_compare_simple_dicts_different_values(self):
        """Should successfully compare simple dictionaries with keys of same types but different values, and do not contain any inner dictionaries as one of their values and raise an AssertionError"""

        obj_1 = {
            'first-key': 1
        }

        obj_2 = {
            'first-key': 2
        }

        expected_msg = ("Value in path ['first-key'] is '1' in first dict and "
                        "it is '2' in second dict")
        with self.assertRaises(AssertionError) as raised:
            assert_dicts_equal(obj_1, obj_2)
        self.assertEqual(raised.exception.message, expected_msg)

    def test_successfully_compare_complex_dicts(self):
        """Should successfully compare identical complex dictionaries, which include other dictionaries as their values"""

        obj_1 = obj_2 = {
            'first-key': 'one',
            'second-key': {
                'sublevel-1': {
                    'sublevel-2': {
                        'sublevel-3-first': 'leaf-value',
                        'sublevel-3-second': [1, 3, 4, {'simple': 'dictionary'}]
                    }
                }
            }
        }

        assert_dicts_equal(obj_1, obj_2)

    def test_successfully_compare_complex_dicts_different_inner_key_types(self):
        """Should successfully compare complex dictionaries, which include other dictionaries as their values containing keys of different types"""

        obj_1 = {
            'first-key': 'one',
            'second-key': {
                'sublevel-1': {
                    'sublevel-2': {
                        'sublevel-3-first': 'leaf-value',
                        'sublevel-3-second': [1, 3, 4, {'simple': 'dictionary'}]
                    }
                }
            }
        }

        obj_2 = {
            'first-key': 'one',
            'second-key': {
                'sublevel-1': {
                    'sublevel-2': {
                        'sublevel-3-first': None,
                        'sublevel-3-second': [1, 3, 4, {'simple': 'dictionary'}]
                    }
                }
            }
        }

        expected_msg = ("Value in path ['second-key']['sublevel-1']"
                        "['sublevel-2']['sublevel-3-first'] is of type 'str' "
                        "with value 'leaf-value' in first dict and it is of "
                        "type 'NoneType' with value 'None' in second dict")
        with self.assertRaises(AssertionError) as raised:
            assert_dicts_equal(obj_1, obj_2)
        self.assertEqual(raised.exception.message, expected_msg)

    def test_successfully_compare_complex_dicts_different_inner_values(self):
        """Should successfully compare complex dictionaries, which include other dictionaries as their values containing different values for the same key"""

        obj_1 = {
            'first-key': 'one',
            'second-key': {
                'sublevel-1': {
                    'sublevel-2': {
                        'sublevel-3-first': 'leaf-value',
                        'sublevel-3-second': [1, 3, 4, {'simple': 'dictionary'}]
                    }
                }
            }
        }

        obj_2 = {
            'first-key': 'one',
            'second-key': {
                'sublevel-1': {
                    'sublevel-2': {
                        'sublevel-3-first': 'leaf-value',
                        'sublevel-3-second': [1, 3, 4, {'simple': 'dictionaries'}]
                    }
                }
            }
        }

        expected_msg = ("Value in path ['second-key']['sublevel-1']['sublevel-2']"
                        "['sublevel-3-second'][3]['simple'] is 'dictionary' in "
                        "first dict and it is 'dictionaries' in second dict")
        with self.assertRaises(AssertionError) as raised:
            assert_dicts_equal(obj_1, obj_2)
        self.assertEqual(raised.exception.message, expected_msg)

    def test_items_added(self):
        """Should successfully compare different dictionaries when a key is present in the second dict but is not present in the first one"""

        obj_1 = {
            'first-key': 'one',
            'second-key': {
                'sublevel-1': {
                    'sublevel-2': {
                        'sublevel-3-first': 'leaf-value'
                    }
                }
            }
        }

        obj_2 = {
            'first-key': 'one',
            'second-key': {
                'sublevel-1': {
                    'sublevel-2': {
                        'sublevel-3-first': 'leaf-value',
                        'sublevel-3-second': [1, 3, 4, {'simple': 'dictionaries'}]
                    }
                }
            }
        }

        expected_msg = ("The following path/value is not present in the first "
                        "dict but is present in the second dict: "
                        "['second-key']['sublevel-1']['sublevel-2']"
                        "['sublevel-3-second'] -> [1, 3, 4, {'simple': "
                        "'dictionaries'}]")
        with self.assertRaises(AssertionError) as raised:
            assert_dicts_equal(obj_1, obj_2)
        self.assertEqual(raised.exception.message, expected_msg)

    def test_items_remove(self):
        """Should successfully compare different dictionaries when a key is present in the fi dict but is not present in the second one"""

        obj_1 = {
            'first-key': 'one',
            'second-key': {
                'sublevel-1': {
                    'sublevel-2': {
                        'sublevel-3-first': 'leaf-value',
                        'sublevel-3-second': [1, 3, 4, {'simple': 'dictionaries'}]
                    }
                }
            }
        }

        obj_2 = {
            'first-key': 'one',
            'second-key': {
                'sublevel-1': {
                    'sublevel-2': {
                        'sublevel-3-first': 'leaf-value'
                    }
                }
            }
        }

        expected_msg = ("The following path/value is present in the first "
                        "dict but is not present in the second dict: "
                        "['second-key']['sublevel-1']['sublevel-2']"
                        "['sublevel-3-second'] -> [1, 3, 4, {'simple': "
                        "'dictionaries'}]")
        with self.assertRaises(AssertionError) as raised:
            assert_dicts_equal(obj_1, obj_2)
        self.assertEqual(raised.exception.message, expected_msg)

    def test_multiple_differences(self):
        """Should successfully compare different dictionaries with multiple differences"""

        obj_1 = {
            'first-key': 'one',
            'second-key': {
                'sublevel-1': {
                    'sublevel-2': {
                        'sublevel-3-first': 'leaf-value',
                        'sublevel-3-second': [1, 3, 4, {'simple': 'dictionaries'}]
                    }
                }
            },
            'third-key': 3,
            'fourth-key': ['first', 'second', 'third']
        }

        obj_2 = {
            'first-key': 'one',
            'second-key': {
                'sublevel-1': {
                    'sublevel-2': {
                        'sublevel-3-first': 'leaf-value',
                        'sublevel-3-third': 'another-leaf'
                    }
                }
            },
            'third-key': 'three',
            'fourth-key': ['first', 'third']
        }

        expected_msg = ("Value in path ['third-key'] is of type 'int' with "
                        "value '3' in first dict and it is of type 'str' with "
                        "value 'three' in second dict\nThe following path/value "
                        "is present in the first dict but is not present in the "
                        "second dict: ['second-key']['sublevel-1']['sublevel-2']"
                        "['sublevel-3-second'] -> [1, 3, 4, {'simple': "
                        "'dictionaries'}]\nValue in path ['fourth-key'][1] is "
                        "'second' in first dict and it is 'third' in second "
                        "dict\nThe following path/value is not present in the "
                        "first dict but is present in the second dict: "
                        "['second-key']['sublevel-1']['sublevel-2']"
                        "['sublevel-3-third'] -> another-leaf")

        with self.assertRaises(AssertionError) as raised:
            assert_dicts_equal(obj_1, obj_2)
        self.assertEqual(raised.exception.message, expected_msg)
