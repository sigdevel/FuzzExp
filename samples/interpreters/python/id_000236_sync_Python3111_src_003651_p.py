


"""
Overview
========

Kconfiglib is a Python 2/3 library for scripting and extracting information
from Kconfig (https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt)
configuration systems.

See the homepage at https://github.com/ulfalizer/Kconfiglib for a longer
overview.

Since Kconfiglib 12.0.0, the library version is available in
kconfiglib.VERSION, which is a (<major>, <minor>, <patch>) tuple, e.g.
(12, 0, 0).


Using Kconfiglib on the Linux kernel with the Makefile targets
==============================================================

For the Linux kernel, a handy interface is provided by the
scripts/kconfig/Makefile patch, which can be applied with either 'git am' or
the 'patch' utility:

  $ wget -qO- https://raw.githubusercontent.com/ulfalizer/Kconfiglib/master/makefile.patch | git am
  $ wget -qO- https://raw.githubusercontent.com/ulfalizer/Kconfiglib/master/makefile.patch | patch -p1

Warning: Not passing -p1 to patch will cause the wrong file to be patched.

Please tell me if the patch does not apply. It should be trivial to apply
manually, as it's just a block of text that needs to be inserted near the other
*conf: targets in scripts/kconfig/Makefile.

Look further down for a motivation for the Makefile patch and for instructions
on how you can use Kconfiglib without it.

If you do not wish to install Kconfiglib via pip, the Makefile patch is set up
so that you can also just clone Kconfiglib into the kernel root:

  $ git clone git://github.com/ulfalizer/Kconfiglib.git
  $ git am Kconfiglib/makefile.patch  (or 'patch -p1 < Kconfiglib/makefile.patch')

Warning: The directory name Kconfiglib/ is significant in this case, because
it's added to PYTHONPATH by the new targets in makefile.patch.

The targets added by the Makefile patch are described in the following
sections.


make kmenuconfig
----------------

This target runs the curses menuconfig interface with Python 3. As of
Kconfiglib 12.2.0, both Python 2 and Python 3 are supported (previously, only
Python 3 was supported, so this was a backport).


make guiconfig
--------------

This target runs the Tkinter menuconfig interface. Both Python 2 and Python 3
are supported. To change the Python interpreter used, pass
PYTHONCMD=<executable> to 'make'. The default is 'python'.


make [ARCH=<arch>] iscriptconfig
--------------------------------

This target gives an interactive Python prompt where a Kconfig instance has
been preloaded and is available in 'kconf'. To change the Python interpreter
used, pass PYTHONCMD=<executable> to 'make'. The default is 'python'.

To get a feel for the API, try evaluating and printing the symbols in
kconf.defined_syms, and explore the MenuNode menu tree starting at
kconf.top_node by following 'next' and 'list' pointers.

The item contained in a menu node is found in MenuNode.item (note that this can
be one of the constants kconfiglib.MENU and kconfiglib.COMMENT), and all
symbols and choices have a 'nodes' attribute containing their menu nodes
(usually only one). Printing a menu node will print its item, in Kconfig
format.

If you want to look up a symbol by name, use the kconf.syms dictionary.


make scriptconfig SCRIPT=<script> [SCRIPT_ARG=<arg>]
----------------------------------------------------

This target runs the Python script given by the SCRIPT parameter on the
configuration. sys.argv[1] holds the name of the top-level Kconfig file
(currently always "Kconfig" in practice), and sys.argv[2] holds the SCRIPT_ARG
argument, if given.

See the examples/ subdirectory for example scripts.


make dumpvarsconfig
-------------------

This target prints a list of all environment variables referenced from the
Kconfig files, together with their values. See the
Kconfiglib/examples/dumpvars.py script.

Only environment variables that are referenced via the Kconfig preprocessor
$(FOO) syntax are included. The preprocessor was added in Linux 4.18.


Using Kconfiglib without the Makefile targets
=============================================

The make targets are only needed to pick up environment variables exported from
the Kbuild makefiles and referenced inside Kconfig files, via e.g.
'source "arch/$(SRCARCH)/Kconfig" and commands run via '$(shell,...)'.

These variables are referenced as of writing (Linux 4.18), together with sample
values:

  srctree          (.)
  ARCH             (x86)
  SRCARCH          (x86)
  KERNELVERSION    (4.18.0)
  CC               (gcc)
  HOSTCC           (gcc)
  HOSTCXX          (g++)
  CC_VERSION_TEXT  (gcc (Ubuntu 7.3.0-16ubuntu3) 7.3.0)

Older kernels only reference ARCH, SRCARCH, and KERNELVERSION.

If your kernel is recent enough (4.18+), you can get a list of referenced
environment variables via 'make dumpvarsconfig' (see above). Note that this
command is added by the Makefile patch.

To run Kconfiglib without the Makefile patch, set the environment variables
manually:

  $ srctree=. ARCH=x86 SRCARCH=x86 KERNELVERSION=`make kernelversion` ... python(3)
  >>> import kconfiglib
  >>> kconf = kconfiglib.Kconfig()  "Kconfig"

Search the top-level Makefile for "Additional ARCH settings" to see other
possibilities for ARCH and SRCARCH.


Intro to symbol values
======================

Kconfiglib has the same assignment semantics as the C implementation.

Any symbol can be assigned a value by the user (via Kconfig.load_config() or
Symbol.set_value()), but this user value is only respected if the symbol is
visible, which corresponds to it (currently) being visible in the menuconfig
interface.

For symbols with prompts, the visibility of the symbol is determined by the
condition on the prompt. Symbols without prompts are never visible, so setting
a user value on them is pointless. A warning will be printed by default if
Symbol.set_value() is called on a promptless symbol. Assignments to promptless
symbols are normal within a .config file, so no similar warning will be printed
by load_config().

Dependencies from parents and 'if'/'depends on' are propagated to properties,
including prompts, so these two configurations are logically equivalent:

(1)

  menu "menu"
      depends on A

  if B

  config FOO
      tristate "foo" if D
      default y
      depends on C

  endif

  endmenu

(2)

  menu "menu"
      depends on A

  config FOO
      tristate "foo" if A && B && C && D
      default y if A && B && C

  endmenu

In this example, A && B && C && D (the prompt condition) needs to be non-n for
FOO to be visible (assignable). If its value is m, the symbol can only be
assigned the value m: The visibility sets an upper bound on the value that can
be assigned by the user, and any higher user value will be truncated down.

'default' properties are independent of the visibility, though a 'default' will
often get the same condition as the prompt due to dependency propagation.
'default' properties are used if the symbol is not visible or has no user
value.

Symbols with no user value (or that have a user value but are not visible) and
no (active) 'default' default to n for bool/tristate symbols, and to the empty
string for other symbol types.

'select' works similarly to symbol visibility, but sets a lower bound on the
value of the symbol. The lower bound is determined by the value of the
select*ing* symbol. 'select' does not respect visibility, so non-visible
symbols can be forced to a particular (minimum) value by a select as well.

For non-bool/tristate symbols, it only matters whether the visibility is n or
non-n: m visibility acts the same as y visibility.

Conditions on 'default' and 'select' work in mostly intuitive ways. If the
condition is n, the 'default' or 'select' is disabled. If it is m, the
'default' or 'select' value (the value of the selecting symbol) is truncated
down to m.

When writing a configuration with Kconfig.write_config(), only symbols that are
visible, have an (active) default, or are selected will get written out (note
that this includes all symbols that would accept user values). Kconfiglib
matches the .config format produced by the C implementations down to the
character. This eases testing.

For a visible bool/tristate symbol FOO with value n, this line is written to
.config:

    

The point is to remember the user n selection (which might differ from the
default value the symbol would get), while at the same sticking to the rule
that undefined corresponds to n (.config uses Makefile format, making the line
above a comment). When the .config file is read back in, this line will be
treated the same as the following assignment:

    CONFIG_FOO=n

In Kconfiglib, the set of (currently) assignable values for a bool/tristate
symbol appear in Symbol.assignable. For other symbol types, just check if
sym.visibility is non-0 (non-n) to see whether the user value will have an
effect.


Intro to the menu tree
======================

The menu structure, as seen in e.g. menuconfig, is represented by a tree of
MenuNode objects. The top node of the configuration corresponds to an implicit
top-level menu, the title of which is shown at the top in the standard
menuconfig interface. (The title is also available in Kconfig.mainmenu_text in
Kconfiglib.)

The top node is found in Kconfig.top_node. From there, you can visit child menu
nodes by following the 'list' pointer, and any following menu nodes by
following the 'next' pointer. Usually, a non-None 'list' pointer indicates a
menu or Choice, but menu nodes for symbols can sometimes have a non-None 'list'
pointer too due to submenus created implicitly from dependencies.

MenuNode.item is either a Symbol or a Choice object, or one of the constants
MENU and COMMENT. The prompt of the menu node can be found in MenuNode.prompt,
which also holds the title for menus and comments. For Symbol and Choice,
MenuNode.help holds the help text (if any, otherwise None).

Most symbols will only have a single menu node. A symbol defined in multiple
locations will have one menu node for each location. The list of menu nodes for
a Symbol or Choice can be found in the Symbol/Choice.nodes attribute.

Note that prompts and help texts for symbols and choices are stored in their
menu node(s) rather than in the Symbol or Choice objects themselves. This makes
it possible to define a symbol in multiple locations with a different prompt or
help text in each location. To get the help text or prompt for a symbol with a
single menu node, do sym.nodes[0].help and sym.nodes[0].prompt, respectively.
The prompt is a (text, condition) tuple, where condition determines the
visibility (see 'Intro to expressions' below).

This organization mirrors the C implementation. MenuNode is called
'struct menu' there, but I thought "menu" was a confusing name.

It is possible to give a Choice a name and define it in multiple locations,
hence why Choice.nodes is also a list.

As a convenience, the properties added at a particular definition location are
available on the MenuNode itself, in e.g. MenuNode.defaults. This is helpful
when generating documentation, so that symbols/choices defined in multiple
locations can be shown with the correct properties at each location.


Intro to expressions
====================

Expressions can be evaluated with the expr_value() function and printed with
the expr_str() function (these are used internally as well). Evaluating an
expression always yields a tristate value, where n, m, and y are represented as
0, 1, and 2, respectively.

The following table should help you figure out how expressions are represented.
A, B, C, ... are symbols (Symbol instances), NOT is the kconfiglib.NOT
constant, etc.

Expression            Representation
----------            --------------
A                     A
"A"                   A (constant symbol)
!A                    (NOT, A)
A && B                (AND, A, B)
A && B && C           (AND, A, (AND, B, C))
A || B                (OR, A, B)
A || (B && C && D)    (OR, A, (AND, B, (AND, C, D)))
A = B                 (EQUAL, A, B)
A != "foo"            (UNEQUAL, A, foo (constant symbol))
A && B = C && D       (AND, A, (AND, (EQUAL, B, C), D))
n                     Kconfig.n (constant symbol)
m                     Kconfig.m (constant symbol)
y                     Kconfig.y (constant symbol)
"y"                   Kconfig.y (constant symbol)

Strings like "foo" in 'default "foo"' or 'depends on SYM = "foo"' are
represented as constant symbols, so the only values that appear in expressions
are symbols***. This mirrors the C implementation.

***For choice symbols, the parent Choice will appear in expressions as well,
but it's usually invisible as the value interfaces of Symbol and Choice are
identical. This mirrors the C implementation and makes different choice modes
"just work".

Manual evaluation examples:

  - The value of A && B is min(A.tri_value, B.tri_value)

  - The value of A || B is max(A.tri_value, B.tri_value)

  - The value of !A is 2 - A.tri_value

  - The value of A = B is 2 (y) if A.str_value == B.str_value, and 0 (n)
    otherwise. Note that str_value is used here instead of tri_value.

    For constant (as well as undefined) symbols, str_value matches the name of
    the symbol. This mirrors the C implementation and explains why
    'depends on SYM = "foo"' above works as expected.

n/m/y are automatically converted to the corresponding constant symbols
"n"/"m"/"y" (Kconfig.n/m/y) during parsing.

Kconfig.const_syms is a dictionary like Kconfig.syms but for constant symbols.

If a condition is missing (e.g., <cond> when the 'if <cond>' is removed from
'default A if <cond>'), it is actually Kconfig.y. The standard __str__()
functions just avoid printing 'if y' conditions to give cleaner output.


Kconfig extensions
==================

Kconfiglib includes a couple of Kconfig extensions:

'source' with relative path
---------------------------

The 'rsource' statement sources Kconfig files with a path relative to directory
of the Kconfig file containing the 'rsource' statement, instead of relative to
the project root.

Consider following directory tree:

  Project
  +--Kconfig
  |
  +--src
     +--Kconfig
     |
     +--SubSystem1
        +--Kconfig
        |
        +--ModuleA
           +--Kconfig

In this example, assume that src/SubSystem1/Kconfig wants to source
src/SubSystem1/ModuleA/Kconfig.

With 'source', this statement would be used:

  source "src/SubSystem1/ModuleA/Kconfig"

With 'rsource', this turns into

  rsource "ModuleA/Kconfig"

If an absolute path is given to 'rsource', it acts the same as 'source'.

'rsource' can be used to create "position-independent" Kconfig trees that can
be moved around freely.


Globbing 'source'
-----------------

'source' and 'rsource' accept glob patterns, sourcing all matching Kconfig
files. They require at least one matching file, raising a KconfigError
otherwise.

For example, the following statement might source sub1/foofoofoo and
sub2/foobarfoo:

  source "sub[12]/foo*foo"

The glob patterns accepted are the same as for the standard glob.glob()
function.

Two additional statements are provided for cases where it's acceptable for a
pattern to match no files: 'osource' and 'orsource' (the o is for "optional").

For example, the following statements will be no-ops if neither "foo" nor any
files matching "bar*" exist:

  osource "foo"
  osource "bar*"

'orsource' does a relative optional source.

'source' and 'osource' are analogous to 'include' and '-include' in Make.


Generalized def_* keywords
--------------------------

def_int, def_hex, and def_string are available in addition to def_bool and
def_tristate, allowing int, hex, and string symbols to be given a type and a
default at the same time.


Extra optional warnings
-----------------------

Some optional warnings can be controlled via environment variables:

  - KCONFIG_WARN_UNDEF: If set to 'y', warnings will be generated for all
    references to undefined symbols within Kconfig files. The only gotcha is
    that all hex literals must be prefixed with "0x" or "0X", to make it
    possible to distinguish them from symbol references.

    Some projects (e.g. the Linux kernel) use multiple Kconfig trees with many
    shared Kconfig files, leading to some safe undefined symbol references.
    KCONFIG_WARN_UNDEF is useful in projects that only have a single Kconfig
    tree though.

    KCONFIG_STRICT is an older alias for this environment variable, supported
    for backwards compatibility.

  - KCONFIG_WARN_UNDEF_ASSIGN: If set to 'y', warnings will be generated for
    all assignments to undefined symbols within .config files. By default, no
    such warnings are generated.

    This warning can also be enabled/disabled via the Kconfig.warn_assign_undef
    variable.


Preprocessor user functions defined in Python
---------------------------------------------

Preprocessor functions can be defined in Python, which makes it simple to
integrate information from existing Python tools into Kconfig (e.g. to have
Kconfig symbols depend on hardware information stored in some other format).

Putting a Python module named kconfigfunctions(.py) anywhere in sys.path will
cause it to be imported by Kconfiglib (in Kconfig.__init__()). Note that
sys.path can be customized via PYTHONPATH, and includes the directory of the
module being run by default, as well as installation directories.

If the KCONFIG_FUNCTIONS environment variable is set, it gives a different
module name to use instead of 'kconfigfunctions'.

The imported module is expected to define a global dictionary named 'functions'
that maps function names to Python functions, as follows:

  def my_fn(kconf, name, arg_1, arg_2, ...):
      
      
      
      
      "my-fn"). Think argv[0].
      
      
      
      
      
      
      ...

  def my_other_fn(kconf, name, arg_1, arg_2, ...):
      ...

  functions = {
      "my-fn":       (my_fn,       <min.args>, <max.args>/None),
      "my-other-fn": (my_other_fn, <min.args>, <max.args>/None),
      ...
  }

  ...

<min.args> and <max.args> are the minimum and maximum number of arguments
expected by the function (excluding the implicit 'name' argument). If
<max.args> is None, there is no upper limit to the number of arguments. Passing
an invalid number of arguments will generate a KconfigError exception.

Functions can access the current parsing location as kconf.filename/linenr.
Accessing other fields of the Kconfig object is not safe. See the warning
below.

Keep in mind that for a variable defined like 'foo = $(fn)', 'fn' will be
called only when 'foo' is expanded. If 'fn' uses the parsing location and the
intent is to use the location of the assignment, you want 'foo := $(fn)'
instead, which calls the function immediately.

Once defined, user functions can be called from Kconfig in the same way as
other preprocessor functions:

    config FOO
        ...
        depends on $(my-fn,arg1,arg2)

If my_fn() returns "n", this will result in

    config FOO
        ...
        depends on n

Warning
*******

User-defined preprocessor functions are called as they're encountered at parse
time, before all Kconfig files have been processed, and before the menu tree
has been finalized. There are no guarantees that accessing Kconfig symbols or
the menu tree via the 'kconf' parameter will work, and it could potentially
lead to a crash.

Preferably, user-defined functions should be stateless.


Feedback
========

Send bug reports, suggestions, and questions to ulfalizer a.t Google's email
service, or open a ticket on the GitHub page.
"""
import errno
import importlib
import os
import re
import sys


from glob import iglob
from os.path import dirname, exists, expandvars, islink, join, realpath


VERSION = (14, 1, 0)


















