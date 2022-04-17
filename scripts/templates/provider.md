## {{provider_name}}

{{provider_desc}}

{% for type in types %}
### {{type.__name__}}

{{type.__doc__}}

- type = "{{type | type_token}}"
{%- for prop in type | required_parameters %}
- {{prop.name}}[`{{prop.doc_type or prop.type}}`] **required** {% if prop.secret %}*Secret*{% endif %}{{prop | prop_help}}
{%- endfor %}
{%- for prop in type | optional_parameters %}
- {{prop.name}}[`{{prop.doc_type or prop.type}}`] *(default: `{{prop.default}}`)* {% if prop.secret %}*Secret*{% endif %}{{prop | prop_help}}
{%- endfor %}
{% endfor %}

