# Configuration file

Timebox is configured with a yaml file. The file can have two top-level fields:
- `backups`: mapping of `Backup` (by name). Configuration for what to back-up, and where it should be stored.
- `config`: shared configuration values. If not provided, the default values will be used.

## Backup

| field name | type | value | doc |
| ---        | ---  | --- | --- |
{%- for prop in backup_type | required_parameters %}
| {{prop.name}} | `{{prop | get_type}}`| **required** | {{prop.doc_help }} |
{%- endfor %}
{%- for prop in backup_type | optional_parameters %}
| {{prop.name}} | `{{prop | get_type}}`| *default: `{{prop.default}}`* |  {{prop.doc_help}} |
{%- endfor %}

## Config

| field name | type | value | doc |
| ---        | ---  | --- |  --- |
{%- for prop in config_type | required_parameters %}
| {{prop.name}} | `{{prop | get_type}}`| **required** | {{prop.doc_help }} |
{%- endfor %}
{%- for prop in config_type | optional_parameters %}
| {{prop.name}} | `{{prop | get_type}}`| *default: `{{prop.default}}`* |  {{prop.doc_help}} |
{%- endfor %}

## PostOp

Post operations are program to which the data creted by InputProviders is piped to. Most common usage are compression and encryption.

| field name | type | value | doc |
| ---        | ---  | --- |  --- |
{%- for prop in postop_type | required_parameters %}
| {{prop.name}} | `{{prop | get_type}}`| **required** | {{prop.doc_help }} |
{%- endfor %}
{%- for prop in postop_type | optional_parameters %}
| {{prop.name}} | `{{prop | get_type}}`| *default: `{{prop.default}}`* |  {{prop.doc_help}} |
{%- endfor %}

## Providers 

See [the dedicated page](/docs/providers.md)

# Examples

{% for name, content in examples %}
## {{name}}

```yaml
{{content}}
```
{% endfor %}
