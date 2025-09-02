.. |appendixb| raw:: html

   Appendix B:

#################################
|appendixb| Assigned OSABI Values
#################################

The table below lists all assigned ``EI_OSABI`` values.
This list is updated as new values are assigned, without updating the
document version number.

.. only:: latex

   For the most up-to-date list of values,
   please refer to `gabi.xinuos.com`_.

.. _gabi.xinuos.com: https://gabi.xinuos.com

Values in the architecture-specific value range may be used
for a specific ``e_machine`` value, without registration.
It is advisable to coordinate with other potential users of
that architecture to avoid conflicts.

To request assignment of an ``EI_OSABI`` value for a new OSABI,
please email your request to registry@xinuos.com.
Please include your contact information (preferably a company email
address, not a free email provider), the name of the company, the name
of the operating system with a brief description, your preferred ``ELFOSABI_xxx``
name, and a link (if available) to any public information about the OS.

.. tabularcolumns:: l r >{\raggedright\arraybackslash}p{3.5in}

.. table:: ``EI_OSABI`` Values

   =======================  ===========  ===================================================
   Name                     Value        Meaning
   =======================  ===========  ===================================================
   ``ELFOSABI_NONE``        ``0``        No extensions or unspecified
   ``ELFOSABI_HPUX``        ``1``        Hewlett-Packard HP-UX
   ``ELFOSABI_NETBSD``      ``2``        NetBSD
   ``ELFOSABI_GNU``         ``3``        GNU
   ``ELFOSABI_LINUX``       ``3``        Linux (*historical—alias for ELFOSABI_GNU*)
   ``ELFOSABI_SOLARIS``     ``6``        Sun Solaris
   ``ELFOSABI_AIX``         ``7``        AIX
   ``ELFOSABI_IRIX``        ``8``        IRIX
   ``ELFOSABI_FREEBSD``     ``9``        FreeBSD
   ``ELFOSABI_TRU64``       ``10``       Compaq TRU64 UNIX
   ``ELFOSABI_MODESTO``     ``11``       Novell Modesto
   ``ELFOSABI_OPENBSD``     ``12``       Open BSD
   ``ELFOSABI_OPENVMS``     ``13``       Open VMS
   ``ELFOSABI_NSK``         ``14``       Hewlett-Packard Non-Stop Kernel
   ``ELFOSABI_AROS``        ``15``       Amiga Research OS
   ``ELFOSABI_FENIXOS``     ``16``       The FenixOS highly scalable multi-core OS
   ``ELFOSABI_CLOUDABI``    ``17``       Nuxi CloudABI
   ``ELFOSABI_OPENVOS``     ``18``       Stratus Technologies OpenVOS
   \                        ``64-255``   Architecture-specific value range
   =======================  ===========  ===================================================
