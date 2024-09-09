---
author: Mark Dumay
title: Breadcrumb
date: 2023-12-29
description: Use the breadcrumb shortcode to display the current page’s location within the site's navigational hierarchy.
layout: docs
icon: fas bread-slice
tags: component
---

## Overview

Use the `breadcrumb` shortcode to display the current page’s location within the site's navigational hierarchy. As an example, the following shortcode displays a breadcrumb for the current page.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* breadcrumb path="breadcrumb" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

## Arguments

The shortcode supports the following arguments:

{{< args structure="breadcrumb" group="shortcode" >}}


{{< docs name="breadcrumb" file="assets/scss/components/_breadcrumb.scss" >}}
