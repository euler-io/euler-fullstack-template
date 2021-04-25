{% raw %}#!/bin/bash

#{% if cookiecutter.jwt_secret == "random" %}
#{{ cookiecutter.update({"jwt_secret": random_ascii_string(128) }) }}
#{% endif %}

echo "Generated JWT Secret '{{ cookiecutter.jwt_secret }}'."

#{% if cookiecutter.admin_password == "random" %}
#{{ cookiecutter.update({"admin_password": random_ascii_string(12) }) }}
#{% endif %}

echo "Generated admin password '{{ cookiecutter.admin_password }}'."

#{% if cookiecutter.apiadmin_password == "random" %}
#{{ cookiecutter.update({"apiadmin_password": random_ascii_string(12) }) }}
#{% endif %}

echo "Generated apiadmin password '{{ cookiecutter.apiadmin_password }}'."
{% endraw %}

#{% if cookiecutter.kibana_password == "random" %}
#{{ cookiecutter.update({"kibana_password": random_ascii_string(12) }) }}
#{% endif %}

echo "Generated kibana password '{{ cookiecutter.kibana_password }}'."
{% endraw %}