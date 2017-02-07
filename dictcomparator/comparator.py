# -*- coding: utf-8 -*-
from __future__ import absolute_import

from deepdiff import DeepDiff

from dictcomparator.exceptions import UsageError


def __parse_diff_msg(diff):
    msgs = set()
    for issue_type, issues in diff.items():
        for issue_path in issues:
            path = issue_path.replace('root', '', 1)
            info = issues[issue_path]
            if issue_type == 'type_changes':
                msg = ("Value in path {0} is of type '{1}' with value '{2}' "
                       "in first dict and it is of type '{3}' with value "
                       "'{4}' in second dict").format(
                    path, info['old_type'].__name__, info['old_value'],
                    info['new_type'].__name__, info['new_value'])
            elif issue_type == 'values_changed':
                msg = ("Value in path {0} is '{1}' in first dict and it is "
                       "'{2}' in second dict").format(
                    path, info['old_value'], info['new_value'])
            elif issue_type == 'dictionary_item_added':
                path += ' -> {0}'.format(info)
                msg = ("The following path/value is not present in the first "
                       "dict but is present in the second "
                       "dict: {0}").format(path)
            elif issue_type == 'dictionary_item_removed':
                path += ' -> {0}'.format(info)
                msg = ("The following path/value is present in the first "
                       "dict but is not present in the second "
                       "dict: {0}").format(path)
            msgs.add(msg)
    return '\n'.join(msgs)


def __compare_objs(first, second):
    diff = DeepDiff(first, second, verbose_level=2)
    if diff:
        msg = __parse_diff_msg(diff)
        raise AssertionError(msg)


def assert_dicts_equal(first, second):
    are_dicts = all(
        [isinstance(first, dict), isinstance(second, dict)])

    if not are_dicts:
        raise UsageError(
            'Both objects being compared must be instances of dictionaries')

    if first == second:
        return

    __compare_objs(first, second)
