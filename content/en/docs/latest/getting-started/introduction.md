---
title: Introduction
description: Get started with OpenSees.
date: 2024-08-14
aliases:
  - "/docs/getting-started/"
  - "/getting-started/"
  - "/docs/"
layout: docs
---

`opensees` is a Python package that provides an intuitive API for nonlinear
finite element analysis, implemented in C++ through the OpenSees framework. 
OpenSees features state-of-the-art finite element formulations and solution 
algorithms, including mixed formulations for beams and solids, over 200 material models, and an
extensive collection of continuation algorithms to solve highly nonlinear
problems.

## Prerequisites

OpenSees requires the following software to be installed
on your local machine:

<!-- markdownlint-disable MD037 -->
{{< table >}}
| Software                                                   | Hugo                  | npm                   | Remarks |
|------------------------------------------------------------|-----------------------|-----------------------|---------|
| {{</* link golang_download >}}Go binary{{< /link */>}}     | {{</* fas check */>}} | {{</* fas check */>}} | Required for Hugo modules, including Hinode itself |
| {{</* link hugo_download >}}Hugo (extended){{< /link */>}} | {{</* fas check */>}} |                       | Embedded as npm binary |
| {{</* link nodejs >}}Node.js{{< /link */>}}                |                       | {{</* fas check */>}} | The installation package includes npm |
| {{</* link git_download >}}Git{{< /link */>}}              | recommended           | {{</* fas check */>}} | Recommended for version control |
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

## Adding content

The {{< link repository >}}main OpenSeesRT repository{{< /link >}} contains a 
folder `exampleSite` with sample content for a blog and a project portfolio. 
The examples are available in English, French, and Dutch. 

{{< accordion class="accordion-theme accordion-flush" >}}
  {{< accordion-item header="Adding content" >}}
    OpenSeesRT uses Markdown and templates to define the content for your website. 
  {{< /accordion-item >}}
  {{< accordion-item header="Apply Bootstrap styling to your tables" >}}
    OpenSeesRT enhances the basic tables available in Markdown with optional styling features provided by Bootstrap. You can customize the accentuation, adjust the borders, and make tables more compact. 
  {{< /accordion-item >}}
{{< /accordion >}}


