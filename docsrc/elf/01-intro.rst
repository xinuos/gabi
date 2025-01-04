************
Introduction
************

There are three main types of object files.

* A *relocatable file*
  holds code and data suitable for linking
  with other object files to create an executable
  or a shared object file.

* An *executable file*
  holds a program suitable for execution;
  the file specifies how the system (e.g., ``exec()``)
  creates a program’s process image.

* A *shared object file*
  holds code and data suitable for linking in two contexts.
  First, the link editor processes the shared object file with other relocatable
  and shared object files to create another object file.
  Second, the dynamic linker combines it with an executable file and other
  shared objects to create a process image.

Created by the assembler and link editor, object files are binary
representations of programs intended to be executed directly on
a processor.  Programs that require other abstract machines, such
as shell scripts, are excluded.

File Format
===========

Object files participate in program linking (building a program)
and program execution (running a program).  For convenience and
efficiency, the object file format provides parallel views of a file’s
contents, reflecting the differing needs of those activities.
:numref:`elf-object-file-format` shows an object file’s organization.

.. _elf-object-file-format:

.. figure:: /svg/figure-1.svg
   :alt: ELF Object File Format
   :width: 555pt

   ELF Object File Format

An *ELF header* resides at the beginning and
holds a “road map”
describing the file’s organization. *Sections* hold the bulk
of object file information for the linking view: instructions,
data, symbol table, relocation information, and so on.
Descriptions of special sections appear later.
:ref:`Program-Header` discusses *segments* and the program execution
view of the file.

A *program header table* tells the system how to create a process image.
Files used to build a process image (execute a program)
must have a program header table; relocatable files do not need one.
A *section header table*
contains information describing the file‘s sections.
Every section has an entry in the table; each entry
gives information such as the section name, the
section size, and so on.
Files used during linking must have a section header table;
other object files may or may not have one.

.. note::

   Although :numref:`elf-object-file-format` shows the program header table
   immediately after the ELF header, and the section header table
   following the sections, actual files may differ.
   Moreover, sections and segments have no specified order.
   Only the ELF header has a fixed position in the file.

Data Representation
===================

As described here, the object file format
supports various processors with 8-bit bytes
and either 32-bit or 64-bit architectures.
Nevertheless, it is intended to be extensible to larger
(or smaller) architectures.
Object files therefore represent some control data
with a machine-independent format,
making it possible to identify object files and
interpret their contents in a common way.
Remaining data in an object file
use the encoding of the target processor, regardless of
the machine on which the file was created.

.. _32-bit-data-types:

.. table:: 32-Bit Data Types

   =================  =====  =========  ========================
   Name               Size   Alignment  Purpose
   =================  =====  =========  ========================
   ``Elf32_Addr``     ``4``  ``4``      Unsigned program address
   ``Elf32_Off``      ``4``  ``4``      Unsigned file offset
   ``Elf32_Half``     ``2``  ``2``      Unsigned medium integer
   ``Elf32_Word``     ``4``  ``4``      Unsigned integer
   ``Elf32_Sword``    ``4``  ``4``      Signed integer
   ``unsigned char``  ``1``  ``1``      Unsigned small integer
   =================  =====  =========  ========================

.. _64-bit-data-types:

.. table:: 64-Bit Data Types

   =================  =====  =========  ========================
   Name               Size   Alignment  Purpose
   =================  =====  =========  ========================
   ``Elf64_Addr``     ``8``  ``8``      Unsigned program address
   ``Elf64_Off``      ``8``  ``8``      Unsigned file offset
   ``Elf64_Half``     ``2``  ``2``      Unsigned medium integer
   ``Elf64_Word``     ``4``  ``4``      Unsigned integer
   ``Elf64_Sword``    ``4``  ``4``      Signed integer
   ``Elf64_Xword``    ``8``  ``8``      Unsigned long integer
   ``Elf64_Sxword``   ``8``  ``8``      Signed long integer
   ``unsigned char``  ``1``  ``1``      Unsigned small integer
   =================  =====  =========  ========================

All data structures that the object file format
defines follow the “natural” size and alignment guidelines
for the relevant class.
If necessary, data structures contain explicit padding to
ensure 8-byte alignment for 8-byte objects,
4-byte alignment for 4-byte objects, to force
structure sizes to a multiple of 4 or 8, and so forth.
Data also have suitable alignment from the beginning of the file.
Thus, for example, a structure containing an ``Elf32_Addr``
member will be aligned on a 4-byte boundary within the file.

For portability reasons, ELF uses no bit-fields.

Extensibility
=============

The ELF header contains a version number, which can be incremented for
major changes to the object file format. ELF has been designed, however,
so that such major changes are rare, and the file format can be extended
in several ways that do not require a version number change.

Most object file structures are contained within sections
(see :ref:`sections`), and are designated with special section types.
Additional control structures can be defined by defining new section types.

Many control structures have fields with enumerated values, and the
standard sets aside certain ranges of values for these fields for
implementation-specific uses. These extensions can fall into one of two
classes: processor-specific extensions, which depend on the machine
architecture (see ``e_machine`` in
:ref:`Contents-of-the-ELF-Header`); and OSABI-specific extensions,
which depend on the operating system and psABI (see ``EI_OSABI`` in
:ref:`elf-identification`).

ELF assigns meaning to fields and constant values, throughout the
specification. Any unassigned bits or values not explicitly delegated to
the psABI or OSABI are reserved to the ELF standard for potential future
use. Implementations must not assign meaning, or otherwise make use of,
any unassigned items.

Some object file control structures can grow, because the ELF header
contains their actual sizes. If the object file format changes, a program
may encounter control structures that are larger or smaller than expected.
Programs might therefore ignore “extra” information. The treatment of
“missing” information depends on context and will be specified when and
if extensions are defined. This form of extension is reserved for future
revisions of the ELF standard, and must not be used for
implementation-specific purposes.

Required Features
=================

The ELF standard assigns meaning to a number of features, such as
special sections, symbol types, and program header entries, but an
implementation is not required to support all features defined in this
specification. The psABI supplement should designate which features are
required for a particular implementation.
