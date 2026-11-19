.. _ELF-Header:

**********
ELF Header
**********

The ELF header resides at the beginning of an ELF file.
It identifies the file as an ELF file and contains the information
necessary for interpreting the contents of the file and locating
the other components of the file.

.. _Contents-of-the-ELF-Header:

Contents of the ELF Header
==========================

.. code-block:: c
   :caption: ELF Header

   #define EI_NIDENT 16

   typedef struct {
           unsigned char   e_ident[EI_NIDENT];
           Elf32_Half      e_type;
           Elf32_Half      e_machine;
           Elf32_Word      e_version;
           Elf32_Addr      e_entry;
           Elf32_Off       e_phoff;
           Elf32_Off       e_shoff;
           Elf32_Word      e_flags;
           Elf32_Half      e_ehsize;
           Elf32_Half      e_phentsize;
           Elf32_Half      e_phnum;
           Elf32_Half      e_shentsize;
           Elf32_Half      e_shnum;
           Elf32_Half      e_shstrndx;
   } Elf32_Ehdr;

   typedef struct {
           unsigned char   e_ident[EI_NIDENT];
           Elf64_Half      e_type;
           Elf64_Half      e_machine;
           Elf64_Word      e_version;
           Elf64_Addr      e_entry;
           Elf64_Off       e_phoff;
           Elf64_Off       e_shoff;
           Elf64_Word      e_flags;
           Elf64_Half      e_ehsize;
           Elf64_Half      e_phentsize;
           Elf64_Half      e_phnum;
           Elf64_Half      e_shentsize;
           Elf64_Half      e_shnum;
           Elf64_Half      e_shstrndx;
   } Elf64_Ehdr;

``e_ident``
    The initial bytes mark the file as an object file and
    provide machine-independent
    data with which to decode and interpret the file’s contents.
    Complete descriptions
    appear below in :numref:`Section {number}, {name} <ELF-Identification>`.

``e_type``
    This member identifies the object file type.

    .. tabularcolumns:: l r l

    .. table:: Object File Types

       =============  ==========  =========================
       Name           Value       Meaning
       =============  ==========  =========================
       ``ET_NONE``    ``0``       No file type
       ``ET_REL``     ``1``       Relocatable file
       ``ET_EXEC``    ``2``       Executable file
       ``ET_DYN``     ``3``       Shared object file
       ``ET_CORE``    ``4``       Core file
       ``ET_LOOS``    ``0xfe00``  Operating system-specific
       ``ET_HIOS``    ``0xfeff``  Operating system-specific
       ``ET_LOPROC``  ``0xff00``  Processor-specific
       ``ET_HIPROC``  ``0xffff``  Processor-specific
       =============  ==========  =========================

    Although the core file contents are unspecified,
    type ``ET_CORE``
    is reserved to mark the file.
    Values from ``ET_LOOS``
    through ``ET_HIOS``
    (inclusive) are reserved for operating system-specific semantics.
    Values from ``ET_LOPROC``
    through ``ET_HIPROC``
    (inclusive) are reserved for processor-specific semantics. If meanings
    are specified, the psABI supplement explains them. Other values are
    reserved and will be assigned to new object file types as necessary.

``e_machine``
    This member’s value specifies the required architecture for
    an individual file.

    See :doc:`Appendix A <a-emachine>`
    for currently-assigned values for this field.
    Other values are reserved and will be assigned to new machines
    as necessary.

    Processor-specific ELF names use the machine name to distinguish them.
    For example, the flags mentioned below use the
    prefix ``EF_``;
    a flag named ``WIDGET`` for the ``EM_XYZ``
    machine would be called ``EF_XYZ_WIDGET``.

``e_version``
    This member identifies the object file version.

    .. tabularcolumns:: l r l

    .. table:: Object File Version Numbers

       ==============  =========  ===============
       Name            Value      Meaning
       ==============  =========  ===============
       ``EV_NONE``     ``0``      Invalid version
       ``EV_CURRENT``  ``1``      Current version
       ==============  =========  ===============

    The value ``1`` signifies the original file format;
    extensions will create new versions with higher numbers.
    Although the value of ``EV_CURRENT``
    is shown as ``1`` in the previous table, it will
    change as necessary to reflect the current version number.

``e_entry``
    This member gives the virtual address to which the
    system first transfers
    control, thus starting the process. If the file has no associated entry
    point, this member holds zero.

``e_phoff``
    This member holds the program header table’s file offset in bytes.
    If the file has no program header table, this member holds zero.

