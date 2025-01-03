.. _Dynamic-Linking:

***************
Dynamic Linking
***************

.. _Program-Interpreter:

Program Interpreter
===================

An executable file that participates in
dynamic linking shall have one
``PT_INTERP`` program header element.
During process startup (e.g., ``exec()``),
the system retrieves a path name from the ``PT_INTERP``
segment and creates the initial process image from
the interpreter file’s segments. That is,
instead of using the original executable file’s
segment images, the system composes a memory
image for the interpreter.
It then is the interpreter’s responsibility to
receive control from the system and provide an
environment for the application program.

The interpreter typically receives control in one of two ways.
First, it may receive a file descriptor
to read the executable file, positioned at the beginning.
It can use this file descriptor to read and/or map the executable
file’s segments into memory.
Second, depending on the executable file format, the system
may load the executable file into memory instead of giving the
interpreter an open file descriptor.
With the possible exception of the file descriptor,
the interpreter’s initial process state matches
what the executable file would have received.
The interpreter itself may not require a second interpreter.
An interpreter may be either a shared object
or an executable file.
See the psABI supplement for additional information.

A shared object (the normal case) is loaded as
position-independent, with addresses that may vary
from one process to another; the system creates its segments
in the dynamic segment area used by ``mmap`` and related services.
Consequently, a shared object interpreter typically will
not conflict with the original executable file’s
original segment addresses.

An executable file may be loaded at fixed addresses;
if so, the system creates its segments
using the virtual addresses from the program header table.
Consequently, an executable file interpreter’s
virtual addresses may collide with the
first executable file; the interpreter is responsible
for resolving conflicts.

Dynamic Linker
==============

When building an executable file that uses dynamic linking,
the link editor adds a program header element of type
``PT_INTERP`` to an executable file, telling the system to invoke
the dynamic linker as the program interpreter.

.. note::

   The locations of the system provided dynamic
   linkers are processor specific.

The system loader (e.g., ``exec()``) and the dynamic linker cooperate to
create the process image for the program, which entails
the following actions:

* Adding the executable file’s memory segments to the process image;

* Adding shared object memory segments to the process image;

* Performing relocations for the executable file and its
  shared objects;

* Closing the file descriptor that was used to read the executable file,
  if one was given to the dynamic linker;

* Transferring control to the program, making it look as if
  the program had received control directly from the system loader.

The link editor also constructs various data
that assist the dynamic linker
for executable and shared object files.
As shown in :ref:`Program-Header`, this data resides
in loadable segments, making them available during execution.
(Once again, recall the exact segment contents are processor-specific.
See the psABI supplement for complete information).

* A ``.dynamic`` section with type ``SHT_DYNAMIC``
  holds various data.
  The structure residing at the
  beginning of the section holds the addresses
  of other dynamic linking information.

* The ``.hash`` section with type ``SHT_HASH``
  holds a symbol hash table.

* The ``.got`` and ``.plt`` sections with type
  ``SHT_PROGBITS``
  hold two separate tables:
  the global offset table and the procedure linkage table.
  The psABI supplement discusses how programs use the global offset table
  for position-independent code.
  Sections below explain how the dynamic linker uses
  and changes the tables to create memory images for object files.

Because every ABI-conforming program imports the basic system
services from a shared object library,
the dynamic linker participates in every ABI-conforming program execution.

Shared objects may occupy
virtual memory addresses that are different from the addresses recorded
in the file’s program header table.
The dynamic linker relocates the memory image, updating
absolute addresses before the application gains control.
Although the absolute address values would be correct
if the library were loaded at
the addresses specified in the program header table, this normally
is not the case.

If the process environment contains a variable named ``LD_BIND_NOW``
with a non-null value, the dynamic linker processes
all relocations before transferring control to the program.
For example, all the following environment entries
would specify this behavior.

* ``LD_BIND_NOW=1``

* ``LD_BIND_NOW=on``

* ``LD_BIND_NOW=off``

Otherwise, ``LD_BIND_NOW`` either
does not occur in the environment or has a null value.
The dynamic linker is permitted to evaluate procedure linkage table
entries lazily, thus avoiding symbol resolution and relocation
overhead for functions that are not called.
See the psABI supplement for more information.

.. _Dynamic-Section:

Dynamic Section
===============

If an object file participates in dynamic linking,
its program header table will have an element of type
``PT_DYNAMIC``.
This “segment” contains the ``.dynamic`` section.
A special symbol, ``_DYNAMIC``,
labels the section, which contains
an array of the following structures.

