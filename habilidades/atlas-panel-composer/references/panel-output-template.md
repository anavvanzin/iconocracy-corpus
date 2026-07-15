# Panel layout notation

Use a simple coordinate system on a 12 x 8 landscape field unless another format is required.

Example:

| Object | Position | Size | Crop | Function |
|---|---|---|---|---|
| 01 | x1-y1 | 4x5 | full | anchor |
| 02 | x6-y1 | 3x3 | gesture detail | inversion |
| 03 | x9-y2 | 2x4 | full | institutional reuse |

## Text wireframe

```text
+------------------------------------------------+
| [01 anchor 4x5]       [02 detail 3x3]          |
|                                                |
|                 [04 interval]   [03 2x4]       |
+------------------------------------------------+
```

Always include object numbers, approximate proportions, and a primary reading path.
