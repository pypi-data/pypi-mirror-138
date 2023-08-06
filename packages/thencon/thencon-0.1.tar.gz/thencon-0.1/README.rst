(thencon) A library that’ll help you convert Thai to English / English to Thai(by Kedmanee keyboard layout)
===========================================================================================================

PyPI: https://pypi.org/project/thencon

This library will help you convert Thai to English / English to Thai(by
Kedmanee keyboard layout)

Have you ever type a long phrase and realised you forgot to change the
language on the keyboard? Well, this library can help you out! By
installing this package and run it with python, it can automatically
convert English into Thai or even Thai to English.

btw. “thencon” stands for Thai English Converter in case you want to
know :)

How to install:
~~~~~~~~~~~~~~~

Open CMD / Terminal and type this command

.. code:: python

   pip install thencon

Usage:
~~~~~~

[STEP 1] - Open python IDLE and type…

.. code:: python

   from thencon import translate

[STEP 2]

.. code:: python

   thencon.translate(your-method(1 or 2), your text)

Methods: - (1): Convert English to Thai - (2): Convert Thai to English

[Example]

.. code:: python

   # -*- coding: utf-8 -*-

   from thencon import translate

   entext = ("l;ylfu") #Typing Thai with English keyboard
   thtext = ("็ำสสน") #Typing English with Thai keyboard

   converted_th = translate(1, entext) #Convert English to thai
   converted_en = translate(2, thtext) #Convert Thai to English

   print("The Thai text is: " + converted_th)
   print("The English text is: " + converted_en)

Developed by: ADR
