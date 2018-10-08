============
 j2skaffold
============

A simple `skaffold <https://github.com/GoogleContainerTools/skaffold>`_ wrapper
with support for `jinja2 <http://jinja.pocoo.org>`_ templating.

Status
======

.. image:: https://secure.travis-ci.org/jkozera/j2skaffold.png?branch=master
   :target: http://travis-ci.org/jkozera/j2skaffold
.. image:: https://coveralls.io/repos/jkozera/j2skaffold/badge.png?branch=master
   :target: https://coveralls.io/r/jkozera/j2skaffold?branch=master
.. image:: https://img.shields.io/pypi/v/j2skaffold.svg
   :target: https://pypi.python.org/pypi/j2skaffold
.. image:: https://readthedocs.org/projects/j2skaffold/badge/?version=latest
   :target: https://readthedocs.org/projects/j2skaffold/?badge=latest
   :alt: Documentation Status


Requirements
============

* Python 2.7 or Python 3.3+ or PyPy 2.4.0+

Setup
=====

::

  $ python -m pip install --user j2skaffold
  or
  (venv)$ python -m pip install j2skaffold

Usage
=====

::

  $ j2skaffold dev

will run ``skaffold dev`` after rendering the ``skaffold.jinja2`` file from the
current directory.

::

  $ j2skaffold dev --keep-yaml

will do the same, keeping the rendered ``skaffold.yaml`` file. (Useful for debugging.)


The following special variables are available:

- ``skaffold_command`` (``dev``, ``build``, etc.)
- ``current_profile`` (value of the ``-p`` argument)

The following special yaml key can be used:

- ``_set_profile: [name]`` - sets the current profile using the ``-p``
  argument. Should be always wrapped inside some
  ``{% if not current_profile %}``, otherwise it will get passed through,
  and ``skaffold`` will fail with:

::

  FATA[0000] creating runner: reading configuration: parsing skaffold config: parsing skaffold config: yaml: unmarshal errors:
  line 2: field _set_profile not found in type v1alpha3.SkaffoldConfig


Example ``skaffold.jinja2`` demonstrating all the available features:

::

  {% if skaffold_command == 'dev' and not current_profile %}
  _set_profile: dev
  {% endif %}
  apiVersion: skaffold/v1alpha3
  kind: Config
  build:
    artifacts:
    - imageName: gcr.io/k8s-skaffold/skaffold-example-{{ current_profile }}
  deploy:
    kubectl:
      manifests:
        - k8s-*
  profiles:
  {% for profile in ['dev', 'production'] %}
    - name: {{ profile }}
      # ... use any jinja2 syntax
  {% endfor %}

