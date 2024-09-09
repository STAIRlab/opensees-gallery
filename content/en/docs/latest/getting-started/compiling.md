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

Hinode is a clean documentation and blog theme for {{< link hugo >}}Hugo{{< /link >}} - an open-source static site generator. Based on the {{< link bootstrap >}}Bootstrap{{< /link >}} framework, the rendered site is fast, secure, and responsive. Hinode uses {{< link flexsearch >}}FlexSearch{{< /link >}} to enable full text search across your site. Finally, the theme provides optional support for {{< link npm >}}Node Package Manager{{< /link >}} (npm) to automate the build process and to keep track of dependencies. More information is available on the [about]({{% relref "credits" %}} "about") page.

## Prerequisites

Hinode requires the following software to be installed
on your local machine:

<!-- markdownlint-disable MD037 -->
{{< table >}}
| Software                                                   | Hugo                  | npm                   | Remarks |
|------------------------------------------------------------|-----------------------|-----------------------|---------|
| {{</* link golang_download >}}Go binary{{< /link */>}}     | {{</* fas check */>}} | {{</* fas check */>}} | Required for Hugo modules, including Hinode itself |
| {{</* link hugo_download >}}Hugo (extended){{< /link */>}} | {{</* fas check */>}} |                       | Embedded as npm binary |
| {{</* link nodejs >}}Node.js{{< /link */>}}                |                       | {{</* fas check */>}} | The installation package includes npm |
| {{</* link git_download >}}Git{{< /link */>}}              | recommended           | {{</* fas check */>}} | Recommended for version control |
| {{</* link hugo_sass >}}Dart Sass{{< /link */>}}           | optional              | optional              | Required when using {{</* link "docs/configuration/layout#extended-configuration" >}}Dart Sass transpiler{{< /link */>}} |
{{< /table >}}
<!-- markdownlint-enable MD037 -->

## Installation

The next steps describe the approach how to initialize a new Hinode site using either Hugo or npm.


{{< button collapse="collapse-1" outline=true color="secondary" icon="fab windows" order="first" size="sm" class="mb-4" >}}
    Windows installation notes
{{< /button >}}

{{< collapse id="collapse-1" class="p-3 border rounded mt-n4" >}}
  The installation for Windows requires PowerShell v7. Download it from the Microsoft Store as needed. Check your current version with the command `$PSVersionTable`.
{{< /collapse >}}

<!-- markdownlint-disable MD005 MD029 MD037 -->
{{< nav type="tabs" id="pills-1" >}}
  {{< nav-item header="Hugo" show="true" >}}

1. **Create a new site**

    {{</* command */>}}
    hugo new site my-hinode-site && cd my-hinode-site
    {{</* /command */>}}

2. **Initialize the module system**

    {{</* command */>}}
    hugo mod init example.com/my-hinode-site
    echo "[[module.imports]]" >> hugo.toml
    echo "path = 'github.com/gethinode/hinode'" >> hugo.toml
    {{</* /command */>}}

3. **Start a development server**

    {{</* command */>}}
    hugo server
    {{</* /command */>}}
  {{< /nav-item >}}
  {{< nav-item header="npm" >}}

1. **Create a new repository**

    Go to {{</* link repository_template /*/>}} and login to GitHub as needed. Next, click the green button `Use this template {{</* fas caret-down */>}}` to initialize a new repository based on the Hinode template.

    **Alternatively**, you can use the {{</* link github_cli >}}GitHub cli{{< /link */>}} to initialize the repository from the command line. Replace `--private` with `--public` if you wish to create a public repository instead.

    {{</* command */>}}
    gh repo create my-hinode-site --private --template="{{</* param "links.repository_template" */>}}"
    {{</* /command */>}}

2. **Configure a local site**

    Assuming your repository is `owner/my-hinode-site`, use the `git` command to clone the repository to your local machine.

    {{</* command */>}}
    git clone https://github.com/owner/my-hinode-site && cd my-hinode-site
    {{</* /command */>}}

    Now install the npm packages and hugo modules.

    {{</* command */>}}
    npm install && npm run mod:update
    {{</* /command */>}}

3. **Start the development server**

    {{</* command */>}}
    npm run start
    {{</* /command */>}}
  {{< /nav-item >}}
{{< /nav >}}
<!-- markdownlint-enable MD005 MD029 -->


