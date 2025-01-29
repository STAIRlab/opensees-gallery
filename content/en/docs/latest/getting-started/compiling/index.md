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
| LAPACK      | `liblapack-dev`      |
| BLAS        | `libblas-dev`        |
| Tcl\*       | `tcl-dev`            |

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


<!--

{{< table class="table-striped-columns w-auto" >}}
| Feature            | Azure blob storage | Netlify           |
|--------------------|--------------------|-------------------|
| Automation         | Custom action      | {{</* fas check */>}} |
| Custom domain name | Requires Azure CDN | {{</* fas check */>}} |
| CDN / Edge network | Requires Azure CDN | {{</* fas check */>}} |
| HTTP headers       | Requires Azure CDN | {{</* fas check */>}} |
{{< /table >}}


### Preparations

The repository root should include a file `netlify.toml`. If not, copy it from
the {{< link repository >}}Hinode main repository{{< /link >}}. The
configuration file contains the build settings that Netlify will pick up when
connecting to your repository. The panel below shows the default build
settings. The key command to observe is `npm run build`, which ensures the site
is built properly.

> [!NOTE]
> The default configuration provides basic security headers. Please review the [server configuration]({{% relref "modeling" %}}) for more details about the Content Security Policy. The cache settings are explained in more detail in the {{< link netlify_cache >}}Netlify blog{{< /link >}}.

{{< docs name="netlify" file="netlify.toml" show="true" >}}

The same file also configures several optional plugins. 

{{< docs name="plugins" file="netlify.toml" show="true" >}}

### Configure your site

Sign up for Netlify and configure your site in seven steps.

{{< carousel class="col-sm-12 col-lg-8 mx-auto" >}}
  {{< img src="img/netlify-step1.png" caption="Step 1. Sign up for Netlify" >}}
  {{< img src="img/netlify-step2.png" caption="Step 2. Sign in with your Git provider" >}}
  {{< img src="img/netlify-step3.png" caption="Step 3. Authenticate your sign in (2FA)" >}}
  {{< img src="img/netlify-step4.png" caption="Step 4. Add a new site" >}}
  {{< img src="img/netlify-step5.png" caption="Step 5. Connect to your Git provider" >}}
  {{< img src="img/netlify-step6.png" caption="Step 6. Import an existing project" >}}
  {{< img src="img/netlify-step7.png" caption="Step 7. Configure the build settings" >}}
{{< /carousel >}}

{{< accordion class="accordion-theme accordion-flush" >}}
  {{< accordion-item header="Step 1. Sign up for Netlify" >}}
    Go to {{</* link netlify >}}netlify.com{{< /link */>}} and click on the button `Sign up`. Select your preferred signup method next. This will likely be a hosted Git provider, although you also have the option to sign up with an email address. The next steps use GitHub, but other Git providers will follow a similar process.
  {{< /accordion-item >}}
  {{< accordion-item header="Step 2. Sign in with your Git provider" >}}
    Enter the credentials for your Git provider and click the button to sign in.
  {{< /accordion-item >}}
  {{< accordion-item header="Step 3. Authenticate your sign in (2FA)" >}}
    Assuming you have enabled two-factor authentication with your Git provider, authenticate the sign in next. This example uses the GitHub Mobile app.
  {{< /accordion-item >}}
  {{< accordion-item header="Step 4. Add a new site" >}}
    Click on the button `Add new site` to set up a new site with Netlify.
  {{< /accordion-item >}}
  {{< accordion-item header="Step 5. Connect to your Git provider" >}}
    Connect to your Git provider to import your existing Hinode repository.
  {{< /accordion-item >}}
  {{< accordion-item header="Step 6. Import an existing project" >}}
    Pick a repository from your Git provider. Ensure Netlify has access to the correct repository.
  {{< /accordion-item >}}
  {{< accordion-item header="Step 7. Configure the build settings" >}}
    Review the basic build settings. Netlify will use the settings provided in the [preparations]({{% relref "#preparations-1" %}}). Click on the button `Deploy site` to start the build and deployment process.
  {{< /accordion-item >}}
{{< /accordion >}}

Your site is now ready to be used. Click on the domain settings of your site within the `Site overview` page to provide a domain alias and to edit the site name as needed. The same section also allows the configuration of a custom domain. Be sure to review your [server configuration]({{% relref "modeling" %}}) if you encounter any rendering issues, such as broken links or garbled stylesheets.

-->

