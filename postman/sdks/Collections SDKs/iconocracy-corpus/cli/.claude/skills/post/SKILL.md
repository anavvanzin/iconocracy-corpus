---
name: post
description: Commands for the post service.
---

# iconocracy-corpus-sdk post

## Overview

Commands for the post service.

## Usage

```bash
iconocracy-corpus-sdk post <subcommand> [flags]
```

## Subcommands

| Subcommand  | Description                                                                                                                                        |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `post-data` | This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response. |

A successful POST request typically returns a `200 OK` or `201 Created` response code. |

## Loading Subcommand Details

To get detailed usage for a specific subcommand, load its skill file:

- `post-data`: `.claude/skills/post/post-data/SKILL.md`