class Kconfig(object):
    """
    Represents a Kconfig configuration, e.g. for x86 or ARM. This is the set of
    symbols, choices, and menu nodes appearing in the configuration. Creating
    any number of Kconfig objects (including for different architectures) is
    safe. Kconfiglib doesn't keep any global state.

    The following attributes are available. They should be treated as
    read-only, and some are implemented through @property magic.

    syms:
      A dictionary with all symbols in the configuration, indexed by name. Also
      includes all symbols that are referenced in expressions but never
      defined, except for constant (quoted) symbols.

      Undefined symbols can be recognized by Symbol.nodes being empty -- see
      the 'Intro to the menu tree' section in the module docstring.

    const_syms:
      A dictionary like 'syms' for constant (quoted) symbols

    named_choices:
      A dictionary like 'syms' for named choices (choice FOO)

    defined_syms:
      A list with all defined symbols, in the same order as they appear in the
      Kconfig files. Symbols defined in multiple locations appear multiple
      times.

      Note: You probably want to use 'unique_defined_syms' instead. This
      attribute is mostly maintained for backwards compatibility.

    unique_defined_syms:
      A list like 'defined_syms', but with duplicates removed. Just the first
      instance is kept for symbols defined in multiple locations. Kconfig order
      is preserved otherwise.

      Using this attribute instead of 'defined_syms' can save work, and
      automatically gives reasonable behavior when writing configuration output
      (symbols defined in multiple locations only generate output once, while
      still preserving Kconfig order for readability).

    choices:
      A list with all choices, in the same order as they appear in the Kconfig
      files.

      Note: You probably want to use 'unique_choices' instead. This attribute
      is mostly maintained for backwards compatibility.

    unique_choices:
      Analogous to 'unique_defined_syms', for choices. Named choices can have
      multiple definition locations.

    menus:
      A list with all menus, in the same order as they appear in the Kconfig
      files

    comments:
      A list with all comments, in the same order as they appear in the Kconfig
      files

    kconfig_filenames:
      A list with the filenames of all Kconfig files included in the
      configuration, relative to $srctree (or relative to the current directory
      if $srctree isn't set), except absolute paths (e.g.
      'source "/foo/Kconfig"') are kept as-is.

      The files are listed in the order they are source'd, starting with the
      top-level Kconfig file. If a file is source'd multiple times, it will
      appear multiple times. Use set() to get unique filenames.

      Note that Kconfig.sync_deps() already indirectly catches any file
      modifications that change configuration output.

    env_vars:
      A set() with the names of all environment variables referenced in the
      Kconfig files.

      Only environment variables referenced with the preprocessor $(FOO) syntax
      will be registered. The older $FOO syntax is only supported for backwards
      compatibility.

      Also note that $(FOO) won't be registered unless the environment variable
      $FOO is actually set. If it isn't, $(FOO) is an expansion of an unset
      preprocessor variable (which gives the empty string).

      Another gotcha is that environment variables referenced in the values of
      recursively expanded preprocessor variables (those defined with =) will
      only be registered if the variable is actually used (expanded) somewhere.

      The note from the 'kconfig_filenames' documentation applies here too.

    n/m/y:
      The predefined constant symbols n/m/y. Also available in const_syms.

    modules:
      The Symbol instance for the modules symbol. Currently hardcoded to
      MODULES, which is backwards compatible. Kconfiglib will warn if
      'option modules' is set on some other symbol. Tell me if you need proper
      'option modules' support.

      'modules' is never None. If the MODULES symbol is not explicitly defined,
      its tri_value will be 0 (n), as expected.

      A simple way to enable modules is to do 'kconf.modules.set_value(2)'
      (provided the MODULES symbol is defined and visible). Modules are
      disabled by default in the kernel Kconfig files as of writing, though
      nearly all defconfig files enable them (with 'CONFIG_MODULES=y').

    defconfig_list:
      The Symbol instance for the 'option defconfig_list' symbol, or None if no
      defconfig_list symbol exists. The defconfig filename derived from this
      symbol can be found in Kconfig.defconfig_filename.

    defconfig_filename:
      The filename given by the defconfig_list symbol. This is taken from the
      first 'default' with a satisfied condition where the specified file
      exists (can be opened for reading). If a defconfig file foo/defconfig is
      not found and $srctree was set when the Kconfig was created,
      $srctree/foo/defconfig is looked up as well.

      'defconfig_filename' is None if either no defconfig_list symbol exists,
      or if the defconfig_list symbol has no 'default' with a satisfied
      condition that specifies a file that exists.

      Gotcha: scripts/kconfig/Makefile might pass --defconfig=<defconfig> to
      scripts/kconfig/conf when running e.g. 'make defconfig'. This option
      overrides the defconfig_list symbol, meaning defconfig_filename might not
      always match what 'make defconfig' would use.

    top_node:
      The menu node (see the MenuNode class) of the implicit top-level menu.
      Acts as the root of the menu tree.

    mainmenu_text:
      The prompt (title) of the top menu (top_node). Defaults to "Main menu".
      Can be changed with the 'mainmenu' statement (see kconfig-language.txt).

    variables:
      A dictionary with all preprocessor variables, indexed by name. See the
      Variable class.

    warn:
      Set this variable to True/False to enable/disable warnings. See
      Kconfig.__init__().

      When 'warn' is False, the values of the other warning-related variables
      are ignored.

      This variable as well as the other warn* variables can be read to check
      the current warning settings.

    warn_to_stderr:
      Set this variable to True/False to enable/disable warnings on stderr. See
      Kconfig.__init__().

    warn_assign_undef:
      Set this variable to True to generate warnings for assignments to
      undefined symbols in configuration files.

      This variable is False by default unless the KCONFIG_WARN_UNDEF_ASSIGN
      environment variable was set to 'y' when the Kconfig instance was
      created.

    warn_assign_override:
      Set this variable to True to generate warnings for multiple assignments
      to the same symbol in configuration files, where the assignments set
      different values (e.g. CONFIG_FOO=m followed by CONFIG_FOO=y, where the
      last value would get used).

      This variable is True by default. Disabling it might be useful when
      merging configurations.

    warn_assign_redun:
      Like warn_assign_override, but for multiple assignments setting a symbol
      to the same value.

      This variable is True by default. Disabling it might be useful when
      merging configurations.

    warnings:
      A list of strings containing all warnings that have been generated, for
      cases where more flexibility is needed.

      See the 'warn_to_stderr' parameter to Kconfig.__init__() and the
      Kconfig.warn_to_stderr variable as well. Note that warnings still get
      added to Kconfig.warnings when 'warn_to_stderr' is True.

      Just as for warnings printed to stderr, only warnings that are enabled
      will get added to Kconfig.warnings. See the various Kconfig.warn*
      variables.

    missing_syms:
      A list with (name, value) tuples for all assignments to undefined symbols
      within the most recently loaded .config file(s). 'name' is the symbol
      name without the 'CONFIG_' prefix. 'value' is a string that gives the
      right-hand side of the assignment verbatim.

      See Kconfig.load_config() as well.

    srctree:
      The value the $srctree environment variable had when the Kconfig instance
      was created, or the empty string if $srctree wasn't set. This gives nice
      behavior with os.path.join(), which treats "" as the current directory,
      without adding "./".

      Kconfig files are looked up relative to $srctree (unless absolute paths
      are used), and .config files are looked up relative to $srctree if they
      are not found in the current directory. This is used to support
      out-of-tree builds. The C tools use this environment variable in the same
      way.

      Changing $srctree after creating the Kconfig instance has no effect. Only
      the value when the configuration is loaded matters. This avoids surprises
      if multiple configurations are loaded with different values for $srctree.

    config_prefix:
      The value the CONFIG_ environment variable had when the Kconfig instance
      was created, or "CONFIG_" if CONFIG_ wasn't set. This is the prefix used
      (and expected) on symbol names in .config files and C headers. Used in
      the same way in the C tools.

    config_header:
      The value the KCONFIG_CONFIG_HEADER environment variable had when the
      Kconfig instance was created, or the empty string if
      KCONFIG_CONFIG_HEADER wasn't set. This string is inserted verbatim at the
      beginning of configuration files. See write_config().

    header_header:
      The value the KCONFIG_AUTOHEADER_HEADER environment variable had when the
      Kconfig instance was created, or the empty string if
      KCONFIG_AUTOHEADER_HEADER wasn't set. This string is inserted verbatim at
      the beginning of header files. See write_autoconf().

    filename/linenr:
      The current parsing location, for use in Python preprocessor functions.
      See the module docstring.
    """
    __slots__ = (
        "_encoding",
        "_functions",
        "_set_match",
        "_srctree_prefix",
        "_unset_match",
        "_warn_assign_no_prompt",
        "choices",
        "comments",
        "config_header",
        "config_prefix",
        "const_syms",
        "defconfig_list",
        "defined_syms",
        "env_vars",
        "header_header",
        "kconfig_filenames",
        "m",
        "menus",
        "missing_syms",
        "modules",
        "n",
        "named_choices",
        "srctree",
        "syms",
        "top_node",
        "unique_choices",
        "unique_defined_syms",
        "variables",
        "warn",
        "warn_assign_override",
        "warn_assign_redun",
        "warn_assign_undef",
        "warn_to_stderr",
        "warnings",
        "y",

        
        "_parsing_kconfigs",
        "_readline",
        "filename",
        "linenr",
        "_include_path",
        "_filestack",
        "_line",
        "_tokens",
        "_tokens_i",
        "_reuse_tokens",
    )

    
    
    

    def __init__(self, filename="Kconfig", warn=True, warn_to_stderr=True,
                 encoding="utf-8", suppress_traceback=False):
        """
        Creates a new Kconfig object by parsing Kconfig files.
        Note that Kconfig files are not the same as .config files (which store
        configuration symbol values).

        See the module docstring for some environment variables that influence
        default warning settings (KCONFIG_WARN_UNDEF and
        KCONFIG_WARN_UNDEF_ASSIGN).

        Raises KconfigError on syntax/semantic errors, and OSError or (possibly
        a subclass of) IOError on IO errors ('errno', 'strerror', and
        'filename' are available). Note that IOError is an alias for OSError on
        Python 3, so it's enough to catch OSError there. If you need Python 2/3
        compatibility, it's easiest to catch EnvironmentError, which is a
        common base class of OSError/IOError on Python 2 and an alias for
        OSError on Python 3.

        filename (default: "Kconfig"):
          The Kconfig file to load. For the Linux kernel, you'll want "Kconfig"
          from the top-level directory, as environment variables will make sure
          the right Kconfig is included from there (arch/$SRCARCH/Kconfig as of
          writing).

          If $srctree is set, 'filename' will be looked up relative to it.
          $srctree is also used to look up source'd files within Kconfig files.
          See the class documentation.

          If you are using Kconfiglib via 'make scriptconfig', the filename of
          the base base Kconfig file will be in sys.argv[1]. It's currently
          always "Kconfig" in practice.

        warn (default: True):
          True if warnings related to this configuration should be generated.
          This can be changed later by setting Kconfig.warn to True/False. It
          is provided as a constructor argument since warnings might be
          generated during parsing.

          See the other Kconfig.warn_* variables as well, which enable or
          suppress certain warnings when warnings are enabled.

          All generated warnings are added to the Kconfig.warnings list. See
          the class documentation.

        warn_to_stderr (default: True):
          True if warnings should be printed to stderr in addition to being
          added to Kconfig.warnings.

          This can be changed later by setting Kconfig.warn_to_stderr to
          True/False.

        encoding (default: "utf-8"):
          The encoding to use when reading and writing files, and when decoding
          output from commands run via $(shell). If None, the encoding
          specified in the current locale will be used.

          The "utf-8" default avoids exceptions on systems that are configured
          to use the C locale, which implies an ASCII encoding.

          This parameter has no effect on Python 2, due to implementation
          issues (regular strings turning into Unicode strings, which are
          distinct in Python 2). Python 2 doesn't decode regular strings
          anyway.

          Related PEP: https://www.python.org/dev/peps/pep-0538/

        suppress_traceback (default: False):
          Helper for tools. When True, any EnvironmentError or KconfigError
          generated during parsing is caught, the exception message is printed
          to stderr together with the command name, and sys.exit(1) is called
          (which generates SystemExit).

          This hides the Python traceback for "expected" errors like syntax
          errors in Kconfig files.

          Other exceptions besides EnvironmentError and KconfigError are still
          propagated when suppress_traceback is True.
        """
        try:
            self._init(filename, warn, warn_to_stderr, encoding)
        except (EnvironmentError, KconfigError) as e:
            if suppress_traceback:
                cmd = sys.argv[0]  
                if cmd:
                    cmd += ": "
                
                
                
                sys.exit(cmd + str(e).strip())
            raise

    def _init(self, filename, warn, warn_to_stderr, encoding):
        

        self._encoding = encoding

        self.srctree = os.getenv("srctree", "")
        
        
        
        self._srctree_prefix = realpath(self.srctree) + os.sep

        self.warn = warn
        self.warn_to_stderr = warn_to_stderr
        self.warn_assign_undef = os.getenv("KCONFIG_WARN_UNDEF_ASSIGN") == "y"
        self.warn_assign_override = True
        self.warn_assign_redun = True
        self._warn_assign_no_prompt = True

        self.warnings = []

        self.config_prefix = os.getenv("CONFIG_", "CONFIG_")
        
        self._set_match = _re_match(self.config_prefix + r"([^=]+)=(.*)")
        self._unset_match = _re_match(r"".format(
            self.config_prefix))

        self.config_header = os.getenv("KCONFIG_CONFIG_HEADER", "")
        self.header_header = os.getenv("KCONFIG_AUTOHEADER_HEADER", "")

        self.syms = {}
        self.const_syms = {}
        self.defined_syms = []
        self.missing_syms = []
        self.named_choices = {}
        self.choices = []
        self.menus = []
        self.comments = []

        for nmy in "n", "m", "y":
            sym = Symbol()
            sym.kconfig = self
            sym.name = nmy
            sym.is_constant = True
            sym.orig_type = TRISTATE
            sym._cached_tri_val = STR_TO_TRI[nmy]

            self.const_syms[nmy] = sym

        self.n = self.const_syms["n"]
        self.m = self.const_syms["m"]
        self.y = self.const_syms["y"]

        
        for nmy in "n", "m", "y":
            sym = self.const_syms[nmy]
            sym.rev_dep = sym.weak_rev_dep = sym.direct_dep = self.n

        
        self.variables = {}

        
        self._functions = {
            "info":       (_info_fn,       1, 1),
            "error-if":   (_error_if_fn,   2, 2),
            "filename":   (_filename_fn,   0, 0),
            "lineno":     (_lineno_fn,     0, 0),
            "shell":      (_shell_fn,      1, 1),
            "warning-if": (_warning_if_fn, 2, 2),
        }

        
        try:
            self._functions.update(
                importlib.import_module(
                    os.getenv("KCONFIG_FUNCTIONS", "kconfigfunctions")
                ).functions)
        except ImportError:
            pass

        
        
        
        self._parsing_kconfigs = True

        self.modules = self._lookup_sym("MODULES")
        self.defconfig_list = None

        self.top_node = MenuNode()
        self.top_node.kconfig = self
        self.top_node.item = MENU
        self.top_node.is_menuconfig = True
        self.top_node.visibility = self.y
        self.top_node.prompt = ("Main menu", self.y)
        self.top_node.parent = None
        self.top_node.dep = self.y
        self.top_node.filename = filename
        self.top_node.linenr = 1
        self.top_node.include_path = ()

        

        
        self.kconfig_filenames = [filename]
        self.env_vars = set()

        
        
        self._filestack = []
        self._include_path = ()

        
        self.filename = filename
        self.linenr = 0

        
        
        
        self._reuse_tokens = False

        
        
        self._readline = self._open(join(self.srctree, filename), "r").readline

        try:
            
            
            self._parse_block(None, self.top_node, self.top_node).next = None
            self.top_node.list = self.top_node.next
            self.top_node.next = None
        except UnicodeDecodeError as e:
            _decoding_error(e, self.filename)

        
        
        self._readline.__self__.close()

        self._parsing_kconfigs = False

        
        self._finalize_node(self.top_node, self.y)

        self.unique_defined_syms = _ordered_unique(self.defined_syms)
        self.unique_choices = _ordered_unique(self.choices)

        
        self._check_sym_sanity()
        self._check_choice_sanity()

        
        
        if os.getenv("KCONFIG_WARN_UNDEF") == "y" or \
           os.getenv("KCONFIG_STRICT") == "y":

            self._check_undef_syms()

        
        self._build_dep()

        
        check_dep_loop_sym = _check_dep_loop_sym  
        for sym in self.unique_defined_syms:
            check_dep_loop_sym(sym, False)

        
        
        self._add_choice_deps()

    @property
    def mainmenu_text(self):
        """
        See the class documentation.
        """
        return self.top_node.prompt[0]

    @property
    def defconfig_filename(self):
        """
        See the class documentation.
        """
        if self.defconfig_list:
            for filename, cond in self.defconfig_list.defaults:
                if expr_value(cond):
                    try:
                        with self._open_config(filename.str_value) as f:
                            return f.name
                    except EnvironmentError:
                        continue

        return None

    def load_config(self, filename=None, replace=True, verbose=None):
        """
        Loads symbol values from a file in the .config format. Equivalent to
        calling Symbol.set_value() to set each of the values.

        "" within a .config file sets the user value of
        FOO to n. The C tools work the same way.

        For each symbol, the Symbol.user_value attribute holds the value the
        symbol was assigned in the .config file (if any). The user value might
        differ from Symbol.str/tri_value if there are unsatisfied dependencies.

        Calling this function also updates the Kconfig.missing_syms attribute
        with a list of all assignments to undefined symbols within the
        configuration file. Kconfig.missing_syms is cleared if 'replace' is
        True, and appended to otherwise. See the documentation for
        Kconfig.missing_syms as well.

        See the Kconfig.__init__() docstring for raised exceptions
        (OSError/IOError). KconfigError is never raised here.

        filename (default: None):
          Path to load configuration from (a string). Respects $srctree if set
          (see the class documentation).

          If 'filename' is None (the default), the configuration file to load
          (if any) is calculated automatically, giving the behavior you'd
          usually want:

            1. If the KCONFIG_CONFIG environment variable is set, it gives the
               path to the configuration file to load. Otherwise, ".config" is
               used. See standard_config_filename().

            2. If the path from (1.) doesn't exist, the configuration file
               given by kconf.defconfig_filename is loaded instead, which is
               derived from the 'option defconfig_list' symbol.

            3. If (1.) and (2.) fail to find a configuration file to load, no
               configuration file is loaded, and symbols retain their current
               values (e.g., their default values). This is not an error.

           See the return value as well.

        replace (default: True):
          If True, all existing user values will be cleared before loading the
          .config. Pass False to merge configurations.

        verbose (default: None):
          Limited backwards compatibility to prevent crashes. A warning is
          printed if anything but None is passed.

          Prior to Kconfiglib 12.0.0, this option enabled printing of messages
          to stdout when 'filename' was None. A message is (always) returned
          now instead, which is more flexible.

          Will probably be removed in some future version.

        Returns a string with a message saying which file got loaded (or
        possibly that no file got loaded, when 'filename' is None). This is
        meant to reduce boilerplate in tools, which can do e.g.
        print(kconf.load_config()). The returned message distinguishes between
        loading (replace == True) and merging (replace == False).
        """
        if verbose is not None:
            _warn_verbose_deprecated("load_config")

        msg = None
        if filename is None:
            filename = standard_config_filename()
            if not exists(filename) and \
               not exists(join(self.srctree, filename)):
                defconfig = self.defconfig_filename
                if defconfig is None:
                    return "Using default symbol values (no '{}')" \
                           .format(filename)

                msg = " default configuration '{}' (no '{}')" \
                      .format(defconfig, filename)
                filename = defconfig

        if not msg:
            msg = " configuration '{}'".format(filename)

        
        
        self._warn_assign_no_prompt = False

        
        
        try:
            self._load_config(filename, replace)
        except UnicodeDecodeError as e:
            _decoding_error(e, filename)
        finally:
            self._warn_assign_no_prompt = True

        return ("Loaded" if replace else "Merged") + msg

    def _load_config(self, filename, replace):
        with self._open_config(filename) as f:
            if replace:
                self.missing_syms = []

                
                
                
                
                

                for sym in self.unique_defined_syms:
                    sym._was_set = False

                for choice in self.unique_choices:
                    choice._was_set = False

            
            set_match = self._set_match
            unset_match = self._unset_match
            get_sym = self.syms.get

            for linenr, line in enumerate(f, 1):
                
                line = line.rstrip()

                match = set_match(line)
                if match:
                    name, val = match.groups()
                    sym = get_sym(name)
                    if not sym or not sym.nodes:
                        self._undef_assign(name, val, filename, linenr)
                        continue

                    if sym.orig_type in _BOOL_TRISTATE:
                        
                        
                        if not (sym.orig_type is BOOL
                                and val.startswith(("y", "n")) or
                                sym.orig_type is TRISTATE
                                and val.startswith(("y", "m", "n"))):
                            self._warn("'{}' is not a valid value for the {} "
                                       "symbol {}. Assignment ignored."
                                       .format(val, TYPE_TO_STR[sym.orig_type],
                                               sym.name_and_loc),
                                       filename, linenr)
                            continue

                        val = val[0]

                        if sym.choice and val != "n":
                            
                            
                            

                            prev_mode = sym.choice.user_value
                            if prev_mode is not None and \
                               TRI_TO_STR[prev_mode] != val:

                                self._warn("both m and y assigned to symbols "
                                           "within the same choice",
                                           filename, linenr)

                            
                            sym.choice.set_value(val)

                    elif sym.orig_type is STRING:
                        match = _conf_string_match(val)
                        if not match:
                            self._warn("malformed string literal in "
                                       "assignment to {}. Assignment ignored."
                                       .format(sym.name_and_loc),
                                       filename, linenr)
                            continue

                        val = unescape(match.group(1))

                else:
                    match = unset_match(line)
                    if not match:
                        
                        
                        
                        "" here.
                        if line and not line.lstrip().startswith(""):
                            self._warn("ignoring malformed line '{}'"
                                       .format(line),
                                       filename, linenr)

                        continue

                    name = match.group(1)
                    sym = get_sym(name)
                    if not sym or not sym.nodes:
                        self._undef_assign(name, "n", filename, linenr)
                        continue

                    if sym.orig_type not in _BOOL_TRISTATE:
                        continue

                    val = "n"

                

                if sym._was_set:
                    self._assigned_twice(sym, val, filename, linenr)

                sym.set_value(val)

        if replace:
            
            

            for sym in self.unique_defined_syms:
                if not sym._was_set:
                    sym.unset_value()

            for choice in self.unique_choices:
                if not choice._was_set:
                    choice.unset_value()

    def _undef_assign(self, name, val, filename, linenr):
        

        self.missing_syms.append((name, val))
        if self.warn_assign_undef:
            self._warn(
                "attempt to assign the value '{}' to the undefined symbol {}"
                .format(val, name), filename, linenr)

    def _assigned_twice(self, sym, new_val, filename, linenr):
        

        
        if sym.orig_type in _BOOL_TRISTATE:
            user_val = TRI_TO_STR[sym.user_value]
        else:
            user_val = sym.user_value

        msg = '{} set more than once. Old value "{}", new value "{}".'.format(
            sym.name_and_loc, user_val, new_val)

        if user_val == new_val:
            if self.warn_assign_redun:
                self._warn(msg, filename, linenr)
        elif self.warn_assign_override:
            self._warn(msg, filename, linenr)

    def load_allconfig(self, filename):
        """
        Helper for all*config. Loads (merges) the configuration file specified
        by KCONFIG_ALLCONFIG, if any. See Documentation/kbuild/kconfig.txt in
        the Linux kernel.

        Disables warnings for duplicated assignments within configuration files
        for the duration of the call
        (kconf.warn_assign_override/warn_assign_redun = False), and restores
        the previous warning settings at the end. The KCONFIG_ALLCONFIG
        configuration file is expected to override symbols.

        Exits with sys.exit() (which raises a SystemExit exception) and prints
        an error to stderr if KCONFIG_ALLCONFIG is set but the configuration
        file can't be opened.

        filename:
          Command-specific configuration filename - "allyes.config",
          "allno.config", etc.
        """
        load_allconfig(self, filename)

    def write_autoconf(self, filename=None, header=None):
        r"""
        Writes out symbol values as a C header file, matching the format used
        by include/generated/autoconf.h in the kernel.

        The ordering of the 
        write_config(). The order in the C implementation depends on the hash
        table implementation as of writing, and so won't match.

        If 'filename' exists and its contents is identical to what would get
        written out, it is left untouched. This avoids updating file metadata
        like the modification time and possibly triggering redundant work in
        build tools.

        filename (default: None):
          Path to write header to.

          If None (the default), the path in the environment variable
          KCONFIG_AUTOHEADER is used if set, and "include/generated/autoconf.h"
          otherwise. This is compatible with the C tools.

        header (default: None):
          Text inserted verbatim at the beginning of the file. You would
          usually want it enclosed in '/* */' to make it a C comment, and
          include a trailing newline.

          If None (the default), the value of the environment variable
          KCONFIG_AUTOHEADER_HEADER had when the Kconfig instance was created
          will be used if it was set, and no header otherwise. See the
          Kconfig.header_header attribute.

        Returns a string with a message saying that the header got saved, or
        that there were no changes to it. This is meant to reduce boilerplate
        in tools, which can do e.g. print(kconf.write_autoconf()).
        """
        if filename is None:
            filename = os.getenv("KCONFIG_AUTOHEADER",
                                 "include/generated/autoconf.h")

        if self._write_if_changed(filename, self._autoconf_contents(header)):
            return "Kconfig header saved to '{}'".format(filename)
        return "No change to Kconfig header in '{}'".format(filename)

    def _autoconf_contents(self, header):
        
        

        if header is None:
            header = self.header_header

        chunks = [header]  "".join()ed later
        add = chunks.append

        for sym in self.unique_defined_syms:
            
            
            
            
            
            
            val = sym.str_value
            if not sym._write_to_conf:
                continue

            if sym.orig_type in _BOOL_TRISTATE:
                if val == "y":
                    add(""
                        .format(self.config_prefix, sym.name))
                elif val == "m":
                    add(""
                        .format(self.config_prefix, sym.name))

            elif sym.orig_type is STRING:
                add('"{}"\n'
                    .format(self.config_prefix, sym.name, escape(val)))

            else:  
                if sym.orig_type is HEX and \
                   not val.startswith(("0x", "0X")):
                    val = "0x" + val

                add(""
                    .format(self.config_prefix, sym.name, val))

        return "".join(chunks)

    def write_config(self, filename=None, header=None, save_old=True,
                     verbose=None):
        r"""
        Writes out symbol values in the .config format. The format matches the
        C implementation, including ordering.

        Symbols appear in the same order in generated .config files as they do
        in the Kconfig files. For symbols defined in multiple locations, a
        single assignment is written out corresponding to the first location
        where the symbol is defined.

        See the 'Intro to symbol values' section in the module docstring to
        understand which symbols get written out.

        If 'filename' exists and its contents is identical to what would get
        written out, it is left untouched. This avoids updating file metadata
        like the modification time and possibly triggering redundant work in
        build tools.

        See the Kconfig.__init__() docstring for raised exceptions
        (OSError/IOError). KconfigError is never raised here.

        filename (default: None):
          Path to write configuration to (a string).

          If None (the default), the path in the environment variable
          KCONFIG_CONFIG is used if set, and ".config" otherwise. See
          standard_config_filename().

        header (default: None):
          Text inserted verbatim at the beginning of the file. You would
          usually want each line to start with '
          include a trailing newline.

          if None (the default), the value of the environment variable
          KCONFIG_CONFIG_HEADER had when the Kconfig instance was created will
          be used if it was set, and no header otherwise. See the
          Kconfig.config_header attribute.

        save_old (default: True):
          If True and <filename> already exists, a copy of it will be saved to
          <filename>.old in the same directory before the new configuration is
          written.

          Errors are silently ignored if <filename>.old cannot be written (e.g.
          due to being a directory, or <filename> being something like
          /dev/null).

        verbose (default: None):
          Limited backwards compatibility to prevent crashes. A warning is
          printed if anything but None is passed.

          Prior to Kconfiglib 12.0.0, this option enabled printing of messages
          to stdout when 'filename' was None. A message is (always) returned
          now instead, which is more flexible.

          Will probably be removed in some future version.

        Returns a string with a message saying which file got saved. This is
        meant to reduce boilerplate in tools, which can do e.g.
        print(kconf.write_config()).
        """
        if verbose is not None:
            _warn_verbose_deprecated("write_config")

        if filename is None:
            filename = standard_config_filename()

        contents = self._config_contents(header)
        if self._contents_eq(filename, contents):
            return "No change to configuration in '{}'".format(filename)

        if save_old:
            _save_old(filename)

        with self._open(filename, "w") as f:
            f.write(contents)

        return "Configuration saved to '{}'".format(filename)

    def _config_contents(self, header):
        
        
        
        
        "".join(_config_contents()), but it was a bit slower on my system.

        "Add '
        "). Those comments get tricky to
        

        for sym in self.unique_defined_syms:
            sym._visited = False

        if header is None:
            header = self.config_header

        chunks = [header]  "".join()ed later
        add = chunks.append

        
        after_end_comment = False

        node = self.top_node
        while 1:
            
            if node.list:
                node = node.list
            elif node.next:
                node = node.next
            else:
                while node.parent:
                    node = node.parent

                    
                    if node.item is MENU and expr_value(node.dep) and \
                       expr_value(node.visibility) and \
                       node is not self.top_node:
                        add("".format(node.prompt[0]))
                        after_end_comment = True

                    if node.next:
                        node = node.next
                        break
                else:
                    
                    return "".join(chunks)

            

            item = node.item

            if item.__class__ is Symbol:
                if item._visited:
                    continue
                item._visited = True

                conf_string = item.config_string
                if not conf_string:
                    continue

                if after_end_comment:
                    
                    
                    after_end_comment = False
                    add("\n")
                add(conf_string)

            elif expr_value(node.dep) and \
                 ((item is MENU and expr_value(node.visibility)) or
                  item is COMMENT):

                add("\n".format(node.prompt[0]))
                after_end_comment = False

    def write_min_config(self, filename, header=None):
        """
        Writes out a "minimal" configuration file, omitting symbols whose value
        matches their default value. The format matches the one produced by
        'make savedefconfig'.

        The resulting configuration file is incomplete, but a complete
        configuration can be derived from it by loading it. Minimal
        configuration files can serve as a more manageable configuration format
        compared to a "full" .config file, especially when configurations files
        are merged or edited by hand.

        See the Kconfig.__init__() docstring for raised exceptions
        (OSError/IOError). KconfigError is never raised here.

        filename:
          Path to write minimal configuration to.

        header (default: None):
          Text inserted verbatim at the beginning of the file. You would
          usually want each line to start with '
          include a final terminating newline.

          if None (the default), the value of the environment variable
          KCONFIG_CONFIG_HEADER had when the Kconfig instance was created will
          be used if it was set, and no header otherwise. See the
          Kconfig.config_header attribute.

        Returns a string with a message saying the minimal configuration got
        saved, or that there were no changes to it. This is meant to reduce
        boilerplate in tools, which can do e.g.
        print(kconf.write_min_config()).
        """
        if self._write_if_changed(filename, self._min_config_contents(header)):
            return "Minimal configuration saved to '{}'".format(filename)
        return "No change to minimal configuration in '{}'".format(filename)

    def _min_config_contents(self, header):
        
        

        if header is None:
            header = self.config_header

        chunks = [header]  "".join()ed later
        add = chunks.append

        for sym in self.unique_defined_syms:
            
            
            
            if not sym.choice and \
               sym.visibility <= expr_value(sym.rev_dep):
                continue

            
            if sym.str_value == sym._str_default():
                continue

            
            
            
            
            if sym.choice and \
               not sym.choice.is_optional and \
               sym.choice._selection_from_defaults() is sym and \
               sym.orig_type is BOOL and \
               sym.tri_value == 2:
                continue

            add(sym.config_string)

        return "".join(chunks)

    def sync_deps(self, path):
        """
        Creates or updates a directory structure that can be used to avoid
        doing a full rebuild whenever the configuration is changed, mirroring
        include/config/ in the kernel.

        This function is intended to be called during each build, before
        compiling source files that depend on configuration symbols.

        See the Kconfig.__init__() docstring for raised exceptions
        (OSError/IOError). KconfigError is never raised here.

        path:
          Path to directory

        sync_deps(path) does the following:

          1. If the directory <path> does not exist, it is created.

          2. If <path>/auto.conf exists, old symbol values are loaded from it,
             which are then compared against the current symbol values. If a
             symbol has changed value (would generate different output in
             autoconf.h compared to before), the change is signaled by
             touch'ing a file corresponding to the symbol.

             The first time sync_deps() is run on a directory, <path>/auto.conf
             won't exist, and no old symbol values will be available. This
             logically has the same effect as updating the entire
             configuration.

             The path to a symbol's file is calculated from the symbol's name
             by replacing all '_' with '/' and appending '.h'. For example, the
             symbol FOO_BAR_BAZ gets the file <path>/foo/bar/baz.h, and FOO
             gets the file <path>/foo.h.

             This scheme matches the C tools. The point is to avoid having a
             single directory with a huge number of files, which the underlying
             filesystem might not handle well.

          3. A new auto.conf with the current symbol values is written, to keep
             track of them for the next build.

             If auto.conf exists and its contents is identical to what would
             get written out, it is left untouched. This avoids updating file
             metadata like the modification time and possibly triggering
             redundant work in build tools.


        The last piece of the puzzle is knowing what symbols each source file
        depends on. Knowing that, dependencies can be added from source files
        to the files corresponding to the symbols they depends on. The source
        file will then get recompiled (only) when the symbol value changes
        (provided sync_deps() is run first during each build).

        The tool in the kernel that extracts symbol dependencies from source
        files is scripts/basic/fixdep.c. Missing symbol files also correspond
        to "not changed", which fixdep deals with by using the $(wildcard) Make
        function when adding symbol prerequisites to source files.

        In case you need a different scheme for your project, the sync_deps()
        implementation can be used as a template.
        """
        if not exists(path):
            os.mkdir(path, 0o755)

        
        self._load_old_vals(path)

        for sym in self.unique_defined_syms:
            
            
            
            
            
            
            val = sym.str_value

            
            

            if sym._write_to_conf:
                if sym._old_val is None and \
                   sym.orig_type in _BOOL_TRISTATE and \
                   val == "n":
                    
                    
                    continue

                if val == sym._old_val:
                    
                    continue

            elif sym._old_val is None:
                
                
                
                
                continue

            
            _touch_dep_file(path, sym.name)

        "new old" values.
        
        
        
        
        self._write_old_vals(path)

    def _load_old_vals(self, path):
        
        
        
        
        
        

        for sym in self.unique_defined_syms:
            sym._old_val = None

        try:
            auto_conf = self._open(join(path, "auto.conf"), "r")
        except EnvironmentError as e:
            if e.errno == errno.ENOENT:
                
                return
            raise

        with auto_conf as f:
            for line in f:
                match = self._set_match(line)
                if not match:
                    
                    
                    continue

                name, val = match.groups()
                if name in self.syms:
                    sym = self.syms[name]

                    if sym.orig_type is STRING:
                        match = _conf_string_match(val)
                        if not match:
                            continue
                        val = unescape(match.group(1))

                    self.syms[name]._old_val = val
                else:
                    
                    
                    _touch_dep_file(path, name)

    def _write_old_vals(self, path):
        
        
        
        
        
        
        
        

        self._write_if_changed(
            os.path.join(path, "auto.conf"),
            self._old_vals_contents())

    def _old_vals_contents(self):
        

        
        return "".join([
            sym.config_string for sym in self.unique_defined_syms
                if not (sym.orig_type in _BOOL_TRISTATE and not sym.tri_value)
        ])

    def node_iter(self, unique_syms=False):
        """
        Returns a generator for iterating through all MenuNode's in the Kconfig
        tree. The iteration is done in Kconfig definition order (each node is
        visited before its children, and the children of a node are visited
        before the next node).

        The Kconfig.top_node menu node is skipped. It contains an implicit menu
        that holds the top-level items.

        As an example, the following code will produce a list equal to
        Kconfig.defined_syms:

          defined_syms = [node.item for node in kconf.node_iter()
                          if isinstance(node.item, Symbol)]

        unique_syms (default: False):
          If True, only the first MenuNode will be included for symbols defined
          in multiple locations.

          Using kconf.node_iter(True) in the example above would give a list
          equal to unique_defined_syms.
        """
        if unique_syms:
            for sym in self.unique_defined_syms:
                sym._visited = False

        node = self.top_node
        while 1:
            
            if node.list:
                node = node.list
            elif node.next:
                node = node.next
            else:
                while node.parent:
                    node = node.parent
                    if node.next:
                        node = node.next
                        break
                else:
                    
                    return

            if unique_syms and node.item.__class__ is Symbol:
                if node.item._visited:
                    continue
                node.item._visited = True

            yield node

    def eval_string(self, s):
        """
        Returns the tristate value of the expression 's', represented as 0, 1,
        and 2 for n, m, and y, respectively. Raises KconfigError on syntax
        errors. Warns if undefined symbols are referenced.

        As an example, if FOO and BAR are tristate symbols at least one of
        which has the value y, then eval_string("y && (FOO || BAR)") returns
        2 (y).

        To get the string value of non-bool/tristate symbols, use
        Symbol.str_value. eval_string() always returns a tristate value, and
        all non-bool/tristate symbols have the tristate value 0 (n).

        The expression parsing is consistent with how parsing works for
        conditional ('if ...') expressions in the configuration, and matches
        the C implementation. m is rewritten to 'm && MODULES', so
        eval_string("m") will return 0 (n) unless modules are enabled.
        """
        
        
        

        self.filename = None

        self._tokens = self._tokenize("if " + s)
        "if " to avoid giving confusing error messages
        self._line = s
        self._tokens_i = 1  

        return expr_value(self._expect_expr_and_eol())

    def unset_values(self):
        """
        Removes any user values from all symbols, as if Kconfig.load_config()
        or Symbol.set_value() had never been called.
        """
        self._warn_assign_no_prompt = False
        try:
            
            
            
            for sym in self.unique_defined_syms:
                sym.unset_value()

            for choice in self.unique_choices:
                choice.unset_value()
        finally:
            self._warn_assign_no_prompt = True

    def enable_warnings(self):
        """
        Do 'Kconfig.warn = True' instead. Maintained for backwards
        compatibility.
        """
        self.warn = True

    def disable_warnings(self):
        """
        Do 'Kconfig.warn = False' instead. Maintained for backwards
        compatibility.
        """
        self.warn = False

    def enable_stderr_warnings(self):
        """
        Do 'Kconfig.warn_to_stderr = True' instead. Maintained for backwards
        compatibility.
        """
        self.warn_to_stderr = True

    def disable_stderr_warnings(self):
        """
        Do 'Kconfig.warn_to_stderr = False' instead. Maintained for backwards
        compatibility.
        """
        self.warn_to_stderr = False

    def enable_undef_warnings(self):
        """
        Do 'Kconfig.warn_assign_undef = True' instead. Maintained for backwards
        compatibility.
        """
        self.warn_assign_undef = True

    def disable_undef_warnings(self):
        """
        Do 'Kconfig.warn_assign_undef = False' instead. Maintained for
        backwards compatibility.
        """
        self.warn_assign_undef = False

    def enable_override_warnings(self):
        """
        Do 'Kconfig.warn_assign_override = True' instead. Maintained for
        backwards compatibility.
        """
        self.warn_assign_override = True

    def disable_override_warnings(self):
        """
        Do 'Kconfig.warn_assign_override = False' instead. Maintained for
        backwards compatibility.
        """
        self.warn_assign_override = False

    def enable_redun_warnings(self):
        """
        Do 'Kconfig.warn_assign_redun = True' instead. Maintained for backwards
        compatibility.
        """
        self.warn_assign_redun = True

    def disable_redun_warnings(self):
        """
        Do 'Kconfig.warn_assign_redun = False' instead. Maintained for
        backwards compatibility.
        """
        self.warn_assign_redun = False

    def __repr__(self):
        """
        Returns a string with information about the Kconfig object when it is
        evaluated on e.g. the interactive Python prompt.
        """
        def status(flag):
            return "enabled" if flag else "disabled"

        return "<{}>".format(", ".join((
            "configuration with {} symbols".format(len(self.syms)),
            'main menu prompt "{}"'.format(self.mainmenu_text),
            "srctree is current directory" if not self.srctree else
                'srctree "{}"'.format(self.srctree),
            'config symbol prefix "{}"'.format(self.config_prefix),
            "warnings " + status(self.warn),
            "printing of warnings to stderr " + status(self.warn_to_stderr),
            "undef. symbol assignment warnings " +
                status(self.warn_assign_undef),
            "overriding symbol assignment warnings " +
                status(self.warn_assign_override),
            "redundant symbol assignment warnings " +
                status(self.warn_assign_redun)
        )))

    
    
    


    
    
    

    def _open_config(self, filename):
        
        
        

        try:
            return self._open(filename, "r")
        except EnvironmentError as e:
            
            
            try:
                return self._open(join(self.srctree, filename), "r")
            except EnvironmentError as e2:
                
                
                
                
                e = e2

            raise _KconfigIOError(
                e, "Could not open '{}' ({}: {}). Check that the $srctree "
                   "environment variable ({}) is set correctly."
                   .format(filename, errno.errorcode[e.errno], e.strerror,
                           "set to '{}'".format(self.srctree) if self.srctree
                               else "unset or blank"))

    def _enter_file(self, filename):
        
        
        
        
        

        
        
        
        if filename.startswith(self._srctree_prefix):
            
            
            rel_filename = filename[len(self._srctree_prefix):]
        else:
            
            rel_filename = filename

        self.kconfig_filenames.append(rel_filename)

        
        
        
        
        
        
        
        
        
        
        

        
        
        self._filestack.append((self._include_path, self._readline))

        
        
        self._include_path += ((self.filename, self.linenr),)

        
        for name, _ in self._include_path:
            if name == rel_filename:
                raise KconfigError(
                    "\n{}:{}: recursive 'source' of '{}' detected. Check that "
                    "environment variables are set correctly.\n"
                    "Include path:\n{}"
                    .format(self.filename, self.linenr, rel_filename,
                            "\n".join("{}:{}".format(name, linenr)
                                      for name, linenr in self._include_path)))

        try:
            self._readline = self._open(filename, "r").readline
        except EnvironmentError as e:
            
            raise _KconfigIOError(
                e, "{}:{}: Could not open '{}' (in '{}') ({}: {})"
                   .format(self.filename, self.linenr, filename,
                           self._line.strip(),
                           errno.errorcode[e.errno], e.strerror))

        self.filename = rel_filename
        self.linenr = 0

    def _leave_file(self):
        
        

        
        self.filename, self.linenr = self._include_path[-1]
        
        self._readline.__self__.close()  
        self._include_path, self._readline = self._filestack.pop()

    def _next_line(self):
        
        

        
        
        if self._reuse_tokens:
            self._reuse_tokens = False
            
            
            
            return True

        
        
        line = self._readline()
        if not line:
            return False
        self.linenr += 1

        
        while line.endswith("\\\n"):
            line = line[:-2] + self._readline()
            self.linenr += 1

        self._tokens = self._tokenize(line)
        
        
        self._tokens_i = 1

        return True

    def _line_after_help(self, line):
        
        
        
        
        
        
        

        
        while line.endswith("\\\n"):
            line = line[:-2] + self._readline()
            self.linenr += 1

        self._tokens = self._tokenize(line)
        self._reuse_tokens = True

    def _write_if_changed(self, filename, contents):
        
        
        
        
        
        "/dev/null"), which is
        
        
        
        
        

        if self._contents_eq(filename, contents):
            return False
        with self._open(filename, "w") as f:
            f.write(contents)
        return True

    def _contents_eq(self, filename, contents):
        
        

        try:
            with self._open(filename, "r") as f:
                
                
                return f.read(len(contents) + 1) == contents
        except EnvironmentError:
            
            
            return False

    
    
    

    def _lookup_sym(self, name):
        
        
        

        if name in self.syms:
            return self.syms[name]

        sym = Symbol()
        sym.kconfig = self
        sym.name = name
        sym.is_constant = False
        sym.rev_dep = sym.weak_rev_dep = sym.direct_dep = self.n

        if self._parsing_kconfigs:
            self.syms[name] = sym
        else:
            self._warn("no symbol {} in configuration".format(name))

        return sym

    def _lookup_const_sym(self, name):
        

        if name in self.const_syms:
            return self.const_syms[name]

        sym = Symbol()
        sym.kconfig = self
        sym.name = name
        sym.is_constant = True
        sym.rev_dep = sym.weak_rev_dep = sym.direct_dep = self.n

        if self._parsing_kconfigs:
            self.const_syms[name] = sym

        return sym

    def _tokenize(self, s):
        
        
        
        
        
        
        
        
        
        

        self._line = s  

        
        match = _command_match(s)
        if not match:
            if s.isspace() or s.lstrip().startswith(""):
                return (None,)
            self._parse_error("unknown token at start of line")

        
        
        token = _get_keyword(match.group(1))
        if not token:
            
            "--help--" and "-help---".
            "kconfig: warn
            "), committed in July
            
            if s.strip(" \t\n-") == "help":
                return (_T_HELP, None)

            
            
            
            self._parse_assignment(s)
            return (None,)

        tokens = [token]
        
        i = match.end()

        
        while i < len(s):
            
            
            match = _id_keyword_match(s, i)
            if match:
                

                
                
                

                name = match.group(1)
                keyword = _get_keyword(name)
                if keyword:
                    
                    token = keyword
                    
                    i = match.end()

                elif token not in _STRING_LEX:
                    
                    
                    

                    if "$" in name:
                        
                        name, s, i = self._expand_name(s, i)
                    else:
                        i = match.end()

                    token = self.const_syms[name] if name in STR_TO_TRI else \
                        self._lookup_sym(name)

                else:
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    

                    if token is not _T_CHOICE:
                        self._warn("style: quotes recommended around '{}' in '{}'"
                                   .format(name, self._line.strip()),
                                   self.filename, self.linenr)

                    token = name
                    i = match.end()

            else:
                

                
                
                c = s[i]

                if c in "\"'":
                    if "$" not in s and "\\" not in s:
                        
                        
                        end_i = s.find(c, i + 1) + 1
                        if not end_i:
                            self._parse_error("unterminated string")
                        val = s[i + 1:end_i - 1]
                        i = end_i
                    else:
                        
                        s, end_i = self._expand_str(s, i)

                        
                        
                        
                        
                        
                        
                        
                        val = expandvars(s[i + 1:end_i - 1]
                                         .replace("$UNAME_RELEASE",
                                                  _UNAME_RELEASE))

                        i = end_i

                    
                    "FOO"' does not
                    "FOO".
                    token = \
                        val if token in _STRING_LEX or tokens[0] is _T_OPTION \
                        else self._lookup_const_sym(val)

                elif s.startswith("&&", i):
                    token = _T_AND
                    i += 2

                elif s.startswith("||", i):
                    token = _T_OR
                    i += 2

                elif c == "=":
                    token = _T_EQUAL
                    i += 1

                elif s.startswith("!=", i):
                    token = _T_UNEQUAL
                    i += 2

                elif c == "!":
                    token = _T_NOT
                    i += 1

                elif c == "(":
                    token = _T_OPEN_PAREN
                    i += 1

                elif c == ")":
                    token = _T_CLOSE_PAREN
                    i += 1

                elif c == "":
                    break


                

                elif s.startswith("<=", i):
                    token = _T_LESS_EQUAL
                    i += 2

                elif c == "<":
                    token = _T_LESS
                    i += 1

                elif s.startswith(">=", i):
                    token = _T_GREATER_EQUAL
                    i += 2

                elif c == ">":
                    token = _T_GREATER
                    i += 1


                else:
                    self._parse_error("unknown tokens in line")


                
                while i < len(s) and s[i].isspace():
                    i += 1


            
            tokens.append(token)

        
        tokens.append(None)

        return tokens

    
    
    
    
    

    def _expect_sym(self):
        token = self._tokens[self._tokens_i]
        self._tokens_i += 1

        if token.__class__ is not Symbol:
            self._parse_error("expected symbol")

        return token

    def _expect_nonconst_sym(self):
        

        token = self._tokens[1]
        self._tokens_i = 2

        if token.__class__ is not Symbol or token.is_constant:
            self._parse_error("expected nonconstant symbol")

        return token

    def _expect_str_and_eol(self):
        token = self._tokens[self._tokens_i]
        self._tokens_i += 1

        if token.__class__ is not str:
            self._parse_error("expected string")

        if self._tokens[self._tokens_i] is not None:
            self._trailing_tokens_error()

        return token

    def _expect_expr_and_eol(self):
        expr = self._parse_expr(True)

        if self._tokens[self._tokens_i] is not None:
            self._trailing_tokens_error()

        return expr

    def _check_token(self, token):
        

        if self._tokens[self._tokens_i] is token:
            self._tokens_i += 1
            return True
        return False

    
    
    

    def _parse_assignment(self, s):
        
        
        

        
        
        s = s.lstrip()
        i = 0
        while 1:
            i = _assignment_lhs_fragment_match(s, i).end()
            if s.startswith("$(", i):
                s, i = self._expand_macro(s, i, ())
            else:
                break

        if s.isspace():
            
            
            return

        
        name = s[:i]


        
        rhs_match = _assignment_rhs_match(s, i)
        if not rhs_match:
            self._parse_error("syntax error")

        op, val = rhs_match.groups()


        if name in self.variables:
            
            var = self.variables[name]
        else:
            
            var = Variable()
            var.kconfig = self
            var.name = name
            var._n_expansions = 0
            self.variables[name] = var

            
            
            if op == "+=":
                op = "="

        if op == "=":
            var.is_recursive = True
            var.value = val
        elif op == ":=":
            var.is_recursive = False
            var.value = self._expand_whole(val, ())
        else:  "+="
            
            
            var.value += " " + (val if var.is_recursive else
                                self._expand_whole(val, ()))

    def _expand_whole(self, s, args):
        
        
        
        
        

        i = 0
        while 1:
            i = s.find("$(", i)
            if i == -1:
                break
            s, i = self._expand_macro(s, i, args)
        return s

    def _expand_name(self, s, i):
        
        
        
        
        

        s, end_i = self._expand_name_iter(s, i)
        name = s[i:end_i]
        
        if not name.strip():
            
            
            self._parse_error("macro expanded to blank string")

        
        while end_i < len(s) and s[end_i].isspace():
            end_i += 1

        return name, s, end_i

    def _expand_name_iter(self, s, i):
        
        
        
        

        while 1:
            match = _name_special_search(s, i)

            if match.group() != "$(":
                return (s, match.start())
            s, i = self._expand_macro(s, match.start(), ())

    def _expand_str(self, s, i):
        
        
        
        
        

        quote = s[i]
        i += 1  "/'
        while 1:
            match = _string_special_search(s, i)
            if not match:
                self._parse_error("unterminated string")


            if match.group() == quote:
                
                return (s, match.end())

            elif match.group() == "\\":
                
                
                i = match.end()
                s = s[:match.start()] + s[i:]

            elif match.group() == "$(":
                
                s, i = self._expand_macro(s, match.start(), ())

            else:
                " quotes or vice versa
                i += 1

    def _expand_macro(self, s, i, args):
        
        
        
        
        
        

        res = s[:i]
        i += 2  "$("

        arg_start = i  
        new_args = []  
        nesting = 0  

        while 1:
            match = _macro_special_search(s, i)
            if not match:
                self._parse_error("missing end parenthesis in macro expansion")


            if match.group() == "(":
                nesting += 1
                i = match.end()

            elif match.group() == ")":
                if nesting:
                    nesting -= 1
                    i = match.end()
                    continue

                

                new_args.append(s[arg_start:match.start()])

                
                

                try:
                    
                    
                    res += args[int(new_args[0])]
                except (ValueError, IndexError):
                    
                    
                    res += self._fn_val(new_args)

                return (res + s[match.end():], len(res))

            elif match.group() == ",":
                i = match.end()
                if nesting:
                    continue

                
                new_args.append(s[arg_start:match.start()])
                arg_start = i

            else:  "$("
                
                s, i = self._expand_macro(s, match.start(), args)

    def _fn_val(self, args):
        
        
        

        fn = args[0]

        if fn in self.variables:
            var = self.variables[fn]

            if len(args) == 1:
                
                if var._n_expansions:
                    self._parse_error("Preprocessor variable {} recursively "
                                      "references itself".format(var.name))
            elif var._n_expansions > 100:
                
                
                self._parse_error("Preprocessor function {} seems stuck "
                                  "in infinite recursion".format(var.name))

            var._n_expansions += 1
            res = self._expand_whole(self.variables[fn].value, args)
            var._n_expansions -= 1
            return res

        if fn in self._functions:
            

            py_fn, min_arg, max_arg = self._functions[fn]

            if len(args) - 1 < min_arg or \
               (max_arg is not None and len(args) - 1 > max_arg):

                if min_arg == max_arg:
                    expected_args = min_arg
                elif max_arg is None:
                    expected_args = "{} or more".format(min_arg)
                else:
                    expected_args = "{}-{}".format(min_arg, max_arg)

                raise KconfigError("{}:{}: bad number of arguments in call "
                                   "to {}, expected {}, got {}"
                                   .format(self.filename, self.linenr, fn,
                                           expected_args, len(args) - 1))

            return py_fn(self, *args)

        
        if fn in os.environ:
            self.env_vars.add(fn)
            return os.environ[fn]

        return ""

    
    
    

    def _make_and(self, e1, e2):
        

        if e1 is self.y:
            return e2

        if e2 is self.y:
            return e1

        if e1 is self.n or e2 is self.n:
            return self.n

        return (AND, e1, e2)

    def _make_or(self, e1, e2):
        

        if e1 is self.n:
            return e2

        if e2 is self.n:
            return e1

        if e1 is self.y or e2 is self.y:
            return self.y

        return (OR, e1, e2)

    def _parse_block(self, end_token, parent, prev):
        
        
        
        
        "endif") for ifs.
        
        
        
        
        
        
        
        
        
        
        
        
        "tilt up" the children above the node.
        
        
        

        while self._next_line():
            t0 = self._tokens[0]

            if t0 is _T_CONFIG or t0 is _T_MENUCONFIG:
                
                sym = self._tokens[1]

                if sym.__class__ is not Symbol or sym.is_constant:
                    self._parse_error("missing or bad symbol name")

                if self._tokens[2] is not None:
                    self._trailing_tokens_error()

                self.defined_syms.append(sym)

                node = MenuNode()
                node.kconfig = self
                node.item = sym
                node.is_menuconfig = (t0 is _T_MENUCONFIG)
                node.prompt = node.help = node.list = None
                node.parent = parent
                node.filename = self.filename
                node.linenr = self.linenr
                node.include_path = self._include_path

                sym.nodes.append(node)

                self._parse_props(node)

                if node.is_menuconfig and not node.prompt:
                    self._warn("the menuconfig symbol {} has no prompt"
                               .format(sym.name_and_loc))

                
                
                
                
                
                
                prev.next = prev = node

            elif t0 is None:
                
                continue

            elif t0 in _SOURCE_TOKENS:
                pattern = self._expect_str_and_eol()

                if t0 in _REL_SOURCE_TOKENS:
                    
                    pattern = join(dirname(self.filename), pattern)

                
                
                
                
                
                
                
                
                filenames = sorted(iglob(join(self._srctree_prefix, pattern)))

                if not filenames and t0 in _OBL_SOURCE_TOKENS:
                    raise KconfigError(
                        "{}:{}: '{}' not found (in '{}'). Check that "
                        "environment variables are set correctly (e.g. "
                        "$srctree, which is {}). Also note that unset "
                        "environment variables expand to the empty string."
                        .format(self.filename, self.linenr, pattern,
                                self._line.strip(),
                                "set to '{}'".format(self.srctree)
                                    if self.srctree else "unset or blank"))

                for filename in filenames:
                    self._enter_file(filename)
                    prev = self._parse_block(None, parent, prev)
                    self._leave_file()

            elif t0 is end_token:
                
                

                if self._tokens[1] is not None:
                    self._trailing_tokens_error()

                prev.next = None
                return prev

            elif t0 is _T_IF:
                node = MenuNode()
                node.item = node.prompt = None
                node.parent = parent
                node.dep = self._expect_expr_and_eol()

                self._parse_block(_T_ENDIF, node, node)
                node.list = node.next

                prev.next = prev = node

            elif t0 is _T_MENU:
                node = MenuNode()
                node.kconfig = self
                node.item = t0  
                node.is_menuconfig = True
                node.prompt = (self._expect_str_and_eol(), self.y)
                node.visibility = self.y
                node.parent = parent
                node.filename = self.filename
                node.linenr = self.linenr
                node.include_path = self._include_path

                self.menus.append(node)

                self._parse_props(node)
                self._parse_block(_T_ENDMENU, node, node)
                node.list = node.next

                prev.next = prev = node

            elif t0 is _T_COMMENT:
                node = MenuNode()
                node.kconfig = self
                node.item = t0  
                node.is_menuconfig = False
                node.prompt = (self._expect_str_and_eol(), self.y)
                node.list = None
                node.parent = parent
                node.filename = self.filename
                node.linenr = self.linenr
                node.include_path = self._include_path

                self.comments.append(node)

                self._parse_props(node)

                prev.next = prev = node

            elif t0 is _T_CHOICE:
                if self._tokens[1] is None:
                    choice = Choice()
                    choice.direct_dep = self.n
                else:
                    
                    name = self._expect_str_and_eol()
                    choice = self.named_choices.get(name)
                    if not choice:
                        choice = Choice()
                        choice.name = name
                        choice.direct_dep = self.n
                        self.named_choices[name] = choice

                self.choices.append(choice)

                node = MenuNode()
                node.kconfig = choice.kconfig = self
                node.item = choice
                node.is_menuconfig = True
                node.prompt = node.help = None
                node.parent = parent
                node.filename = self.filename
                node.linenr = self.linenr
                node.include_path = self._include_path

                choice.nodes.append(node)

                self._parse_props(node)
                self._parse_block(_T_ENDCHOICE, node, node)
                node.list = node.next

                prev.next = prev = node

            elif t0 is _T_MAINMENU:
                self.top_node.prompt = (self._expect_str_and_eol(), self.y)

            else:
                
                
                self._parse_error(
                    "no corresponding 'choice'" if t0 is _T_ENDCHOICE else
                    "no corresponding 'if'"     if t0 is _T_ENDIF else
                    "no corresponding 'menu'"   if t0 is _T_ENDMENU else
                    "unrecognized construct")

        

        if end_token:
            raise KconfigError(
                "error: expected '{}' at end of '{}'"
                .format("endchoice" if end_token is _T_ENDCHOICE else
                        "endif"     if end_token is _T_ENDIF else
                        "endmenu",
                        self.filename))

        return prev

    def _parse_cond(self):
        
        

        expr = self._parse_expr(True) if self._check_token(_T_IF) else self.y

        if self._tokens[self._tokens_i] is not None:
            self._trailing_tokens_error()

        return expr

    def _parse_props(self, node):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        
        
        node.dep = self.y

        while self._next_line():
            t0 = self._tokens[0]

            if t0 in _TYPE_TOKENS:
                
                self._set_type(node.item, t0)
                if self._tokens[1] is not None:
                    self._parse_prompt(node)

            elif t0 is _T_DEPENDS:
                if not self._check_token(_T_ON):
                    self._parse_error("expected 'on' after 'depends'")

                node.dep = self._make_and(node.dep,
                                          self._expect_expr_and_eol())

            elif t0 is _T_HELP:
                self._parse_help(node)

            elif t0 is _T_SELECT:
                if node.item.__class__ is not Symbol:
                    self._parse_error("only symbols can select")

                node.selects.append((self._expect_nonconst_sym(),
                                     self._parse_cond()))

            elif t0 is None:
                
                continue

            elif t0 is _T_DEFAULT:
                node.defaults.append((self._parse_expr(False),
                                      self._parse_cond()))

            elif t0 in _DEF_TOKEN_TO_TYPE:
                self._set_type(node.item, _DEF_TOKEN_TO_TYPE[t0])
                node.defaults.append((self._parse_expr(False),
                                      self._parse_cond()))

            elif t0 is _T_PROMPT:
                self._parse_prompt(node)

            elif t0 is _T_RANGE:
                node.ranges.append((self._expect_sym(), self._expect_sym(),
                                    self._parse_cond()))

            elif t0 is _T_IMPLY:
                if node.item.__class__ is not Symbol:
                    self._parse_error("only symbols can imply")

                node.implies.append((self._expect_nonconst_sym(),
                                     self._parse_cond()))

            elif t0 is _T_VISIBLE:
                if not self._check_token(_T_IF):
                    self._parse_error("expected 'if' after 'visible'")

                node.visibility = self._make_and(node.visibility,
                                                 self._expect_expr_and_eol())

            elif t0 is _T_OPTION:
                if self._check_token(_T_ENV):
                    if not self._check_token(_T_EQUAL):
                        self._parse_error("expected '=' after 'env'")

                    env_var = self._expect_str_and_eol()
                    node.item.env_var = env_var

                    if env_var in os.environ:
                        node.defaults.append(
                            (self._lookup_const_sym(os.environ[env_var]),
                             self.y))
                    else:
                        self._warn("{1} has 'option env=\"{0}\"', "
                                   "but the environment variable {0} is not "
                                   "set".format(node.item.name, env_var),
                                   self.filename, self.linenr)

                    if env_var != node.item.name:
                        self._warn("Kconfiglib expands environment variables "
                                   "in strings directly, meaning you do not "
                                   "need 'option env=...' \"bounce\" symbols. "
                                   "For compatibility with the C tools, "
                                   "rename {} to {} (so that the symbol name "
                                   "matches the environment variable name)."
                                   .format(node.item.name, env_var),
                                   self.filename, self.linenr)

                elif self._check_token(_T_DEFCONFIG_LIST):
                    if not self.defconfig_list:
                        self.defconfig_list = node.item
                    else:
                        self._warn("'option defconfig_list' set on multiple "
                                   "symbols ({0} and {1}). Only {0} will be "
                                   "used.".format(self.defconfig_list.name,
                                                  node.item.name),
                                   self.filename, self.linenr)

                elif self._check_token(_T_MODULES):
                    
                    
                    
                    
                    "MODULES".
                    if node.item is not self.modules:
                        self._warn("the 'modules' option is not supported. "
                                   "Let me know if this is a problem for you, "
                                   "as it wouldn't be that hard to implement. "
                                   "Note that modules are supported -- "
                                   "Kconfiglib just assumes the symbol name "
                                   "MODULES, like older versions of the C "
                                   "implementation did when 'option modules' "
                                   "wasn't used.",
                                   self.filename, self.linenr)

                elif self._check_token(_T_ALLNOCONFIG_Y):
                    if node.item.__class__ is not Symbol:
                        self._parse_error("the 'allnoconfig_y' option is only "
                                          "valid for symbols")

                    node.item.is_allnoconfig_y = True

                else:
                    self._parse_error("unrecognized option")

            elif t0 is _T_OPTIONAL:
                if node.item.__class__ is not Choice:
                    self._parse_error('"optional" is only valid for choices')

                node.item.is_optional = True

            else:
                
                self._reuse_tokens = True
                return

    def _set_type(self, sc, new_type):
        

        
        if sc.orig_type and sc.orig_type is not new_type:
            self._warn("{} defined with multiple types, {} will be used"
                       .format(sc.name_and_loc, TYPE_TO_STR[new_type]))

        sc.orig_type = new_type

    def _parse_prompt(self, node):
        
        
        

        if node.prompt:
            self._warn(node.item.name_and_loc +
                       " defined with multiple prompts in single location")

        prompt = self._tokens[1]
        self._tokens_i = 2

        if prompt.__class__ is not str:
            self._parse_error("expected prompt string")

        if prompt != prompt.strip():
            self._warn(node.item.name_and_loc +
                       " has leading or trailing whitespace in its prompt")

            
            
            prompt = prompt.strip()

        node.prompt = (prompt, self._parse_cond())

    def _parse_help(self, node):
        if node.help is not None:
            self._warn(node.item.name_and_loc + " defined with more than "
                       "one help text -- only the last one will be used")

        
        readline = self._readline

        
        

        while 1:
            line = readline()
            self.linenr += 1
            if not line:
                self._empty_help(node, line)
                return
            if not line.isspace():
                break

        len_ = len  

        
        
        
        expline = line.expandtabs()
        indent = len_(expline) - len_(expline.lstrip())
        if not indent:
            self._empty_help(node, line)
            return

        
        

        
        lines = [expline[indent:]]
        add_line = lines.append  

        while 1:
            line = readline()
            if line.isspace():
                
                add_line("\n")
            elif not line:
                
                break
            else:
                expline = line.expandtabs()
                if len_(expline) - len_(expline.lstrip()) < indent:
                    break
                add_line(expline[indent:])

        self.linenr += len_(lines)
        node.help = "".join(lines).rstrip()
        if line:
            self._line_after_help(line)

    def _empty_help(self, node, line):
        self._warn(node.item.name_and_loc +
                   " has 'help' but empty help text")
        node.help = ""
        if line:
            self._line_after_help(line)

    def _parse_expr(self, transform_m):
        
        
        
        
        
        
        

        
        
        
        
        
        
        
        
        
        
        

        
        
        
        
        
        
        
        
        
        
        

        and_expr = self._parse_and_expr(transform_m)

        "single-operand" OR.
        
        
        return and_expr if not self._check_token(_T_OR) else \
            (OR, and_expr, self._parse_expr(transform_m))

    def _parse_and_expr(self, transform_m):
        factor = self._parse_factor(transform_m)

        "single-operand" AND.
        
        
        return factor if not self._check_token(_T_AND) else \
            (AND, factor, self._parse_and_expr(transform_m))

    def _parse_factor(self, transform_m):
        token = self._tokens[self._tokens_i]
        self._tokens_i += 1

        if token.__class__ is Symbol:
            

            if self._tokens[self._tokens_i] not in _RELATIONS:
                

                
                
                if transform_m and token is self.m:
                    return (AND, self.m, self.modules)

                return token

            
            
            
            
            self._tokens_i += 1
            return (self._tokens[self._tokens_i - 1], token,
                    self._expect_sym())

        if token is _T_NOT:
            
            return (token, self._parse_factor(transform_m))

        if token is _T_OPEN_PAREN:
            expr_parse = self._parse_expr(transform_m)
            if self._check_token(_T_CLOSE_PAREN):
                return expr_parse

        self._parse_error("malformed expression")

    
    
    

    def _build_dep(self):
        
        
        
        
        
        
        

        depend_on = _depend_on  

        
        
        
        for sym in self.unique_defined_syms:
            

            
            for node in sym.nodes:
                if node.prompt:
                    depend_on(sym, node.prompt[1])

            
            for value, cond in sym.defaults:
                depend_on(sym, value)
                depend_on(sym, cond)

            
            depend_on(sym, sym.rev_dep)
            depend_on(sym, sym.weak_rev_dep)

            
            for low, high, cond in sym.ranges:
                depend_on(sym, low)
                depend_on(sym, high)
                depend_on(sym, cond)

            
            
            
            
            
            depend_on(sym, sym.direct_dep)

            
            
            
            

        for choice in self.unique_choices:
            

            
            for node in choice.nodes:
                if node.prompt:
                    depend_on(choice, node.prompt[1])

            
            for _, cond in choice.defaults:
                depend_on(choice, cond)

    def _add_choice_deps(self):
        
        
        
        
        
        
        
        

        for choice in self.unique_choices:
            for sym in choice.syms:
                sym._dependents.add(choice)

    def _invalidate_all(self):
        
        
        
        for sym in self.unique_defined_syms:
            sym._invalidate()

        for choice in self.unique_choices:
            choice._invalidate()

    
    
    
    

    def _finalize_node(self, node, visible_if):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        if node.item.__class__ is Symbol:
            
            self._add_props_to_sym(node)

            
            
            cur = node
            while cur.next and _auto_menu_dep(node, cur.next):
                
                
                self._finalize_node(cur.next, visible_if)
                cur = cur.next
                cur.parent = node

            if cur is not node:
                
                
                node.list = node.next
                node.next = cur.next
                cur.next = None

        elif node.list:
            

            if node.item is MENU:
                visible_if = self._make_and(visible_if, node.visibility)

            
            
            
            
            self._propagate_deps(node, visible_if)

            
            cur = node.list
            while cur:
                self._finalize_node(cur, visible_if)
                cur = cur.next

        if node.list:
            
            "level" in the menu tree.
            _flatten(node.list)
            _remove_ifs(node)

        
        
        if node.item.__class__ is Choice:
            
            
            choice = node.item
            choice.direct_dep = self._make_or(choice.direct_dep, node.dep)
            choice.defaults += node.defaults

            _finalize_choice(node)

    def _propagate_deps(self, node, visible_if):
        

        
        
        
        
        
        
        
        basedep = node.item if node.item.__class__ is Choice else node.dep

        cur = node.list
        while cur:
            dep = cur.dep = self._make_and(cur.dep, basedep)

            if cur.item.__class__ in _SYMBOL_CHOICE:
                
                if cur.prompt:
                    cur.prompt = (cur.prompt[0],
                                  self._make_and(
                                      cur.prompt[1],
                                      self._make_and(visible_if, dep)))

                
                if cur.defaults:
                    cur.defaults = [(default, self._make_and(cond, dep))
                                    for default, cond in cur.defaults]

                
                if cur.ranges:
                    cur.ranges = [(low, high, self._make_and(cond, dep))
                                  for low, high, cond in cur.ranges]

                
                if cur.selects:
                    cur.selects = [(target, self._make_and(cond, dep))
                                   for target, cond in cur.selects]

                
                if cur.implies:
                    cur.implies = [(target, self._make_and(cond, dep))
                                   for target, cond in cur.implies]

            elif cur.prompt:  
                
                
                cur.prompt = (cur.prompt[0],
                              self._make_and(cur.prompt[1], dep))

            cur = cur.next

    def _add_props_to_sym(self, node):
        
        
        
        
        
        
        
        

        sym = node.item

        
        sym.direct_dep = self._make_or(sym.direct_dep, node.dep)

        sym.defaults += node.defaults
        sym.ranges += node.ranges
        sym.selects += node.selects
        sym.implies += node.implies

        
        for target, cond in node.selects:
            target.rev_dep = self._make_or(
                target.rev_dep,
                self._make_and(sym, cond))

        
        
        for target, cond in node.implies:
            target.weak_rev_dep = self._make_or(
                target.weak_rev_dep,
                self._make_and(sym, cond))

    
    
    

    def _check_sym_sanity(self):
        
        

        def num_ok(sym, type_):
            
            

            
            "123"
            if not sym.nodes:
                return _is_base_n(sym.name, _TYPE_TO_BASE[type_])

            return sym.orig_type is type_

        for sym in self.unique_defined_syms:
            if sym.orig_type in _BOOL_TRISTATE:
                
                

                for target_sym, _ in sym.selects:
                    if target_sym.orig_type not in _BOOL_TRISTATE_UNKNOWN:
                        self._warn("{} selects the {} symbol {}, which is not "
                                   "bool or tristate"
                                   .format(sym.name_and_loc,
                                           TYPE_TO_STR[target_sym.orig_type],
                                           target_sym.name_and_loc))

                for target_sym, _ in sym.implies:
                    if target_sym.orig_type not in _BOOL_TRISTATE_UNKNOWN:
                        self._warn("{} implies the {} symbol {}, which is not "
                                   "bool or tristate"
                                   .format(sym.name_and_loc,
                                           TYPE_TO_STR[target_sym.orig_type],
                                           target_sym.name_and_loc))

            elif sym.orig_type:  
                for default, _ in sym.defaults:
                    if default.__class__ is not Symbol:
                        raise KconfigError(
                            "the {} symbol {} has a malformed default {} -- "
                            "expected a single symbol"
                            .format(TYPE_TO_STR[sym.orig_type],
                                    sym.name_and_loc, expr_str(default)))

                    if sym.orig_type is STRING:
                        if not default.is_constant and not default.nodes and \
                           not default.name.isupper():
                            
                            
                            
                            
                            self._warn("style: quotes recommended around "
                                       "default value for string symbol "
                                       + sym.name_and_loc)

                    elif not num_ok(default, sym.orig_type):  
                        self._warn("the {0} symbol {1} has a non-{0} default {2}"
                                   .format(TYPE_TO_STR[sym.orig_type],
                                           sym.name_and_loc,
                                           default.name_and_loc))

                if sym.selects or sym.implies:
                    self._warn("the {} symbol {} has selects or implies"
                               .format(TYPE_TO_STR[sym.orig_type],
                                       sym.name_and_loc))

            else:  
                self._warn("{} defined without a type"
                           .format(sym.name_and_loc))


            if sym.ranges:
                if sym.orig_type not in _INT_HEX:
                    self._warn(
                        "the {} symbol {} has ranges, but is not int or hex"
                        .format(TYPE_TO_STR[sym.orig_type],
                                sym.name_and_loc))
                else:
                    for low, high, _ in sym.ranges:
                        if not num_ok(low, sym.orig_type) or \
                           not num_ok(high, sym.orig_type):

                            self._warn("the {0} symbol {1} has a non-{0} "
                                       "range [{2}, {3}]"
                                       .format(TYPE_TO_STR[sym.orig_type],
                                               sym.name_and_loc,
                                               low.name_and_loc,
                                               high.name_and_loc))

    def _check_choice_sanity(self):
        
        

        def warn_select_imply(sym, expr, expr_type):
            msg = "the choice symbol {} is {} by the following symbols, but " \
                  "select/imply has no effect on choice symbols" \
                  .format(sym.name_and_loc, expr_type)

            
            for si in split_expr(expr, OR):
                msg += "\n - " + split_expr(si, AND)[0].name_and_loc

            self._warn(msg)

        for choice in self.unique_choices:
            if choice.orig_type not in _BOOL_TRISTATE:
                self._warn("{} defined with type {}"
                           .format(choice.name_and_loc,
                                   TYPE_TO_STR[choice.orig_type]))

            for node in choice.nodes:
                if node.prompt:
                    break
            else:
                self._warn(choice.name_and_loc + " defined without a prompt")

            for default, _ in choice.defaults:
                if default.__class__ is not Symbol:
                    raise KconfigError(
                        "{} has a malformed default {}"
                        .format(choice.name_and_loc, expr_str(default)))

                if default.choice is not choice:
                    self._warn("the default selection {} of {} is not "
                               "contained in the choice"
                               .format(default.name_and_loc,
                                       choice.name_and_loc))

            for sym in choice.syms:
                if sym.defaults:
                    self._warn("default on the choice symbol {} will have "
                               "no effect, as defaults do not affect choice "
                               "symbols".format(sym.name_and_loc))

                if sym.rev_dep is not sym.kconfig.n:
                    warn_select_imply(sym, sym.rev_dep, "selected")

                if sym.weak_rev_dep is not sym.kconfig.n:
                    warn_select_imply(sym, sym.weak_rev_dep, "implied")

                for node in sym.nodes:
                    if node.parent.item is choice:
                        if not node.prompt:
                            self._warn("the choice symbol {} has no prompt"
                                       .format(sym.name_and_loc))

                    elif node.prompt:
                        self._warn("the choice symbol {} is defined with a "
                                   "prompt outside the choice"
                                   .format(sym.name_and_loc))

    def _parse_error(self, msg):
        raise KconfigError("{}error: couldn't parse '{}': {}".format(
            "" if self.filename is None else
                "{}:{}: ".format(self.filename, self.linenr),
            self._line.strip(), msg))

    def _trailing_tokens_error(self):
        self._parse_error("extra tokens at end of line")

    def _open(self, filename, mode):
        
        
        
        
        
        
        "U" flag would currently work for both Python 2 and 3, but it's
        
        
        
        
        
        
        
        
        "rU"):
        
        
        
        
        
        
        
        
        
        
        
        "r" and
        "rU" for parsing performance on Python 2.
        
        
        
        
        return open(filename, "rU" if mode == "r" else mode) if _IS_PY2 else \
               open(filename, mode, encoding=self._encoding)

    def _check_undef_syms(self):
        
        

        def is_num(s):
            
            
            
            
            
            
            
            

            try:
                int(s)
            except ValueError:
                if not s.startswith(("0x", "0X")):
                    return False

                try:
                    int(s, 16)
                except ValueError:
                    return False

            return True

        for sym in (self.syms.viewvalues if _IS_PY2 else self.syms.values)():
            
            
            
            
            
            
            
            if not sym.nodes and not is_num(sym.name) and \
               sym.name != "MODULES":

                msg = "undefined symbol {}:".format(sym.name)
                for node in self.node_iter():
                    if sym in node.referenced:
                        msg += "\n\n- Referenced at {}:{}:\n\n{}" \
                               .format(node.filename, node.linenr, node)
                self._warn(msg)

    def _warn(self, msg, filename=None, linenr=None):
        

        if not self.warn:
            return

        msg = "warning: " + msg
        if filename is not None:
            msg = "{}:{}: {}".format(filename, linenr, msg)

        self.warnings.append(msg)
        if self.warn_to_stderr:
            sys.stderr.write(msg + "\n")


