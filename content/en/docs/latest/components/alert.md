---
author: Mark Dumay
title: Alert
date: 2023-12-29
description: Use the alert shortcode to display a contextual feedback message.
layout: docs
icon: fas triangle-exclamation
tags: component
---

## Overview

Use the `alert` shortcode to display a contextual feedback message. The inner content is used as alert text.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* alert color="danger" */>}}
    A simple danger alert—check it out!
{{</* /alert */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

## Arguments

The shortcode supports the following arguments:

{{< args structure="alert" group="shortcode" >}}

## Examples

Change the style of your accordion with arguments.

### Colored alert

As an example, the following shortcodes displays a simple alert for each theme color.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* alert color="primary" */>}}
    A simple primary alert—check it out!
{{</* /alert */>}}

{{</* alert color="secondary" */>}}
    A simple secondary alert—check it out!
{{</* /alert */>}}

{{</* alert color="success" */>}}
    A simple success alert—check it out!
{{</* /alert */>}}

{{</* alert color="danger" */>}}
    A simple danger alert—check it out!
{{</* /alert */>}}

{{</* alert color="warning" */>}}
    A simple warning alert-check it out!
{{</* /alert */>}}

{{</* alert color="info" */>}}
    A simple info alert—check it out!
{{</* /alert */>}}

{{</* alert color="light" */>}}
    A simple light alert—check it out!
{{</* /alert */>}}

{{</* alert color="dark" */>}}
    A simple dark alert—check it out!
{{</* /alert */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

### Dismissible alert

As an example, the following shortcode displays a dismissible alert.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* alert color="danger" dismissible="true" */>}}
    A dismissible alert—check it out!
{{</* /alert */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

### Alert with icon

As an example, the following shortcode displays an alert with an icon. The icon is resized to size `2x` and pulled to the left by default.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* alert color="danger" icon="fas triangle-exclamation" */>}}
    An illustrated alert—check it out!
{{</* /alert */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

### Alert of specific type

As an example, the following shortcode displays an informative alert with an icon.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* alert type="info" */>}}
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur
sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
est laborum.
{{</* /alert */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

As an example, the following shortcode displays a warning with an icon.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* alert type="danger" */>}}
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur
sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
est laborum.
{{</* /alert */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->
