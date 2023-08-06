# TidyBear

A tidier approach to pandas.

This package is a collection of functions, routines, and processes that I frequently use, challanged myself to implement, or find particularly nice to write in a certain way. I hope they can be useful to you.

## Examples

- [Verbs](examples/verbs.ipynb)

## Groupby and Summarise

```python
with tb.GroupBy(df, "gr") as g:

    # built in statistcs
    g.n()
    g.sum("x")

    # multiple aggs to a single column
    g.agg("x", ["mean", "median"])

    # same agg across multiple columns using built in
    g.mean(["y", "z"])

    # multiple aggs across multiple columns
    g.agg(["y", "z"], ["median", "std"])

    # send a lambda function to agg
    g.agg("x", lambda x: len(x.unique()), name="n_distinct_x1")

    # Use 'temp' keyword to return series and use it later
    max_val = g.max("x", temp=True)
    min_val = g.min("x", temp=True)

    # create a custom stat directly
    g.stat("midpoint", (max_val + min_val) / 2)

    summary = g.summarise() # or g.summarize()
```
