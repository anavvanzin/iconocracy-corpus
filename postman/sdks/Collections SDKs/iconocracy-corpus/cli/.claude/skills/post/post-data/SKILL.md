---
name: post-data
description: This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.

A successful POST request typically returns a `200 OK` or `201 Created` response code.
---

# post post-data

## Overview

This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.

A successful POST request typically returns a `200 OK` or `201 Created` response code.

## Usage

```bash
iconocracy-corpus-sdk post post-data [--body '<json>' | --body-file <path>]
```

**Example:**

```bash
iconocracy-corpus-sdk post post-data --body '{"key": "value"}'
```

## Request Body

Provide the request body using one of the following methods:

| Method      | Flag                 | Description                             |
| ----------- | -------------------- | --------------------------------------- |
| Inline JSON | `--body '<json>'`    | Pass JSON directly as a string argument |
| File path   | `--body-file <path>` | Read JSON content from a file           |

**Example inline:**

```bash
# Minimal example with inline JSON body
iconocracy-corpus-sdk post post-data --body '{"key": "value"}'
```

**Example from file:**

```bash
# Minimal example with JSON from file
iconocracy-corpus-sdk post post-data --body-file ./request.json
```
