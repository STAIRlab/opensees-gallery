---
author: Mark Dumay
title: Animation
date: 2024-01-02
description: Use the animation shortcode to show an After Effects animation.
layout: docs
icon: fa circle-play
tags: component
modules: ["lottie"]
---

## Overview

{{< release version="v0.20.4" >}}

Use the animation shortcode to show an After Effects animation, powered by {{< link lottie >}}Lottie{{< /link >}}. The Lottie library supports animations that have been exported as JSON with Bodymovin. The animation uses vector graphics and is responsive. The shortcode is a simplified wrapper of the Lottie library that provides basic functionality. As an example, the following shortcode shows an animation that plays when hovering the mouse over it.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* animation data="animation/gatin.json" auto=false hover=true class="col-6 mx-auto" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

## Arguments

The shortcode supports the following arguments:

{{< args structure="animation" group="shortcode" >}}

## Examples

Change the behavior of your animation with shortcode arguments.

### Default animation

Assign a valid path to `data` to provide a JSON file that contains the animation as input. The file should be stored in the `static` folder, or in one of its subfolders.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* animation data="animation/gatin.json" class="col-6 mx-auto" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

### Animation on hover

Set `auto` to false and `hover` to true to trigger the animation when hovering the mouse over it.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* animation data="animation/gatin.json" auto=false hover=true class="col-6 mx-auto" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

### Identification

Assign a specific identified to the animation by setting the `id` argument. The following example assigns the id `gatin-animation` to the animation.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* animation id="gatin-animation" data="animation/gatin.json" class="col-6 mx-auto" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->
