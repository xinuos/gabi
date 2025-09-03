.. _Sections:

********
Sections
********

An object file’s section header table lets one
locate all the file’s sections.
The section header table is an array of ``Elf32_Shdr``
or ``Elf64_Shdr`` structures
as described below.
A section header table index is a subscript into this array.
The ELF header’s ``e_shoff``
member gives the byte offset from the beginning of the
file to the section header table.
``e_shnum`` normally tells how many entries the section header table contains.
``e_shentsize`` gives the size in bytes of each entry.

Sections contain all information in an object file
except the ELF header, the program header table,
and the section header table.
Moreover, object files’ sections satisfy several conditions.

* Every section in an object file has exactly one
  section header describing it.
  Section headers may exist that do not have a section.

* Each section occupies one contiguous (possibly empty)
  sequence of bytes within a file.

* Sections in a file may not overlap.
  No byte in a file resides in more than one section.

* An object file may have inactive space.
  The various headers and the sections might not
  “cover” every byte in an object file.
  The contents of the inactive data are unspecified.

  .. note::

     A common example of inactive space is the padding
     placed between sections to ensure proper alignment
     for the subsequent section.

If the number of sections is greater than or equal to
``SHN_LORESERVE`` (\ ``0xff00``\ ), ``e_shnum``
has the value ``SHN_UNDEF`` (\ ``0``\ ) and the
actual number of section header table
entries is contained in the ``sh_size`` field of
the section header at index ``0``
(otherwise, the ``sh_size`` member of the initial entry
contains ``0``\ ).

.. _special-section-indexes:

Special Section Indexes
=======================

Some section header table indexes are reserved in contexts
where index size is restricted, for example, the ``st_shndx``
member of a symbol table entry and the ``e_shnum`` and
``e_shstrndx`` members of the ELF header.
In such contexts, the reserved values do not represent actual
sections in the object file.  Also in such contexts, an escape
value indicates that the actual section
index is to be found elsewhere, in a larger field.

.. tabularcolumns:: l r

.. table:: Special Section Indexes
   :width: 50%

   =================  ==========
   Name               Value
   =================  ==========
   ``SHN_UNDEF``      ``0``
   ``SHN_LORESERVE``  ``0xff00``
   ``SHN_LOPROC``     ``0xff00``
   ``SHN_HIPROC``     ``0xff1f``
   ``SHN_LOOS``       ``0xff20``
   ``SHN_HIOS``       ``0xff3f``
   ``SHN_ABS``        ``0xfff1``
   ``SHN_COMMON``     ``0xfff2``
   ``SHN_XINDEX``     ``0xffff``
   ``SHN_HIRESERVE``  ``0xffff``
   =================  ==========

``SHN_UNDEF``
    This value marks an undefined, missing, irrelevant, or
    otherwise meaningless section reference.
    For example, a symbol “defined” relative to section number
    ``SHN_UNDEF`` is an undefined symbol.

    .. note::

       Although index 0 is reserved as the undefined value,
       the section header table contains an entry for index 0.
       If the ``e_shnum``
       member of the ELF header says a file has 6 entries
       in the section header table, they have the indexes 0 through 5.
       The contents of the initial entry are specified in
       :numref:`Section {number}, {name} <first-section-header-table-entry>`.

``SHN_LORESERVE``
    This value specifies the lower bound of the
    range of reserved indexes.

``SHN_LOPROC`` through \ ``SHN_HIPROC``
    Values in this inclusive range
    are reserved for processor-specific semantics.

``SHN_LOOS`` through \ ``SHN_HIOS``
    Values in this inclusive range
    are reserved for operating system-specific semantics.

``SHN_ABS``
    This value specifies absolute values for the corresponding reference.
    For example, symbols defined relative to section number ``SHN_ABS``
    have absolute values and are not affected by relocation.

``SHN_COMMON``
    Symbols defined relative to this section are common symbols,
    such as FORTRAN
    ``COMMON``
    or unallocated C external variables.

``SHN_XINDEX``
    This value is an escape value.
    It indicates that the actual section header index is too large to fit
    in the containing field and is to be found in another location
    (specific to the structure where it appears).

``SHN_HIRESERVE``
    This value specifies the upper bound of the
    range of reserved indexes.
    The system reserves indexes between ``SHN_LORESERVE``
    and ``SHN_HIRESERVE``,
    inclusive; the values do not reference the section header table.
    The section header table does not
    contain entries for the reserved indexes.

Section Header Table Entry
==========================

A section header has the following structure.

.. code-block:: c
   :caption: Section Header

   typedef struct {
       Elf32_Word  sh_name;
       Elf32_Word  sh_type;
       Elf32_Word  sh_flags;
       Elf32_Addr  sh_addr;
       Elf32_Off   sh_offset;
       Elf32_Word  sh_size;
       Elf32_Word  sh_link;
       Elf32_Word  sh_info;
       Elf32_Word  sh_addralign;
       Elf32_Word  sh_entsize;
   } Elf32_Shdr;

   typedef struct {
       Elf64_Word  sh_name;
       Elf64_Word  sh_type;
       Elf64_Xword sh_flags;
       Elf64_Addr  sh_addr;
       Elf64_Off   sh_offset;
       Elf64_Xword sh_size;
       Elf64_Word  sh_link;
       Elf64_Word  sh_info;
       Elf64_Xword sh_addralign;
       Elf64_Xword sh_entsize;
   } Elf64_Shdr;

