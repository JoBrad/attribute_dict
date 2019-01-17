# -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import (unicode_literals, print_function)
from collections.abc import (Callable, MappingView, Sequence)
from functools import partial, reduce
import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from attribute_dict import AttributeDict

__all__ = [
    'AttributeDict', 'to_dict', 'run_tests', 'Test',
    'create_objs', 'get_dict', 'get_kwargs', 'get_args',
    'compare_objs'
]

def create_objs(func_tuple, *args, **kwargs):
    """
    Returns a tuple of the results of passing each function
    in func_tuple args and kwargs
    """
    results = []
    for func in func_tuple:
        results.append(func(*args, **kwargs))
    return tuple(results)

def to_dict(*iterables, **kwargs):
    """
    Returns a dictionary that contains all passed iterables and keyword arguments
    """
    data = {}
    for iterable in iterables:
        data.update(dict(iterable))
    data.update(**kwargs)
    return data

def _lists_match_reducer(sequence_one, sequence_two):
    """
    Returns list_one if sequence_one matches sequence_two
    Otherwise returns False
    """
    __tracebackhide__ = True
    try:
        if sequence_one is not False:
            l1 = list(sequence_one)
            l2 = list(sequence_two)
            if l1 == l2:
                return l1
    except:
        pass

    return False

def _cmp_views_for_objs(fx_name, *objs):
    """
    Returns True if the result of obj.fx_name() matches
    for each provided object
    """
    # Proceed step by step to aid troubleshooting if one of them fails
    fxs = [getattr(ob, fx_name) for ob in objs]
    fx_results = [fx() for fx in fxs]
    result = reduce(_lists_match_reducer, fx_results)
    return result is not False

_cmp_keys = partial(_cmp_views_for_objs, 'keys')
_cmp_values = partial(_cmp_views_for_objs, 'values')

def _cmp_objs(constructed_obj, comparison_obj, instance_comparators=(AttributeDict, dict)):
    """
    Creates an object by passing constructor_fx and validator_fx args and kwargs, and then returns a
    Generator of 3 values, which will be either True, or an AssertionError:
        * True if isinstance(constructor_fx, instance_comparators) is True, or an AssertionError
        * True if the keys for constructed_obj and comparison_obj match, or an AssertionError
        * True if the values for constructed_obj and comparison_obj match, or an AssertionError
    """
    __tracebackhide__ = True
    constructed_obj_instance = constructed_obj.__class__.__name__ or 'The provided object'

    if not isinstance(constructed_obj, instance_comparators):
        inst_mismatches = []
        for inst in instance_comparators:
            if not isinstance(constructed_obj, inst):
                inst_mismatches.append(inst.__name__)
        yield AssertionError('{constructed_obj_instance} was not of type {inst_name}!'.format(
            constructed_obj_instance = constructed_obj_instance,
            inst_name = ' or '.join(inst_mismatches)))
    else:
        # Instance comparison passed!
        yield True

    if _cmp_keys(constructed_obj, comparison_obj) is False:
        yield AssertionError('{constructed_obj_instance} did not contain the expected keys!')
    else:
        # Key comparison passed!
        yield True

    if _cmp_values(constructed_obj, comparison_obj) is False:
        yield AssertionError('{constructed_obj_instance} did not contain the expected values!')
    else:
        # Value comparison passed!
        yield True

def compare_objs(it, actual, expected, instance_types):
    test_gen = _cmp_objs(actual, expected, instance_types)
    it.assertEqual(next(test_gen), True, 'The object was not of type AttributeDict or dict!')
    it.assertEqual(next(test_gen), True, 'The object did not have the expected set of keys!')
    it.assertEqual(next(test_gen), True, 'The object did not have the expected set of values!')

def run_tests(test_cases):
    """
    test_cases = tuple(assert_function, assert_function_args, fail_message)
    assert_function should fail or return False on failure
    """
    assert_failure_message = None
    try:
        for (assert_function, assert_function_args, fail_message) in test_cases:
            test_result = False
            assert_failure_message = fail_message
            if isinstance(assert_function_args, tuple):
                test_result = assert_function(*assert_function_args)
            elif isinstance(assert_function_args, dict):
                test_result = assert_function(**assert_function_args)
            else:
                test_result = assert_function(assert_function_args)
            if test_result is False:
                raise AssertionError()

    except Exception as ex:
        err_message = [assert_failure_message or '']
        err_message.append(ex)
        pytest.fail('\n'.join(err_message))

def get_dict():
    return {'foo': 'bar'}

def get_kwargs():
    return {'foo': 'bar', 'foobar': 'foo'}

def get_args():
    return ({'foo': 'foo'}, {'foo': 'bar', 'bar': 'b'}, {'bar': 'fo'}, (('bar', 'foo'), ))
