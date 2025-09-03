######################
ELF Object File Format
######################

.. rubric:: Version |version|

This document describes the
ELF (Executable and Linking Format) object file format.
Chapter 1 presents an overview of the file format
and its data representation.
Chapters 2–6 describe the file header and the structures that
pertain to building programs.
Chapters 7 and 8 describe additional structures that are
necessary to execute a program.

.. only:: html

   This document is also available in `PDF format`_.

.. toctree::
   :maxdepth: 2

   elf/00-foreword

.. toctree::
   :maxdepth: 2
   :numbered:

   elf/01-intro
   elf/02-eheader
   elf/03-sheader
   elf/04-strtab
   elf/05-symtab
   elf/06-reloc
   elf/07-pheader
   elf/08-dynamic

.. toctree::
   :maxdepth: 1

   elf/a-emachine
   elf/b-osabi
   elf/c-history


.. comment

   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

.. _PDF format: elf.pdf
