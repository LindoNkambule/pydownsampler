pydownsampler
=============

A Python package for downsampling sequence alignment files.

Installation
------------

pydownsampler is available through `pypi`_. To install, type:

.. code:: bash

   pip install pydownsampler

Usage
-----

.. code:: bash

   $ pydownsampler (<file>) [-d <dcov>]
   $ pydownsampler (<file>) [-d <dcov>] [-o <output>]
   $ pydownsampler (<file>) [-c]
   $ pydownsampler [-h] | [--help]
   $ pydownsampler [-v] [--version]

Arguments and Options
---------------------

+------------------------+--------------------------------------------+
| **Argument/ Option**   | **Description**                            |
+========================+============================================+
| ``-h, --help``         | Show help message to screen.               |
+------------------------+--------------------------------------------+
| ``-v, --version``      | Show version.                              |
+------------------------+--------------------------------------------+
| ``<file>``             | Input BAM/CRAM/SAM file                    |
+------------------------+--------------------------------------------+
| ``-d, --downcoverage`` | The coverage you want to downsample to     |
|                        | (Required argument)                        |
+------------------------+--------------------------------------------+
| ``-o, --output``       | Output filename prefix (Optional)          |
+------------------------+--------------------------------------------+
| ``-c, --coverage``     | Check file coverage                        |
+------------------------+--------------------------------------------+

Examples
--------

.. code:: bash

   # option 1 (default):
   $ pydownsampler input.bam -d 10
   In the example above, the file 'input.bam' will be downsampled to 10X coverage. The output filename will be 'input.Downsampled10X.bam'.

   # option 2 (optional):
   $ pydownsampler input.bam -d 10 -o downsampled

   # check coverage of a BAM/CRAM/SAM file
   $ pydownsampler input.bam -c

Authors
-------

`Lindokuhle Nkambule`_

`Scott Hazelhurst`_

License
-------

pydownsampler is generously distributed under The MIT License

.. _pypi: https://pypi.org/project/pydownsampler
.. _Lindokuhle Nkambule: https://github.com/LindoNkambule
.. _Scott Hazelhurst: https://github.com/shaze