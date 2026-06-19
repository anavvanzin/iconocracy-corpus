---
name: get
description: Commands for the get service.
---

# iconocracy-corpus-sdk get

## Overview

Commands for the get service.

## Usage

```bash
iconocracy-corpus-sdk get <subcommand> [flags]
```

## Subcommands

| Subcommand | Description                                                                                                                                                                                                                              |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get-data` | This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`). |

A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data. |

## Loading Subcommand Details

To get detailed usage for a specific subcommand, load its skill file:

- `get-data`: `.claude/skills/get/get-data/SKILL.md`