class Symbol(object):
    """
    Represents a configuration symbol:

      (menu)config FOO
          ...

    The following attributes are available. They should be viewed as read-only,
    and some are implemented through @property magic (but are still efficient
    to access due to internal caching).

    Note: Prompts, help texts, and locations are stored in the Symbol's
    MenuNode(s) rather than in the Symbol itself. Check the MenuNode class and
    the Symbol.nodes attribute. This organization matches the C tools.

    name:
      The name of the symbol, e.g. "FOO" for 'config FOO'.

    type:
      The type of the symbol. One of BOOL, TRISTATE, STRING, INT, HEX, UNKNOWN.
      UNKNOWN is for undefined symbols, (non-special) constant symbols, and
      symbols defined without a type.

      When running without modules (MODULES having the value n), TRISTATE
      symbols magically change type to BOOL. This also happens for symbols
      within choices in "y" mode. This matches the C tools, and makes sense for
      menuconfig-like functionality.

    orig_type:
      The type as given in the Kconfig file, without any magic applied. Used
      when printing the symbol.

    tri_value:
      The tristate value of the symbol as an integer. One of 0, 1, 2,
      representing n, m, y. Always 0 (n) for non-bool/tristate symbols.

      This is the symbol value that's used outside of relation expressions
      (A, !A, A && B, A || B).

    str_value:
      The value of the symbol as a string. Gives the value for string/int/hex
      symbols. For bool/tristate symbols, gives "n", "m", or "y".

      This is the symbol value that's used in relational expressions
      (A = B, A != B, etc.)

      Gotcha: For int/hex symbols, the exact format of the value is often
      preserved (e.g. when writing a .config file), hence why you can't get it
      directly as an int. Do int(int_sym.str_value) or
      int(hex_sym.str_value, 16) to get the integer value.

    user_value:
      The user value of the symbol. None if no user value has been assigned
      (via Kconfig.load_config() or Symbol.set_value()).

      Holds 0, 1, or 2 for bool/tristate symbols, and a string for the other
      symbol types.

      WARNING: Do not assign directly to this. It will break things. Use
      Symbol.set_value().

    assignable:
      A tuple containing the tristate user values that can currently be
      assigned to the symbol (that would be respected), ordered from lowest (0,
      representing n) to highest (2, representing y). This corresponds to the
      selections available in the menuconfig interface. The set of assignable
      values is calculated from the symbol's visibility and selects/implies.

      Returns the empty set for non-bool/tristate symbols and for symbols with
      visibility n. The other possible values are (0, 2), (0, 1, 2), (1, 2),
      (1,), and (2,). A (1,) or (2,) result means the symbol is visible but
      "locked" to m or y through a select, perhaps in combination with the
      visibility. menuconfig represents this as -M- and -*-, respectively.

      For string/hex/int symbols, check if Symbol.visibility is non-0 (non-n)
      instead to determine if the value can be changed.

      Some handy 'assignable' idioms:

        
        if sym.assignable:
            
            
            sym_high = sym.assignable[-1]

            
            sym_low = sym.assignable[0]

            
            if sym.assignable[-1] >= 1:
                ...

        
        if 1 in sym.assignable:
            ...

    visibility:
      The visibility of the symbol. One of 0, 1, 2, representing n, m, y. See
      the module documentation for an overview of symbol values and visibility.

    config_string:
      The .config assignment string that would get written out for the symbol
      by Kconfig.write_config(). Returns the empty string if no .config
      assignment would get written out.

      In general, visible symbols, symbols with (active) defaults, and selected
      symbols get written out. This includes all non-n-valued bool/tristate
      symbols, and all visible string/int/hex symbols.

      Symbols with the (no longer needed) 'option env=...' option generate no
      configuration output, and neither does the special
      'option defconfig_list' symbol.

      Tip: This field is useful when generating custom configuration output,
      even for non-.config-like formats. To write just the symbols that would
      get written out to .config files, do this:

        if sym.config_string:
            *Write symbol, e.g. by looking sym.str_value*

      This is a superset of the symbols written out by write_autoconf().
      That function skips all n-valued symbols.

      There usually won't be any great harm in just writing all symbols either,
      though you might get some special symbols and possibly some "redundant"
      n-valued symbol entries in there.

    name_and_loc:
      Holds a string like

        "MY_SYMBOL (defined at foo/Kconfig:12, bar/Kconfig:14)"

      , giving the name of the symbol and its definition location(s).

      If the symbol is undefined, the location is given as "(undefined)".

    nodes:
      A list of MenuNodes for this symbol. Will contain a single MenuNode for
      most symbols. Undefined and constant symbols have an empty nodes list.
      Symbols defined in multiple locations get one node for each location.

    choice:
      Holds the parent Choice for choice symbols, and None for non-choice
      symbols. Doubles as a flag for whether a symbol is a choice symbol.

    defaults:
      List of (default, cond) tuples for the symbol's 'default' properties. For
      example, 'default A && B if C || D' is represented as
      ((AND, A, B), (OR, C, D)). If no condition was given, 'cond' is
      self.kconfig.y.

      Note that 'depends on' and parent dependencies are propagated to
      'default' conditions.

    selects:
      List of (symbol, cond) tuples for the symbol's 'select' properties. For
      example, 'select A if B && C' is represented as (A, (AND, B, C)). If no
      condition was given, 'cond' is self.kconfig.y.

      Note that 'depends on' and parent dependencies are propagated to 'select'
      conditions.

    implies:
      Like 'selects', for imply.

    ranges:
      List of (low, high, cond) tuples for the symbol's 'range' properties. For
      example, 'range 1 2 if A' is represented as (1, 2, A). If there is no
      condition, 'cond' is self.kconfig.y.

      Note that 'depends on' and parent dependencies are propagated to 'range'
      conditions.

      Gotcha: 1 and 2 above will be represented as (undefined) Symbols rather
      than plain integers. Undefined symbols get their name as their string
      value, so this works out. The C tools work the same way.

    orig_defaults:
    orig_selects:
    orig_implies:
    orig_ranges:
      See the corresponding attributes on the MenuNode class.

    rev_dep:
      Reverse dependency expression from other symbols selecting this symbol.
      Multiple selections get ORed together. A condition on a select is ANDed
      with the selecting symbol.

      For example, if A has 'select FOO' and B has 'select FOO if C', then
      FOO's rev_dep will be (OR, A, (AND, B, C)).

    weak_rev_dep:
      Like rev_dep, for imply.

    direct_dep:
      The direct ('depends on') dependencies for the symbol, or self.kconfig.y
      if there are no direct dependencies.

      This attribute includes any dependencies from surrounding menus and ifs.
      Those get propagated to the direct dependencies, and the resulting direct
      dependencies in turn get propagated to the conditions of all properties.

      If the symbol is defined in multiple locations, the dependencies from the
      different locations get ORed together.

    referenced:
      A set() with all symbols and choices referenced in the properties and
      property conditions of the symbol.

      Also includes dependencies from surrounding menus and ifs, because those
      get propagated to the symbol (see the 'Intro to symbol values' section in
      the module docstring).

      Choices appear in the dependencies of choice symbols.

      For the following definitions, only B and not C appears in A's
      'referenced'. To get transitive references, you'll have to recursively
      expand 'references' until no new items appear.

        config A
                bool
                depends on B

        config B
                bool
                depends on C

        config C
                bool

      See the Symbol.direct_dep attribute if you're only interested in the
      direct dependencies of the symbol (its 'depends on'). You can extract the
      symbols in it with the global expr_items() function.

    env_var:
      If the Symbol has an 'option env="FOO"' option, this contains the name
      ("FOO") of the environment variable. None for symbols without no
      'option env'.

      'option env="FOO"' acts like a 'default' property whose value is the
      value of $FOO.

      Symbols with 'option env' are never written out to .config files, even if
      they are visible. env_var corresponds to a flag called SYMBOL_AUTO in the
      C implementation.

    is_allnoconfig_y:
      True if the symbol has 'option allnoconfig_y' set on it. This has no
      effect internally (except when printing symbols), but can be checked by
      scripts.

    is_constant:
      True if the symbol is a constant (quoted) symbol.

    kconfig:
      The Kconfig instance this symbol is from.
    """
    __slots__ = (
        "_cached_assignable",
        "_cached_str_val",
        "_cached_tri_val",
        "_cached_vis",
        "_dependents",
        "_old_val",
        "_visited",
        "_was_set",
        "_write_to_conf",
        "choice",
        "defaults",
        "direct_dep",
        "env_var",
        "implies",
        "is_allnoconfig_y",
        "is_constant",
        "kconfig",
        "name",
        "nodes",
        "orig_type",
        "ranges",
        "rev_dep",
        "selects",
        "user_value",
        "weak_rev_dep",
    )

    
    
    

    @property
    def type(self):
        """
        See the class documentation.
        """
        if self.orig_type is TRISTATE and \
           (self.choice and self.choice.tri_value == 2 or
            not self.kconfig.modules.tri_value):

            return BOOL

        return self.orig_type

    @property
    def str_value(self):
        """
        See the class documentation.
        """
        if self._cached_str_val is not None:
            return self._cached_str_val

        if self.orig_type in _BOOL_TRISTATE:
            
            self._cached_str_val = TRI_TO_STR[self.tri_value]
            return self._cached_str_val

        
        "FOO = bar" work for seeing if
        "bar".
        if not self.orig_type:  
            self._cached_str_val = self.name
            return self.name

        val = ""
        
        
        vis = self.visibility

        self._write_to_conf = (vis != 0)

        if self.orig_type in _INT_HEX:
            
            
            
            

            base = _TYPE_TO_BASE[self.orig_type]

            
            for low_expr, high_expr, cond in self.ranges:
                if expr_value(cond):
                    has_active_range = True

                    
                    
                    low = int(low_expr.str_value, base) if \
                      _is_base_n(low_expr.str_value, base) else 0
                    high = int(high_expr.str_value, base) if \
                      _is_base_n(high_expr.str_value, base) else 0

                    break
            else:
                has_active_range = False

            
            
            use_defaults = True

            if vis and self.user_value:
                user_val = int(self.user_value, base)
                if has_active_range and not low <= user_val <= high:
                    num2str = str if base == 10 else hex
                    self.kconfig._warn(
                        "user value {} on the {} symbol {} ignored due to "
                        "being outside the active range ([{}, {}]) -- falling "
                        "back on defaults"
                        .format(num2str(user_val), TYPE_TO_STR[self.orig_type],
                                self.name_and_loc,
                                num2str(low), num2str(high)))
                else:
                    
                    
                    "0x", etc.)
                    val = self.user_value
                    use_defaults = False

            if use_defaults:
                

                
                has_default = False

                for sym, cond in self.defaults:
                    if expr_value(cond):
                        has_default = self._write_to_conf = True

                        val = sym.str_value

                        if _is_base_n(val, base):
                            val_num = int(val, base)
                        else:
                            val_num = 0  

                        break
                else:
                    val_num = 0  

                
                if has_active_range:
                    clamp = None
                    if val_num < low:
                        clamp = low
                    elif val_num > high:
                        clamp = high

                    if clamp is not None:
                        
                        
                        val = str(clamp) \
                              if self.orig_type is INT else \
                              hex(clamp)

                        if has_default:
                            num2str = str if base == 10 else hex
                            self.kconfig._warn(
                                "default value {} on {} clamped to {} due to "
                                "being outside the active range ([{}, {}])"
                                .format(val_num, self.name_and_loc,
                                        num2str(clamp), num2str(low),
                                        num2str(high)))

        elif self.orig_type is STRING:
            if vis and self.user_value is not None:
                
                val = self.user_value
            else:
                
                for sym, cond in self.defaults:
                    if expr_value(cond):
                        val = sym.str_value
                        self._write_to_conf = True
                        break

        
        
        
        
        
        if self.env_var is not None or self is self.kconfig.defconfig_list:
            self._write_to_conf = False

        self._cached_str_val = val
        return val

    @property
    def tri_value(self):
        """
        See the class documentation.
        """
        if self._cached_tri_val is not None:
            return self._cached_tri_val

        if self.orig_type not in _BOOL_TRISTATE:
            if self.orig_type:  
                
                self.kconfig._warn(
                    "The {} symbol {} is being evaluated in a logical context "
                    "somewhere. It will always evaluate to n."
                    .format(TYPE_TO_STR[self.orig_type], self.name_and_loc))

            self._cached_tri_val = 0
            return 0

        
        
        vis = self.visibility
        self._write_to_conf = (vis != 0)

        val = 0

        if not self.choice:
            

            if vis and self.user_value is not None:
                
                val = min(self.user_value, vis)

            else:
                
                

                for default, cond in self.defaults:
                    dep_val = expr_value(cond)
                    if dep_val:
                        val = min(expr_value(default), dep_val)
                        if val:
                            self._write_to_conf = True
                        break

                
                
                dep_val = expr_value(self.weak_rev_dep)
                if dep_val and expr_value(self.direct_dep):
                    val = max(dep_val, val)
                    self._write_to_conf = True

            
            dep_val = expr_value(self.rev_dep)
            if dep_val:
                if expr_value(self.direct_dep) < dep_val:
                    self._warn_select_unsatisfied_deps()

                val = max(dep_val, val)
                self._write_to_conf = True

            
            
            if val == 1 and \
               (self.type is BOOL or expr_value(self.weak_rev_dep) == 2):
                val = 2

        elif vis == 2:
            
            
            
            val = 2 if self.choice.selection is self else 0

        elif vis and self.user_value:
            
            val = 1

        self._cached_tri_val = val
        return val

    @property
    def assignable(self):
        """
        See the class documentation.
        """
        if self._cached_assignable is None:
            self._cached_assignable = self._assignable()
        return self._cached_assignable

    @property
    def visibility(self):
        """
        See the class documentation.
        """
        if self._cached_vis is None:
            self._cached_vis = _visibility(self)
        return self._cached_vis

    @property
    def config_string(self):
        """
        See the class documentation.
        """
        
        
        val = self.str_value
        if not self._write_to_conf:
            return ""

        if self.orig_type in _BOOL_TRISTATE:
            return "{}{}={}\n" \
                   .format(self.kconfig.config_prefix, self.name, val) \
                   if val != "n" else \
                   "" \
                   .format(self.kconfig.config_prefix, self.name)

        if self.orig_type in _INT_HEX:
            return "{}{}={}\n" \
                   .format(self.kconfig.config_prefix, self.name, val)

        
        return '{}{}="{}"\n' \
               .format(self.kconfig.config_prefix, self.name, escape(val))

    @property
    def name_and_loc(self):
        """
        See the class documentation.
        """
        return self.name + " " + _locs(self)

    def set_value(self, value):
        """
        Sets the user value of the symbol.

        Equal in effect to assigning the value to the symbol within a .config
        file. For bool and tristate symbols, use the 'assignable' attribute to
        check which values can currently be assigned. Setting values outside
        'assignable' will cause Symbol.user_value to differ from
        Symbol.str/tri_value (be truncated down or up).

        Setting a choice symbol to 2 (y) sets Choice.user_selection to the
        choice symbol in addition to setting Symbol.user_value.
        Choice.user_selection is considered when the choice is in y mode (the
        "normal" mode).

        Other symbols that depend (possibly indirectly) on this symbol are
        automatically recalculated to reflect the assigned value.

        value:
          The user value to give to the symbol. For bool and tristate symbols,
          n/m/y can be specified either as 0/1/2 (the usual format for tristate
          values in Kconfiglib) or as one of the strings "n", "m", or "y". For
          other symbol types, pass a string.

          Note that the value for an int/hex symbol is passed as a string, e.g.
          "123" or "0x0123". The format of this string is preserved in the
          output.

          Values that are invalid for the type (such as "foo" or 1 (m) for a
          BOOL or "0x123" for an INT) are ignored and won't be stored in
          Symbol.user_value. Kconfiglib will print a warning by default for
          invalid assignments, and set_value() will return False.

        Returns True if the value is valid for the type of the symbol, and
        False otherwise. This only looks at the form of the value. For BOOL and
        TRISTATE symbols, check the Symbol.assignable attribute to see what
        values are currently in range and would actually be reflected in the
        value of the symbol. For other symbol types, check whether the
        visibility is non-n.
        """
        if self.orig_type in _BOOL_TRISTATE and value in STR_TO_TRI:
            value = STR_TO_TRI[value]

        
        
        
        
        
        
        
        if value == self.user_value and not self.choice:
            self._was_set = True
            return True

        
        if not (self.orig_type is BOOL     and value in (2, 0)     or
                self.orig_type is TRISTATE and value in TRI_TO_STR or
                value.__class__ is str and
                (self.orig_type is STRING                        or
                 self.orig_type is INT and _is_base_n(value, 10) or
                 self.orig_type is HEX and _is_base_n(value, 16)
                                       and int(value, 16) >= 0)):

            
            self.kconfig._warn(
                "the value {} is invalid for {}, which has type {} -- "
                "assignment ignored"
                .format(TRI_TO_STR[value] if value in TRI_TO_STR else
                            "'{}'".format(value),
                        self.name_and_loc, TYPE_TO_STR[self.orig_type]))

            return False

        self.user_value = value
        self._was_set = True

        if self.choice and value == 2:
            
            
            
            
            self.choice.user_selection = self
            self.choice._was_set = True
            self.choice._rec_invalidate()
        else:
            self._rec_invalidate_if_has_prompt()

        return True

    def unset_value(self):
        """
        Removes any user value from the symbol, as if the symbol had never
        gotten a user value via Kconfig.load_config() or Symbol.set_value().
        """
        if self.user_value is not None:
            self.user_value = None
            self._rec_invalidate_if_has_prompt()

    @property
    def referenced(self):
        """
        See the class documentation.
        """
        return {item for node in self.nodes for item in node.referenced}

    @property
    def orig_defaults(self):
        """
        See the class documentation.
        """
        return [d for node in self.nodes for d in node.orig_defaults]

    @property
    def orig_selects(self):
        """
        See the class documentation.
        """
        return [s for node in self.nodes for s in node.orig_selects]

    @property
    def orig_implies(self):
        """
        See the class documentation.
        """
        return [i for node in self.nodes for i in node.orig_implies]

    @property
    def orig_ranges(self):
        """
        See the class documentation.
        """
        return [r for node in self.nodes for r in node.orig_ranges]

    def __repr__(self):
        """
        Returns a string with information about the symbol (including its name,
        value, visibility, and location(s)) when it is evaluated on e.g. the
        interactive Python prompt.
        """
        fields = ["symbol " + self.name, TYPE_TO_STR[self.type]]
        add = fields.append

        for node in self.nodes:
            if node.prompt:
                add('"{}"'.format(node.prompt[0]))

        
        add("value " + (self.str_value if self.orig_type in _BOOL_TRISTATE
                        else '"{}"'.format(self.str_value)))

        if not self.is_constant:
            

            if self.user_value is not None:
                
                add("user value " + (TRI_TO_STR[self.user_value]
                                     if self.orig_type in _BOOL_TRISTATE
                                     else '"{}"'.format(self.user_value)))

            add("visibility " + TRI_TO_STR[self.visibility])

            if self.choice:
                add("choice symbol")

            if self.is_allnoconfig_y:
                add("allnoconfig_y")

            if self is self.kconfig.defconfig_list:
                add("is the defconfig_list symbol")

            if self.env_var is not None:
                add("from environment variable " + self.env_var)

            if self is self.kconfig.modules:
                add("is the modules symbol")

            add("direct deps " + TRI_TO_STR[expr_value(self.direct_dep)])

        if self.nodes:
            for node in self.nodes:
                add("{}:{}".format(node.filename, node.linenr))
        else:
            add("constant" if self.is_constant else "undefined")

        return "<{}>".format(", ".join(fields))

    def __str__(self):
        """
        Returns a string representation of the symbol when it is printed.
        Matches the Kconfig format, with any parent dependencies propagated to
        the 'depends on' condition.

        The string is constructed by joining the strings returned by
        MenuNode.__str__() for each of the symbol's menu nodes, so symbols
        defined in multiple locations will return a string with all
        definitions.

        The returned string does not end in a newline. An empty string is
        returned for undefined and constant symbols.
        """
        return self.custom_str(standard_sc_expr_str)

    def custom_str(self, sc_expr_str_fn):
        """
        Works like Symbol.__str__(), but allows a custom format to be used for
        all symbol/choice references. See expr_str().
        """
        return "\n\n".join(node.custom_str(sc_expr_str_fn)
                           for node in self.nodes)

    
    
    

    def __init__(self):
        """
        Symbol constructor -- not intended to be called directly by Kconfiglib
        clients.
        """
        
        
        
        
        
        
        
        

        
        
        self.orig_type = self._visited = 0

        self.nodes = []

        self.defaults = []
        self.selects = []
        self.implies = []
        self.ranges = []

        self.user_value = \
        self.choice = \
        self.env_var = \
        self._cached_str_val = self._cached_tri_val = self._cached_vis = \
        self._cached_assignable = None

        
        

        self.is_allnoconfig_y = \
        self._was_set = \
        self._write_to_conf = False

        
        self._dependents = set()

    def _assignable(self):
        

        if self.orig_type not in _BOOL_TRISTATE:
            return ()

        
        
        vis = self.visibility
        if not vis:
            return ()

        rev_dep_val = expr_value(self.rev_dep)

        if vis == 2:
            if self.choice:
                return (2,)

            if not rev_dep_val:
                if self.type is BOOL or expr_value(self.weak_rev_dep) == 2:
                    return (0, 2)
                return (0, 1, 2)

            if rev_dep_val == 2:
                return (2,)

            

            if self.type is BOOL or expr_value(self.weak_rev_dep) == 2:
                return (2,)
            return (1, 2)

        

        

        if not rev_dep_val:
            return (0, 1) if expr_value(self.weak_rev_dep) != 2 else (0, 2)

        if rev_dep_val == 2:
            return (2,)

        

        return (1,)

    def _invalidate(self):
        

        self._cached_str_val = self._cached_tri_val = self._cached_vis = \
        self._cached_assignable = None

    def _rec_invalidate(self):
        

        if self is self.kconfig.modules:
            
            self.kconfig._invalidate_all()
        else:
            self._invalidate()

            for item in self._dependents:
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                if item._cached_vis is not None:
                    item._rec_invalidate()

    def _rec_invalidate_if_has_prompt(self):
        
        
        
        
        
        
        
        
        
        
        

        for node in self.nodes:
            if node.prompt:
                self._rec_invalidate()
                return

        if self.kconfig._warn_assign_no_prompt:
            self.kconfig._warn(self.name_and_loc + " has no prompt, meaning "
                               "user values have no effect on it")

    def _str_default(self):
        
        
        
        

        if self.orig_type in _BOOL_TRISTATE:
            val = 0

            
            if not self.choice:
                for default, cond in self.defaults:
                    cond_val = expr_value(cond)
                    if cond_val:
                        val = min(expr_value(default), cond_val)
                        break

                val = max(expr_value(self.rev_dep),
                          expr_value(self.weak_rev_dep),
                          val)

                
                
                if val == 1 and self.type is BOOL:
                    val = 2

            return TRI_TO_STR[val]

        if self.orig_type:  
            for default, cond in self.defaults:
                if expr_value(cond):
                    return default.str_value

        return ""

    def _warn_select_unsatisfied_deps(self):
        
        
        
        

        msg = "{} has direct dependencies {} with value {}, but is " \
              "currently being {}-selected by the following symbols:" \
              .format(self.name_and_loc, expr_str(self.direct_dep),
                      TRI_TO_STR[expr_value(self.direct_dep)],
                      TRI_TO_STR[expr_value(self.rev_dep)])

        
        for select in split_expr(self.rev_dep, OR):
            if expr_value(select) <= expr_value(self.direct_dep):
                
                continue

            
            
            
            
            selecting_sym = split_expr(select, AND)[0]

            msg += "\n - {}, with value {}, direct dependencies {} " \
                   "(value: {})" \
                   .format(selecting_sym.name_and_loc,
                           selecting_sym.str_value,
                           expr_str(selecting_sym.direct_dep),
                           TRI_TO_STR[expr_value(selecting_sym.direct_dep)])

            if select.__class__ is tuple:
                msg += ", and select condition {} (value: {})" \
                       .format(expr_str(select[2]),
                               TRI_TO_STR[expr_value(select[2])])

        self.kconfig._warn(msg)


