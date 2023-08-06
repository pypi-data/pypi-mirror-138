# Development howtos

## Install git version

```
poetry add 'git+https://github.com/m1kc/notalib.git@master'
```

## Prepare a release

1. Create a PR (master -> stable)
2. Bump package version in `pyproject.toml` on `master`
3. `poetry build`