.. code-block:: c
   :caption: Dynamic Structure

   typedef struct {
       Elf32_Sword d_tag;
       union {
           Elf32_Word  d_val;
           Elf32_Addr  d_ptr;
       } d_un;
   } Elf32_Dyn;

   extern Elf32_Dyn    _DYNAMIC[];

   typedef struct {
       Elf64_Sxword    d_tag;
       union {
           Elf64_Xword d_val;
           Elf64_Addr  d_ptr;
       } d_un;
   } Elf64_Dyn;

   extern Elf64_Dyn    _DYNAMIC[];

For each object with this type, ``d_tag``
controls the interpretation of ``d_un``.

``d_val``
    These objects represent integer values with various
    interpretations.

``d_ptr``
    These objects represent program virtual addresses.
    As mentioned previously, a file’s virtual addresses
    might not match the memory virtual addresses during execution.
    When interpreting addresses contained in the dynamic
    structure, the dynamic linker computes actual addresses,
    based on the original file value and the memory base address.
    For consistency, files do *not*
    contain relocation entries to “correct” addresses in the dynamic
    structure.

To make it simpler for tools to interpret the contents of
dynamic section entries, the value of each tag, except for those in
two special compatibility ranges,
will determine the interpretation of the ``d_un``
union.  A tag whose value is an even number
indicates a dynamic section entry that uses ``d_ptr``.
A tag whose value is an odd number indicates a dynamic section entry
that uses ``d_val`` or that uses neither ``d_ptr``
nor ``d_val``.  Tags whose values are less
than the special value ``DT_ENCODING`` and tags
whose values fall between ``DT_HIOS`` and
``DT_LOPROC`` do not follow these rules.

The following table summarizes the tag requirements
for executable and shared object files.
If a tag is marked “mandatory”, the dynamic linking
array for an ABI-conforming file must have an entry of that type.
Likewise, “optional” means an entry for the tag may appear
but is not required.

.. table:: Dynamic Array Tags, ``d_tag``

   ======================  ==============  ===========  ==============  =================
   Name                    Value           ``d_un``     Executable      Shared Object
   ======================  ==============  ===========  ==============  =================
   ``DT_NULL``             ``0``           ignored      mandatory       mandatory
   ``DT_NEEDED``           ``1``           ``d_val``    optional        optional
   ``DT_PLTRELSZ``         ``2``           ``d_val``    optional        optional
   ``DT_PLTGOT``           ``3``           ``d_ptr``    optional        optional
   ``DT_HASH``             ``4``           ``d_ptr``    mandatory†      mandatory†
   ``DT_STRTAB``           ``5``           ``d_ptr``    mandatory       mandatory
   ``DT_SYMTAB``           ``6``           ``d_ptr``    mandatory       mandatory
   ``DT_RELA``             ``7``           ``d_ptr``    mandatory       optional
   ``DT_RELASZ``           ``8``           ``d_val``    mandatory       optional
   ``DT_RELAENT``          ``9``           ``d_val``    mandatory       optional
   ``DT_STRSZ``            ``10``          ``d_val``    mandatory       mandatory
   ``DT_SYMENT``           ``11``          ``d_val``    mandatory       mandatory
   ``DT_INIT``             ``12``          ``d_ptr``    optional        optional
   ``DT_FINI``             ``13``          ``d_ptr``    optional        optional
   ``DT_SONAME``           ``14``          ``d_val``    ignored         optional
   ``DT_RPATH``\ *         ``15``          ``d_val``    optional        ignored
   ``DT_SYMBOLIC``\ *      ``16``          ignored      ignored         optional
   ``DT_REL``              ``17``          ``d_ptr``    mandatory       optional
   ``DT_RELSZ``            ``18``          ``d_val``    mandatory       optional
   ``DT_RELENT``           ``19``          ``d_val``    mandatory       optional
   ``DT_PLTREL``           ``20``          ``d_val``    optional        optional
   ``DT_DEBUG``            ``21``          ``d_ptr``    optional        ignored
   ``DT_TEXTREL``\ *       ``22``          ignored      optional        optional
   ``DT_JMPREL``           ``23``          ``d_ptr``    optional        optional
   ``DT_BIND_NOW``\ *      ``24``          ignored      optional        optional
   ``DT_INIT_ARRAY``       ``25``          ``d_ptr``    optional        optional
   ``DT_FINI_ARRAY``       ``26``          ``d_ptr``    optional        optional
   ``DT_INIT_ARRAYSZ``     ``27``          ``d_val``    optional        optional
   ``DT_FINI_ARRAYSZ``     ``28``          ``d_val``    optional        optional
   ``DT_RUNPATH``          ``29``          ``d_val``    optional        optional
   ``DT_FLAGS``            ``30``          ``d_val``    optional        optional
   ``DT_ENCODING``         ``32``          unspecified  unspecified     unspecified
   ``DT_PREINIT_ARRAY``    ``32``          ``d_ptr``    optional        ignored
   ``DT_PREINIT_ARRAYSZ``  ``33``          ``d_val``    optional        ignored
   ``DT_SYMTAB_SHNDX``     ``34``          ``d_ptr``    optional        optional
   ``DT_RELRSZ``           ``35``          ``d_val``    optional        optional
   ``DT_RELR``             ``36``          ``d_ptr``    optional        optional
   ``DT_RELRENT``          ``37``          ``d_val``    optional        optional
   ``DT_SYMTABSZ``         ``39``          ``d_val``    optional†       optional†
   ``DT_LOOS``             ``0x6000000D``  unspecified  unspecified     unspecified
   ``DT_HIOS``             ``0x6ffff000``  unspecified  unspecified     unspecified
   ``DT_LOPROC``           ``0x70000000``  unspecified  unspecified     unspecified
   ``DT_HIPROC``           ``0x7fffffff``  unspecified  unspecified     unspecified
   ======================  ==============  ===========  ==============  =================