class Choice(object):
    """
    Represents a choice statement:

      choice
          ...
      endchoice

    The following attributes are available on Choice instances. They should be
    treated as read-only, and some are implemented through @property magic (but
    are still efficient to access due to internal caching).

    Note: Prompts, help texts, and locations are stored in the Choice's
    MenuNode(s) rather than in the Choice itself. Check the MenuNode class and
    the Choice.nodes attribute. This organization matches the C tools.

    name:
      The name of the choice, e.g. "FOO" for 'choice FOO', or None if the
      Choice has no name.

    type:
      The type of the choice. One of BOOL, TRISTATE, UNKNOWN. UNKNOWN is for
      choices defined without a type where none of the contained symbols have a
      type either (otherwise the choice inherits the type of the first symbol
      defined with a type).

      When running without modules (CONFIG_MODULES=n), TRISTATE choices
      magically change type to BOOL. This matches the C tools, and makes sense
      for menuconfig-like functionality.

    orig_type:
      The type as given in the Kconfig file, without any magic applied. Used
      when printing the choice.

    tri_value:
      The tristate value (mode) of the choice. A choice can be in one of three
      modes:

        0 (n) - The choice is disabled and no symbols can be selected. For
                visible choices, this mode is only possible for choices with
                the 'optional' flag set (see kconfig-language.txt).

        1 (m) - Any number of choice symbols can be set to m, the rest will
                be n.

        2 (y) - One symbol will be y, the rest n.

      Only tristate choices can be in m mode. The visibility of the choice is
      an upper bound on the mode, and the mode in turn is an upper bound on the
      visibility of the choice symbols.

      To change the mode, use Choice.set_value().

      Implementation note:
        The C tools internally represent choices as a type of symbol, with
        special-casing in many code paths. This is why there is a lot of
        similarity to Symbol. The value (mode) of a choice is really just a
        normal symbol value, and an implicit reverse dependency forces its
        lower bound to m for visible non-optional choices (the reverse
        dependency is 'm && <visibility>').

        Symbols within choices get the choice propagated as a dependency to
        their properties. This turns the mode of the choice into an upper bound
        on e.g. the visibility of choice symbols, and explains the gotcha
        related to printing choice symbols mentioned in the module docstring.

        Kconfiglib uses a separate Choice class only because it makes the code
        and interface less confusing (especially in a user-facing interface).
        Corresponding attributes have the same name in the Symbol and Choice
        classes, for consistency and compatibility.

    str_value:
      Like choice.tri_value, but gives the value as one of the strings
      "n", "m", or "y"

    user_value:
      The value (mode) selected by the user through Choice.set_value(). Either
      0, 1, or 2, or None if the user hasn't selected a mode. See
      Symbol.user_value.

      WARNING: Do not assign directly to this. It will break things. Use
      Choice.set_value() instead.

    assignable:
      See the symbol class documentation. Gives the assignable values (modes).

    selection:
      The Symbol instance of the currently selected symbol. None if the Choice
      is not in y mode or has no selected symbol (due to unsatisfied
      dependencies on choice symbols).

      WARNING: Do not assign directly to this. It will break things. Call
      sym.set_value(2) on the choice symbol you want to select instead.

    user_selection:
      The symbol selected by the user (by setting it to y). Ignored if the
      choice is not in y mode, but still remembered so that the choice "snaps
      back" to the user selection if the mode is changed back to y. This might
      differ from 'selection' due to unsatisfied dependencies.

      WARNING: Do not assign directly to this. It will break things. Call
      sym.set_value(2) on the choice symbol to be selected instead.

    visibility:
      See the Symbol class documentation. Acts on the value (mode).

    name_and_loc:
      Holds a string like

        "<choice MY_CHOICE> (defined at foo/Kconfig:12)"

      , giving the name of the choice and its definition location(s). If the
      choice has no name (isn't defined with 'choice MY_CHOICE'), then it will
      be shown as "<choice>" before the list of locations (always a single one
      in that case).

    syms:
      List of symbols contained in the choice.

      Obscure gotcha: If a symbol depends on the previous symbol within a
      choice so that an implicit menu is created, it won't be a choice symbol,
      and won't be included in 'syms'.

    nodes:
      A list of MenuNodes for this choice. In practice, the list will probably
      always contain a single MenuNode, but it is possible to give a choice a
      name and define it in multiple locations.

    defaults:
      List of (symbol, cond) tuples for the choice's 'defaults' properties. For
      example, 'default A if B && C' is represented as (A, (AND, B, C)). If
      there is no condition, 'cond' is self.kconfig.y.

      Note that 'depends on' and parent dependencies are propagated to
      'default' conditions.

    orig_defaults:
      See the corresponding attribute on the MenuNode class.

    direct_dep:
      See Symbol.direct_dep.

    referenced:
      A set() with all symbols referenced in the properties and property
      conditions of the choice.

      Also includes dependencies from surrounding menus and ifs, because those
      get propagated to the choice (see the 'Intro to symbol values' section in
      the module docstring).

    is_optional:
      True if the choice has the 'optional' flag set on it and can be in
      n mode.

    kconfig:
      The Kconfig instance this choice is from.
    """
    __slots__ = (
        "_cached_assignable",
        "_cached_selection",
        "_cached_vis",
        "_dependents",
        "_visited",
        "_was_set",
        "defaults",
        "direct_dep",
        "is_constant",
        "is_optional",
        "kconfig",
        "name",
        "nodes",
        "orig_type",
        "syms",
        "user_selection",
        "user_value",
    )

    
    
    

    @property
    def type(self):
        """
        Returns the type of the choice. See Symbol.type.
        """
        if self.orig_type is TRISTATE and not self.kconfig.modules.tri_value:
            return BOOL
        return self.orig_type

    @property
    def str_value(self):
        """
        See the class documentation.
        """
        return TRI_TO_STR[self.tri_value]

    @property
    def tri_value(self):
        """
        See the class documentation.
        """
        
        

        val = 0 if self.is_optional else 1

        if self.user_value is not None:
            val = max(val, self.user_value)

        
        
        val = min(val, self.visibility)

        
        return 2 if val == 1 and self.type is BOOL else val

    @property
    def assignable(self):
        """
        See the class documentation.
        """
        if self._cached_assignable is None:
            self._cached_assignable = self._assignable()
        return self._cached_assignable

    @property
    def visibility(self):
        """
        See the class documentation.
        """
        if self._cached_vis is None:
            self._cached_vis = _visibility(self)
        return self._cached_vis

    @property
    def name_and_loc(self):
        """
        See the class documentation.
        """
        
        return standard_sc_expr_str(self) + " " + _locs(self)

    @property
    def selection(self):
        """
        See the class documentation.
        """
        if self._cached_selection is _NO_CACHED_SELECTION:
            self._cached_selection = self._selection()
        return self._cached_selection

    def set_value(self, value):
        """
        Sets the user value (mode) of the choice. Like for Symbol.set_value(),
        the visibility might truncate the value. Choices without the 'optional'
        attribute (is_optional) can never be in n mode, but 0/"n" is still
        accepted since it's not a malformed value (though it will have no
        effect).

        Returns True if the value is valid for the type of the choice, and
        False otherwise. This only looks at the form of the value. Check the
        Choice.assignable attribute to see what values are currently in range
        and would actually be reflected in the mode of the choice.
        """
        if value in STR_TO_TRI:
            value = STR_TO_TRI[value]

        if value == self.user_value:
            
            
            self._was_set = True
            return True

        if not (self.orig_type is BOOL     and value in (2, 0) or
                self.orig_type is TRISTATE and value in TRI_TO_STR):

            
            self.kconfig._warn(
                "the value {} is invalid for {}, which has type {} -- "
                "assignment ignored"
                .format(TRI_TO_STR[value] if value in TRI_TO_STR else
                            "'{}'".format(value),
                        self.name_and_loc, TYPE_TO_STR[self.orig_type]))

            return False

        self.user_value = value
        self._was_set = True
        self._rec_invalidate()

        return True

    def unset_value(self):
        """
        Resets the user value (mode) and user selection of the Choice, as if
        the user had never touched the mode or any of the choice symbols.
        """
        if self.user_value is not None or self.user_selection:
            self.user_value = self.user_selection = None
            self._rec_invalidate()

    @property
    def referenced(self):
        """
        See the class documentation.
        """
        return {item for node in self.nodes for item in node.referenced}

    @property
    def orig_defaults(self):
        """
        See the class documentation.
        """
        return [d for node in self.nodes for d in node.orig_defaults]

    def __repr__(self):
        """
        Returns a string with information about the choice when it is evaluated
        on e.g. the interactive Python prompt.
        """
        fields = ["choice " + self.name if self.name else "choice",
                  TYPE_TO_STR[self.type]]
        add = fields.append

        for node in self.nodes:
            if node.prompt:
                add('"{}"'.format(node.prompt[0]))

        add("mode " + self.str_value)

        if self.user_value is not None:
            add('user mode {}'.format(TRI_TO_STR[self.user_value]))

        if self.selection:
            add("{} selected".format(self.selection.name))

        if self.user_selection:
            user_sel_str = "{} selected by user" \
                           .format(self.user_selection.name)

            if self.selection is not self.user_selection:
                user_sel_str += " (overridden)"

            add(user_sel_str)

        add("visibility " + TRI_TO_STR[self.visibility])

        if self.is_optional:
            add("optional")

        for node in self.nodes:
            add("{}:{}".format(node.filename, node.linenr))

        return "<{}>".format(", ".join(fields))

    def __str__(self):
        """
        Returns a string representation of the choice when it is printed.
        Matches the Kconfig format (though without the contained choice
        symbols), with any parent dependencies propagated to the 'depends on'
        condition.

        The returned string does not end in a newline.

        See Symbol.__str__() as well.
        """
        return self.custom_str(standard_sc_expr_str)

    def custom_str(self, sc_expr_str_fn):
        """
        Works like Choice.__str__(), but allows a custom format to be used for
        all symbol/choice references. See expr_str().
        """
        return "\n\n".join(node.custom_str(sc_expr_str_fn)
                           for node in self.nodes)

    
    
    

    def __init__(self):
        """
        Choice constructor -- not intended to be called directly by Kconfiglib
        clients.
        """
        
        
        
        

        
        
        self.orig_type = self._visited = 0

        self.nodes = []

        self.syms = []
        self.defaults = []

        self.name = \
        self.user_value = self.user_selection = \
        self._cached_vis = self._cached_assignable = None

        self._cached_selection = _NO_CACHED_SELECTION

        
        
        self.is_constant = self.is_optional = False

        
        self._dependents = set()

    def _assignable(self):
        

        
        
        vis = self.visibility

        if not vis:
            return ()

        if vis == 2:
            if not self.is_optional:
                return (2,) if self.type is BOOL else (1, 2)
            return (0, 2) if self.type is BOOL else (0, 1, 2)

        

        return (0, 1) if self.is_optional else (1,)

    def _selection(self):
        

        
        
        if self.tri_value != 2:
            
            return None

        
        if self.user_selection and self.user_selection.visibility:
            return self.user_selection

        
        return self._selection_from_defaults()

    def _selection_from_defaults(self):
        
        for sym, cond in self.defaults:
            
            if expr_value(cond) and sym.visibility:
                return sym

        
        for sym in self.syms:
            if sym.visibility:
                return sym

        
        return None

    def _invalidate(self):
        self._cached_vis = self._cached_assignable = None
        self._cached_selection = _NO_CACHED_SELECTION

    def _rec_invalidate(self):
        

        self._invalidate()

        for item in self._dependents:
            if item._cached_vis is not None:
                item._rec_invalidate()