``sh_name``
    This member specifies the name of the section.
    Its value is an index into the section header string table section
    (see :numref:`Chapter {number}, {name} <String-Table>`),
    giving the location of a null-terminated string.

``sh_type``
    This member categorizes the section’s contents and semantics.
    Section types and their descriptions appear
    below.

``sh_flags``
    Sections support 1-bit flags that describe miscellaneous attributes.
    Flag definitions appear
    below.

``sh_addr``
    If the section will appear in the memory image of a process,
    this member gives the address at which the section’s first
    byte should reside.
    Otherwise, the member contains 0.

``sh_offset``
    This member’s value gives the byte offset from the beginning of the file
    to the first byte in the section.
    One section type, ``SHT_NOBITS``
    described
    below,
    occupies no space in the file, and its
    ``sh_offset`` member locates the conceptual placement in the file.

``sh_size``
    This member gives the section’s size in bytes.
    Unless the section type is
    ``SHT_NOBITS``, the section occupies ``sh_size``
    bytes in the file.
    A section of type ``SHT_NOBITS``
    may have a non-zero size, but it occupies no space in the file.

``sh_link``
    This member holds a section header table index link,
    whose interpretation depends on the section type.
    (See :numref:`Section {number}, {name} <shlink-shinfo-fields>`.)

``sh_info``
    This member holds extra information,
    whose interpretation depends on the section type.
    (See :numref:`Section {number}, {name} <shlink-shinfo-fields>`.)
    If the ``sh_flags`` field for this
    section header includes the attribute ``SHF_INFO_LINK``, then this member represents a section header table index.

``sh_addralign``
    Some sections have address alignment constraints.
    For example, if a section holds a doubleword,
    the system must ensure doubleword alignment for the entire section.
    The value of ``sh_addr``
    must be congruent to 0, modulo the value of ``sh_addralign``.
    Currently, only 0 and positive integral powers of two are allowed.
    Values 0 and 1 mean the section has no alignment constraints.

``sh_entsize``
    Some sections hold a table of fixed-size entries,
    such as a symbol table.
    For such a section, this member gives the size in bytes of each entry.
    The member contains 0 if the section does not hold a table
    of fixed-size entries.

Section Type
============

A section header’s ``sh_type`` member specifies the section’s semantics.

.. tabularcolumns:: l r

.. table:: Section Types, ``sh_type``

   =====================  ==============
   Name                   Value
   =====================  ==============
   ``SHT_NULL``           ``0``
   ``SHT_PROGBITS``       ``1``
   ``SHT_SYMTAB``         ``2``
   ``SHT_STRTAB``         ``3``
   ``SHT_RELA``           ``4``
   ``SHT_HASH``           ``5``
   ``SHT_DYNAMIC``        ``6``
   ``SHT_NOTE``           ``7``
   ``SHT_NOBITS``         ``8``
   ``SHT_REL``            ``9``
   ``SHT_SHLIB``          ``10``
   ``SHT_DYNSYM``         ``11``
   ``SHT_INIT_ARRAY``     ``14``
   ``SHT_FINI_ARRAY``     ``15``
   ``SHT_PREINIT_ARRAY``  ``16``
   ``SHT_GROUP``          ``17``
   ``SHT_SYMTAB_SHNDX``   ``18``
   ``SHT_RELR``           ``19``
   ``SHT_LOOS``           ``0x60000000``
   ``SHT_HIOS``           ``0x6fffffff``
   ``SHT_LOPROC``         ``0x70000000``
   ``SHT_HIPROC``         ``0x7fffffff``
   ``SHT_LOUSER``         ``0x80000000``
   ``SHT_HIUSER``         ``0xffffffff``
   =====================  ==============

``SHT_NULL``
    This value marks the section header as inactive;
    it does not have an associated section.
    Other members of the section header have undefined values.

``SHT_PROGBITS``
    The section holds information defined by the program,
    whose format and meaning are determined solely by the program.

``SHT_SYMTAB`` and \ ``SHT_DYNSYM``
    These sections hold a symbol table.
    Currently, an object file may have only one section of each type,
    but this restriction may be relaxed in the future.
    Typically, ``SHT_SYMTAB``
    provides symbols for link editing, though it may also be
    used for dynamic linking.
    As a complete symbol table, it may contain many symbols unnecessary
    for dynamic linking.
    Consequently, an object file may also contain a ``SHT_DYNSYM``
    section, which holds a minimal set of dynamic linking symbols,
    to save space.
    See “Symbol Table” below
    for details.

``SHT_STRTAB``
    The section holds a string table.
    An object file may have multiple string table sections.
    See :numref:`Chapter {number}, {name} <String-Table>`, for details.

