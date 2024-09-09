---
title: Colors
description: Use Bootstrap's color system to easily adjust your website's colors.
date: 2023-09-02
layout: docs
---

## Theme colors

Hinode uses Bootstrap's color system. You can adjust them in the `/config/_default/params.toml` file in the `style` section.

{{< docs name="theme-colors" file="config/_default/params.toml" >}}

In addition, the background colors `black` and `white` are available too. Below is an overview of the rendered colors.

{{< card-group cols="3" padding="3" gutter="3" wrapper="my-4 p-4" class="border rounded-3" >}}
    {{< card color="primary" >}}primary{{< /card >}}
    {{< card color="secondary" >}}secondary{{< /card >}}
    {{< card color="success" >}}success{{< /card >}}
    {{< card color="danger" >}}danger{{< /card >}}
    {{< card color="warning" >}}warning{{< /card >}}
    {{< card color="info" >}}info{{< /card >}}
    {{< card color="light" >}}light{{< /card >}}
    {{< card color="dark" >}}dark{{< /card >}}
    {{< card color="white" class="text-bg-light" >}}white{{< /card >}}
    {{< card color="black" class="text-white" >}}black{{< /card >}}
{{< /card-group >}}

## Adaptive colors



<!-- markdownlint-disable MD037 -->
{{< example >}}
{{</* card-group cols="2" padding="3" gutter="3" wrapper="my-4 p-4" class="border rounded-3" */>}}
    {{</* card class="bg-body text-bg-white" >}}body{{< /card */>}}
    {{</* card class="bg-body-tertiary text-bg-white" >}}body-tertiary{{< /card */>}}
{{</* /card-group */>}}
{{< /example>}}
<!-- markdownlint-enable MD037 -->

## Background colors

Components such as the [timeline]({{% relref "timeline" %}}) support *subtle* background colors. These colors are also [adaptive]({{% relref "#adaptive-colors" %}}). The following background colors are available.

{{< card-group cols="3" padding="3" gutter="3" wrapper="my-4 p-4" class="border rounded-3" >}}
    {{< card class="bg-primary-subtle" >}}bg-primary-subtle{{< /card >}}
    {{< card class="bg-secondary-subtle" >}}bg-secondary-subtle{{< /card >}}
    {{< card class="bg-success-subtle" >}}bg-success-subtle{{< /card >}}
    {{< card class="bg-danger-subtle" >}}bg-danger-subtle{{< /card >}}
    {{< card class="bg-warning-subtle" >}}bg-warning-subtle{{< /card >}}
    {{< card class="bg-info-subtle" >}}bg-info-subtle{{< /card >}}
    {{< card class="bg-light-subtle" >}}bg-light-subtle{{< /card >}}
    {{< card class="bg-dark-subtle" >}}bg-dark-subtle{{< /card >}}
{{< /card-group >}}

## Colored contrasting links

Hinode defines additional classes to render links that contrast with their background. Simply add `link-bg-<color>` to the class of an `<a>` anchor element. The next example adds a link constrasting with the background color `bg-success`.

<!-- markdownlint-disable MD037 -->
{{< example >}}
{{</* card class="col-md-2 rounded-3 text-center" color="success" >}}{{< link href="#!" class="link-bg-success" >}}success{{< /link >}}{{< /card */>}}
{{< /example>}}
<!-- markdownlint-enable MD037 -->

Below grid illustrates the contrasting colors for each background.

{{< card-group cols="3" padding="3" gutter="3" wrapper="my-4 p-4" class="border rounded-3" >}}
    {{< card color="primary" >}}{{< link href="#!" class="link-bg-primary" >}}primary{{< /link >}}{{< /card >}}
    {{< card color="secondary" >}}{{< link href="#!" class="link-bg-secondary" >}}secondary{{< /link >}}{{< /card >}}
    {{< card color="success" >}}{{< link href="#!" class="link-bg-success" >}}success{{< /link >}}{{< /card >}}
    {{< card color="danger" >}}{{< link href="#!" class="link-bg-danger" >}}danger{{< /link >}}{{< /card >}}
    {{< card color="warning" >}}{{< link href="#!" class="link-bg-warning" >}}warning{{< /link >}}{{< /card >}}
    {{< card color="info" >}}{{< link href="#!" class="link-bg-info" >}}info{{< /link >}}{{< /card >}}
    {{< card color="light" >}}{{< link href="#!" class="link-bg-light" >}}light{{< /link >}}{{< /card >}}
    {{< card color="dark" >}}{{< link href="#!" class="link-bg-dark" >}}dark{{< /link >}}{{< /card >}}
    {{< card color="white" class="text-bg-light" >}}{{< link href="#!" class="link-bg-white" >}}white{{< /link >}}{{< /card >}}
    {{< card color="black" class="text-white" >}}{{< link href="#!" class="link-bg-black" >}}black{{< /link >}}{{< /card >}}
    {{< card class="bg-body text-bg-white" >}}{{< link href="#!" class="link-bg-body" >}}body{{< /link >}}{{< /card >}}
    {{< card class="bg-body-tertiary text-bg-white" >}}{{< link href="#!" class="link-bg-body-tertiary" >}}body-tertiary{{< /link >}}{{< /card >}}
{{< /card-group >}}

## Generating helper

The SCSS generator for the colored links is defined in `assets/scss/helpers/_colored-links.scss`.

{{< docs name="colored-links" file="assets/scss/helpers/_colored-links.scss" >}}