class MenuNode(object):
    """
    Represents a menu node in the configuration. This corresponds to an entry
    in e.g. the 'make menuconfig' interface, though non-visible choices, menus,
    and comments also get menu nodes. If a symbol or choice is defined in
    multiple locations, it gets one menu node for each location.

    The top-level menu node, corresponding to the implicit top-level menu, is
    available in Kconfig.top_node.

    The menu nodes for a Symbol or Choice can be found in the
    Symbol/Choice.nodes attribute. Menus and comments are represented as plain
    menu nodes, with their text stored in the prompt attribute (prompt[0]).
    This mirrors the C implementation.

    The following attributes are available on MenuNode instances. They should
    be viewed as read-only.

    item:
      Either a Symbol, a Choice, or one of the constants MENU and COMMENT.
      Menus and comments are represented as plain menu nodes. Ifs are collapsed
      (matching the C implementation) and do not appear in the final menu tree.

    next:
      The following menu node. None if there is no following node.

    list:
      The first child menu node. None if there are no children.

      Choices and menus naturally have children, but Symbols can also have
      children because of menus created automatically from dependencies (see
      kconfig-language.txt).

    parent:
      The parent menu node. None if there is no parent.

    prompt:
      A (string, cond) tuple with the prompt for the menu node and its
      conditional expression (which is self.kconfig.y if there is no
      condition). None if there is no prompt.

      For symbols and choices, the prompt is stored in the MenuNode rather than
      the Symbol or Choice instance. For menus and comments, the prompt holds
      the text.

    defaults:
      The 'default' properties for this particular menu node. See
      symbol.defaults.

      When evaluating defaults, you should use Symbol/Choice.defaults instead,
      as it include properties from all menu nodes (a symbol/choice can have
      multiple definition locations/menu nodes). MenuNode.defaults is meant for
      documentation generation.

    selects:
      Like MenuNode.defaults, for selects.

    implies:
      Like MenuNode.defaults, for implies.

    ranges:
      Like MenuNode.defaults, for ranges.

    orig_prompt:
    orig_defaults:
    orig_selects:
    orig_implies:
    orig_ranges:
      These work the like the corresponding attributes without orig_*, but omit
      any dependencies propagated from 'depends on' and surrounding 'if's (the
      direct dependencies, stored in MenuNode.dep).

      One use for this is generating less cluttered documentation, by only
      showing the direct dependencies in one place.

    help:
      The help text for the menu node for Symbols and Choices. None if there is
      no help text. Always stored in the node rather than the Symbol or Choice.
      It is possible to have a separate help text at each location if a symbol
      is defined in multiple locations.

      Trailing whitespace (including a final newline) is stripped from the help
      text. This was not the case before Kconfiglib 10.21.0, where the format
      was undocumented.

    dep:
      The direct ('depends on') dependencies for the menu node, or
      self.kconfig.y if there are no direct dependencies.

      This attribute includes any dependencies from surrounding menus and ifs.
      Those get propagated to the direct dependencies, and the resulting direct
      dependencies in turn get propagated to the conditions of all properties.

      If a symbol or choice is defined in multiple locations, only the
      properties defined at a particular location get the corresponding
      MenuNode.dep dependencies propagated to them.

    visibility:
      The 'visible if' dependencies for the menu node (which must represent a
      menu), or self.kconfig.y if there are no 'visible if' dependencies.
      'visible if' dependencies are recursively propagated to the prompts of
      symbols and choices within the menu.

    referenced:
      A set() with all symbols and choices referenced in the properties and
      property conditions of the menu node.

      Also includes dependencies inherited from surrounding menus and ifs.
      Choices appear in the dependencies of choice symbols.

    is_menuconfig:
      Set to True if the children of the menu node should be displayed in a
      separate menu. This is the case for the following items:

        - Menus (node.item == MENU)

        - Choices

        - Symbols defined with the 'menuconfig' keyword. The children come from
          implicitly created submenus, and should be displayed in a separate
          menu rather than being indented.

      'is_menuconfig' is just a hint on how to display the menu node. It's
      ignored internally by Kconfiglib, except when printing symbols.

    filename/linenr:
      The location where the menu node appears. The filename is relative to
      $srctree (or to the current directory if $srctree isn't set), except
      absolute paths are used for paths outside $srctree.

    include_path:
      A tuple of (filename, linenr) tuples, giving the locations of the
      'source' statements via which the Kconfig file containing this menu node
      was included. The first element is the location of the 'source' statement
      in the top-level Kconfig file passed to Kconfig.__init__(), etc.

      Note that the Kconfig file of the menu node itself isn't included. Check
      'filename' and 'linenr' for that.

    kconfig:
      The Kconfig instance the menu node is from.
    """
    __slots__ = (
        "dep",
        "filename",
        "help",
        "include_path",
        "is_menuconfig",
        "item",
        "kconfig",
        "linenr",
        "list",
        "next",
        "parent",
        "prompt",
        "visibility",

        
        "defaults",
        "selects",
        "implies",
        "ranges",
    )

    def __init__(self):
        
        
        
        self.defaults = []
        self.selects = []
        self.implies = []
        self.ranges = []

    @property
    def orig_prompt(self):
        """
        See the class documentation.
        """
        if not self.prompt:
            return None
        return (self.prompt[0], self._strip_dep(self.prompt[1]))

    @property
    def orig_defaults(self):
        """
        See the class documentation.
        """
        return [(default, self._strip_dep(cond))
                for default, cond in self.defaults]

    @property
    def orig_selects(self):
        """
        See the class documentation.
        """
        return [(select, self._strip_dep(cond))
                for select, cond in self.selects]

    @property
    def orig_implies(self):
        """
        See the class documentation.
        """
        return [(imply, self._strip_dep(cond))
                for imply, cond in self.implies]

    @property
    def orig_ranges(self):
        """
        See the class documentation.
        """
        return [(low, high, self._strip_dep(cond))
                for low, high, cond in self.ranges]

    @property
    def referenced(self):
        """
        See the class documentation.
        """
        
        
        res = expr_items(self.dep)

        if self.prompt:
            res |= expr_items(self.prompt[1])

        if self.item is MENU:
            res |= expr_items(self.visibility)

        for value, cond in self.defaults:
            res |= expr_items(value)
            res |= expr_items(cond)

        for value, cond in self.selects:
            res.add(value)
            res |= expr_items(cond)

        for value, cond in self.implies:
            res.add(value)
            res |= expr_items(cond)

        for low, high, cond in self.ranges:
            res.add(low)
            res.add(high)
            res |= expr_items(cond)

        return res

    def __repr__(self):
        """
        Returns a string with information about the menu node when it is
        evaluated on e.g. the interactive Python prompt.
        """
        fields = []
        add = fields.append

        if self.item.__class__ is Symbol:
            add("menu node for symbol " + self.item.name)

        elif self.item.__class__ is Choice:
            s = "menu node for choice"
            if self.item.name is not None:
                s += " " + self.item.name
            add(s)

        elif self.item is MENU:
            add("menu node for menu")

        else:  
            add("menu node for comment")

        if self.prompt:
            add('prompt "{}" (visibility {})'.format(
                self.prompt[0], TRI_TO_STR[expr_value(self.prompt[1])]))

        if self.item.__class__ is Symbol and self.is_menuconfig:
            add("is menuconfig")

        add("deps " + TRI_TO_STR[expr_value(self.dep)])

        if self.item is MENU:
            add("'visible if' deps " + TRI_TO_STR[expr_value(self.visibility)])

        if self.item.__class__ in _SYMBOL_CHOICE and self.help is not None:
            add("has help")

        if self.list:
            add("has child")

        if self.next:
            add("has next")

        add("{}:{}".format(self.filename, self.linenr))

        return "<{}>".format(", ".join(fields))

    def __str__(self):
        """
        Returns a string representation of the menu node. Matches the Kconfig
        format, with any parent dependencies propagated to the 'depends on'
        condition.

        The output could (almost) be fed back into a Kconfig parser to redefine
        the object associated with the menu node. See the module documentation
        for a gotcha related to choice symbols.

        For symbols and choices with multiple menu nodes (multiple definition
        locations), properties that aren't associated with a particular menu
        node are shown on all menu nodes ('option env=...', 'optional' for
        choices, etc.).

        The returned string does not end in a newline.
        """
        return self.custom_str(standard_sc_expr_str)

    def custom_str(self, sc_expr_str_fn):
        """
        Works like MenuNode.__str__(), but allows a custom format to be used
        for all symbol/choice references. See expr_str().
        """
        return self._menu_comment_node_str(sc_expr_str_fn) \
               if self.item in _MENU_COMMENT else \
               self._sym_choice_node_str(sc_expr_str_fn)

    def _menu_comment_node_str(self, sc_expr_str_fn):
        s = '{} "{}"'.format("menu" if self.item is MENU else "comment",
                             self.prompt[0])

        if self.dep is not self.kconfig.y:
            s += "\n\tdepends on {}".format(expr_str(self.dep, sc_expr_str_fn))

        if self.item is MENU and self.visibility is not self.kconfig.y:
            s += "\n\tvisible if {}".format(expr_str(self.visibility,
                                                     sc_expr_str_fn))

        return s

    def _sym_choice_node_str(self, sc_expr_str_fn):
        def indent_add(s):
            lines.append("\t" + s)

        def indent_add_cond(s, cond):
            if cond is not self.kconfig.y:
                s += " if " + expr_str(cond, sc_expr_str_fn)
            indent_add(s)

        sc = self.item

        if sc.__class__ is Symbol:
            lines = [("menuconfig " if self.is_menuconfig else "config ")
                     + sc.name]
        else:
            lines = ["choice " + sc.name if sc.name else "choice"]

        if sc.orig_type and not self.prompt:  
            "prompt"' shorthand
            
            indent_add(TYPE_TO_STR[sc.orig_type])

        if self.prompt:
            if sc.orig_type:
                prefix = TYPE_TO_STR[sc.orig_type]
            else:
                
                prefix = "prompt"

            indent_add_cond(prefix + ' "{}"'.format(escape(self.prompt[0])),
                            self.orig_prompt[1])

        if sc.__class__ is Symbol:
            if sc.is_allnoconfig_y:
                indent_add("option allnoconfig_y")

            if sc is sc.kconfig.defconfig_list:
                indent_add("option defconfig_list")

            if sc.env_var is not None:
                indent_add('option env="{}"'.format(sc.env_var))

            if sc is sc.kconfig.modules:
                indent_add("option modules")

            for low, high, cond in self.orig_ranges:
                indent_add_cond(
                    "range {} {}".format(sc_expr_str_fn(low),
                                         sc_expr_str_fn(high)),
                    cond)

        for default, cond in self.orig_defaults:
            indent_add_cond("default " + expr_str(default, sc_expr_str_fn),
                            cond)

        if sc.__class__ is Choice and sc.is_optional:
            indent_add("optional")

        if sc.__class__ is Symbol:
            for select, cond in self.orig_selects:
                indent_add_cond("select " + sc_expr_str_fn(select), cond)

            for imply, cond in self.orig_implies:
                indent_add_cond("imply " + sc_expr_str_fn(imply), cond)

        if self.dep is not sc.kconfig.y:
            indent_add("depends on " + expr_str(self.dep, sc_expr_str_fn))

        if self.help is not None:
            indent_add("help")
            for line in self.help.splitlines():
                indent_add("  " + line)

        return "\n".join(lines)

    def _strip_dep(self, expr):
        
        
        

        
        if self.dep is expr:
            return self.kconfig.y

        
        if expr.__class__ is tuple and expr[0] is AND and expr[2] is self.dep:
            return expr[1]

        return expr


