######################
ELF Object File Format
######################

.. rubric:: Version 4.3 DRAFT (2025)

This document describes the
object file format, called ELF (Executable and Linking Format).

Chapter 1 presents an overview of the file format
and its data representation.

Chapters 2–6 describe the file header and the structures that
pertain to building programs.

Chapters 7–9 describe additional structures that are
necessary to execute a program.

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
   elf/07-loading-intro
   elf/08-pheader
   elf/09-dynamic

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
