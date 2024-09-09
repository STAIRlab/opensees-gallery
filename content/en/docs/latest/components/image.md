---
author: Mark Dumay
title: Image
date: 2024-08-17
description: Use the image shortcode to display a responsive image with a specific aspect ratio.
layout: docs
icon: fas image
tags: component
---

## Overview

Use the `image` shortcode to display a responsive image with a specific aspect ratio. The source link can refer to either an image available in the `/assets/img` folder of your site or a public web location. The shortcode renders the image as a so-called {{< link mozilla_image >}}image set{{< /link >}} to optimize the image for different screen sizes and resolutions. Behind the scenes, Hugo renders the images in `WebP` format and stores them in a local folder (`resources` or `public`). The images are processed using the quality setting specified in the `[imaging]` section of the main {{< link hugo_imaging >}}config file{{< /link >}} (defaults to 75). Supported image types are `.png`, `.jpeg`, `.gif`, `.tiff`, `.bmp`, and `.webp`. A fallback image of type `.jpeg` is provided for older browsers.

As an example, the following shortcode displays an image with its original aspect ratio. The image is adjusted for the active color mode. The shortcode processes two images behind the scenes, being `img/responsive-light.png` and `img/responsive-dark.png`. Only the image that matches the current color mode is shown.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* image src="img/responsive.png" mode="true" caption="Image caption" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

## Arguments

The shortcode supports the following arguments:

{{< args structure="image" group="shortcode" >}}

## Examples

Change the style of your card with class attributes and shortcode arguments.

### Aspect ratio

As an example, the following shortcodes display a centered image with various aspect ratios.

Set the `ratio` to `1x1` for a square aspect ratio.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* image src="img/flowers.jpg" ratio="1x1" wrapper="col-6 mx-auto" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

Set the `ratio` to `3x2` for a landscape aspect ratio.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* image src="img/flowers.jpg" ratio="3x2" wrapper="col-6 mx-auto" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

Set the `ratio` to `4x3` for a landscape aspect ratio.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* image src="img/flowers.jpg" ratio="4x3" wrapper="col-6 mx-auto" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

Set the `ratio` to `16x9` for a landscape aspect ratio.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* image src="img/flowers.jpg" ratio="16x9" wrapper="col-6 mx-auto" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

Set the `ratio` to `21x9` for a landscape aspect ratio.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* image src="img/flowers.jpg" ratio="21x9" wrapper="col-6 mx-auto" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

Omit the `ratio` to keep the original aspect ratio.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* image src="img/flowers.jpg" wrapper="col-6 mx-auto" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

### Color mode

Set `mode` to `true` to use an image that is color-mode aware. The shortcode processes two images behind the scenes, being `img/responsive-light.png` and `img/responsive-dark.png`. Only the image that matches the current color mode is shown.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* image src="img/responsive.png" mode="true" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

### Figures

Add a `caption` to transform the image into a figure with caption.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* image src="img/watch.jpg" caption="Figure caption" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

### Vector images

The shortcode supports vector images of type `.svg` too. The shortcode supports the regular arguments, however, vector images are contained instead of cropped when the `ratio` is set. The next example shows a color-mode-aware vector image. The background is set to a contrasting color to illustrate the ratio behavior.

> [!IMPORTANT]
> Since release {{< release version="v0.26.3" short="true" type="link" >}}, vector images stored in the site's `assets` folder are embedded as inline vector images. Vector images stored in the `static` folder are kept as separate files.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* image src="/img/logo_var.svg#logo" class="img-fluid w-50" wrapper="text-center" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->
