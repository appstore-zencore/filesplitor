file-split
==========

.. image:: https://travis-ci.org/appstore-zencore/filesplitor.svg?branch=master
    :target: https://travis-ci.org/appstore-zencore/filesplitor

.. image:: https://img.shields.io/codecov/c/github/appstore-zencore/filesplitor.svg?style=flat-square
    :target: https://codecov.io/gh/appstore-zencore/filesplitor


Split file into small ones.


Install
-------

::

    pip install filesplitor


Usage
-----

::

    E:\s\b>filesplitor split test.txt -s 2
    Split file [test.txt] into 2B sized files...
    test.txt.1
    test.txt.2
    Done!

    E:\s\b>filesplitor merge b.txt test.txt.*
    Merge files ['test.txt.1', 'test.txt.2'] into one file [b.txt]...
    Done!


Command Help
------------

::

    E:\s\b>filesplitor --help
    Usage: filesplitor [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    merge
    split

    E:\s\b>filesplitor split --help
    Usage: filesplitor split [OPTIONS] SRC [DST]

    Options:
    -s, --size TEXT  File slice size, default to 1G. Accepted units are B, K, M,
                    G, T.
    --help           Show this message and exit.

    E:\s\b>filesplitor merge --help
    Usage: filesplitor merge [OPTIONS] DST FILENAMES...

    Options:
    --help  Show this message and exit.

