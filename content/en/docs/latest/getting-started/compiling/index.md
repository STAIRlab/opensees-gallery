---
title: Compiling
description: Compiling your own version of OpenSees.
date: 2024-08-14
aliases:
  - "/docs/getting-started/compiling/"
  - "/docs/compiling/"
  - "/compiling/"
layout: docs
---

## Dependencies

Compiling OpenSees requires the following software to be installed on your local machine:

The primary system dependencies required for compiling are LAPACK/BLAS and Tcl.
Packages providing these libraries are listed below for various package
management ecosystems.

> [!NOTE]
> When building in an Anaconda environment, you should install 
> **all** dependencies with `conda` or `mamba`, and preferably from the
> `conda-forge` channel. Expand the notes on Anaconda below.



{{< accordion class="accordion-theme accordion-flush" >}}
  {{< accordion-item header="Anaconda (Mac, Windows, Linux)" >}}

When using conda, you need to ensure that CMake only finds 
compilers that are compatible with the libraries in the
environment. <b>System compilers (like those installed
by the operating system's package manager) often cannot be used
and can lead to segfaults.</b>
The following command should install everything you need:

``` shell
conda install -c conda-forge fortran-compiler cxx-compiler c-compiler openblas openmpi
```

  {{< /accordion-item >}}
  {{< accordion-item header="APT (Ubuntu, Debian Linux)" >}}

| Dependency  | Package              |
|:------------|:---------------------|
| BLAS        | `libopenblas-dev`    |
| Tcl\*       | `tcl-dev`            |
| Compilers   | `build-essential`    |

  {{< /accordion-item >}}


  {{< accordion-item header="Pacman (Arch, Manjaro Linux)" >}}

| Dependency  | Package       |
|:------------|:--------------|
| LAPACK      | `lapack`      |
| BLAS        | `blas`        |
| Tcl\*       | `tcl`         |

  {{< /accordion-item >}}
  {{< accordion-item header="Yum (CentOS, Redhat Linux)" >}}

| Dependency | Package        |
|------------|----------------|
| LAPACK     | `lapack-devel` |
| Tcl\*      | `tcl-devel`    |


  {{< /accordion-item >}}
{{< /accordion >}}



## Prerequisites


1. Clone the package repository:

   {{< command >}}
   git clone https://github.com/claudioperez/OpenSeesRT
   {{< /command >}}

2. install *run-time* dependencies. These are the libraries that will be needed 
   in order to use OpenSees. To install these, run:

   {{< command >}}
   python -m pip install opensees
   {{< /command >}}


2. Install *compile-time* dependencies; see **Dependencies** below. These dependencies are only
   needed for the compilinf process.

{{< button collapse="collapse-1" outline=true color="secondary" icon="fab windows" order="first" size="sm" class="mb-4" >}}
    Windows installation notes
{{< /button >}}

{{< collapse id="collapse-1" class="p-3 border rounded mt-n4" >}}
On Windows you should additionally install Intel compilers and Conan
{{< /collapse >}}



## Compiling

The next steps describe how to set up your compilers and build the OpenSees library.


<!-- markdownlint-disable MD005 MD029 MD037 -->
{{< nav type="tabs" id="pills-1" >}}
  {{< nav-item header="Unix" show="true" >}}

1. **Create a directory to hold build artifacts**

    {{</* command */>}}
    mkdir build
    {{</* /command */>}}

2. **Configure the system for your system**

    {{</* command */>}}
    cd build
    cmake ..
    {{</* /command */>}}

3. **Start compiling**

    {{</* command */>}}
    cmake --build . --target OpenSees -j8
    {{</* /command */>}}

4. When `libOpenSeesRT.so` is compiled locally, the `opensees` 
   package needs to be told where to find it. This can be done by setting
   an environment variable with the name `OPENSEESRT_LIB` to point to
   the location of `libOpenSeesRT.so` in the build tree.
   To this end, you may want to add a line like the following to your shell
   startup script (e.g., `.bashrc`):
   ```bash
   export OPENSEESRT_LIB="/path/to/your/compiled/libOpenSeesRT.so"
   ```

  {{< /nav-item >}}
  {{< nav-item header="Conan" >}}

1. **Create a directory to hold build artifacts**

    {{</* command */>}}
    mkdir build
    {{</* /command */>}}

2. **Run Conan**

    {{</* command */>}}
    cd build
    conan install .. --build missing
    {{</* /command */>}}

3. **Configure the system for your system**

    {{</* command */>}}
    cmake ..
    {{</* /command */>}}

4. **Start compiling**

    {{</* command */>}}
    cmake --build . --target OpenSees -j8
    {{</* /command */>}}

5. When `libOpenSeesRT.so` is compiled locally, the `opensees` 
   package needs to be told where to find it. This can be done by setting
   an environment variable with the name `OPENSEESRT_LIB` to point to
   the location of `libOpenSeesRT.so` in the build tree.
   To this end, you may want to add a line like the following to your shell
   startup script (e.g., `.bashrc`):
   {{</* command */>}}
   export OPENSEESRT_LIB="/path/to/your/compiled/libOpenSeesRT.so"
   {{</* /command */>}}
  {{< /nav-item >}}
{{< /nav >}}
<!-- markdownlint-enable MD005 MD029 -->


Check that everything was built properly by running the following command:
```shell
python -m opensees
```
This should start an OpenSees interpreter which can be closed by running
the `exit` command.

--------------------------------------------




