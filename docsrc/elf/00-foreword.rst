********
Foreword
********

.. rubric:: The SVR4 ABI

The System V Release 4 (SVR4) Application Binary Interface (ABI)
is composed of several components, ranging from
a high-level specification of the programming interface
to the low-level machine details.
The ABI contains the following chapters:

*  **Chapter 1: Introduction**.

*  **Chapter 2: Software Installation**
   covers installation media,
   and physical distribution formats.

*  **Chapter 3: Low Level System Information**.
   This processor-dependent chapter covers the machine details,
   data representation, calling conventions,
   parameter passing, register usage, stack frame layout,
   stack unwinding, and dynamic linking conventions.

*  **Chapter 4: Object Files**
   covers the ELF object file format and relocatable objects.

*  **Chapter 5: Program Loading and Dynamic Linking**
   covers the ELF object file format,
   and executable and shared objects.

*  **Chapter 6: Libraries**
   covers the processor-independent API available to the program,
   and the processor-specific binding of the API to the binary interface.
   It provides structure layouts, values for symbolic contants, and other
   implementation-specific details left unspecified by the API document.

*  **Chapter 7: Development Environment**
   covers the development and packaging tools.

*  **Chapter 8: Execution Environment**
   covers the runtime environment, file system structure,
   and system services available to the running application.

The SVR4 ABI is published in two parts: a *generic* ABI document (gABI),
which covers the machine-independent components of the ABI,
and a processor-specific ABI supplement (psABI),
published separately for each machine architecture supported by the SVR4 ABI.

The SVR4 gABI and several other ABIs share ELF as a common object file format,
and the official specification of the ELF object file format is
published here. This specification replaces the material that was
contained in Chapters 4 and 5 of the SVR4 gABI document.

.. only:: latex

   The most up-to-date version of this document
   is available at `gabi.xinuos.com`_.

.. _gabi.xinuos.com: https://gabi.xinuos.com
