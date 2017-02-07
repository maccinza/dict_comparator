==============
DictComparator
==============
Improved output for dictionaries comparison



What is it?
~~~~~~~~~~~~~~~~~~~~~~~~

It is a very simple library aimed to developers which provides better output when
comparing python dictionaries during tests.


How does it work?
~~~~~~~~~~~~~~~~~

The library uses the open source library deepdiff_ to check for dictionaries
differences and parses its output for a more friendly set of error messages
when an *AssertionError* is raised.

The library exposes a function, **assert_dicts_equal**, which should be used
in tests when comparing a result dict object to an expected dict object.


Installation
~~~~~~~~~~~~

Simply run:

.. code:: bash

    $ pip install dictcomparator


Usage
~~~~~

For using the library in tests it is as simple as the following:

.. code:: python

    from dictcomparator import assert_dicts_equal

    ...
    # dict_1 and dict_2 are the two dictionaries being compared
    assert_dicts_equal(dict_1, dict_2)


If the dictionaries have any differences they will be detailed in the error
messages of the *AssertionError* exception raised.


Tests
~~~~~

The library includes its own set of simple tests. You may run them using your
favorite tests runner. For development *nose* was used as the test runner.


.. _deepdiff: https://github.com/seperman/deepdiff
