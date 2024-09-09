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

## Adding content

The {{< link repository >}}main Hinode repository{{< /link >}} contains a folder `exampleSite` with sample content for a blog and a project portfolio. The examples are available in English, French, and Dutch. Review the following items on to how organize and enrich your content.

{{< accordion class="accordion-theme accordion-flush" >}}
  {{< accordion-item header="Adding content" >}}
    Hinode uses Markdown and templates to define the content for your website. See the [content management]({{% relref "content-management" %}}) page for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Organize the content" >}}
    Hinode uses a structured approach to organize and present content. See the [content organization]({{% relref "content-organization" %}}) page for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Enrich Markdown content with Bootstrap styling" >}}
    Hinode uses a mix of basic Markdown syntax enriched with Bootstrap styling for the typography. Review the [typography documentation]({{% relref "typography" %}}) for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Use Markdown and Hugo shortcodes to generate links and cross-references" >}}
    Generate internal links and external links using a combination of Markdown and Hugo shortcodes. You can optionally manage your external links in a central configuration file. Review the [links documentation]({{% relref "links-and-cross-references" %}}) for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Add responsive images optimized for multiple screen sizes and devices">}}
    Hinode supports responsive images out-of-the-box. Hinode uses Hugo to preprocess images on the server. By taking advantage of so-called image sets, the client’s browser can decide which image to download whilst reducing the download size. Review the [image documentation]({{% relref "images-and-figures" %}}) for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Apply Bootstrap styling to your tables" >}}
    Hinode enhances the basic tables available in Markdown with optional styling features provided by Bootstrap. You can customize the accentuation, adjust the borders, and make tables more compact. Review the [tables documentation]({{% relref "tables" %}}) for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Include Font Awesome icons on the fly" >}}
    Hinode provides out-of-the box access to the free icons of {{</* link fontawesome >}}Font Awesome{{< /link */>}}. The icon library provides various styling options. Review the [icons documentation]({{% relref "../content/icons" %}}) for more details.
  {{< /accordion-item >}}
{{< /accordion >}}

## Quick configuration settings

The main site configuration is available in `./config/_default`. Review the following items to get you started.

{{< accordion class="accordion-theme accordion-flush" >}}
  {{< accordion-item header="Review the layout options" >}}
    Hinode uses a base layout for the home page, list pages, and individual pages. Individual pages can also be configured as documentation page instead of a regular page. Review the [layout documentation]({{% relref "colors" %}}) for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Adjust the theme colors" >}}
    Hinode uses eight configurable theme colors. You can adjust them in the `style` section of  `/config/_default/params.toml`. Review the [colors documentation]({{% relref "colors" %}}) for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Set the main font" >}}
    Set the `themeFont` and `themeFontPath` in the `style` section of `/config/_default/params.toml` to adjust the main font. Hinode includes supports for [Emoji]({{% relref "typography#emoji" %}}) by default. Review the [fonts documentation]({{% relref "fonts" %}}) for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Configure the supported languages">}}
    Configure each supported language in `config/_default/languages.toml`. Set the default behavior in `config/_default/hugo.toml`. Review the [languages documentation]({{% relref "languages" %}}) for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Define the main menu" >}}
    Define the main menu entries for each language in `config/_default/menus`. For example, the English menu entries are defined in `menus.en.toml`. See the [navigation documentation]({{% relref "navigation" %}}) for more details.
  {{< /accordion-item >}}
{{< /accordion >}}

## Advanced configuration settings

The next topics give an overview of the advanced configuration settings.

<!-- markdownlint-disable MD037 -->
{{< accordion class="accordion-theme accordion-flush" >}}
  {{< accordion-item header="Review the approach to dependency management and virtualization" >}}
    Hinode supports {{</* link npm >}}npm{{< /link */>}} packages to automate various tasks. In addition, it uses Hugo's {{</* link hugo_mounts >}}mounted folders{{< /link */>}} to create a virtual file system. Review the [advanced settings overview]({{% relref "../advanced-settings/overview" %}}) for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Adjust the build pipeline for Sass files" >}}
    Hinode uses Bootstrap's Sass files to generate the cascading style sheets of the website. The main entrypoint is defined in `assets/scss/app.scss`. See the [styles documentation]({{% relref "styles" %}}) for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Bundle JavaScript files for deployment">}}
    Hinodes uses npm to include the latest JavaScript files of external packages such as {{</* link bootstrap >}}Bootstrap{{< /link */>}} and {{</* link flexsearch >}}FlexSearch{{< /link */>}}. All local and external files are bundled in a single JavaScript file. See the [scripts documentation]({{% relref "scripts" %}}) for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Process icon files to apply theme colors" >}}
    Hinode replaces Bootstrap's embedded icons with file-based icons to comply with its security settings. The icon files are parameterized to use the theme colors. See the [icons documentation]({{% relref "../advanced-settings/icons" %}}) for more details.
  {{< /accordion-item >}}
  {{< accordion-item header="Refine header settings to adjust the Content Security Policy" >}}
    Hinode uses rather strict security policies to ensure the site is secure by default. Be sure to include references to external sources in the header configuration to avoid broken links. The settings of the local development server are defined in `config/_default/server.toml`. Similar settings are defined in the `netlify.toml` file provided in the repository's root when deploying to {{</* link netlify >}}Netlify{{< /link */>}}. See the [server documentation]({{% relref "server-headers" %}}) for more details.
  {{< /accordion-item >}}
{{< /accordion >}}
<!-- markdownlint-enable MD037 -->
