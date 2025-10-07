.. |appendixc| raw:: html

   Appendix C:

############################
|appendixc| Revision History
############################

First Draft (Published May 14, 1998)

Second Draft (Published May 3, 1999)

* New values introduced for ELF header ``e_machine`` field.
* Revised language for ``EI_OSABI`` and ``EI_ABIVERSION`` fields
  of the ELF header ``e_ident`` array.
* New section flags ``SHF_MERGE`` and ``SHF_STRINGS`` added.
* New values added to a symbol table entry’s ``st_other`` field
  to describe a symbol’s visibility.
* New dynamic section tags ``DT_RUNPATH`` and ``DT_FLAGS`` added.
  Deprecated dynamic section tag ``DT_RPATH``.
* New semantics for shared object path searching,
  including new “Substitution Sequences”.

Third Draft (Published May 12, 1999)

* A new symbol type, ``STT_COMMON``, has been added.
* Added language restricting the types of objects that may contain symbols
  with the section index ``SHN_COMMON``.
* Dynamic section entries ``DT_SYMBOLIC``, ``DT_TEXTREL`` and ``DT_BIND_NOW``
  have been deprecated.
  New ``DT_FLAGS`` values ``DF_SYMBOLIC``, ``DF_TEXTREL`` and ``DF_BIND_NOW``
  have been added as replacements.
* New rules for interpreting dynamic section tag encodings have been added.
* The OS and processor specific ranges for ``DT_FLAGS`` have been removed.
* The language motivating the use of ``DF_ORIGIN`` has been changed.

Fourth Draft (Published July 6, 1999)

* New language has been added warning about the use of WEAK symbols
  in application programs.
* New rules have been defined for composition of consecutive relocation
  entries that reference the same location.
* Language has been added clarifying the order of execution for functions
  specified by initialization and termination arrays.

Fifth Draft (Published July 21, 1999)

* New section types and section names added for init arrays, fini arrays,
  and pre-init arrays.
* An object may now have both ``DT_INIT`` and ``DT_INIT_ARRAY`` entries
  (and both ``DT_FINI`` and ``DT_FINI_ARRAY`` entries).
  The relative execution order is specified.
* The language describing the order of execution for termination functions
  has been revised.
* A new pre-initialization mechanism has been added.
* It is now up to the psABI supplement for each processor
  to specify whether the dynamic linker must invoke the executable file’s
  init and fini routines.

Sixth Draft (Published September 14, 1999)

* Changed the numbering of some new section types previously added to account
  for type numbers already in use in particular vendor implementations.
* Increased the number of section flag bits available in the OS specific range.

Seventh Draft (Published October 4, 1999)

* Changed the values used for some new section attribute flags to accommodate
  platforms already using previously assigned values.
* Added new section attribute flags ``SHF_INFO_LINK``, ``SHF_LINK_ORDER``,
  and ``SHF_OS_NONCONFORMING``
* Added rules for linkers when linking sections with unrecognized types or flags.

Eighth Draft (Published March 30, 2000)

* Added the concept of section groups.
* Removed the macros for ``ELF32_ST_OTHER`` and ``ELF64_ST_OTHER``.

Ninth Draft (Published March 30, 2000)

* Added language clarifying the semantics of symbols marked as ``STV_PROTECTED``.
* Added language clarifying the contents of the initialization and termination arrays.

Tenth Draft (Published 22 June 2000)

* Added a sentence spelling out the behavior when resolving a symbol
  to a ``STV_PROTECTED`` definition from a shared object.
* Added support for more than 65,000 sections in the ELF header,
  and with ``SHT_SYMTAB_SHNDX`` sections, and in symbol tables.

Eleventh Draft (Published 24 April 2001)

* Updated table of EM_* entries.
* Added ``GRP_MASKOS`` and ``GRP_MASKPROC``.
  Changed section group description in a few ways,
  clarifying some fuzzy points and rewriting the rules for symbols
  referencing into section groups.
* Changed the warning about using weak to be stronger.
* Reworded the ``EI_OSABI`` byte description to make its use clearer.
* Added the table of now generic ``EI_OSABI`` values.
* Added ``SHF_TLS``, ``PT_TLS`` and its contents, ``DF_STATIC_TLS``,
  ``STT_TLS``, .tbss, and .tdata.
* Changed the rules for ``SHT_SYMTAB_SHNDX`` contents to require 0
  when the corresponding ``st_shndx`` field is not ``SHN_XINDEX``.

Twelfth Draft (Published 26 March 2007)

* Updated table of EM_* entries.

Thirteenth Draft (Published 03 November 2009)

* Updated table of EM_* entries.
* Added ``ELFOSABI_FENIXOS`` to the ``EI_OSABI`` values.
* Added ``ELFOSABI_GNU`` to the ``EI_OSABI`` values; aliased to ``ELFOSABI_LINUX``.

Fourteenth Draft (Published 10 June 2013)

* Added ``SHF_COMPRESSED`` to the Section Attribute Flags.
* Updated table of EM_* entries.

Fifteenth Draft (Published 23 July 2015)

* Clarified the description of ``SHT_SYMTAB_SHNDX``;
  allow usage with any symbol table section.
* Added ``DT_SYMTAB_SHNDX`` to the Dynamic Array Tags.

Version 4.2 (Published 2025)

* Converted to ReStructuredText.
* ELF specification is now separate from the gABI document.
* Removed empty placeholders for psABI sections.

Version 4.3 (DRAFT)

* Added extra requirements for ``SHF_LINK_ORDER`` flag.
* Added relative relocation table (``Elf32_Relr`` and ``Elf64_Relr``).
* Changed the symbol visibility attribute to use the lower 3 bits
  of ``st_other`` (instead of 2 bits).
* Added `STV_EXPORTED`, `STV_SINGLETON`, and `STV_ELIMINATE`
  visibility flags.
* Added ``DT_SYMTABSZ`` entry, and made ``DT_HASH`` optional if
  ``DT_SYMTABSZ`` is provided.
* Changed ``SHF_COMPRESSED`` to allow with ``SHF_ALLOC`` sections
  in ``ET_REL`` objects.
* Added ``ELFCOMPRESS_ZSTD`` compression algorithm.
