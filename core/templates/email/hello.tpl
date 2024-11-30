{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account Activation

{% endblock %}

{% block html %}
Token {{token}}
{% endblock %}