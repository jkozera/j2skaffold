from __future__ import print_function
from contextlib import contextmanager
import os
import sys

import jinja2
import yaml


@contextmanager
def temp_write(path, contents, force=False, remove_file=True):
    if os.path.isfile(path) and not force:
        print('ERROR: {}: already exists.'.format(path), file=sys.stderr)
        sys.exit(1)

    ret = open(path, 'w')

    try:
        ret.write(contents)
        ret.close()
        yield ret
    finally:
        if remove_file:
            os.remove(path)


def render(in_name, out_name, variables, keep_yaml=False):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('.')
    )
    if not os.path.isfile(in_name):
        print('ERROR: {}: no such file.'.format(in_name), file=sys.stderr)
        sys.exit(1)
    tpl = env.get_template(in_name)
    rendered = tpl.render(**variables)
    contents = yaml.load(rendered)
    kwargs = {}
    if keep_yaml:
        kwargs['remove_file'] = False
    if '_set_profile' in contents:
        profile = contents['_set_profile']
        variables['current_profile'] = profile
        manager = temp_write(
            out_name, tpl.render(**variables), force=True, **kwargs
        )
        return {'manager': manager, 'profile': profile}
    return {'manager': temp_write(out_name, rendered, **kwargs),
            'profile': None}
