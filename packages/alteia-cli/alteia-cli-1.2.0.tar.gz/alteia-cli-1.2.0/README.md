# CLI for alteia

# `alteia`

**Usage**:

```console
$ alteia [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `analytics`: Interact with Analytics
* `configure`: Configure your credentials to connect to the...
* `credentials`: Interact your Docker registry credentials
* `products`: Interact with Products

## `alteia configure`

Configure your credentials to connect to the platform

**Usage**:

```console
$ alteia configure [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `alteia analytics`

Interact with Analytics

**Usage**:

```console
$ alteia analytics [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a new analytic
* `delete`: Delete an analytic
* `list`: List the analytics
* `share`: Share an analytic
* `unshare`: Unshare an analytic

### `alteia analytics create`

Create a new analytic

**Usage**:

```console
$ alteia analytics create [OPTIONS]
```

**Options**:

* `--description PATH`: Path of the Analytic description (YAML file)  [required]
* `--company TEXT`: Company identifier
* `--help`: Show this message and exit.

### `alteia analytics delete`

Delete an analytic

**Usage**:

```console
$ alteia analytics delete [OPTIONS] ANALYTIC_NAME
```

**Options**:

* `--version TEXT`: Version range of the analytic in SemVer format. If not provided, all the versions will be deleted.
* `--help`: Show this message and exit.

### `alteia analytics list`

List the analytics

**Usage**:

```console
$ alteia analytics list [OPTIONS]
```

**Options**:

* `--limit INTEGER`: Max number of analytics returned
* `--all`: If set, display all kinds of analytics (otherwise only custom analytics are displayed).
* `--help`: Show this message and exit.

### `alteia analytics share`

Share an analytic

**Usage**:

```console
$ alteia analytics share [OPTIONS] ANALYTIC_NAME
```

**Options**:

* `--version TEXT`: Range of versions in SemVer format. If not provided, all the versions will be shared.
* `--company TEXT`: Identifier of the company to share the analytic with.

When providing the identifier of the root company of your domain,
the analytic is shared with all the companies of the domain
(equivalent to using the --domain option)
* `--domain / --no-domain`: To share the analytic with the root company of your domain.

This has the effect to share the analytic with all the
companies of your domain and is equivalent to using the
--company option providing the id of the root company.
* `--help`: Show this message and exit.

### `alteia analytics unshare`

Unshare an analytic

**Usage**:

```console
$ alteia analytics unshare [OPTIONS] ANALYTIC_NAME
```

**Options**:

* `--version TEXT`: Range of versions in SemVer format. If not provided, all the versions will be unshared.
* `--company TEXT`: Identifier of the company to unshare the analytic with.
* `--domain / --no-domain`: To unshare the analytic with the root company of your domain.

This is equivalent to using the --company option providing
the id of the root company.
Note that if you specifically shared the analytic with a company
of your domain, the analytic will still be shared with that company.
* `--help`: Show this message and exit.

## `alteia credentials`

Interact your Docker registry credentials

**Usage**:

```console
$ alteia credentials [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a new credential entry
* `delete`: Delete a credential entry by its name
* `list`: List the existing credentials

### `alteia credentials create`

Create a new credential entry

**Usage**:

```console
$ alteia credentials create [OPTIONS]
```

**Options**:

* `--filepath PATH`: Path of the Credential JSON file  [required]
* `--company TEXT`: Company identifier
* `--help`: Show this message and exit.

### `alteia credentials delete`

Delete a credential entry by its name

**Usage**:

```console
$ alteia credentials delete [OPTIONS] NAME
```

**Options**:

* `--help`: Show this message and exit.

### `alteia credentials list`

List the existing credentials

**Usage**:

```console
$ alteia credentials list [OPTIONS]
```

**Options**:

* `--company TEXT`: Company identifier
* `--help`: Show this message and exit.

## `alteia products`

Interact with Products

**Usage**:

```console
$ alteia products [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `cancel`: Cancel a running product
* `list`: List the products
* `logs`: Retrieve the logs of a product

### `alteia products cancel`

Cancel a running product

**Usage**:

```console
$ alteia products cancel [OPTIONS] PRODUCT_ID
```

**Options**:

* `--help`: Show this message and exit.

### `alteia products list`

List the products

**Usage**:

```console
$ alteia products list [OPTIONS]
```

**Options**:

* `-n, --limit INTEGER`: Max number of products returned  [default: 10]
* `--analytic TEXT`: Analytic name
* `--company TEXT`: Company identifier
* `--status [pending|processing|available|rejected|failed]`: Product status
* `--all`: If set, display also the products from platform analytics (otherwise only products from custom analytics are displayed).
* `--help`: Show this message and exit.

### `alteia products logs`

Retrieve the logs of a product

**Usage**:

```console
$ alteia products logs [OPTIONS] PRODUCT_ID
```

**Options**:

* `-f, --follow`: Follow logs
* `--help`: Show this message and exit.

---

*Generated with `typer alteia_cli/main.py utils docs --name alteia`*