| \* Signifies an entry that has been deprecated.
| † ``DT_HASH`` is optional if ``DT_SYMTABSZ`` is provided.

``DT_NULL``
    An entry with a ``DT_NULL`` tag marks the end of the
    ``_DYNAMIC`` array.

``DT_NEEDED``
    This element holds the string table offset of a null-terminated string,
    giving the name of a needed library.
    The offset is an index into the table recorded in the ``DT_STRTAB`` code.
    See :ref:`Shared-Object-Dependencies` for more
    information about these names.
    The dynamic array may contain multiple entries with
    this type.
    These entries’ relative order is significant, though their
    relation to entries of other types is not.

``DT_PLTRELSZ``
    This element holds the total size, in bytes,
    of the relocation entries associated with the procedure linkage table.
    If an entry of type ``DT_JMPREL`` is present, a
    ``DT_PLTRELSZ`` must accompany it.

``DT_PLTGOT``
    This element holds an address associated with the procedure linkage table
    and/or the global offset table.
    See the psABI supplement for details.

``DT_HASH``
    This element holds the address of the symbol hash table,
    described in :ref:`Hash-Table`.
    This hash table refers to the symbol table referenced by the ``DT_SYMTAB``
    element.

    ``DT_HASH`` is normally mandatory. The psABI supplement is allowed
    to override this requirement by providing an alternative hash
    mechanism. In such cases, DT_SYMTABSZ, which is normally optional,
    becomes mandatory.

``DT_STRTAB``
    This element holds the address of the string table,
    described in :ref:`String-Table`.
    Symbol names, library names, and other strings reside
    in this table.

``DT_SYMTAB``
    This element holds the address of the dynamic linking symbol table,
    as described in :ref:`Symbol-Table`,
    with ``Elf32_Sym`` entries for the 32-bit class of files and ``Elf64_Sym``
    entries for the 64-bit class of files.

``DT_RELA``
    This element holds the address of a relocation table,
    described in :ref:`Relocation`.
    Entries in the table have explicit addends
    (``Elf32_Rela`` for the 32-bit file class
    or ``Elf64_Rela`` for the 64-bit file class).
    An object file may have multiple relocation sections.
    When building the relocation table for an
    executable or shared object file, the link editor
    concatenates those sections to form a single table.
    Although the sections remain independent in the object file,
    the dynamic linker sees a single table.
    When the dynamic linker creates the process image for
    an executable file or adds a shared object to the
    process image, it reads the relocation table and performs
    the associated actions.
    If this element is present, the dynamic structure must also have
    ``DT_RELASZ`` and ``DT_RELAENT`` elements.
    When relocation is “mandatory” for a file, either
    ``DT_RELA`` or ``DT_REL`` may occur (both are permitted but not required).

``DT_RELASZ``
    This element holds the total size, in bytes, of the
    ``DT_RELA`` relocation table.

``DT_RELAENT``
    This element holds the size, in bytes, of the
    ``DT_RELA`` relocation entry.

``DT_STRSZ``
    This element holds the size, in bytes, of the string table.

``DT_SYMENT``
    This element holds the size, in bytes, of a symbol table entry.

``DT_INIT``
    This element holds the address of the initialization function,
    discussed in :ref:`Initialization-and-Termination-Functions`.

``DT_FINI``
    This element holds the address of the termination function,
    discussed in :ref:`Initialization-and-Termination-Functions`.

``DT_SONAME``
    This element holds the string table offset of a null-terminated string,
    giving the name of the shared object.
    The offset is an index into the table recorded in the ``DT_STRTAB`` entry.
    See :ref:`Shared-Object-Dependencies` for more
    information about these names.