``e_shoff``
    This member holds the section header table’s file offset in bytes.
    If the file has no section header table, this member holds zero.

``e_flags``
    This member holds processor-specific flags associated with the file.
    Flag names take the form
    ``EF_``\ *machine*\ **_**\ *flag*.

``e_ehsize``
    This member holds the ELF header’s size in bytes.

``e_phentsize``
    This member holds the size in bytes of one entry in the file’s program
    header table; all entries are the same size.

``e_phnum``
    This member holds the number of entries in the program header table.
    Thus the product of
    ``e_phentsize`` and ``e_phnum`` gives the
    table’s size in bytes.
    If a file has no program header table, ``e_phnum``
    holds the value zero.

``e_shentsize``
    This member holds a section header’s size in bytes. A section header
    is one entry in the section header table; all entries are the same size.

``e_shnum``
    This member holds the number of entries in the section header table.
    Thus the product of ``e_shentsize`` and
    ``e_shnum`` gives the
    section header table’s size in bytes.
    If a file has no section header table,
    ``e_shnum`` holds the value zero.

    If the number of sections is greater than or equal to
    ``SHN_LORESERVE`` (\ ``0xff00``\ ), this member
    has the value zero and the actual number of section header table
    entries is contained in the ``sh_size`` field of
    the section header at index ``0``.
    (Otherwise, the ``sh_size`` member of the initial entry
    contains ``0``.)

``e_shstrndx``
    This member holds the section header table index of the
    entry associated with the section name string table.
    If the file has no section name string
    table, this member holds the value ``SHN_UNDEF``.
    See :numref:`Chapter {number}, {name} <Sections>`,
    and :numref:`Chapter {number}, {name} <String-Table>`,
    for more information.

    If the section name string table section index is greater than or equal to
    ``SHN_LORESERVE`` (\ ``0xff00``\ ), this member
    has the value ``SHN_XINDEX`` (\ ``0xffff``\ ) and the
    actual index of the section name string table section
    is contained in the ``sh_link`` field of
    the section header at index ``0``.
    (Otherwise, the ``sh_link`` member of the initial entry
    contains ``0``.)

.. _ELF-Identification:

ELF Identification
==================

As mentioned above, ELF provides an object file framework to support
multiple processors, multiple data encodings, and multiple
classes of machines.  To support this object file family,
the initial bytes of the file specify
how to interpret the file, independent of the processor on
which the inquiry is made and independent of the file’s
remaining contents.

The initial bytes of an ELF header (and an object file) correspond to
the ``e_ident`` member.

.. tabularcolumns:: l r l

.. table:: ``e_ident[]`` Identification Indexes

   =================  =========  ===================================
   Name               Value      Purpose
   =================  =========  ===================================
   ``EI_MAG0``        ``0``      File identification
   ``EI_MAG1``        ``1``      File identification
   ``EI_MAG2``        ``2``      File identification
   ``EI_MAG3``        ``3``      File identification
   ``EI_CLASS``       ``4``      File class
   ``EI_DATA``        ``5``      Data encoding
   ``EI_VERSION``     ``6``      File version
   ``EI_OSABI``       ``7``      Operating system/ABI identification
   ``EI_ABIVERSION``  ``8``      ABI version
   ``EI_PAD``         ``9``      Start of padding bytes
   ``EI_NIDENT``      ``16``     Size of ``e_ident[]``
   =================  =========  ===================================

These indexes access bytes that hold the following values.

``EI_MAG0`` to \ ``EI_MAG3``
    A file’s first 4 bytes hold a “magic number,” identifying the file
    as an ELF object file.

    .. tabularcolumns:: l c l

    .. table:: ELF Magic Numbers

       ===========  ==============  ====================
       Name         Value           Position
       ===========  ==============  ====================
       ``ELFMAG0``  ``0x7f``        ``e_ident[EI_MAG0]``
       ``ELFMAG1``  ``0x45 (’E’)``    ``e_ident[EI_MAG1]``
       ``ELFMAG2``  ``0x4C (’L’)``    ``e_ident[EI_MAG2]``
       ``ELFMAG3``  ``0x46 (’F’)``    ``e_ident[EI_MAG3]``
       ===========  ==============  ====================

