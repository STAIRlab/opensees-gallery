---
author: Mark Dumay
title: Example
date: 2023-12-29
description: The example shortcode displays a code example and renders a preview of the same input.
layout: docs
icon: fa lightbulb
tags: component
---

## Overview

{{< release version="v0.8.0" >}}

The `example` shortcode displays a code example and renders a preview of the same input. The shortcode accepts the {{< link hugo_chroma >}}languages supported by Hugo's highlight function{{< /link >}}.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* command */>}}
export MY_VAR=123
{{</* /command */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

## Arguments

The shortcode supports the following arguments:

{{< args structure="example" group="shortcode" >}}

## Examples

Change the style and language of your code snippet with shortcode arguments.

### Hugo code example

Set the `lang` argument to `hugo` to render a Hugo code example. Be sure to escape the input with `/*` and `*/` delimiters to avoid rendering issues.

#### Preview

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo">}}
{{</* command */>}}
export MY_VAR=123
{{</* /command */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

#### Input

```go-html-template
{{</* example lang="hugo" */>}}
    {{</*/* command */*/>}}
    export MY_VAR=123
    {{</*/* /command */*/>}}
{{</* /example */>}}
```

### Hidden markup

Set `show_markup` to `false` to hide the code input and to display the preview only.

#### Preview

{{< example lang="hugo" show_markup=false >}}
This is a lead paragraph. It stands out from regular paragraphs.
{.lead}
{{< /example >}}

#### Input

```go-html-template
{{</* example show_markup=false */>}}
This is a lead paragraph. It stands out from regular paragraphs.
{.lead}
{{</* /example */>}}
```

### Hidden preview

Set `show_preview` to `false` to hide the output and to display the code input only.

#### Preview

{{< example lang="hugo" show_preview=false >}}
This is a lead paragraph. It stands out from regular paragraphs.
{.lead}
{{< /example >}}

#### Input

```go-html-template
{{</* example show_preview=false */>}}
This is a lead paragraph. It stands out from regular paragraphs.
{.lead}
{{</* /example */>}}
```
