---
sidebarDepth: 1
---

# Command Line Interface

Meltano provides a command line interface (CLI) that allows you to manage the configuration and orchestration of Meltano instances. It provides a single source of truth for the entire data pipeline. The CLI makes it easy to develop, run, and debug every step of the data life cycle.

## `add`

The `add` command allows you to add an extractor, loader, or transform to your Meltano instance.

### Extractor / Loader

When you add a extractor or loader to a Meltano instance, Meltano will:

1. Add it to the `meltano.yml` file
1. Installs it in the `.meltano` directory with `venv` and `pip`

#### Examples

```bash
# Extractor / Loader Template
meltano add [extractor | loader] [name_of_plugin]

# Extractor Example
meltano add extractor tap-gitlab

# Loader Example
meltano add loader target-postgres
```

### Transform

When you add a transform to a Meltano instance, Meltano will:

1. Installs dbt transformer to enable transformations (if needed)
1. Add transform to `meltano.yml file`
1. Updates the dbt packages and project configuration

#### Example

```bash
# Transform Template
meltano add [transform] [name_of_transform]
```

### Model

When you add a model to a Meltano instance, Meltano will:

1. Add a model bundle to your `meltano.yml` file to help you interactively generate SQL
1. Installed inside the `.meltano` directory which are then available to use in the Meltano webapp

#### Example

```bash
meltano add model [name_of_model]
```

### Orchestration

When you add an orchestrator to a Meltano instance, Meltano will:

1. Adds an orchestrator plugin to your **meltano.yml**
1. Installs it

#### Example

```bash
meltano add orchestrator [name_of_orchestrator]
```

## `config`

Enables you to change a plugin's configuration.

Meltano uses configuration layers to resolve a plugin's configuration:

1. Environments variables
1. Plugin definition's `config:` attribute in **meltano.yml**
1. Settings set via `meltano config` or the in the UI (stored in the meltano database)
1. Default values set in the setting definition in **discovery.yml**

This way, a Meltano project can stay secure in production, where environment variables shall be used for sensible settings (such as _passwords_ or _keys_) or use the settings database.

::: info
Meltano stores the configuration as-is, without encryption. The most secure way to set a plugin's setting to a sensible value is to use the environment variable associated with it.

Use `meltano config <plugin_name> list` to see the proper variable to set for a setting.
:::

In development, however, one can use the **meltano.yml** to quickly set the configuration, via the `config:` attribute in each plugin, or use a different set of environment variables.

### How to use

```bash
# Displays the plugin's configuration.
meltano config <plugin_name>

# List the available settings for the plugin.
meltano config <plugin_name> list

# Sets the configuration's setting `<name>` to `<value>`.
meltano config <plugin_name> set <name> <value>

# Remove the configuration's setting `<name>`.
meltano config <plugin_name> unset <name>

# Clear the configuration (back to defaults).
meltano config <plugin_name> reset
```

## `discover`

Lists the available plugins you are interested in.

### How to Use

```bash
# List all available plugins
meltano discover all

# Only list available extractors
meltano discover extractors

# Only list available loaders
meltano discover loaders

# Only list available models
meltano discover models
```

## `elt`

This allows you to run your ELT pipeline to Extract, Load, and Transform the data with configurations of your choosing:

1. The `job_id` is autogenerated using the current date and time if it is not provided
1. All the output generated by this command is also logged in `.meltano/run/logs/{job_id}/elt_{timestamp}.log`

::: info
Meltano keeps the logs for the 10 most recent elt runs with the same `job_id`. The number of logs kept can also be set by using the environment variable `$MELTANO_MAX_LOGS_PER_JOB_ID`.
:::

### How to use

```bash
meltano elt <extractor> <loader> [--job_id TEXT] [--transform run] [--dry]
```

### Parameters

- The `--transform` option can be:

  - `run`: run the Transforms
  - `skip`: skip the Transforms (Default)
  - `only`: only run the Transforms (skip the Extract and Load steps)

### Examples

```bash
meltano select --exclude tap-carbon-intensity '*' 'longitude'
```

```bash
meltano select --exclude tap-carbon-intensity '*' 'latitude'
```