``DT_RPATH``
    This element holds the string table offset of a null-terminated search
    library search path string discussed in :ref:`Shared-Object-Dependencies`.
    The offset is an index into the table recorded in the
    ``DT_STRTAB`` entry.  This entry is deprecated; its
    use has been superseded by ``DT_RUNPATH``.

``DT_SYMBOLIC``
    This element’s presence in a shared object library alters
    the dynamic linker’s symbol resolution algorithm for
    references within the library.
    Instead of starting a symbol search with the
    executable file, the dynamic linker starts from the
    shared object itself.
    If the shared object fails to supply the referenced
    symbol, the dynamic linker then searches the
    executable file and other shared objects as usual.
    This entry is deprecated; its use has been superseded
    by the ``DF_SYMBOLIC`` flag.

``DT_REL``
    This element is similar to ``DT_RELA``,
    except its table has implicit addends
    (``Elf32_Rel`` for the 32-bit file class
    or ``Elf64_Rel`` for the 64-bit file class).
    If this element is present, the dynamic structure must also have
    ``DT_RELSZ`` and ``DT_RELENT`` elements.

``DT_RELSZ``
    This element holds the total size, in bytes, of the
    ``DT_REL`` relocation table.

``DT_RELENT``
    This element holds the size, in bytes, of the
    ``DT_REL`` relocation entry.

``DT_PLTREL``
    This member specifies the type of relocation entry
    to which the procedure linkage table refers.
    The ``d_val`` member holds ``DT_REL`` or ``DT_RELA``,
    as appropriate.
    All relocations in a procedure linkage table must use
    the same relocation.

``DT_DEBUG``
    This member is used for debugging.  Its contents are not specified
    for the ABI; programs that access this entry are not
    ABI-conforming.

``DT_TEXTREL``
    This member’s absence signifies that no
    relocation entry should cause a modification to a non-writable
    segment, as specified by the segment permissions in the program
    header table.
    If this member is present, one or more relocation entries might
    request modifications to a non-writable segment, and the dynamic
    linker can prepare accordingly.
    This entry is deprecated; its use has been superseded
    by the ``DF_TEXTREL`` flag.

``DT_JMPREL``
    If present, this entry’s ``d_ptr``
    member holds the address of relocation entries associated solely
    with the procedure linkage table.
    Separating these relocation entries lets the dynamic linker ignore
    them during process initialization, if lazy binding is enabled.
    If this entry is present, the related entries of types
    ``DT_PLTRELSZ`` and ``DT_PLTREL``
    must also be present.

``DT_BIND_NOW``
    If present in a shared object or executable, this entry
    instructs the dynamic linker to process all relocations
    for the object containing this entry before transferring
    control to the program.
    The presence of this entry takes
    precedence over a directive to use lazy binding for this object when
    specified through the environment or via ``dlopen()``.
    This entry is deprecated; its use has been superseded
    by the ``DF_BIND_NOW`` flag.

``DT_INIT_ARRAY``
    This element holds the address of the array of pointers to initialization
    functions, discussed in :ref:`Initialization-and-Termination-Functions`.

``DT_FINI_ARRAY``
    This element holds the address of the array of pointers to termination
    functions, discussed in :ref:`Initialization-and-Termination-Functions`.

``DT_INIT_ARRAYSZ``
    This element holds the size in bytes of the array of initialization
    functions pointed to by the ``DT_INIT_ARRAY`` entry.
    If an object has a ``DT_INIT_ARRAY`` entry, it must
    also have a ``DT_INIT_ARRAYSZ`` entry.

``DT_FINI_ARRAYSZ``
    This element holds the size in bytes of the array of termination
    functions pointed to by the ``DT_FINI_ARRAY`` entry.
    If an object has a ``DT_FINI_ARRAY`` entry, it must
    also have a ``DT_FINI_ARRAYSZ`` entry.

``DT_RUNPATH``
    This element holds the string table offset of a null-terminated
    library search path string discussed in
    :ref:`Shared-Object-Dependencies`.
    The offset is an index into the table recorded in the
    ``DT_STRTAB`` entry.

``DT_FLAGS``
    This element holds flag values specific to the object being
    loaded.  Each flag value will have the name ``DF_``\ *flag_name*.
    Defined values and their meanings are described below.
    All other values are reserved.

``DT_PREINIT_ARRAY``
    This element holds the address of the array of pointers to pre-initialization
    functions, discussed in :ref:`Initialization-and-Termination-Functions`.
    The ``DT_PREINIT_ARRAY`` table is processed only
    in an executable file; it is ignored if contained in a shared object.

