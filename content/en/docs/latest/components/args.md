---
author: Mark Dumay
title: Args
date: 2024-01-04
description: Use the args shortcode to generates a table of structured arguments.
layout: docs
icon: fas sliders
tags: component
---

## Overview

{{< release version="v0.22.0" >}}

Use the args shortcode to generates a table of structured arguments. The argument definitions are expected to be defined in a data file identified by a provided structure name.

<!-- markdownlint-disable MD037 -->
{{< example lang="hugo" >}}
{{</* args "args" */>}}
{{< /example >}}
<!-- markdownlint-enable MD037 -->

## Arguments

The shortcode supports both unnamed and named arguments.

{{< args "args" >}}

## Data format

<!-- TODO: add args data format -->
Define a file in the `data/structures` folder that contains the argument specifications.

### Supported attributes

The format supports the following attributes:

<!-- markdownlint-disable MD037 -->
{{< table >}}
| Name | Required | Description |
|-----------|----------|-------------|
| name | yes | Argument name. |
| type | yes | Data type of the argument, either a primitive or complex type. |
| optional | | Flag to indicate if the argument is optional, defaults to false. |
| default | | Default value when no value is provided. |
| parent  | | Defines if the argument inherits a value from its parent, either `cascade` or `merge`. |
| release | | Points to the version in which the argument was released. See the {{</* link "release" /*/>}} shortcode for more details. |
| deprecated | | Points to the version in which the argument was deprecated. See the {{</* link "release" /*/>}} shortcode for more details. |
| comment | | Documentation about the argument. |
| options | | Conditional value requirements, pending data type. |
{{< /table >}}
<!-- markdownlint-enable MD037 -->

### Supported primitive types

Several primitives are supported. The validation function uses these to test if the provided argument value conforms to the expected data type.

{{< table >}}
| Primitive | Description |
|-----------|-------------|
| bool      | Boolean, either `true` or `false`. The validation supports both quoted and unquoted values. Maps to the Hugo type `bool`. |
| string | Free format plain text. Maps to the Hugo type `string`. |
| int       | A whole number, including negative values. Optionally, specify the allowed value range using `options.min` and `options.max`. Maps to the Hugo type `int`. |
| float     | A fractional number, including negative values. Optionally, specify the allowed value range using `options.min` and `options.max`. Maps to the Hugo type `float64`. |
| select    | A single string value from a set of options. Specify the allowed values in `options.values`. Maps to the Hugo type `string`. |
| datetime  | A date with optional time value. |
| url       | A web address to a particular file or page. The address should include the protocol, hostname, and optional file name. Maps to the Hugo type `string`. |
| path      | Path to a local file or directory. By convention, paths that start with `/` are relative to the repository root. When used as source argument, the base directory may be mapped to one of Hugo's mount folders (e.g. `assets`, `data`, `content`, `static`). Windows paths are mapped to Unix-style paths using forward slashes. Maps to the Hugo type `string`. |
{{< /table >}}

### Supported complex types

Any provided type not matching a primitive is considered a complex type. Type confirmation is tested with `printf "%T"`. For example, to validate if the page context is of the correct type, use `*hugolib.pageState`.

<!-- TODO: add example -->

### Example file

The following file illustrates the definition of the `card` shortcode and partial.

{{< file path="data/structures/card.yml" full="true" show="false" >}}