``SHT_RELA``
    The section holds relocation entries
    with explicit addends, such as type
    ``Elf32_Rela`` for the 32-bit class of object files
    or type ``Elf64_Rela`` for the 64-bit class of object files.
    An object file may have multiple relocation sections.
    See :numref:`Chapter {number}, {name} <Relocation>`, for details.

``SHT_HASH``
    The section holds a symbol hash table.
    Currently, an object file may have only one hash table,
    but this restriction may be relaxed in the future.
    See :numref:`Section {number}, {name} <Hash-Table>`, for details.

``SHT_DYNAMIC``
    The section holds information for dynamic linking.
    Currently, an object file may have only one dynamic section,
    but this restriction may be relaxed in the future.
    See :numref:`Section {number}, {name} <Dynamic-Section>`, for details.

``SHT_NOTE``
    The section holds information that marks the file in some way.
    See :numref:`Section {number}, {name} <Note-Sections>`, for details.

``SHT_NOBITS``
    A section of this type occupies no space in the file but
    otherwise resembles
    ``SHT_PROGBITS``.
    Although this section contains no bytes, the ``sh_offset``
    member contains the conceptual file offset.

``SHT_REL``
    The section holds relocation entries
    without explicit addends, such as type
    ``Elf32_Rel`` for the 32-bit class of object files or
    type ``Elf64_Rel`` for the 64-bit class of object files.
    An object file may have multiple relocation sections.
    See :numref:`Chapter {number}, {name} <Relocation>`, for details.

``SHT_SHLIB``
    This section type is reserved but has unspecified semantics.

``SHT_INIT_ARRAY``
    This section contains an array of pointers to initialization functions,
    as described in
    :numref:`Section {number}, {name} <Initialization-and-Termination-Functions>`.
    Each pointer in the array is taken as a parameterless procedure
    with a void return.

``SHT_FINI_ARRAY``
    This section contains an array of pointers to termination functions,
    as described in
    :numref:`Section {number}, {name} <Initialization-and-Termination-Functions>`.
    Each pointer in the array is taken as a parameterless procedure
    with a void return.

``SHT_PREINIT_ARRAY``
    This section contains an array of pointers to functions that are
    invoked before all other initialization functions,
    as described in
    :numref:`Section {number}, {name} <Initialization-and-Termination-Functions>`.
    Each pointer in the array is taken as a parameterless procedure
    with a void return.

``SHT_GROUP``
    This section defines a section group.  A section group
    is a set of sections that are related and that must be treated
    specially by the linker (see below for further
    details).  Sections of type ``SHT_GROUP`` may appear only
    in relocatable objects (objects with the ELF header ``e_type``
    member set to ``ET_REL``\ ).   The section header table entry
    for a group section must appear in the section header table
    before the entries for any of the sections that are members of
    the group.

``SHT_SYMTAB_SHNDX``
    This section is associated with a symbol table section
    and is required if any of the section header indexes referenced
    by that symbol table contain the escape value ``SHN_XINDEX``.
    The section is an array of ``Elf32_Word/Elf64_Word`` values.
    Each value corresponds one to one with a symbol table entry
    and appear in the same order as those entries.
    The values represent the section header indexes against which
    the symbol table entries are defined.
    Only if the corresponding symbol table entry’s ``st_shndx`` field
    contains the escape value ``SHN_XINDEX``
    will the matching word hold the actual section header index;
    otherwise, the entry must be ``SHN_UNDEF`` (\ ``0``\ ).

``SHT_RELR``
   The section holds an array of relocation entries, used to encode
   relative relocations that do not require explicit addends or other
   information. Array elements are of type ``Elf32_Relr`` for
   ``ELFCLASS32`` objects, and ``Elf64_Relr`` for ``ELFCLASS64``
   objects. ``SHT_RELR`` sections are for dynamic linking, and may only
   appear in object files of type ``ET_EXEC`` or ``ET_DYN``. An object
   file may have multiple relocation sections.
   See :numref:`Chapter {number}, {name} <Relocation>` for details.

``SHT_LOOS`` through \ ``SHT_HIOS``
    Values in this inclusive range
    are reserved for operating system-specific semantics.

``SHT_LOPROC`` through \ ``SHT_HIPROC``
    Values in this inclusive range
    are reserved for processor-specific semantics.

``SHT_LOUSER``
    This value specifies the lower bound of the range of
    indexes reserved for application programs.

``SHT_HIUSER``
    This value specifies the upper bound of the range of
    indexes reserved for application programs.
    Section types between ``SHT_LOUSER`` and
    ``SHT_HIUSER`` may be used by the application, without conflicting with
    current or future system-defined section types.

Other section type values are reserved.

Section Flags
=============

A section header’s ``sh_flags``
member holds 1-bit flags that describe the section’s attributes.
Defined values appear in the following table;
other values are reserved.

.. tabularcolumns:: l r

