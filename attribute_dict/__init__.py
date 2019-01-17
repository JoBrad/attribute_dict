# -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import sys
_str = str if sys.version[0] == '3' else unicode

__all__ = ['AttributeDict']
__version__ = '1.0.0'
name = 'attribute_dict'
"""
A subclass of dict that allows object-style access to its entries
"""

class AttributeDict(dict):
    """
    A subclass of dict that allows object-style access to its entries

    @example
        # Create a new AttributeDict by "stacking" iterables
        # Each iterable will overwrite keys in the previous one (kwargs are processed last!)
        iterable_one = {'foo': 'foo'}
        iterable_two = {'foo': 'ba', 'bar': 'foo'}

        sample_dict = AttributeDict(iterable_one, iterable_two, {'foobar': 'foo', 'foo': 'bar'})
        sample_dict # => AttributeDict({'foo': 'bar', 'bar': 'foo', 'foobar': 'foo'})

        # Create a new AttributeDict by shallow-copying an existing one
        new_sample_dict = sample_dict.copy()
        new_sample_dict # => AttributeDict({'foo': 'bar', 'bar': 'foo', 'foobar': 'foo'})
        isinstance(new_sample_dict, AttributeDict) # => True

        # NOTE: Child values are NOT processed!
        sample_dict = AttributeDict({'foo': iterable_two})
        sample_dict # => AttributeDict({'foo': {'foo': 'ba', 'bar': 'foo'}})
        sample_dict.foo # => {'foo': 'ba', 'bar': 'foo'}
        sample_dict.__class__.__name__ # => 'AttributeDict'
        sample_dict.foo.__class__.__name__ # => 'dict'

    """
    def __init__(self, *iterables, **kwargs):
        """Creates a new AttributeDict

        >>> AttributeDict({'foo': 'bar'})
        AttributeDict({'foo': 'bar'})

        # Stack arguments and kwargs (kwargs are processed last!)
        >>> AttributeDict({'foo': 'foo'}, {'foo': 'ba', 'bar': 'foo'}, {'foo': 'bar'}, {'foobar': 'bar'}, foobar='foo')
        AttributeDict({'foo': 'bar', 'bar': 'foo', 'foobar': 'foo'})

        >>> # The object is just subclassed from dict, and has all of the standard functions
        >>> isinstance(AttributeDict(), dict)
        True
        """
        data = {}
        for iterable in iterables:
            data.update(dict(iterable))
        data.update(**kwargs)
        super(AttributeDict, self).__init__(data)

    def __getattribute__(self, name):
        """Return name from self

        >>> sample_dict = AttributeDict({'foo': 'bar'})
        >>> sample_dict['foo']
        'bar'

        >>> sample_dict.foo
        'bar'
        """
        if name == '__reserved__':
            return dir({})
        elif name in dir({}):
            return super(AttributeDict, self).__getattribute__(name)
        else:
            return super(AttributeDict, self).__getitem__(name)

    def __setattr__(self, name, value):
        """Sets name equal to value for self

        # Set the value using dot notation
        >>> sample_dict = AttributeDict()
        >>> sample_dict.foo = 2
        >>> sample_dict.foo
        2

        # Add a new value using dot notation
        >>> sample_dict.bar = 'foo'
        >>> sample_dict.bar
        'foo'
        """
        if name == '__reserved__' or name in self.__reserved__:
            raise NotImplementedError('Cannot set reserved attribute `' + _str(name) + '`!')
        super(AttributeDict, self).__setitem__(name, value)

    def __delattr__(self, name):
        """Deletes name from self

        >>> sample_dict = AttributeDict({'foo': 'bar', 'bar': 'foo'})
        >>> del sample_dict['foo']
        >>> 'foo' in sample_dict
        False
        >>> del sample_dict.bar
        >>> 'bar' in sample_dict
        False
        >>> sample_dict
        AttributeDict({})
        """
        if name == '__reserved__' or name in self.__reserved__:
            raise NotImplementedError('Cannot set reserved attribute `' + _str(name) + '`!')
        else:
            super().__delitem__(name)

    def copy(self):
        """
        Returns a shallow copy of this object

        >>> sample_dict = AttributeDict({'foo': 'bar'})
        >>> new_sample_dict = sample_dict.copy()
        >>> new_sample_dict
        AttributeDict({'foo': 'bar'})
        >>> new_sample_dict is sample_dict
        False
        >>> new_sample_dict == sample_dict
        True
        >>> isinstance(new_sample_dict, AttributeDict)
        True
        """
        return AttributeDict(**super(AttributeDict, self).copy())

    def __repr__(self):
        """
        Returns a printable representation of this object
        >>> sample_dict = AttributeDict({'foo': 'bar'})
        >>> repr(sample_dict)
        "AttributeDict({'foo': 'bar'})"
        """
        return self.__class__.__name__ + '(' + _str(dict(self.items())) + ')'
