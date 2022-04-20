## {{provider_name}}

{{provider_desc}}

{% for type in types %}
### {{type.__name__}}

{{type.__doc__ | format_docstring}}


| field name | type | value | secret  | doc |
| ---        | ---  | --- | ---     | --- |
| type       |  | "{{type | type_token}}" | | |
{%- for prop in type | required_parameters %}
| {{prop.name}} | `{{prop | get_type}}`| **required** | {% if prop.secret %}*Secret*{% endif %} | {{prop.doc_help }} |
{%- endfor %}
{%- for prop in type | optional_parameters %}
| {{prop.name}} | `{{prop | get_type}}`| *default: `{{prop.default}}`* | {% if prop.secret %}*Secret*{% endif %} | {{prop.doc_help}} |
{%- endfor %}

{% endfor %}