.. table:: Section Attribute Flags

   ========================  ==============
   Name                      Value
   ========================  ==============
   ``SHF_WRITE``             ``0x1``
   ``SHF_ALLOC``             ``0x2``
   ``SHF_EXECINSTR``         ``0x4``
   ``SHF_MERGE``             ``0x10``
   ``SHF_STRINGS``           ``0x20``
   ``SHF_INFO_LINK``         ``0x40``
   ``SHF_LINK_ORDER``        ``0x80``
   ``SHF_OS_NONCONFORMING``  ``0x100``
   ``SHF_GROUP``             ``0x200``
   ``SHF_TLS``               ``0x400``
   ``SHF_COMPRESSED``        ``0x800``
   ``SHF_MASKOS``            ``0x0ff00000``
   ``SHF_MASKPROC``          ``0xf0000000``
   ========================  ==============

If a flag bit is set in ``sh_flags``,
the attribute is “on” for the section.
Otherwise, the attribute is “off” or does not apply.
Undefined attributes are set to zero.

``SHF_WRITE``
    The section contains data that should be writable during
    process execution.

``SHF_ALLOC``
    The section occupies memory during process execution.
    Some control sections do not reside in the memory image
    of an object file; this attribute is off for those sections.

``SHF_EXECINSTR``
    The section contains executable machine instructions.

``SHF_MERGE``
    The data in the section may be merged to eliminate duplication.
    Unless the ``SHF_STRINGS`` flag is also set,
    the data elements in the section are of a uniform size.
    The size of each element is specified in the section
    header’s ``sh_entsize`` field.
    If the ``SHF_STRINGS`` flag is also set,
    the data elements consist of null-terminated character strings.
    The size of each character is specified in the section
    header’s ``sh_entsize`` field.

    Each element in the section is compared against other elements
    in sections with the same name, type and flags.
    Elements that would have identical values at program run-time
    may be merged.
    Relocations referencing elements of such sections must be
    resolved to the merged locations of the referenced values.
    Note that any relocatable values, including
    values that would result in run-time relocations, must be
    analyzed to determine whether the run-time values would actually
    be identical.  An ABI-conforming object file may not depend
    on specific elements being merged, and an ABI-conforming
    link editor may choose not to merge specific elements.

``SHF_STRINGS``
    The data elements in the section consist of null-terminated character
    strings.  The size of each character is specified in the section
    header’s ``sh_entsize`` field.

``SHF_INFO_LINK``
    The ``sh_info`` field of this section header holds a section
    header table index.

``SHF_LINK_ORDER``
    This flag adds special ordering requirements for link editors. The
    requirements apply to the referenced section identified by the
    ``sh_link`` field of this section's header. If this section is combined
    with other sections in the output file, the section must appear in
    the same relative order with respect to those sections, as the
    referenced section appears with respect to sections the referenced
    section is combined with.

    .. note::

       A typical use of this flag is to build a table that references text or
       data sections in address order.

    In addition to adding ordering requirements, ``SHF_LINK_ORDER``
    indicates that the section contains metadata describing the
    referenced section. When performing unused section elimination, the
    link editor should ensure that both the section and the referenced
    section are retained or discarded together. Furthermore, relocations
    from this section into the referenced section should not be taken as
    evidence that the referenced section should be retained.

``SHF_OS_NONCONFORMING``
    This section requires special OS-specific processing
    (beyond the standard linking rules)
    to avoid incorrect behavior.
    If this section has either an ``sh_type`` value
    or contains ``sh_flags`` bits in the OS-specific ranges for
    those fields, and a link editor processing this section does not
    recognize those values, then the link editor should reject
    the object file containing this section with an error.

``SHF_GROUP``
    This section is a member (perhaps the only one) of a section group.
    The section must be referenced by a section of type ``SHT_GROUP``.
    The ``SHF_GROUP`` flag may be set only for sections contained
    in relocatable objects (objects with the ELF header ``e_type``
    member set to ``ET_REL``\ ).
    See below for further details.

``SHF_TLS``
    This section holds *Thread-Local Storage*,
    meaning that each separate execution flow
    has its own distinct instance of this data.
    Implementations need not support this flag.

``SHF_COMPRESSED``
    This flag identifies a section containing compressed data. In
    ET_EXEC and ET_DYN files, SHF_COMPRESSED cannot be used in
    conjunction with SHF_ALLOC.  In addition, SHF_COMPRESSED cannot be
    applied to sections of type SHT_NOBITS.
    See :numref:`Section {number}, {name} <Compressed-Sections>`, below.

``SHF_MASKOS``
    All bits included in this mask
    are reserved for operating system-specific semantics.

``SHF_MASKPROC``
    All bits included in this mask
    are reserved for processor-specific semantics.
    If meanings are specified, the psABI supplement explains them.

.. _shlink-shinfo-fields:

The sh_link and sh_info Fields
==============================

Two members in the section header,
``sh_link`` and ``sh_info``,
hold special information, depending on section type.

.. tabularcolumns::  >{\raggedright\arraybackslash}p{1.5in} >{\raggedright\arraybackslash}p{2in} >{\raggedright\arraybackslash}p{2in}

