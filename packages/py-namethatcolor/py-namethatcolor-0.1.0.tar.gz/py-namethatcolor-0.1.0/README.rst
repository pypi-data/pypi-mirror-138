py-namethatcolor
================


About
-----

The script allows to get the closest known color to any given one and also generates its general shade (like Blue, Red, Black, etc)

.. code ::

    >>> from py_namethatcolor import get_color
    >>> color = get_color("#336699")
    >>> color.name
    'Lochmara'
    >>> color.shade.name
    'Blue'


Credits
-------

It's a Python port of the "`Name that Color <https://chir.ag/projects/name-that-color/#6195ED>`_"
script that was originally written by Chirag Mehta and also its improved
version developed for "`Color Name & Hue <https://www.color-blindness.com/color-name-hue/>`_"
by Daniel Flueck
