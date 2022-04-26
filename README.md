PTXdist IDE Integration
=======================

When an IDE is used to develop an application for a PTXdist BSP then the
IDE must be configured correctly. PTXdist can export the necessary
information with `ptxdist full-bsp-report`. The tools here use that to
generate IDE specific configuration files.

Visual Studio Code
------------------

For vscode there is a simple script that uses jinja templating to generate
configuration files. Multiple template directories can be stacked to allow
project specific customizations without copying the full template
directory. The script converts all files found in the template directories
and writes a corresponding output file with the same name. There are two
special cases:

 - All hidden files (starting with ".") are ignored. They can be used for
   includes etc.
 - If a filename ends with ".sh" then the generated file will be
   executable.

The default template provides the following features:

 - A CMake kit that uses the BSP to build with the correct compiler etc.
 - Debug configuration to run the application with gdbserver on the DUT and
   attach to it with the correct cross gdb.

Usage:

```sh
$ ./vscode/generate.py --report /path/to/the/BSP/platform-foo/release/full-bsp-report.yaml \
    /path/to/the/application/.vscode/
```

or with a custom template:

```sh
$ ./vscode/generate.py --report /path/to/the/BSP/platform-foo/release/full-bsp-report.yaml \
    --template /my/custom/template/ vscode/templates/default/ \
    /path/to/the/application/.vscode/
```