.. table:: ``sh_link`` and ``sh_info`` Interpretation
   :width: 100%
   :widths: 1, 2, 2

   ====================================  ====================================  ================================================================
   ``sh_type``                           ``sh_link``                           ``sh_info``
   ====================================  ====================================  ================================================================
   ``SHT_DYNAMIC``                       The section header index of           ``0``
                                         the string table used by
                                         entries in the section.

   ``SHT_HASH``                          The section header index of           ``0``
                                         the symbol table to which
                                         the hash table applies.

   ``SHT_REL`` |br| ``SHT_RELA``         The section header index of           The section header index of
                                         the associated symbol table.          the section to which the
                                                                               relocation applies.

   ``SHT_SYMTAB`` |br| ``SHT_DYNSYM``    The section header index of           One greater than the symbol table index of the last local
                                         the associated string table.          symbol (binding ``STB_LOCAL``\ ).

   ``SHT_GROUP``                         The section header index of           The symbol table index of an entry in the
                                         the associated symbol table.          associated symbol table.  The name of the specified symbol table
                                                                               entry provides a signature for the section group.

   ``SHT_SYMTAB_SHNDX``                  The section header index of           ``0``
                                         the associated symbol table section.
   ====================================  ====================================  ================================================================

.. _first-section-header-table-entry:

First Section Header Table Entry
================================

As mentioned before, the section header at index 0 (\ ``SHN_UNDEF``\ )
exists, even though the index marks undefined section references.
This entry holds the following.

.. tabularcolumns:: l l l

.. table:: First Section Header Table Entry

   ================  ============  =================================================================
   Name              Value         Note
   ================  ============  =================================================================
   ``sh_name``       ``0``         No name
   ``sh_type``       ``SHT_NULL``  Inactive
   ``sh_flags``      ``0``         No flags
   ``sh_addr``       ``0``         No address
   ``sh_offset``     ``0``         No offset
   ``sh_size``       Unspecified   If non-zero, the actual number of section header entries
   ``sh_link``       Unspecified   If non-zero, the index of the section header string table section
   ``sh_info``       ``0``         No auxiliary information
   ``sh_addralign``  ``0``         No alignment
   ``sh_entsize``    ``0``         No entries
   ================  ============  =================================================================

.. _Compressed-Sections:

Compressed Sections
===================

The ``SHF_COMPRESSED`` section header flag indicates a section
that has been compressed to save space in the object file.

All relocations to a compressed section specify offsets to the
uncompressed section data.  It is therefore necessary to decompress
the section data before relocations can be applied.  Each compressed section
specifies the algorithm independently.  It is permissible for
different sections in a given ELF object to employ different compression
algorithms.

Compressed sections begin with a compression header structure that
identifies the compression algorithm.

.. code-block:: c
   :caption: Compression Header

   typedef struct {
       Elf32_Word  ch_type;
       Elf32_Word  ch_size;
       Elf32_Word  ch_addralign;
   } Elf32_Chdr;

   typedef struct {
       Elf64_Word  ch_type;
       Elf64_Word  ch_reserved;
       Elf64_Xword ch_size;
       Elf64_Xword ch_addralign;
   } Elf64_Chdr;

``ch_type``
    This member specifies the compression algorithm.  Supported algorithms
    and their descriptions are listed in the
    ELF Compression Types table below.

``ch_size``
    This member provides the size in bytes of the uncompressed data.
    See ``sh_size``.

``ch_addralign``
    Specifies the required alignment for the uncompressed data.
    See ``sh_addralign``.

The ``sh_size`` and ``sh_addralign`` fields of the section
header for a compressed section reflect the requirements of the
compressed section.  The ``ch_size`` and ``ch_addralign``
fields in the compression header provide the corresponding values for the
uncompressed data, thereby supplying the values that ``sh_size`` and
``sh_addralign`` would have had if the section had not been
compressed.

The layout and interpretation of the data that follows the compression header
is specific to each algorithm, and is defined below for each value of
``ch_type``.  This area may contain algorithm specific parameters
and alignment padding in addition to compressed data bytes.

A compression header’s ``ch_type`` member specifies the
compression algorithm employed, as shown in the following table.

.. tabularcolumns:: l r

.. table:: ELF Compression Types, ``ch_type``
   :width: 50%

   ======================  ==============
   Name                    Value
   ======================  ==============
   ``ELFCOMPRESS_ZLIB``    ``1``
   ``ELFCOMPRESS_ZSTD``    ``2``
   ``ELFCOMPRESS_LOOS``    ``0x60000000``
   ``ELFCOMPRESS_HIOS``    ``0x6fffffff``
   ``ELFCOMPRESS_LOPROC``  ``0x70000000``
   ``ELFCOMPRESS_HIPROC``  ``0x7fffffff``
   ======================  ==============

``ELFCOMPRESS_ZLIB``
    The section data is compressed with the ZLIB algorithm.  The compressed
    ZLIB data bytes begin with the byte immediately following the compression
    header, and extend to the end of the section.  Additional documentation
    for ZLIB may be found at http://zlib.net.

``ELFCOMPRESS_ZSTD``
    The section data is compressed with the Zstandard algorithm. The
    compressed Zstandard data bytes begin with the byte immediately
    following the compression header, and extend to the end of the
    section. Additional documentation for Zstandard may be found at
    http://www.zstandard.org.

