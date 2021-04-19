{% raw %}#!/bin/bash

#{% if cookiecutter.jwt_secret == "random" %}
#{{ cookiecutter.update({"jwt_secret": random_ascii_string(128) }) }}
#{% endif %}

echo "Generated JWT Secret {{ cookiecutter.jwt_secret }}'."
{% endraw %}