``DT_PREINIT_ARRAYSZ``
    This element holds the size in bytes of the array of pre-initialization
    functions pointed to by the ``DT_PREINIT_ARRAY`` entry.
    If an object has a ``DT_PREINIT_ARRAY`` entry, it must
    also have a ``DT_PREINIT_ARRAYSZ`` entry.  As with
    ``DT_PREINIT_ARRAY``, this entry is ignored if it appears
    in a shared object.

``DT_SYMTAB_SHNDX``
    This element holds the address of the ``SHT_SYMTAB_SHNDX``
    section associated with the dynamic symbol table referenced by the
    ``DT_SYMTAB`` element.

``DT_RELR``
    This element holds the address of an ``SHT_RELR`` relocation table,
    described in :ref:`Relocation`. This table will hold entries of
    either ``Elf32_Relr`` for the 32-bit file class or ``Elf64_Relr``
    for the 64-bit file class. If this element is present, the dynamic
    structure must also have ``DT_RELRSZ`` and ``DT_RELRENT`` elements.
    During dynamic linking, a ``DT_RELR`` element is processed before
    any ``DT_REL`` or ``DT_RELA`` elements in the same object file.

``DT_RELRSZ``
    This element holds the total size, in bytes, of the ``DT_RELR``
    relocation table.

``DT_RELRENT``
    This element holds the size, in bytes, of the ``DT_RELR`` relocation
    entry.

``DT_SYMTABSZ``
    This element holds the size, in bytes, of the ``DT_SYMTAB`` dynamic
    linking symbol table. It must be provided if the ``DT_HASH`` symbol
    hash table is omitted.

``DT_ENCODING``
    Values greater than or equal to ``DT_ENCODING``
    and less than ``DT_LOOS``
    follow the rules for the interpretation of the ``d_un`` union
    described above.

``DT_LOOS`` through ``DT_HIOS``
    Values in this inclusive range
    are reserved for operating system-specific semantics.
    All such values follow the rules for the interpretation of the
    ``d_un`` union described above.

``DT_LOPROC`` through ``DT_HIPROC``
    Values in this inclusive range
    are reserved for processor-specific semantics. If meanings
    are specified, the psABI supplement explains them.
    All such values follow the rules for the interpretation of the
    ``d_un`` union described above.

Except for the ``DT_NULL`` element at the end of the array,
and the relative order of ``DT_NEEDED``
elements, entries may appear in any order.
Tag values not appearing in the table are reserved.

.. table:: ``DT_FLAGS`` values

   =================  =========
   Name               Value
   =================  =========
   ``DF_ORIGIN``      ``0x1``
   ``DF_SYMBOLIC``    ``0x2``
   ``DF_TEXTREL``     ``0x4``
   ``DF_BIND_NOW``    ``0x8``
   ``DF_STATIC_TLS``  ``0x10``
   =================  =========

``DF_ORIGIN``
    This flag signifies that the object being loaded may make reference
    to the ``$ORIGIN`` substitution string (see :ref:`Substitution-Sequences`\ ).
    The dynamic linker must determine the pathname of the object
    containing this entry when the object is loaded.

``DF_SYMBOLIC``
    If this flag is set in a shared object library,
    the dynamic linker’s symbol resolution algorithm for
    references within the library is changed.
    Instead of starting a symbol search with the
    executable file, the dynamic linker starts from the
    shared object itself.
    If the shared object fails to supply the referenced
    symbol, the dynamic linker then searches the
    executable file and other shared objects as usual.

``DF_TEXTREL``
    If this flag is not set, no
    relocation entry should cause a modification to a non-writable
    segment, as specified by the segment permissions in the program
    header table.
    If this flag is set, one or more relocation entries might
    request modifications to a non-writable segment, and the dynamic
    linker can prepare accordingly.

``DF_BIND_NOW``
    If set in a shared object or executable, this flag
    instructs the dynamic linker to process all relocations
    for the object containing this entry before transferring
    control to the program.
    The presence of this entry takes
    precedence over a directive to use lazy binding for this object when
    specified through the environment or via ``dlopen()``.

``DF_STATIC_TLS``
    If set in a shared object or executable,
    this flag instructs the dynamic linker to reject
    attempts to load this file dynamically.
    It indicates that the shared object or executable
    contains code using a *static thread-local storage* scheme.
    Implementations need not support any form of thread-local storage.

.. _Shared-Object-Dependencies:

Shared Object Dependencies
==========================

When the link editor processes an archive library,
it extracts library members and copies them into
the output object file.
These statically linked services are available during
execution without involving the dynamic linker.
Shared objects also provide services, and
the dynamic linker must attach the proper shared object files to
the process image for execution.