``ELFCOMPRESS_LOOS - ELFCOMPRESS_HIOS``
    Values in this inclusive range are reserved for operating system-specific
    semantics.

``ELFCOMPRESS_LOPROC - ELF_COMPRESS_HIPROC``
    Values in this inclusive range are reserved for processor-specific semantics.

Rules for Linking Unrecognized Sections
=======================================

If a link editor encounters sections whose headers contain OS-specific
values it does not recognize in the ``sh_type``
or ``sh_flags`` fields, the link editor should combine those
sections as described below.

If the section’s ``sh_flags`` bits include the attribute
``SHF_OS_NONCONFORMING``, then the section requires
special knowledge to be correctly processed, and the link editor should
reject the object containing the section with an error.

Unrecognized sections that do not have the
``SHF_OS_NONCONFORMING`` attribute, are combined in a two-phase
process.  As the link editor combines sections using this process,
it must honor the alignment constraints of the
input sections (asserted by the ``sh_addralign`` field),
padding between sections with zero bytes, if necessary, and producing
a combination with the maximum alignment constraint of its
component input sections.

1. In the first phase, input sections that match in name, type
   and attribute flags should be concatenated into single sections.
   The concatenation order should satisfy the requirements of
   any known input section attributes (e.g, ``SHF_MERGE``
   and ``SHF_LINK_ORDER``\ ).  When not otherwise constrained,
   sections should be emitted in input order.

2. In the second phase, sections should be assigned to segments or
   other units based on their attribute flags.  Sections of each particular
   unrecognized type should be assigned to the same unit unless
   prevented by incompatible flags, and within a unit, sections
   of the same unrecognized type should be placed together
   if possible.

Non OS-specific processing (e.g. relocation) should be applied
to unrecognized section types.  An output section header table,
if present, should contain entries for unknown sections.
Any unrecognized section attribute flags should be removed.

.. note::

   It is recommended that link editors follow the same two-phase
   ordering approach described above when linking sections of
   known types.  Padding between such sections may have values
   different from zero, where appropriate.

Section Groups
==============

Some sections occur in interrelated groups.  For example, an out-of-line
definition of an inline function might require, in addition to the
section containing its executable instructions, a read-only data
section containing literals referenced, one or more debugging information
sections and other informational sections.  Furthermore, there may be
internal references among these sections that would not make sense
if one of the sections were removed or replaced by a duplicate from
another object.  Therefore, such groups must be
included or omitted from the linked object as a unit.
A section cannot be a member of more than one group.

A section of type ``SHT_GROUP`` defines such a grouping
of sections. The name of a symbol from one of the containing
object’s symbol tables provides a signature for the section group.
The section header of the ``SHT_GROUP`` section specifies
the identifying symbol entry, as described above:
the ``sh_link`` member contains the section header index
of the symbol table section that contains the entry.
The ``sh_info`` member contains the symbol table index of
the identifying entry.   The ``sh_flags``
member of the section header contains ``0``.
The name of the section (\ ``sh_name``\ ) is not specified.

The referenced signature symbol is not restricted.
Its containing symbol table section need not be a member of the group,
for example.

The section data of a ``SHT_GROUP`` section is an array
of ``Elf32_Word/Elf64_Word`` entries.  The first entry is a flag word.
The remaining entries are a sequence of section header indices.

The following flags are currently defined:

.. tabularcolumns:: l r

.. table:: Section Group Flags

   ================  ==============
   Name              Value
   ================  ==============
   ``GRP_COMDAT``    ``0x1``
   ``GRP_MASKOS``    ``0x0ff00000``
   ``GRP_MASKPROC``  ``0xf0000000``
   ================  ==============

``GRP_COMDAT``
    This is a COMDAT group.  It may duplicate another COMDAT group
    in another object file, where duplication is defined as having the
    same group signature.  In such cases, only one of the
    duplicate groups may be retained by the linker, and the
    members of the remaining groups must be discarded.

``GRP_MASKOS``
    All bits included in this mask
    are reserved for operating system-specific semantics.

``GRP_MASKPROC``
    All bits included in this mask
    are reserved for processor-specific semantics.
    If meanings are specified, the psABI supplement explains them.

The section header indices in the ``SHT_GROUP`` section
identify the sections that make up the group.  Each such section
must have the ``SHF_GROUP`` flag set in its ``sh_flags``
section header member.  If the linker decides to remove the section
group, it must remove all members of the group.

.. note::

   This requirement is not intended to imply that special case behavior
   like removing debugging information requires removing the sections
   to which that information refers, even if they are part of the same
   group.

To facilitate removing a group without leaving dangling references
and with only minimal processing of the symbol table,
the following rules must be followed:

* A symbol table entry with ``STB_GLOBAL`` or ``STB_WEAK``
  binding that is defined relative to one of a group’s sections,
  and that is contained in a symbol table section
  that is not part of the group,
  must be converted to an undefined symbol
  (its section index must be changed to ``SHN_UNDEF``\ )
  if the group members are discarded.
  References to this symbol table entry from outside the group are allowed.