class Variable(object):
    """
    Represents a preprocessor variable/function.

    The following attributes are available:

    name:
      The name of the variable.

    value:
      The unexpanded value of the variable.

    expanded_value:
      The expanded value of the variable. For simple variables (those defined
      with :=), this will equal 'value'. Accessing this property will raise a
      KconfigError if the expansion seems to be stuck in a loop.

      Accessing this field is the same as calling expanded_value_w_args() with
      no arguments. I hadn't considered function arguments when adding it. It
      is retained for backwards compatibility though.

    is_recursive:
      True if the variable is recursive (defined with =).
    """
    __slots__ = (
        "_n_expansions",
        "is_recursive",
        "kconfig",
        "name",
        "value",
    )

    @property
    def expanded_value(self):
        """
        See the class documentation.
        """
        return self.expanded_value_w_args()

    def expanded_value_w_args(self, *args):
        """
        Returns the expanded value of the variable/function. Any arguments
        passed will be substituted for $(1), $(2), etc.

        Raises a KconfigError if the expansion seems to be stuck in a loop.
        """
        return self.kconfig._fn_val((self.name,) + args)

    def __repr__(self):
        return "<variable {}, {}, value '{}'>" \
               .format(self.name,
                       "recursive" if self.is_recursive else "immediate",
                       self.value)


