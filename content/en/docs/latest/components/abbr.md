---
author: Mark Dumay
title: Abbr
date: 2023-12-29
description: Use the abbr shortcode to show the long form of an abbrevitation.
layout: docs
icon: fas question
tags: component
---

## Overview

{{< release version="v0.19.0" >}}

Use the abbr shortcode to show the long form of an abbrevitation on hover. The abbreviation data is retrieved from a central data file. By default, the shortcode uses "data/abbr.yaml" with translation support.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* abbr HTML */>}}
{{</* abbr key="html" class="initialism" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

## Arguments

The shortcode supports a single unnamed argument, which maps to the `key` argument. When using named parameters, the following arguments are supported:

{{< args structure="abbr" group="shortcode" >}}

## Data format

Define a file in the `data` folder that contains the abbreviation data. The format expects the following attributes:

{{< table >}}
| Attribute | Required | Description |
|-----------|----------|-------------|
| id        | Yes      | Required key of the abbeviation. Store the key in lower case to ensure it can be matched. |
| long      | Yes      | Required long form of the abbreviation. |
{{< /table >}}

The following snippet defines three entries in `yml` format.

```yml
- id: css
  long: "Cascading Style Sheets"

- id: html
  long: "HyperText Markup Language"

- id: svg
  long: "Scalable Vector Graphics"
```
