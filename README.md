# attribute_dict
A subclass of dict that allows object-style access to its entries.

# Installation
```sh
pipenv install attribute_dict
```

# Usage
```py
    from attribute_dict import AttributeDict
    sample_dict = AttributeDict({'foo': 'bar'})
    sample_dict # => AttributeDict({'foo': 'bar'})

    # The object is just subclassed from dict, and has all of the standard functions
    isinstance(sample_dict, dict) # => True

    # Create a new AttributeDict by "stacking" iterables
    # Each iterable will overwrite keys in the previous one (kwargs are processed last!)
    sample_dict = AttributeDict({'foo': 'foo'}, {'foo': 'ba', 'bar': 'foo'}, {'foo': 'bar'}, {'foobar': 'bar'}, foobar='foo')
    # => AttributeDict({'foo': 'bar', 'bar': 'foo', 'foobar': 'foo'})

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
```

# Tests
Tests use nose2. Clone the Github project. Install dev dependencies, and run tests using the nose2 command.

```sh
pipenv install --dev
pipenv shell
nose2
```