When the dynamic linker creates the memory segments for
an object file, the dependencies (recorded in
``DT_NEEDED`` entries of the dynamic structure)
tell what shared objects are needed to
supply the program’s services.
By repeatedly connecting referenced shared objects and
their dependencies, the dynamic linker builds a complete process image.
When resolving symbolic references, the dynamic linker
examines the symbol tables with a breadth-first search.
That is, it first looks at the symbol table of the
executable program itself, then at the symbol tables
of the ``DT_NEEDED`` entries (in order),
and then at the second level ``DT_NEEDED`` entries, and
so on.  Shared object files must be readable by the process;
other permissions are not required.

.. note::

   Even when a shared object is referenced multiple
   times in the dependency list, the dynamic linker will
   connect the object only once to the process.

Names in the dependency list are copies either of the
``DT_SONAME`` strings or the path names of the shared objects used to build
the object file.
For example, if the link editor builds an executable
file using one shared object with a
``DT_SONAME`` entry of ``lib1``
and another shared object library with the path name
``/usr/lib/lib2``, the executable file will contain
``lib1`` and ``/usr/lib/lib2`` in its dependency list.

If a shared object name has one or more slash (\ ``/``\ )
characters anywhere in the name, such as ``/usr/lib/lib2``
or ``directory/file``, the dynamic linker uses that string directly
as the path name.
If the name has no slashes, such as ``lib1``,
three facilities specify shared object path searching.

* The dynamic array tag ``DT_RUNPATH`` gives a string that
  holds a list of directories, separated by colons (\ ``:``\ ).
  For example, the string
  ``/home/dir/lib:/home/dir2/lib:``
  tells the dynamic linker to search first the directory
  ``/home/dir/lib``, then ``/home/dir2/lib``,
  and then the current directory to find dependencies.

  The set of directories specified by a given ``DT_RUNPATH``
  entry is used to find only the immediate dependencies
  of the executable or shared object containing the ``DT_RUNPATH``
  entry.  That is, it is used only for those dependencies contained in
  the ``DT_NEEDED`` entries of the dynamic structure containing
  the ``DT_RUNPATH`` entry, itself.
  One object’s ``DT_RUNPATH`` entry does not affect the search
  for any other object’s dependencies.

* A variable called ``LD_LIBRARY_PATH`` in the process environment
  may hold a list of directories as above, optionally
  followed by a semicolon (\ ``;``\ ) and
  another directory list.
  The following values would be equivalent to the previous example:

  * ``LD_LIBRARY_PATH=/home/dir/usr/lib:/home/dir2/usr/lib:``

  * ``LD_LIBRARY_PATH=/home/dir/usr/lib;/home/dir2/usr/lib:``

  * ``LD_LIBRARY_PATH=/home/dir/usr/lib:/home/dir2/usr/lib:;``

  Although some programs (such as the link editor) treat the lists
  before and after the semicolon differently,
  the dynamic linker does not.
  Nevertheless, the dynamic linker accepts the semicolon
  notation, with the semantics described previously.

  All ``LD_LIBRARY_PATH`` directories are searched before those from
  ``DT_RUNPATH``.

* Finally, if the other two groups of directories
  fail to locate the desired library, the dynamic linker searches
  the default directories, ``/usr/lib`` or such other
  directories as may be specified by the psABI supplement.

When the dynamic linker is searching for shared objects, it is
not a fatal error if an ELF file with the wrong attributes
is encountered in the search.  Instead, the dynamic linker
shall exhaust the search of all paths before determining
that a matching object could not be found.  For this determination,
the relevant attributes are contained in the following ELF header fields:
``e_ident[EI_DATA]``,
``e_ident[EI_CLASS]``,
``e_ident[EI_OSABI]``,
``e_ident[EI_ABIVERSION]``,
``e_machine``,
``e_type``, ``e_flags``
and ``e_version``.

.. note::

   For security, the dynamic linker ignores
   ``LD_LIBRARY_PATH`` for set-user and
   set-group ID programs.
   It does, however, search ``DT_RUNPATH`` directories
   and the default directories.
   The same restriction may be applied to processes that have more than
   minimal privileges on systems with installed extended security
   mechanisms.

.. note::

   A fourth search facility, the dynamic array tag ``DT_RPATH``,
   has been deprecated.
   It provides a colon-separated list of directories to search.
   Directories specified by ``DT_RPATH`` are searched
   before directories specified by ``LD_LIBRARY_PATH``.

   If both ``DT_RPATH`` and ``DT_RUNPATH``
   entries appear in a single object’s dynamic array,
   the dynamic linker processes only the ``DT_RUNPATH``
   entry.