This will exclude all `longitude` and `latitude` attributes.

## `extract`

Extract data to a loader and optionally transform the data

### How to Use

```bash
meltano extract [name of extractor] --to [name of loader]`
```

## `init`

Used to create a new meltano project with a basic infrastructure in place.

### How to use

```bash
# Format
meltano init [project_name] [--no_usage_stats]
```

### Parameters

- **project_name** - This determines the folder name for the project

### Options

- **no_usage_stats** - This flag disables sending anonymous usage data when creating a new project.

## `install`

Installs all the dependencies of your project based on the **meltano.yml** file.

### How to Use

```bash
meltano install
```

## `invoke`

- `meltano invoke <plugin_name> PLUGIN_ARGS...`: Invoke the plugin manually.

## `list`

Use `--list` to list the current selected tap attributes.

> Note: `--all` can be used to show all the tap attributes with their selected status.

## `permissions`

::: info
This is an optional tool for users who want to configure permissions if they're using Snowflake as the data warehouse and want to granularly set who has access to which data at the warehouse level.

Alpha-quality [Role Based Access Control (RBAC)](/docs/security-and-privacy.html#role-based-access-control-rbac-alpha) is also available.
:::

Use this command to check and manage the permissions of a Snowflake account.

```bash
meltano permissions grant <spec_file> --db snowflake [--dry] [--diff] [--full-refresh]
```

Given the parameters to connect to a Snowflake account and a YAML file (a "spec") representing the desired database configuration, this command makes sure that the configuration of that database matches the spec. If there are differences, it will return the sql commands required to make it match the spec.

We currently support only Snowflake, as [pgbedrock](https://github.com/Squarespace/pgbedrock) can be used for managing the permissions in a Postgres database.

#### spec_file

The YAML specification file is used to define in a declarative way the databases, roles, users and warehouses in a Snowflake account, together with the permissions for databases, schemas and tables for the same account.

Its syntax is inspired by [pgbedrock](https://github.com/Squarespace/pgbedrock), with additional options for Snowflake.

All permissions are abbreviated as `read` or `write` permissions, with Meltano generating the proper grants for each type of object. This includes shared databases which have simpler and more limited permissions than non-shared databases.

Tables and views are listed under `tables` and handled properly behind the scenes.

If `*` is provided as the parameter for tables the grant statement will use the `ALL <object_type>S in SCHEMA` syntax. It will also grant to future tables and views. See Snowflake documenation for [`ON FUTURE`](https://docs.snowflake.net/manuals/sql-reference/sql/grant-privilege.html#optional-parameters)

If a schema name includes an asterisk, such as `snowplow_*`, then all schemas that match this pattern will be included in grant statement. This can be coupled with the asterisk for table grants to grant permissions on all tables in all schemas that match the given pattern. This is useful for date-partitioned schemas.

A specification file has the following structure:

```bash
# Databases
databases:
    - db_name:
        shared: boolean
    - db_name:
        shared: boolean
    ... ... ...

# Roles
roles:
    - role_name:
        warehouses:
            - warehouse_name
            - warehouse_name
            ...

        member_of:
            - role_name
            - role_name
            ...

        privileges:
            databases:
                read:
                    - database_name
                    - database_name
                    ...
                write:
                    - database_name
                    - database_name
                    ...
            schemas:
                read:
                    - database_name.*
                    - database_name.schema_name
                    - database_name.schema_partial_*
                    ...
                write:
                    - database_name.*
                    - database_name.schema_name
                    - database_name.schema_partial_*
                    ...
            tables:
                read:
                    - database_name.*.*
                    - database_name.schema_name.*
                    - database_name.schema_partial_*.*
                    - database_name.schema_name.table_name
                    ...
                write:
                    - database_name.*.*
                    - database_name.schema_name.*
                    - database_name.schema_partial_*.*
                    - database_name.schema_name.table_name
                    ...

        owns:
            databases:
                - database_name
                ...
            schemas:
                - database_name.*
                - database_name.schema_name
                - database_name.schema_partial_*
                ...
            tables:
                - database_name.*.*
                - database_name.schema_name.*
                - database_name.schema_partial_*.*
                - database_name.schema_name.table_name
                ...

    - role_name:
    ... ... ...