* A symbol table entry with ``STB_LOCAL`` binding
  that is defined relative to one of a group’s sections,
  and that is contained in a symbol table section
  that is not part of the group,
  must be discarded if the group members are discarded.
  References to this symbol table entry from outside the group are not allowed.

* An undefined symbol that is referenced only from one or more sections
  that are part of a particular group,
  and that is contained in a symbol table section
  that is not part of the group,
  is not removed when the group members are discarded.
  In other words,
  the undefined symbol is not removed
  even if no references to that symbol remain.

* There may not be non-symbol references to the sections comprising
  a group from outside the group, for example, use of a group
  member’s section header index in an ``sh_link`` or
  ``sh_info`` member.

.. _Special-Sections:

Special Sections
================

Various sections hold program and control information.

The following table
shows sections that are used by the system
and have the indicated types and attributes.

.. tabularcolumns:: l l l

.. table:: Special Sections

   ==================  =====================  ===============================
   Name                Type                   Attributes
   ==================  =====================  ===============================
   ``.bss``            ``SHT_NOBITS``         ``SHF_ALLOC+SHF_WRITE``
   ``.comment``        ``SHT_PROGBITS``       none
   ``.data``           ``SHT_PROGBITS``       ``SHF_ALLOC+SHF_WRITE``
   ``.data1``          ``SHT_PROGBITS``       ``SHF_ALLOC+SHF_WRITE``
   ``.debug``          ``SHT_PROGBITS``       none
   ``.dynamic``        ``SHT_DYNAMIC``        see below
   ``.dynstr``         ``SHT_STRTAB``         ``SHF_ALLOC``
   ``.dynsym``         ``SHT_DYNSYM``         ``SHF_ALLOC``
   ``.fini``           ``SHT_PROGBITS``       ``SHF_ALLOC+SHF_EXECINSTR``
   ``.fini_array``     ``SHT_FINI_ARRAY``     ``SHF_ALLOC+SHF_WRITE``
   ``.got``            ``SHT_PROGBITS``       see below
   ``.hash``           ``SHT_HASH``           ``SHF_ALLOC``
   ``.init``           ``SHT_PROGBITS``       ``SHF_ALLOC+SHF_EXECINSTR``
   ``.init_array``     ``SHT_INIT_ARRAY``     ``SHF_ALLOC+SHF_WRITE``
   ``.interp``         ``SHT_PROGBITS``       see below
   ``.line``           ``SHT_PROGBITS``       none
   ``.note``           ``SHT_NOTE``           none
   ``.plt``            ``SHT_PROGBITS``       see below
   ``.preinit_array``  ``SHT_PREINIT_ARRAY``  ``SHF_ALLOC+SHF_WRITE``
   ``.rel``\ *name*    ``SHT_REL``            see below
   ``.rela``\ *name*   ``SHT_RELA``           see below
   ``.relr.dyn``       ``SHT_RELR``           ``SHF_ALLOC``
   ``.rodata``         ``SHT_PROGBITS``       ``SHF_ALLOC``
   ``.rodata1``        ``SHT_PROGBITS``       ``SHF_ALLOC``
   ``.shstrtab``       ``SHT_STRTAB``         none
   ``.strtab``         ``SHT_STRTAB``         see below
   ``.symtab``         ``SHT_SYMTAB``         see below
   ``.symtab_shndx``   ``SHT_SYMTAB_SHNDX``   see below
   ``.tbss``           ``SHT_NOBITS``         ``SHF_ALLOC+SHF_WRITE+SHF_TLS``
   ``.tdata``          ``SHT_PROGBITS``       ``SHF_ALLOC+SHF_WRITE+SHF_TLS``
   ``.tdata1``         ``SHT_PROGBITS``       ``SHF_ALLOC+SHF_WRITE+SHF_TLS``
   ``.text``           ``SHT_PROGBITS``       ``SHF_ALLOC+SHF_EXECINSTR``
   ==================  =====================  ===============================

``.bss``
    This section holds uninitialized data that contribute
    to the program’s memory image.
    By definition, the system initializes the data with zeros
    when the program begins to run.
    The section occupies no file space, as indicated by the section type,
    ``SHT_NOBITS``.

``.comment``
    This section holds version control information.

``.data`` and ``.data1``
    These sections hold initialized data that contribute
    to the program’s memory image.

``.debug``
    This section holds information for symbolic debugging.
    The contents are unspecified.  All section names with the
    prefix ``.debug`` are reserved for future use in the
    ABI.

``.dynamic``
    This section holds dynamic linking information.
    The section’s attributes will include the ``SHF_ALLOC`` bit.
    Whether the ``SHF_WRITE`` bit is set is processor specific.
    See :numref:`Section {number}, {name} <Dynamic-Section>`, for more information.

``.dynstr``
    This section holds strings needed for dynamic linking,
    most commonly the strings
    that represent the names associated with symbol table entries.
    See :numref:`Section {number}, {name} <Dynamic-Section>`, for more information.

``.dynsym``
    This section holds the dynamic linking symbol table,
    as described in :numref:`Chapter {number}, {name} <Symbol-Table>`,
    and :numref:`Chapter {number}, {name} <Dynamic-Linking>`.