.. _Substitution-Sequences:

Substitution Sequences
++++++++++++++++++++++

Within a string provided by dynamic array entries with the
``DT_NEEDED`` or ``DT_RUNPATH`` tags and in
pathnames passed as parameters to the ``dlopen()`` routine, a
dollar sign (\ ``$``\ ) introduces a substitution sequence.
This sequence consists of the dollar sign immediately followed
by either the longest *name* sequence or a name contained
within left and right braces (\ ``{``\ ) and (\ ``}``\ ).
A name is a sequence of bytes that start with either a letter or
an underscore followed by zero or more letters, digits or underscores.
If a dollar sign is not immediately followed by a name or a
brace-enclosed name, the behavior of the dynamic linker is unspecified.

If the name is “\ ``ORIGIN``”, then the substitution
sequence is replaced by the dynamic linker with the absolute
pathname of the directory in which the object containing the
substitution sequence originated.  Moreover, the pathname will
contain no symbolic links or use of “\ ``.``” or
“\ ``..``” components.
Otherwise (when the name is not “\ ``ORIGIN``”)
the behavior of the dynamic linker is unspecified.

When the dynamic linker loads an object that uses ``$ORIGIN``,
it must calculate the pathname of the directory containing the object.
Because this calculation can be computationally expensive,
implementations may want to avoid the calculation for objects
that do not use ``$ORIGIN``.
If an object calls ``dlopen()`` with a string
containing ``$ORIGIN`` and does not use ``$ORIGIN``
in one if its dynamic array entries,
the dynamic linker may not have calculated the
pathname for the object until the ``dlopen()`` actually
occurs.  Since the application may have changed its current
working directory before the ``dlopen()`` call,
the calculation may not yield the correct result.
To avoid this possibility, an object may signal its intention
to reference ``$ORIGIN`` by setting the
``DF_ORIGIN`` flag.
An implementation may reject an attempt to use ``$ORIGIN``
within a ``dlopen()`` call from an object that
did not set the ``DF_ORIGIN`` flag and did not
use ``$ORIGIN`` within its dynamic array.

.. note::

   For security, the dynamic linker does not allow use of
   ``$ORIGIN`` substitution sequences for set-user and
   set-group ID programs.  For such sequences that appear
   within strings specified by ``DT_RUNPATH`` dynamic
   array entries, the specific search path containing the
   ``$ORIGIN`` sequence is ignored (though other
   search paths in the same string are processed).
   ``$ORIGIN`` sequences within a ``DT_NEEDED``
   entry or path passed as a parameter to ``dlopen()``
   are treated as errors.
   The same restrictions may be applied to processes that have more than
   minimal privileges on systems with installed extended security
   mechanisms.

.. _Hash-Table:

Hash Table
==========

A hash table of ``Elf32_Word``
objects supports symbol table access.  The same table
layout is used for both the 32-bit and 64-bit file class.
Labels appear below
to help explain the hash table organization,
but they are not part of the specification.

.. figure:: /svg/figure-6.svg
   :alt: Hash Table
   :width: 270pt

   Hash Table

The ``bucket`` array contains ``nbucket``
entries, and the ``chain`` array contains ``nchain``
entries; indexes start at 0.
Both ``bucket`` and ``chain``
hold symbol table indexes.
Chain table entries parallel the symbol table.
The number of symbol table entries should equal
``nchain``;
so symbol table indexes also select chain table entries.
A hashing function (shown below) accepts a symbol name and returns a
value that may be used to compute a ``bucket`` index.
Consequently, if the hashing function returns the value
*x* for some name, ``bucket[``\ *x*\ ``%nbucket]`` gives
an index, *y*,
into both the symbol table and the chain table.
If the symbol table entry is not the one desired,
``chain[``\ *y*\ ``]`` gives the next symbol table entry
with the same hash value.
One can follow the ``chain``
links until either the selected symbol table entry
holds the desired name or the ``chain`` entry contains the value
``STN_UNDEF``.

.. code-block:: c
   :caption: Hashing Function

   unsigned long
   elf_hash(const unsigned char *name)
   {
       unsigned long   h = 0, g;
       while (*name)
       {
           h = (h << 4) + *name++;
           if (g = h & 0xf0000000)
               h ^= g >> 24;
           h &= ~g;
       }
       return h;
   }

.. _Initialization-and-Termination-Functions:

Initialization and Termination Functions
========================================

After the dynamic linker has built the process image
and performed the relocations, each shared object and the executable
file get the opportunity to execute some initialization functions.
All shared object initializations happen before the executable
file gains control.

