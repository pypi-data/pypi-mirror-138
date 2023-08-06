NoseOfYeti aware black
======================

This is a monkey patch of black (https://github.com/psf/black) to give it the
ability to understand the noseOfYeti (http://noseofyeti.readthedocs.io)
``spec`` coding.

To use it::

   $ pip install noy_black
   $ noy_black file_to_format.py

Where all the arguments are the same as the normal black command.

It will even use noseOfYeti to tokenize the original and the formatted files to
check that the ast is equivalent before and after formatting with black.

Caveats
-------

Because ``it``, ``ignore``, ``describe``, ``before_each`` and
``after_each`` are special keywords only for noseOfYeti, you can still use these
words as variable names. However you cannot start a line with any of these
keywords or black will get confused.

For example:

.. code-block:: python

   # This will confuse black
   describe = 1

   # This will not confuse black
   one, describe = 1, 2

   # this will also not confuse black
   for it in [1, 2]:
      print(it)

   # but this will
   it = 1

Also, this works by defining the whole python grammar plus some extra grammar
so new versions of black will mean I have to update my version of the Grammar.

Doesn't work anymore!
---------------------

Since the stable version of black now comes as binary .so files, the hack that
makes this work no longer works and you need to do something like::

    python -m pip install --no-binary black noy_black

Changelog
---------

0.3.2 - 17 February 2022
    * Fixes for new version of black

0.3.1 - 16 February 2022
    * Upgrade black to 22.1.0

0.3.0 - 6 November 2021
    * Upgrade black to 21.10b0

0.2.1 - 22 November 2020
    * Upgrade version of black to use with this

0.2.0 - 22 March 2020
    * Now only support noseOfYeti>=2.0.0

0.1.5 - 9 November 2019
    * Make it compatible with python3.6

0.1.4 - 9 November 2019
    * Make it compatible with python3.8

0.1.3 - 30 October 2019
    * Initial release
