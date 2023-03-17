## Installation

```bash
$ pip install -r requirements.txt
```

## Run

```bash
$ python run.py
```

## Tests

> **Requirement**
> 
> You need to install `pytest` package in your own environment.
> 
> ```bash
> $ pip install pytest
> ```

Run the following command to test:

```bash
$ pytest
```

## Lint

> **Requirement**
> 
> You need to install `pylint` package in your own environment.
> 
> ```bash
> $ pip install pylint
> ```

Run the following command to lint:

```bash
$ pylint $(git ls-files '*.py')
```

`pylint` supports to display display a full report with score.

```bash
$ pylint $(git ls-files '*.py') --reports=yes
```

## Dependencies

Use [NetworkX](https://networkx.org/documentation/stable/reference/index.html) package for classes for graph objects and algorithms to analyze the resulting networks.