``.fini``
    This section holds executable instructions that contribute
    to the process termination code.
    That is, when a program exits normally, the system arranges
    to execute the code in this section.

``.fini_array``
    This section holds an array of function pointers that contributes
    to a single termination array for the executable or shared
    object containing the section.

``.got``
    This section holds the global offset table.
    See the psABI supplement for more information.

``.hash``
    This section holds a symbol hash table.
    See :numref:`Section {number}, {name} <Hash-Table>`, for more information.

``.init``
    This section holds executable instructions that contribute
    to the process initialization code.
    When a program starts to run, the system arranges
    to execute the code in this section before calling the
    main program entry point (called ``main`` for C programs).

``.init_array``
    This section holds an array of function pointers that contributes
    to a single initialization array for the executable or shared
    object containing the section.

``.interp``
    This section holds the path name of a program interpreter.
    If the file has a loadable segment that includes
    relocation, the sections’ attributes will include the
    ``SHF_ALLOC`` bit; otherwise, that bit will be off.
    See :numref:`Section {number}, {name} <Program-Interpreter>`, for more information.

``.line``
    This section holds line number information for symbolic
    debugging, which describes
    the correspondence between the source program and the
    machine code.
    The contents are unspecified.

``.note``
    This section holds information as described in
    :numref:`Section {number}, {name} <Note-Sections>`.

``.plt``
    This section holds the procedure linkage table.
    See the psABI supplement for more information.

``.preinit_array``
    This section holds an array of function pointers that contributes
    to a single pre-initialization array for the executable or shared
    object containing the section.

``.rel``\ *name* and \ ``.rela``\ *name*
    These sections hold relocation information, as described in
    :numref:`Chapter {number}, {name} <Relocation>`.
    If the file has a loadable segment that includes
    relocation, the sections’ attributes will include the
    ``SHF_ALLOC`` bit; otherwise, that bit will be off.
    Conventionally, *name*
    is supplied by the section to which the relocations apply.
    Thus a relocation section for ``.text``
    normally would have the name ``.rel.text`` or ``.rela.text``.

``.relr.dyn``
    This section holds relative relocation information for dynamic
    linking, compactly encoded as described in
    :numref:`Section {number}, {name} <relative-relocation-table>`.
    The relocations in this section are processed before other relocations
    in any ``SHT_REL`` or ``SHT_RELA`` section.

``.rodata`` and \ ``.rodata1``
    These sections hold read-only data that
    typically contribute to a non-writable segment
    in the process image.
    See :numref:`Chapter {number}, {name} <Program-Header>` for more information.

``.shstrtab``
    This section holds section names.

``.strtab``
    This section holds strings, most commonly the strings
    that represent the names associated with symbol table entries.
    If the file has a loadable segment that includes the
    symbol string table, the section’s attributes will include the
    ``SHF_ALLOC``
    bit; otherwise, that bit will be off.

``.symtab``
    This section holds a symbol table, as described in
    :numref:`Chapter {number}, {name} <Symbol-Table>`.
    If the file has a loadable segment that includes the
    symbol table, the section’s attributes will include the
    ``SHF_ALLOC`` bit; otherwise, that bit will be off.

``.symtab_shndx``
    This section holds the special symbol table section index
    array, as described above.  The section’s attributes will include
    the ``SHF_ALLOC`` bit if the associated symbol table
    section does; otherwise that bit will be off.

``.tbss``
    This section holds uninitialized *thread-local data* that contribute
    to the program’s memory image.
    By definition,
    the system initializes the data with zeros
    when the data is instantiated for each new execution flow.
    The section occupies no file space, as indicated by the section type,
    ``SHT_NOBITS``.
    Implementations need not support thread-local storage.

``.tdata``
    This section holds initialized *thread-local data* that contributes
    to the program’s memory image.
    A copy of its contents is instantiated by the system
    for each new execution flow.
    Implementations need not support thread-local storage.

``.text``
    This section holds the “text,” or executable
    instructions, of a program.

Section names with a dot (``.``) prefix
are reserved for the system,
although applications may use these sections
if their existing meanings are satisfactory.
Applications may use names without the prefix to
avoid conflicts with system sections.
The object file format lets one define sections not
shown in the previous list.
An object file may have more than one section
with the same name.

Section names reserved for a processor architecture
are formed by placing an abbreviation of the architecture
name ahead of the section name.
The name should be taken from the
architecture names used for ``e_machine``.
For instance ``.FOO.psect`` is the ``psect``
section defined by the FOO architecture.
Existing extensions are called by their historical names.

.. table:: **Pre-existing Extensions**

   =============  ============
   ``.sdata``     ``.tdesc``
   ``.sbss``      ``.lit4``
   ``.lit8``      ``.reginfo``
   ``.gptab``     ``.liblist``
   ``.conflict``
   =============  ============

.. note::

   For information on processor-specific sections,
   see the psABI supplement for the desired processor.

.. |br| replace:: |htmlbr| |latexbr|

.. |htmlbr| raw:: html

   <br />

.. |latexbr| raw:: latex

   \newline