Before the initialization functions for any object A is called, the initialization
functions for any other objects that object A depends on are called.
For these purposes, an object A depends on another object B,
if B appears in A’s list of needed objects (recorded in the ``DT_NEEDED``
entries of the dynamic structure).
The order of initialization for circular dependencies is undefined.

The initialization of objects occurs by recursing through the needed
entries of each object.
The initialization functions for an object are invoked after the needed
entries for that object have been processed.
The order of processing among the entries of a particular list of
needed objects is unspecified.

.. note::

   Each psABI supplement may optionally further restrict
   the algorithm used to determine the order of initialization.
   Any such restriction, however, may not conflict with
   the rules described by this specification.

The following example illustrates two of the possible correct orderings
which can be generated for the example NEEDED lists.
In this example the *a.out* is dependent on ``b``, ``d``, and ``e``.
``b`` is dependent on ``d`` and ``f``, while ``d`` is dependent on ``e`` and ``g``.
From this information a dependency graph can be drawn.
The above algorithm on initialization will then allow the following
specified initialization orderings (among others).

.. figure:: /svg/init-term.dot.svg
   :width: 654pt

.. figure:: /svg/init-term.dot.2.svg
   :width: 639pt

   Initialization Ordering Example

Similarly, shared objects and executable files may have termination
functions, which are executed with the ``atexit()`` mechanism after
the base process begins its termination sequence.
The termination functions for any object A must be called before
the termination functions for any other objects that object A depends
on.  For these purposes, an object A depends on another object B,
if B appears in A’s list of needed objects (recorded in the ``DT_NEEDED``
entries of the dynamic structure).
The order of termination for circular dependencies is undefined.

Finally, an executable file may have pre-initialization functions.
These functions are executed after the dynamic linker has built
the process image and performed relocations but before any shared
object initialization functions.  Pre-initialization functions are
not permitted in shared objects.

.. note::

   Complete initialization of system libraries may not have occurred when
   pre-initializations are executed, so some features of the system
   may not be available to pre-initialization code.  In general,
   use of pre-initialization code can be considered portable only
   if it has no dependencies on system libraries.

The dynamic linker ensures that it will not execute any initialization,
pre-initialization, or termination functions more than once.

Shared objects designate their
initialization and termination code in one of two ways.
First, they may specify the address of a function to execute
via the ``DT_INIT`` and ``DT_FINI`` entries in the dynamic structure,
described in :ref:`Dynamic-Section`.

.. note::

   Note that the address of a function
   need not be the same as a pointer to a function
   as defined by the psABI supplement.

Shared objects may also (or instead) specify the address and size of
an array of function pointers.  Each element of this
array is a pointer to a function to be executed by the dynamic linker.
Each array element is the size of a pointer in the
programming model followed by the object containing
the array.  The address of the array of initialization
function pointers is specified by the ``DT_INIT_ARRAY``
entry in the dynamic structure.  Similarly, the address of
the array of pre-initialization functions is specified by
``DT_PREINIT_ARRAY`` and the address of the array
of termination functions is specified by ``DT_FINI_ARRAY``.
The size of each array is specified by the ``DT_INIT_ARRAYSZ``,
``DT_PREINIT_ARRAYSZ``, and ``DT_FINI_ARRAYSZ``
entries.

.. note::

   The addresses contained in the initialization and termination arrays
   are function pointers as defined by the psABI supplement for
   each processor.  On some architectures, a function pointer may not
   contain the actual address of the function.

The functions pointed to in the arrays
specified by ``DT_INIT_ARRAY`` and by ``DT_PREINIT_ARRAY``
are executed by the dynamic
linker in the same order in which their addresses appear in
the array; those specified by ``DT_FINI_ARRAY``
are executed in reverse order.

If an object contains both ``DT_INIT``
and ``DT_INIT_ARRAY`` entries, the function referenced
by the ``DT_INIT`` entry is processed before those
referenced by the ``DT_INIT_ARRAY`` entry for that object.
If an object contains both ``DT_FINI``
and ``DT_FINI_ARRAY`` entries, the functions referenced
by the ``DT_FINI_ARRAY`` entry are processed before the one
referenced by the ``DT_FINI`` entry for that object.

.. note::

   Although the ``atexit()`` termination processing normally will be done,
   it is not guaranteed to have executed upon process death.
   In particular, the process will not execute the termination processing
   if it calls ``_exit()`` or if the process dies because it received a signal
   that it neither caught nor ignored.

The psABI supplement for each processor specifies whether the
dynamic linker is responsible for calling the executable file’s
initialization function or registering the executable file’s
termination function with ``atexit()``.
Termination functions specified by users via the ``atexit()`` mechanism
must be executed before any termination functions of shared objects.
