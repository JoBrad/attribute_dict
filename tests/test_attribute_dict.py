# -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals, print_function
import unittest
import nose2
from nose2.tools import such

from .utils import (
    AttributeDict, to_dict, create_objs,
    get_dict, get_kwargs, get_args, compare_objs
)

with such.A('AttributeDict class') as it:
    @it.has_test_setup
    def setup(case):
        case.actual = None
        case.expected = None

    @it.has_test_teardown
    def tearDown(case):
        case.actual = None
        case.expected = None

    @it.should('Be able to create a blank AttributeDict object')
    def test_item_creation(case):
        case.actual = AttributeDict()
        case.expected = to_dict()
        it.assertEqual(case.actual.keys(), case.expected.keys())

    @it.should('Be able to create an AttributeDict object by passing arguments')
    def test_create_with_args(case):
        case.actual, case.expected = create_objs((AttributeDict, to_dict), *get_args())
        compare_objs(it, case.actual, case.expected, (AttributeDict, dict))

    @it.should('Be able to create an AttributeDict object by passing keyword arguments')
    def test_create_with_kwargs(case):
        case.actual, case.expected = create_objs((AttributeDict, to_dict), **get_kwargs())
        compare_objs(it, case.actual, case.expected, (AttributeDict, dict))

    @it.should('Be able to create an AttributeDict object by passing arguments and keyword arguments')
    def test_create_with_kwargs(case):
        case.actual, case.expected = create_objs((AttributeDict, to_dict), *get_args(), **get_kwargs())
        compare_objs(it, case.actual, case.expected, (AttributeDict, dict))

    @it.should('Be able to add items using dictionary-style notation (e.g. obj[name] = value')
    def test_item_addition(case):
        case.expected = to_dict(get_kwargs())
        case.actual = AttributeDict()
        for k, v in case.expected.items():
            case.actual[k] = v
            it.assertIn(k, case.actual)
        compare_objs(it, case.actual, case.expected, (AttributeDict, dict))

    @it.should('Be able to add items using object-style notation (e.g. obj.name = value')
    def test_attr_creation(case):
        case.expected = to_dict(**get_kwargs())
        case.actual = AttributeDict()
        for k, v in case.expected.items():
            try:
                setattr(case.actual, k, v)
            except Exception as ex:
                it.fail(ex)
        compare_objs(it, case.actual, case.expected, (AttributeDict, dict))

    with it.having('AttributeDict with items'):
        description = '*** AttributeDict dictionary-style item access ***'
        @it.has_test_setup
        def setup(case):
            case.actual = AttributeDict(**get_kwargs())
            case.expected = to_dict(**get_kwargs())

        @it.should('Create a new object with .copy()')
        def test_obj_copy(case):
            actual_copy = case.actual.copy()
            assert actual_copy is not case.actual

        @it.should('Copy should contain all items from original')
        def test_obj_copy(case):
            actual_copy = case.actual.copy()
            compare_objs(it, actual_copy, case.actual, (AttributeDict, dict))

        @it.should('Be able to access items using dictionary-style notation (e.g. obj[name])')
        def test_item_access(case):
            for k, v in case.expected.items():
                it.assertIn(k, case.actual)
                try:
                    it.assertEqual(case.actual[k], v)
                except Exception as ex:
                    it.fail(ex)

        @it.should('Be able to access items using object-style notation (e.g. obj.name')
        def test_attr_access(case):
            for k, v in case.expected.items():
                it.assertIn(k, case.actual)
                try:
                    it.assertEqual(getattr(case.actual, k), v)
                except Exception as ex:
                    it.fail(ex)

        @it.should('Be able to delete items using dictionary-style notation (e.g. del obj[name])')
        def test_item_deletion(case):
            for k, v in case.expected.items():
                it.assertIn(k, case.actual)
                try:
                    del case.actual[k]
                    it.assertNotIn(k, case.actual)
                except Exception as ex:
                    it.fail(ex)

        @it.should('Be able to delete items using object-style notation (e.g. del obj.name)')
        def test_attr_deletion(case):
            for k, v in case.expected.items():
                it.assertIn(k, case.actual)
                try:
                    delattr(case.actual, k)
                    it.assertNotIn(k, case.actual)
                except Exception as ex:
                    it.fail(ex)

it.createTests(globals())

if __name__ == '__main__':
    nose2.main(verbosity=3)