class KconfigError(Exception):
    """
    Exception raised for Kconfig-related errors.

    KconfigError and KconfigSyntaxError are the same class. The
    KconfigSyntaxError alias is only maintained for backwards compatibility.
    """

KconfigSyntaxError = KconfigError  


class InternalError(Exception):
    "Never raised. Kept around for backwards compatibility."





"[Errno <errno>] <strerror>", ignoring any custom message passed to the


class _KconfigIOError(IOError):
    def __init__(self, ioerror, msg):
        self.msg = msg
        super(_KconfigIOError, self).__init__(
            ioerror.errno, ioerror.strerror, ioerror.filename)

    def __str__(self):
        return self.msg







def expr_value(expr):
    """
    Evaluates the expression 'expr' to a tristate value. Returns 0 (n), 1 (m),
    or 2 (y).

    'expr' must be an already-parsed expression from a Symbol, Choice, or
    MenuNode property. To evaluate an expression represented as a string, use
    Kconfig.eval_string().

    Passing subexpressions of expressions to this function works as expected.
    """
    if expr.__class__ is not tuple:
        return expr.tri_value

    if expr[0] is AND:
        v1 = expr_value(expr[1])
        
        
        return 0 if not v1 else min(v1, expr_value(expr[2]))

    if expr[0] is OR:
        v1 = expr_value(expr[1])
        
        return 2 if v1 == 2 else max(v1, expr_value(expr[2]))

    if expr[0] is NOT:
        return 2 - expr_value(expr[1])

    
    
    
    
    

    rel, v1, v2 = expr

    
    if v1.orig_type is STRING and v2.orig_type is STRING:
        
        comp = _strcmp(v1.str_value, v2.str_value)
    else:
        
        try:
            comp = _sym_to_num(v1) - _sym_to_num(v2)
        except ValueError:
            
            
            comp = _strcmp(v1.str_value, v2.str_value)

    return 2*(comp == 0 if rel is EQUAL else
              comp != 0 if rel is UNEQUAL else
              comp <  0 if rel is LESS else
              comp <= 0 if rel is LESS_EQUAL else
              comp >  0 if rel is GREATER else
              comp >= 0)


def standard_sc_expr_str(sc):
    """
    Standard symbol/choice printing function. Uses plain Kconfig syntax, and
    displays choices as <choice> (or <choice NAME>, for named choices).

    See expr_str().
    """
    if sc.__class__ is Symbol:
        if sc.is_constant and sc.name not in STR_TO_TRI:
            return '"{}"'.format(escape(sc.name))
        return sc.name

    return "<choice {}>".format(sc.name) if sc.name else "<choice>"


def expr_str(expr, sc_expr_str_fn=standard_sc_expr_str):
    """
    Returns the string representation of the expression 'expr', as in a Kconfig
    file.

    Passing subexpressions of expressions to this function works as expected.

    sc_expr_str_fn (default: standard_sc_expr_str):
      This function is called for every symbol/choice (hence "sc") appearing in
      the expression, with the symbol/choice as the argument. It is expected to
      return a string to be used for the symbol/choice.

      This can be used e.g. to turn symbols/choices into links when generating
      documentation, or for printing the value of each symbol/choice after it.

      Note that quoted values are represented as constants symbols
      (Symbol.is_constant == True).
    """
    if expr.__class__ is not tuple:
        return sc_expr_str_fn(expr)

    if expr[0] is AND:
        return "{} && {}".format(_parenthesize(expr[1], OR, sc_expr_str_fn),
                                 _parenthesize(expr[2], OR, sc_expr_str_fn))

    if expr[0] is OR:
        "(A && B) || (C && D)", which is
        
        return "{} || {}".format(_parenthesize(expr[1], AND, sc_expr_str_fn),
                                 _parenthesize(expr[2], AND, sc_expr_str_fn))

    if expr[0] is NOT:
        if expr[1].__class__ is tuple:
            return "!({})".format(expr_str(expr[1], sc_expr_str_fn))
        return "!" + sc_expr_str_fn(expr[1])  

    
    
    
    
    return "{} {} {}".format(sc_expr_str_fn(expr[1]), REL_TO_STR[expr[0]],
                             sc_expr_str_fn(expr[2]))


def expr_items(expr):
    """
    Returns a set() of all items (symbols and choices) that appear in the
    expression 'expr'.

    Passing subexpressions of expressions to this function works as expected.
    """
    res = set()

    def rec(subexpr):
        if subexpr.__class__ is tuple:
            

            rec(subexpr[1])

            
            if subexpr[0] is not NOT:
                rec(subexpr[2])

        else:
            
            res.add(subexpr)

    rec(expr)
    return res


