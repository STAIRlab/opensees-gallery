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

## Prerequisites

Compiling OpenSees requires the following software to be installed on your local machine:

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


--------------------------------------------


As a static website, your Hinode site can be deployed virtually anywhere. Hugo provides a comprehensive overview of the more popular {{< link hugo_deployment >}}deployment solutions{{< /link >}}. Hinode uses a different build process compared to a default Hugo site. Review the [considerations]({{% relref "#considerations" %}}) for more details. The next paragraphs highlight the specific build and deployment process of Hinode for a few selected hosting providers.

## Considerations

Before deciding on your hosting and deployment approach, review the following considerations.

1. **Include npm in your build process**

   Hinode supports npm to automate the build process. Visit the [Hinode introduction]({{% relref "introduction" %}}) and [commands overview]({{% relref "compiling" %}}) for more details.

2. **Configure the build timeout**

   You might encounter timeout errors when you generate a large site that contains many resources (such as images). Adjust the `timeout` in `config/_default/hugo.toml` as needed.

   {{< docs name="timeout" file="config/_default/hugo.toml" >}}

3. **Consider using build automation**

   Many popular Git providers provide the option to automate the build and deployment process ({{ abbr "CI/CD" >}}). You can trigger this process on each release to your main repository branch, or set up a preview during a Pull Request. The examples on this page assume you have a Git repository with GitHub.

4. **Understand the support for custom domain names**

   Most hosting providers provide a subdomain, such as `<username>.github.io`, to access your website by default. Usually you have the ability to use a custom domain instead, although additional services and configuration might be needed.

5. **Decide on multiregion and CDN support**

   Websites that serve a global audience might benefit from a multiregion or edge deployment to increase availability and reduce latency. You can also consider adding a dedicated {{< abbr CDN >}}, which has the ability to reduce the impact of {{< abbr DDoS >}} attacks for example.

6. **Consider using custom HTTP headers**

   Hinode uses custom HTTP headers to enable the [Content Security Policy]({{% relref "modeling" %}}). The support for custom HTTP headers varies per provider, and might need additional services and configuration.

The table below gives a brief overview of the features supported by a few selected hosting providers. The next paragraphs describe the build and deployment process for each provider in more detail.

<!-- markdownlint-disable MD037 -->
{{< table class="table-striped-columns w-auto" >}}
| Feature            | Azure blob storage | Netlify           |
|--------------------|--------------------|-------------------|
| Automation         | Custom action      | {{</* fas check */>}} |
| Custom domain name | Requires Azure CDN | {{</* fas check */>}} |
| CDN / Edge network | Requires Azure CDN | {{</* fas check */>}} |
| HTTP headers       | Requires Azure CDN | {{</* fas check */>}} |
{{< /table >}}
<!-- markdownlint-enable MD037 -->

<!-- | Feature            | Azure blob storage | Azure Static Web App | GitHub pages      | Netlify           |
|--------------------|--------------------|----------------------|-------------------|-------------------|
| Automation         | Custom action      | {{</* fas check */>}}    | {{</* fas check */>}} | {{</* fas check */>}} |
| Custom domain name | Requires Azure CDN | {{</* fas check */>}}    | {{</* fas check */>}} | {{</* fas check */>}} |
| CDN / Edge network | Requires Azure CDN | {{</* fas check */>}}    | {{</* fas check */>}} | {{</* fas check */>}} |
| HTTP headers       | Requires Azure CDN | {{</* fas check */>}}    |                   | {{</* fas check */>}} |
{.table} -->



## Host on Netlify

Netlify can host your website with continuous deployment from your Git
provider. The starter price plan is free for any public repository and provides


> [!NOTE]
> The starter plan requires your repository to be public. You will require a paid plan if your repository is set to private.

### Assumptions

- You have a Hinode website you are ready to deploy.
- You do not already have a Netlify account.

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

<!-- markdownlint-disable MD037 -->
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
<!-- markdownlint-enable MD037 -->

Your site is now ready to be used. Click on the domain settings of your site within the `Site overview` page to provide a domain alias and to edit the site name as needed. The same section also allows the configuration of a custom domain. Be sure to review your [server configuration]({{% relref "modeling" %}}) if you encounter any rendering issues, such as broken links or garbled stylesheets.

