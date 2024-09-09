---
title: Server-side redirection
description: Enable server-side redirection (Netlify only)
date: 2023-08-03
layout: docs
---

Hugo supports {{< link hugo_alias >}}client-side redirection using aliases{{< /link >}}. In this approach, the browser receives an instruction to redirect to a new URL when visiting the initial page. We can instruct the server to redirect the URL instead, thus safing an additional roundtrip.

Hinode has defined a template in {{< link repository_redir >}}layouts/index.redir{{< /link >}} to automatically generate server-side redirection rules for **Netlify**. When you add the status code `200` to such a rule, the {{< link netlify_rewrite >}}redirection becomes a rewrite{{< /link >}}. In a **rewrite**, the URL in the visitor's address bar remains the same, while the content is fetched from a different location behind the scenes. We will use this mechanism to fetch the content from the branch site.

The below settings creates a file `public/_redirects` when building the site. It is suggested to add these settings to your **production configuration** in `config/production/hugo.toml`. The setting `disableAliases` disables all client-side redirection rules. Instead, the `REDIR` output generates all redirection rules for the server, including rewrites.

```toml
disableAliases = true

[outputFormats.REDIR]
mediaType = "text/netlify"
baseName = "_redirects"
isPlainText = true
notAlternative = true

[mediaTypes."text/netlify"]
delimiter = ""

[outputs]
home = ["HTML", "RSS", "REDIR"]
```