def split_expr(expr, op):
    """
    Returns a list containing the top-level AND or OR operands in the
    expression 'expr', in the same (left-to-right) order as they appear in
    the expression.

    This can be handy e.g. for splitting (weak) reverse dependencies
    from 'select' and 'imply' into individual selects/implies.

    op:
      Either AND to get AND operands, or OR to get OR operands.

      (Having this as an operand might be more future-safe than having two
      hardcoded functions.)


    Pseudo-code examples:

      split_expr( A                    , OR  )  ->  [A]
      split_expr( A && B               , OR  )  ->  [A && B]
      split_expr( A || B               , OR  )  ->  [A, B]
      split_expr( A || B               , AND )  ->  [A || B]
      split_expr( A || B || (C && D)   , OR  )  ->  [A, B, C && D]

      
      split_expr( A || (B && (C || D)) , OR )  ->  [A, B && (C || D)]

      
      
      split_expr( (A || B) || C        , OR )  ->  [A, B, C]
      split_expr( A || (B || C)        , OR )  ->  [A, B, C]
    """
    res = []

    def rec(subexpr):
        if subexpr.__class__ is tuple and subexpr[0] is op:
            rec(subexpr[1])
            rec(subexpr[2])
        else:
            res.append(subexpr)

    rec(expr)
    return res


def escape(s):
    r"""
    Escapes the string 's' in the same fashion as is done for display in
    Kconfig format and when writing strings to a .config file. " and \ are
    replaced by \" and \\, respectively.
    """
    " to avoid double escaping
    return s.replace("\\", r"\\").replace('"', r'\"')


def unescape(s):
    r"""
    Unescapes the string 's'. \ followed by any character is replaced with just
    that character. Used internally when reading .config files.
    """
    return _unescape_sub(r"\1", s)


_unescape_sub = re.compile(r"\\(.)").sub


def standard_kconfig(description=None):
    """
    Argument parsing helper for tools that take a single optional Kconfig file
    argument (default: Kconfig). Returns the Kconfig instance for the parsed
    configuration. Uses argparse internally.

    Exits with sys.exit() (which raises SystemExit) on errors.

    description (default: None):
      The 'description' passed to argparse.ArgumentParser().
      argparse.RawDescriptionHelpFormatter is used, so formatting is preserved.
    """
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description)

    parser.add_argument(
        "kconfig",
        metavar="KCONFIG",
        default="Kconfig",
        nargs="?",
        help="Top-level Kconfig file (default: Kconfig)")

    return Kconfig(parser.parse_args().kconfig, suppress_traceback=True)


def standard_config_filename():
    """
    Helper for tools. Returns the value of KCONFIG_CONFIG (which specifies the
    .config file to load/save) if it is set, and ".config" otherwise.

    Calling load_config() with filename=None might give the behavior you want,
    without having to use this function.
    """
    return os.getenv("KCONFIG_CONFIG", ".config")


def load_allconfig(kconf, filename):
    """
    Use Kconfig.load_allconfig() instead, which was added in Kconfiglib 13.4.0.
    Supported for backwards compatibility. Might be removed at some point after
    a long period of deprecation warnings.
    """
    allconfig = os.getenv("KCONFIG_ALLCONFIG")
    if allconfig is None:
        return

    def std_msg(e):
        "Upcasts" a _KconfigIOError to an IOError, removing the custom
        
        
        
        
        
        return IOError(e.errno, e.strerror, e.filename)

    old_warn_assign_override = kconf.warn_assign_override
    old_warn_assign_redun = kconf.warn_assign_redun
    kconf.warn_assign_override = kconf.warn_assign_redun = False

    if allconfig in ("", "1"):
        try:
            print(kconf.load_config(filename, False))
        except EnvironmentError as e1:
            try:
                print(kconf.load_config("all.config", False))
            except EnvironmentError as e2:
                sys.exit("error: KCONFIG_ALLCONFIG is set, but neither {} "
                         "nor all.config could be opened: {}, {}"
                         .format(filename, std_msg(e1), std_msg(e2)))
    else:
        try:
            print(kconf.load_config(allconfig, False))
        except EnvironmentError as e:
            sys.exit("error: KCONFIG_ALLCONFIG is set to '{}', which "
                     "could not be opened: {}"
                     .format(allconfig, std_msg(e)))

    kconf.warn_assign_override = old_warn_assign_override
    kconf.warn_assign_redun = old_warn_assign_redun







def _visibility(sc):
    "visibility" that acts as an upper bound on
    
    
    

    vis = 0

    for node in sc.nodes:
        if node.prompt:
            vis = max(vis, expr_value(node.prompt[1]))

    if sc.__class__ is Symbol and sc.choice:
        if sc.choice.orig_type is TRISTATE and \
           sc.orig_type is not TRISTATE and sc.choice.tri_value != 2:
            
            return 0

        if sc.orig_type is TRISTATE and vis == 1 and sc.choice.tri_value == 2:
            
            return 0

    
    
    if vis == 1 and sc.type is not TRISTATE:
        return 2

    return vis


def _depend_on(sc, expr):
    "dependee" to all symbols in 'expr'.
    
    

    if expr.__class__ is tuple:
        

        _depend_on(sc, expr[1])

        
        if expr[0] is not NOT:
            _depend_on(sc, expr[2])

    elif not expr.is_constant:
        
        expr._dependents.add(sc)


def _parenthesize(expr, type_, sc_expr_str_fn):
    

    if expr.__class__ is tuple and expr[0] is type_:
        return "({})".format(expr_str(expr, sc_expr_str_fn))
    return expr_str(expr, sc_expr_str_fn)


def _ordered_unique(lst):
    
    
    

    seen = set()
    seen_add = seen.add
    return [x for x in lst if x not in seen and not seen_add(x)]


def _is_base_n(s, n):
    try:
        int(s, n)
        return True
    except ValueError:
        return False


def _strcmp(s1, s2):
    

    return (s1 > s2) - (s1 < s2)


def _sym_to_num(sym):
    
    

    
    "kconfig: fix relational operators for bool and tristate symbols") in
    
    return sym.tri_value if sym.orig_type in _BOOL_TRISTATE else \
           int(sym.str_value, _TYPE_TO_BASE[sym.orig_type])


def _touch_dep_file(path, sym_name):
    
    

    sym_path = path + os.sep + sym_name.lower().replace("_", os.sep) + ".h"
    sym_path_dir = dirname(sym_path)
    if not exists(sym_path_dir):
        os.makedirs(sym_path_dir, 0o755)

    
    os.close(os.open(
        sym_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644))


def _save_old(path):
    

    def copy(src, dst):
        
        import shutil
        shutil.copyfile(src, dst)

    if islink(path):
        
        copy_fn = copy
    elif hasattr(os, "replace"):
        
        
        copy_fn = os.replace
    elif os.name == "posix":
        
        copy_fn = os.rename
    else:
        
        copy_fn = copy

    try:
        copy_fn(path, path + ".old")
    except Exception:
        
        
        
        
        pass


def _locs(sc):
    "(defined at ...)" part of
    

    if sc.nodes:
        return "(defined at {})".format(
            ", ".join("{0.filename}:{0.linenr}".format(node)
                      for node in sc.nodes))

    return "(undefined)"





def _expr_depends_on(expr, sym):
    
    
    

    if expr.__class__ is not tuple:
        return expr is sym

    if expr[0] in _EQUAL_UNEQUAL:
        
        

        left, right = expr[1:]

        if right is sym:
            left, right = right, left
        elif left is not sym:
            return False

        return (expr[0] is EQUAL and right is sym.kconfig.m or
                                     right is sym.kconfig.y) or \
               (expr[0] is UNEQUAL and right is sym.kconfig.n)

    return expr[0] is AND and \
           (_expr_depends_on(expr[1], sym) or
            _expr_depends_on(expr[2], sym))


def _auto_menu_dep(node1, node2):
    "automatic menu dependency" on node1. If
    
    

    return _expr_depends_on(node2.prompt[1] if node2.prompt else node2.dep,
                            node1.item)


def _flatten(node):
    "Flattens" menu nodes without prompts (e.g. 'if' nodes and non-visible
    
    
    "jumps" in the indentation.
    
    "legitimately" if a
    
    
    

    while node:
        if node.list and not node.prompt and \
           node.item.__class__ is not Choice:

            last_node = node.list
            while 1:
                last_node.parent = node.parent
                if not last_node.next:
                    break
                last_node = last_node.next

            last_node.next = node.next
            node.next = node.list
            node.list = None

        node = node.next


def _remove_ifs(node):
    
    
    
    

    cur = node.list
    while cur and not cur.item:
        cur = cur.next

    node.list = cur

    while cur:
        next = cur.next
        while next and not next.item:
            next = next.next

        
        
        
        
        
        
        cur.next = cur = next


def _finalize_choice(node):
    
    
    

    choice = node.item

    cur = node.list
    while cur:
        if cur.item.__class__ is Symbol:
            cur.item.choice = choice
            choice.syms.append(cur.item)
        cur = cur.next

    
    
    if not choice.orig_type:
        for item in choice.syms:
            if item.orig_type:
                choice.orig_type = item.orig_type
                break

    
    for sym in choice.syms:
        if not sym.orig_type:
            sym.orig_type = choice.orig_type


def _check_dep_loop_sym(sym, ignore_choice):
    
    
    
    
    
    
    
    
    "visited, potentially part of a dependency loop". The recursive
    
    
    
    
    "on the way back") until X is seen
    
    
    
    
    "visited, not part of a dependency
    ".
    
    
    
    
    
    "entered" via a choice symbol
    
    
    
    
    

    if not sym._visited:
        

        sym._visited = 1

        for dep in sym._dependents:
            
            
            
            
            
            
            loop = _check_dep_loop_choice(dep, None) \
                   if dep.__class__ is Choice \
                   else _check_dep_loop_sym(dep, False)

            if loop:
                
                return _found_dep_loop(loop, sym)

        if sym.choice and not ignore_choice:
            loop = _check_dep_loop_choice(sym.choice, sym)
            if loop:
                
                return _found_dep_loop(loop, sym)

        
        sym._visited = 2

        
        return None

    if sym._visited == 2:
        
        
        return None

    
    
    return (sym,)


def _check_dep_loop_choice(choice, skip):
    if not choice._visited:
        

        choice._visited = 1

        
        
        
        for sym in choice.syms:
            if sym is not skip:
                
                "is a choice symbol" path by passing True
                loop = _check_dep_loop_sym(sym, True)
                if loop:
                    
                    return _found_dep_loop(loop, choice)

        
        choice._visited = 2

        
        return None

    if choice._visited == 2:
        
        
        return None

    
    
    return (choice,)


def _found_dep_loop(loop, cur):
    "on the way back" when we know we have a loop

    
    if cur is not loop[0]:
        
        return loop + (cur,)

    

    msg = "\nDependency loop\n" \
            "===============\n\n"

    for item in loop:
        if item is not loop[0]:
            msg += "...depends on "
            if item.__class__ is Symbol and item.choice:
                msg += "the choice symbol "

        msg += "{}, with definition...\n\n{}\n\n" \
               .format(item.name_and_loc, item)

        
        
        
        
        
        "disappear". For example,
        
        
        
        
        
        

        if item.__class__ is Symbol:
            if item.rev_dep is not item.kconfig.n:
                msg += "(select-related dependencies: {})\n\n" \
                       .format(expr_str(item.rev_dep))

            if item.weak_rev_dep is not item.kconfig.n:
                msg += "(imply-related dependencies: {})\n\n" \
                       .format(expr_str(item.rev_dep))

    msg += "...depends again on " + loop[0].name_and_loc

    raise KconfigError(msg)


def _decoding_error(e, filename, macro_linenr=None):
    
    
    
    
    
    

    raise KconfigError(
        "\n"
        "Malformed {} in {}\n"
        "Context: {}\n"
        "Problematic data: {}\n"
        "Reason: {}".format(
            e.encoding,
            "'{}'".format(filename) if macro_linenr is None else
                "output from macro at {}:{}".format(filename, macro_linenr),
            e.object[max(e.start - 40, 0):e.end + 40],
            e.object[e.start:e.end],
            e.reason))


def _warn_verbose_deprecated(fn_name):
    sys.stderr.write(
        "Deprecation warning: {0}()'s 'verbose' argument has no effect. Since "
        "Kconfiglib 12.0.0, the message is returned from {0}() instead, "
        "and is always generated. Do e.g. print(kconf.{0}()) if you want to "
        "want to show a message like \"Loaded configuration '.config'\" on "
        "stdout. The old API required ugly hacks to reuse messages in "
        "configuration interfaces.\n".format(fn_name))





def _filename_fn(kconf, _):
    return kconf.filename


def _lineno_fn(kconf, _):
    return str(kconf.linenr)


def _info_fn(kconf, _, msg):
    print("{}:{}: {}".format(kconf.filename, kconf.linenr, msg))

    return ""


def _warning_if_fn(kconf, _, cond, msg):
    if cond == "y":
        kconf._warn(msg, kconf.filename, kconf.linenr)

    return ""


def _error_if_fn(kconf, _, cond, msg):
    if cond == "y":
        raise KconfigError("{}:{}: {}".format(
            kconf.filename, kconf.linenr, msg))

    return ""


def _shell_fn(kconf, _, command):
    import subprocess  

    stdout, stderr = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()

    if not _IS_PY2:
        try:
            stdout = stdout.decode(kconf._encoding)
            stderr = stderr.decode(kconf._encoding)
        except UnicodeDecodeError as e:
            _decoding_error(e, kconf.filename, kconf.linenr)

    if stderr:
        kconf._warn("'{}' wrote to stderr: {}".format(
                        command, "\n".join(stderr.splitlines())),
                    kconf.filename, kconf.linenr)

    
    
    
    
    
    
    
    return "\n".join(stdout.splitlines()).rstrip("\n").replace("\n", " ")





TRI_TO_STR = {
    0: "n",
    1: "m",
    2: "y",
}

STR_TO_TRI = {
    "n": 0,
    "m": 1,
    "y": 2,
}




_NO_CACHED_SELECTION = 0


_IS_PY2 = sys.version_info[0] < 3

try:
    _UNAME_RELEASE = os.uname()[2]
except AttributeError:
    
    import platform
    _UNAME_RELEASE = platform.uname()[2]












(
    _T_ALLNOCONFIG_Y,
    _T_AND,
    _T_BOOL,
    _T_CHOICE,
    _T_CLOSE_PAREN,
    _T_COMMENT,
    _T_CONFIG,
    _T_DEFAULT,
    _T_DEFCONFIG_LIST,
    _T_DEF_BOOL,
    _T_DEF_HEX,
    _T_DEF_INT,
    _T_DEF_STRING,
    _T_DEF_TRISTATE,
    _T_DEPENDS,
    _T_ENDCHOICE,
    _T_ENDIF,
    _T_ENDMENU,
    _T_ENV,
    _T_EQUAL,
    _T_GREATER,
    _T_GREATER_EQUAL,
    _T_HELP,
    _T_HEX,
    _T_IF,
    _T_IMPLY,
    _T_INT,
    _T_LESS,
    _T_LESS_EQUAL,
    _T_MAINMENU,
    _T_MENU,
    _T_MENUCONFIG,
    _T_MODULES,
    _T_NOT,
    _T_ON,
    _T_OPEN_PAREN,
    _T_OPTION,
    _T_OPTIONAL,
    _T_OR,
    _T_ORSOURCE,
    _T_OSOURCE,
    _T_PROMPT,
    _T_RANGE,
    _T_RSOURCE,
    _T_SELECT,
    _T_SOURCE,
    _T_STRING,
    _T_TRISTATE,
    _T_UNEQUAL,
    _T_VISIBLE,
) = range(1, 51)



_get_keyword = {
    "---help---":     _T_HELP,
    "allnoconfig_y":  _T_ALLNOCONFIG_Y,
    "bool":           _T_BOOL,
    "boolean":        _T_BOOL,
    "choice":         _T_CHOICE,
    "comment":        _T_COMMENT,
    "config":         _T_CONFIG,
    "def_bool":       _T_DEF_BOOL,
    "def_hex":        _T_DEF_HEX,
    "def_int":        _T_DEF_INT,
    "def_string":     _T_DEF_STRING,
    "def_tristate":   _T_DEF_TRISTATE,
    "default":        _T_DEFAULT,
    "defconfig_list": _T_DEFCONFIG_LIST,
    "depends":        _T_DEPENDS,
    "endchoice":      _T_ENDCHOICE,
    "endif":          _T_ENDIF,
    "endmenu":        _T_ENDMENU,
    "env":            _T_ENV,
    "grsource":       _T_ORSOURCE,  
    "gsource":        _T_OSOURCE,   
    "help":           _T_HELP,
    "hex":            _T_HEX,
    "if":             _T_IF,
    "imply":          _T_IMPLY,
    "int":            _T_INT,
    "mainmenu":       _T_MAINMENU,
    "menu":           _T_MENU,
    "menuconfig":     _T_MENUCONFIG,
    "modules":        _T_MODULES,
    "on":             _T_ON,
    "option":         _T_OPTION,
    "optional":       _T_OPTIONAL,
    "orsource":       _T_ORSOURCE,
    "osource":        _T_OSOURCE,
    "prompt":         _T_PROMPT,
    "range":          _T_RANGE,
    "rsource":        _T_RSOURCE,
    "select":         _T_SELECT,
    "source":         _T_SOURCE,
    "string":         _T_STRING,
    "tristate":       _T_TRISTATE,
    "visible":        _T_VISIBLE,
}.get





MENU    = _T_MENU
COMMENT = _T_COMMENT


AND           = _T_AND
OR            = _T_OR
NOT           = _T_NOT
EQUAL         = _T_EQUAL
UNEQUAL       = _T_UNEQUAL
LESS          = _T_LESS
LESS_EQUAL    = _T_LESS_EQUAL
GREATER       = _T_GREATER
GREATER_EQUAL = _T_GREATER_EQUAL

REL_TO_STR = {
    EQUAL:         "=",
    UNEQUAL:       "!=",
    LESS:          "<",
    LESS_EQUAL:    "<=",
    GREATER:       ">",
    GREATER_EQUAL: ">=",
}




UNKNOWN  = 0
BOOL     = _T_BOOL
TRISTATE = _T_TRISTATE
STRING   = _T_STRING
INT      = _T_INT
HEX      = _T_HEX

TYPE_TO_STR = {
    UNKNOWN:  "unknown",
    BOOL:     "bool",
    TRISTATE: "tristate",
    STRING:   "string",
    INT:      "int",
    HEX:      "hex",
}



_TYPE_TO_BASE = {
    HEX:      16,
    INT:      10,
    STRING:   0,
    UNKNOWN:  0,
}


_DEF_TOKEN_TO_TYPE = {
    _T_DEF_BOOL:     BOOL,
    _T_DEF_HEX:      HEX,
    _T_DEF_INT:      INT,
    _T_DEF_STRING:   STRING,
    _T_DEF_TRISTATE: TRISTATE,
}





"missing quotes") are also treated as strings after


_STRING_LEX = frozenset({
    _T_BOOL,
    _T_CHOICE,
    _T_COMMENT,
    _T_HEX,
    _T_INT,
    _T_MAINMENU,
    _T_MENU,
    _T_ORSOURCE,
    _T_OSOURCE,
    _T_PROMPT,
    _T_RSOURCE,
    _T_SOURCE,
    _T_STRING,
    _T_TRISTATE,
})




_TYPE_TOKENS = frozenset({
    _T_BOOL,
    _T_TRISTATE,
    _T_INT,
    _T_HEX,
    _T_STRING,
})

_SOURCE_TOKENS = frozenset({
    _T_SOURCE,
    _T_RSOURCE,
    _T_OSOURCE,
    _T_ORSOURCE,
})

_REL_SOURCE_TOKENS = frozenset({
    _T_RSOURCE,
    _T_ORSOURCE,
})


_OBL_SOURCE_TOKENS = frozenset({
    _T_SOURCE,
    _T_RSOURCE,
})

_BOOL_TRISTATE = frozenset({
    BOOL,
    TRISTATE,
})

_BOOL_TRISTATE_UNKNOWN = frozenset({
    BOOL,
    TRISTATE,
    UNKNOWN,
})

_INT_HEX = frozenset({
    INT,
    HEX,
})

_SYMBOL_CHOICE = frozenset({
    Symbol,
    Choice,
})

_MENU_COMMENT = frozenset({
    MENU,
    COMMENT,
})

_EQUAL_UNEQUAL = frozenset({
    EQUAL,
    UNEQUAL,
})

_RELATIONS = frozenset({
    EQUAL,
    UNEQUAL,
    LESS,
    LESS_EQUAL,
    GREATER,
    GREATER_EQUAL,
})







def _re_match(regex):
    return re.compile(regex, 0 if _IS_PY2 else re.ASCII).match


def _re_search(regex):
    return re.compile(regex, 0 if _IS_PY2 else re.ASCII).search












_command_match = _re_match(r"\s*([A-Za-z0-9_$-]+)\s*")



_id_keyword_match = _re_match(r"([A-Za-z0-9_$/.-]+)\s*")




_assignment_lhs_fragment_match = _re_match("[A-Za-z0-9_-]*")



_assignment_rhs_match = _re_match(r"\s*(=|:=|\+=)\s*(.*)")


_macro_special_search = _re_search(r"\(|\)|,|\$\(")


_string_special_search = _re_search(r'"|\'|\\|\$\(')



_name_special_search = _re_search(r'[^A-Za-z0-9_$/.-]|\$\(|$')



_conf_string_match = _re_match(r'"((?:[^\\"]|\\.)*)"')
