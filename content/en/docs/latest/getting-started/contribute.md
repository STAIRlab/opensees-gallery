---
title: Contribute
description: Contribute to the open-source development of OpenSees.
date: 2024-08-14
aliases:
  - "/docs/contribute/"
  - "/contribute/"
layout: docs
---

OpenSees is fully open source and welcomes any contribution, either big or
small. To streamline the contribution process, please take a moment to review
the guidelines outlined in this article.

## Using the issue tracker

The {{< link issue_tracker >}}issue tracker{{< /link >}} on GitHub is the
preferred channel for bug reports, feature requests and submitting pull
requests.

## Asking for support

Use the {{< link discussions >}}GitHub Discussions{{< /link >}} to ask for {{< link discussions_help >}}support from the OpenSees community{{< /link >}}. The discussion forum also includes other topics, such as {{< link discussions_ideas >}}ideas{{< /link >}} and {{< link discussions_showcases >}}showcases{{< /link >}}. We strive for a safe, welcoming, and productive community. The {{< link community_guidelines >}}community guidelines{{< /link >}} provide more context about the expectations, moderation policy, and terms of service.

## Bug reports

A bug is a *demonstrable problem* that is caused by the code in the repository. This may also include issues with the documentation or configuration files. Before filing a bug report, please consider the following guidelines:

- Validate your HTML and Markdown content to ensure your problem isn't caused by a simple error in your own code.
- Use the GitHub {{< link issue_tracker >}}issue search{{< /link >}} — check if the issue has already been reported.
- Check if the issue has been fixed — try to reproduce it using the latest main in the {{< link repository >}}repository{{< /link >}}.
- Isolate the problem — ideally create a reduced test case.
- Use the provided template in the {{< link issue_tracker >}}issue tracker{{< /link >}} to capture the context, evidence and steps on how to reproduce the issue.

## Feature requests

Feature requests are welcome. But take a moment to find out whether your idea fits with the scope and aims of the project. Please use the provided template in the {{< link issue_tracker >}}issue tracker{{< /link >}} to capture the idea and context.

## Pull requests

> [!IMPORTANT]
> By submitting a patch, you agree to allow the project owners to license your work under the terms of the {{< link license >}}MIT license{{< /link >}} (if it includes code changes) and under the terms of the Creative Commons ({{< link cc_by_nc_4_0 >}}CC BY-NC 4.0){{< /link >}} license (if it includes documentation changes).

Good pull requests—patches, improvements, new features—are a fantastic help. They should remain focused in scope and avoid containing unrelated commits.

**Please ask first** before embarking on any **significant** pull request (e.g. implementing features, refactoring code, porting to a different language), otherwise you risk spending a lot of time working on something that the project's developers might not want to merge into the project. For trivial things, or things that don't require a lot of your time, you can go ahead and make a PR.

Please adhere to the [coding guidelines](#coding-guidelines) used throughout the project (indentation, accurate comments, etc.) and any other requirements (such as test coverage).

Adhering to the following process is the best way to get your work included in the project:

1. Fork the project, clone your fork, and configure the remotes:

    ```bash
    git clone https://github.com/<your-username>/OpenSeesRT.git
    cd OpenSeesRT
    git remote add upstream https://github.com/claudioperez/OpenSeesRT
    ```

1. If you cloned a while ago, get the latest changes from upstream:

    ```bash
    git checkout main
    git pull upstream main
    ```

1. Create a new topic branch (off the main project development branch) to contain your feature, change, or fix:

    ```bash
    git checkout -b <topic-branch-name>
    ```

1. Commit your changes in logical chunks. Please adhere to these {{< link commit_message >}}git commit message guidelines{{</link >}}. Use Git's {{< link github_rebase >}}interactive rebase{{< /link >}} feature to tidy up your commits before making them public.

1. Locally merge (or rebase) the upstream development branch into your topic branch:

    ```bash
    git pull [--rebase] upstream main
    ```

1. Push your topic branch up to your fork:

    ```bash
    git push origin <topic-branch-name>
    ```

1. Open a {{< link github_pr >}}Pull Request{{< /link >}} with a clear title and description against the main branch.

## Module contributions

OpenSees supports Hugo modules to to provide a flexible and extensible modular framework. Please consider the [module development conventions]({{% relref "module-development" %}}) to take full advantage of OpenSees's processing pipelines.

## Coding guidelines

In general, run `npm run lint` before committing to ensure your changes follow our coding standards.

### Partials and shortcodes

{{< link "docs/advanced-settings/partial-development" >}}Follow the coding conventions for partial development{{< /link >}}.

### HTML

{{< link html_codeguide >}}Adhere to the Code Guide{{< /link >}}.

- Use tags and elements appropriate for an HTML5 doctype (e.g., self-closing tags).
- Use WAI-ARIA attributes in documentation examples to promote accessibility.

### CSS

{{< link css_codeguide >}}Adhere to the Code Guide{{< /link >}}.

- When feasible, default color palettes should comply with {{< link wcag_contrast >}}WCAG color contrast guidelines{{< /link >}}.

### Javascript

Bundle related client-side javascript in a logically named file. Add the file to the `assets/js` when using Hugo templating. Adjust the eslint configuration as needed to handle necessary exceptions. When adapting someone else's code, please add a link to the original source to give them credit.

- No semicolons (in client-side JS)
- 2 spaces (no tabs)
- strict mode
- "Attractive"

### Markdown

See {{< link markdown_rules >}}markdown rules{{< /link >}} for more details. The following rules are globally disabled:

<!-- markdownlint-disable MD037 -->
{{< table >}}
| #     | Rule | Remarks |
|-------|-----------------------------------------------------------------------------------------------|---------------------------------|
| MD013 | {{</* link markdown_md013 >}}Line length{{< /link */>}}                                           | |
| MD024 | {{</* link markdown_md024 >}}Multiple headings with the same content{{< /link */>}}               | |
| MD026 | {{</* link markdown_md026 >}}Trailing punctuation in heading{{< /link */>}}                       | |
| MD034 | {{</* link markdown_md034 >}}Bare URL used{{< /link */>}}                                         | |
| MD051 | {{</* link markdown_md051 >}}Link fragments should be valid{{< /link */>}}                        | |
| MD053 | {{</* link markdown_md053 >}}Link and image reference definitions should be needed{{< /link */>}} | Disabled due to false positives |
{{< /table >}}
<!-- markdownlint-enable MD037 -->

## License

By contributing your code, you agree to license your contribution under the 
{{<link license >}}BSD license{{< /link >}}. 
By contributing to the documentation,
you agree to license your contribution under the Creative Commons 
({{< link cc_by_nc_4_0 >}}CC BY-NC 4.0{{< /link >}}) license.

