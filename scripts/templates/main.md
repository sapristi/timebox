# Configuration file

Timebox is configured with a yaml file. The file can have two top-level fields:
- `backups`: mapping of `Backup` (by name). Configuration for what to back-up, and where it should be stored.
- `config`: shared configuration values. If not provided, the default values will be used.

## Backup

{% for prop in backup_type | required_parameters %}
- {{prop.name}}[`{{prop.doc_type or prop.type}}`] **required** {{prop | prop_help}}
{%- endfor %}
{%- for prop in backup_type | optional_parameters %}
- {{prop.name}}[`{{prop.doc_type or prop.type}}`] (default: `{{prop.default}}`) {{prop | prop_help}}
{%- endfor %}

## Config

{% for prop in config_type | required_parameters %}
- {{prop.name}}[`{{prop.doc_type or prop.type}}`] **required** {{prop | prop_help}}
{%- endfor %}
{%- for prop in config_type | optional_parameters %}
- {{prop.name}}[`{{prop.doc_type or prop.type}}`] (default: `{{prop.default}}`) {{prop | prop_help}}
{%- endfor %}

## PostOp

Post operations are program to which the data creted by InputProviders is piped to. Most common usage are compression and encryption.

{% for prop in postop_type | required_parameters %}
- {{prop.name}}[`{{prop.doc_type or prop.type}}`] **required** {{prop | prop_help}}
{%- endfor %}
{%- for prop in postop_type | optional_parameters %}
- {{prop.name}}[`{{prop.doc_type or prop.type}}`] (default: `{{prop.default}}`) {{prop | prop_help}}
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
