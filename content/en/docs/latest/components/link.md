---
author: Mark Dumay
title: Link
date: 2024-08-17
description: Use the link shortcode to add a managed link to your page content.
layout: docs
icon: fas link
tags: component
---

## Overview

{{< release version="v0.16.8" >}}

Since Hinode `v0.16.8` you can add a managed link to your page content using a configurable shortcode. Managed links refer to an external URL that is centrally maintained in the site's parameters. The shortcode also supports internal links that refer to a regular page or published asset.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* link mozilla_image /*/>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

## Arguments

> [!IMPORTANT]
> The link shortcode recognizes language-specific pages, identified by a language prefix. For example, use `/fr/about` to link to the French translation of the `about` page. Do **not** use the alias `/fr/a-propos` in this case.

The shortcode supports a single unnamed parameter, or various named parameters. The unnamed parameter is recognized as a url if it starts with `http`, else it is treated as either a named link or **relative** internal reference (in that order). Any inner text is rendered as the link title, otherwise it uses the host name (for external links), link title (for internal links), or anchor name (for any local references containing a `#`). The shortcode supports the following named arguments:

{{< args structure="link" group="shortcode" >}}

## Site configuration

> [!IMPORTANT]
> The `--minify` flag of `hugo` purges HTML whitespace by default. Unfortunately, this also removes the spacing behind the visual cue of external links. Add the following configuration to your main configuration to prevent this:
>
>```toml
>[minify]
>  [minify.tdewolff.html]
>    keepWhitespace = true
>```

You can [configure the behavior of managed links]({{% relref "layout#extended-configuration" %}}) in the `/config/_default/params.toml` file in the `main.externalLinks` section. Manage the named links in the `links` section of the same file:

```toml
[links]
    mozilla_image = "https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images"
```

## Examples

Use either named links or common url's to generate a managed link. If a link name cannot be found, Hinode tries to find the reference relative to the current page instead. The reference may include a cross-reference `#`, although the reference itself is not validated.

Use the `cue` and `tab` arguments to override the default behavior of displaying and opening external links. Omit the link's content to generate a reference to the host (for external links) or the target page's title (for internal links). Lastly, set `case` to false to set the obtained page title to lower case.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}

- {{</* link mozilla_image >}}Named link with default settings{{< /link */>}}
- {{</* link name=mozilla_image cue=false tab=false >}}Named link opening in current tab w/o icon{{< /link */>}}
- {{</* link name=mozilla_image cue=true tab=true >}}Named link opening in new tab with icon{{< /link */>}}
- {{</* link mozilla_image /*/>}}
- {{</* link "https://developer.mozilla.org" >}}External link{{< /link */>}}
- {{</* link "../getting-started/introduction" >}}Internal link with title{{< /link */>}}
- {{</* link "../about/license" >}}Internal link with relative path{{< /link */>}}
- {{</* link "/docs/about/license" >}}Internal link with absolute path{{< /link */>}}
- {{</* link "docs/about/license" >}}Internal link with full path{{< /link */>}}
- {{</* link url="../about/license" case=false /*/>}}
- {{</* link "#arguments" /*/>}}
- {{</* link "image#examples" /*/>}}

{{< /example >}}
<!-- markdownlint-enable MD037 -->
