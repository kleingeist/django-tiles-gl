# Development

## Node dependencies

We are using node to manage the javascript dependencies to maplibre and for building the default style and fonts.

**Node 12.22 (lts/erbium) is required to install the dependencies.**
You may use [nvm](https://github.com/nvm-sh/nvm) to install and use it:

```shell
nvm install lts/erbium
nvm use lts/erbium
```

### Upgrading maplibre

1. Update the version in `package.json`
2. Call `./scripts/install-maplibre.sh` to install the files to the modules static folder

### Making fonts, style and sprites

See helper `/scripts/` directory.