``EI_CLASS``
    The next byte, ``e_ident[EI_CLASS]``, identifies the
    file’s class, or capacity.

    .. tabularcolumns:: l r l

    .. table:: ELF Class

       ================  =========  ==============
       Name              Value      Meaning
       ================  =========  ==============
       ``ELFCLASSNONE``  ``0``      Invalid class
       ``ELFCLASS32``    ``1``      32-bit objects
       ``ELFCLASS64``    ``2``      64-bit objects
       ================  =========  ==============

    The file format is designed to be portable among machines of various
    sizes, without imposing the sizes of the largest machine on the
    smallest.  The class of the file defines the basic types
    used by the data structures
    of the object file container itself. The data contained in object file
    sections may follow a different programming model. If so, the psABI
    supplement describes the model used.

    Class ``ELFCLASS32`` supports machines with
    32-bit architectures. It uses the basic types defined in
    :numref:`thirty-two-bit-data-types`
    in :numref:`Section {number}, {name} <data-representation>`.

    Class ``ELFCLASS64`` supports machines with 64-bit
    architectures.  It uses the basic types defined in
    :numref:`sixty-four-bit-data-types`
    in :numref:`Section {number}, {name} <data-representation>`.

    Other classes will be defined as necessary, with different basic types
    and sizes for object file data.

.. _ei-data:

``EI_DATA``
    Byte ``e_ident[EI_DATA]`` specifies the
    encoding of both the data structures used by object file container
    and data contained in object file sections.
    The following encodings are currently defined.

    .. tabularcolumns:: l r l

    .. table:: ELF Data Encoding

       ===============  =========  =====================
       Name             Value      Meaning
       ===============  =========  =====================
       ``ELFDATANONE``  ``0``      Invalid data encoding
       ``ELFDATA2LSB``  ``1``      See below
       ``ELFDATA2MSB``  ``2``      See below
       ===============  =========  =====================

    Other values are reserved and will be assigned to new
    encodings as necessary.

    .. note::

       Primarily for the convenience of code that looks at the ELF
       file at runtime, the ELF data structures are intended to have the
       same byte order as that of the running program.

``EI_VERSION``
    Byte ``e_ident[EI_VERSION]`` specifies the
    ELF header version
    number. Currently, this value must be ``EV_CURRENT``,
    as explained above for ``e_version``.

``EI_OSABI``
    Byte ``e_ident[EI_OSABI]`` identifies the
    OS- or ABI-specific ELF extensions used by this file.
    Some fields in other ELF structures have flags and values
    that have operating system and/or ABI specific meanings;
    the interpretation of those fields is determined by the value of this byte.
    If the object file does not use any extensions,
    it is recommended that this byte be set to ``0``.
    If the value for this byte is ``64`` through ``255``,
    its meaning depends on the value of the ``e_machine`` header member.
    The psABI supplement for an architecture
    can define its own associated set of values for this byte in this range.
    If the psABI supplement does not specify a set of values,
    one of the values defined in :doc:`Appendix B <b-osabi>` shall be used,
    where ``0`` (``ELFOSABI_NONE``) can also be taken to mean *unspecified*.

``EI_ABIVERSION``
    Byte ``e_ident[EI_ABIVERSION]`` identifies the
    version of the ABI to which the object is targeted.
    This field is used to distinguish among incompatible versions
    of an ABI.  The interpretation of this version number
    is dependent on the ABI identified by the ``EI_OSABI``
    field.  If no values are specified for the ``EI_OSABI``
    field by the psABI supplement or no version values are
    specified for the ABI determined by a particular value of the
    ``EI_OSABI`` byte, the value ``0`` shall
    be used for the ``EI_ABIVERSION`` byte; it
    indicates *unspecified*.

``EI_PAD``
    This value marks the beginning of the unused bytes in
    ``e_ident``.  These bytes are reserved and set to zero;
    programs that read object files
    should ignore them. The value of ``EI_PAD`` will
    change in the future if currently unused bytes are given
    meanings.

Data Encoding
=============

A file’s data encoding specifies how to interpret the basic objects
in a file. Class ``ELFCLASS32`` files use objects
that occupy 1, 2, and 4 bytes. Class ``ELFCLASS64`` files
use objects that occupy 1, 2, 4, and 8 bytes. Under the defined
encodings, objects are represented as shown below.

Encoding ``ELFDATA2LSB`` specifies 2’s complement values,
with the least significant byte occupying the lowest address.
Encoding ``ELFDATA2MSB`` specifies 2’s complement values,
with the most significant byte occupying the lowest address.
See :numref:`data-encoding`.

.. _data-encoding:

.. figure:: /svg/figure-2.*
   :alt: Data Encoding
   :width: 702pt

   Data Encodings for 8-, 16-, 32-, and 64-bit Values
