=============
Using Copydoc
=============

Basic usage
-----------

Copydoc cleans and parses HTML from Google docs. Download the HTML version of a
Google document and pass it as a string to the CopyDoc constructor:

.. code:: python

    with open('path/to/html') as f:
        html = f.read()
    doc = CopyDoc(html)

Now you can print the parsed document:

.. code:: python

    print(str(doc))

Access parsed, Beautifulsoup object:

.. code:: python

    soup = doc.soup

Using named tokens
------------------

You can define simple key/value pairs in your docs, for example:

    HEADLINE: Independent candidates gain in polls

    FEATURED_GIF: \https://media.giphy.com/media/l3nWl5bhBoim7glNu/giphy.gif

These key/values can be parsed out by passing a list to the Copydoc constructor:

.. code:: python

    tokens = (
      ('HEADLINE', 'headline'),
      ('FEATURED_GIF', 'featured_gif'),
    )
    doc = CopyDoc(html, tokens)

Now you can access the key/value pairs as attributes on the Copydoc object.

.. code:: python

    print(doc.HEADLINE)

This will print "Independent candidates gain in polls".

Using with Jinja
----------------

The behavior of Copydoc has been designed to work nicely with Jinja.

Here's a sample template snippet based on the doc from above:

.. code:: html

    <h1>{{ doc.headline }}</h1>

    <img src="{{ doc.featured_gif }}" alt="Featured GIF" />

    {{ doc }}