# Users
users:
    - user_name:
        can_login: boolean
        member_of:
            - role_name
            ...
    - user_name:
    ... ... ...

# Warehouses
warehouses:
    - warehouse_name:
        size: x-small
    ... ... ...
```

For a working example, you can check [the Snowflake specification file](https://gitlab.com/meltano/meltano/blob/master/tests/meltano/core/permissions/specs/snowflake_spec.yml) that we are using for testing `meltano permissions`.

#### --db

The database to be used, either `postgres` or `snowflake`. Postgres is still experimental and may be fully supported in the future.

#### --diff

When this flag is set, a full diff with both new and already granted commands is returned. Otherwise, only required commands for matching the definitions on the spec are returned.

#### --dry

When this flag is set, the permission queries generated are not actually sent to the server and run; They are just returned to the user for examining them and running them manually.

Currently we are still evaluating the results generated by the `meltano permissions grant` command, so the `--dry` flag is required.

#### --full-refresh

When this flag is set, the permission queries generated are revoke statements for all roles, warehouse, databases, schemas, and tables listed in the spec file. Currently it will not revoke ownership of database objects or disable users. The revoke commands are run prior to the grant commands.

#### Connection Parameters

The following environmental variables must be available to connect to Snowflake:

```bash
$PERMISSION_BOT_USER
$PERMISSION_BOT_PASSWORD
$PERMISSION_BOT_ACCOUNT
$PERMISSION_BOT_DATABASE
$PERMISSION_BOT_ROLE
$PERMISSION_BOT_WAREHOUSE
```

## `schedule`

::: tip
An `orchestrator` plugin is required to use `meltano schedule`: refer to the [Orchestration](/docs/orchestration.html) documentation to get started with Meltano orchestration.
:::

Meltano provides a `schedule` method to run specified ELT pipelines at regular intervals. Schedules are defined inside the `meltano.yml` project as such:

- `meltano schedule <schedule_name> <extractor> <loader> <interval> [--transform]`: Schedule an ELT pipeline to run using an orchestrator.
  - `meltano schedule list`: List the project's schedules.

```yaml
schedules:
  - name: test
    interval: '@daily'
    extractor: tap-mock
    loader: target-mock
    transform: skip
    env: {}
```

## `select`

Use the `select` command to add select patterns to a specific extractor in your Meltano project.

- `meltano select [--list] [--all] <tap_name> [ENTITIES_PATTERN] [ATTRIBUTE_PATTERN]`: Manage the selected entities/attributes for a specific tap.

::: warning
Not all taps support this feature. In addition, taps needs to support the `--discover` switch. You can use `meltano invoke tap-... --discover` to see if the tap supports it.
:::

### How to use

Meltano select patterns are inspired by the [glob](<https://en.wikipedia.org/wiki/Glob_(programming)>) syntax you might find in your operating system.

- `*`: matches any sequence of characters
- `?`: matches one character
- `[abc]`: matches either `a`, `b`, or `c`
- `[!abc]`: matches any character **but** `a`, `b`, or `c`

### Examples

```bash
$ meltano select tap-carbon-intensity '*' 'name*'
```

This will select all attributes starting with `name`.

```bash
$ meltano select tap-carbon-intensity 'region'
```

This will select all attributes of the `region` entity.

::: tip
Most shells parse glob syntax: you must escape the special characters in the select pattern by quoting the pattern.
:::

### Exclude Parameter

Use `--exclude` to exclude all attributes that match the filter.

::: info
Exclusion has precedence over inclusion. If an attribute is excluded, there is no way to include it back without removing the exclusion pattern first.
:::

## `ui`

- `meltano ui`: Start the Meltano UI.

## `upgrade`

Upgrade Meltano to the latest version.

This function will following process to upgrade Meltano:

- Run `pip install --upgrade meltano`
- Run the database migrations
- Send a [SIGHUP](http://docs.gunicorn.org/en/stable/signals.html#reload-the-configuration) to the process running under the `.meltano/run/gunicorn.pid`, thus restarting the workers

## `version`

It is used to check which version of Meltano you are using:

### How to use

```bash
meltano --version
```