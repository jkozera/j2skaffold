import argparse
import subprocess
import sys

from j2skaffold import templating


def main():
    if len(sys.argv) < 2:
        sys.exit(subprocess.call(['skaffold']))
    elif '--help' in sys.argv or '-h' in sys.argv:
        # pass `help` through to skaffold
        sys.exit(subprocess.call(['skaffold', '--help']))
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('command', type=str)
        parser.add_argument('-p', '--profile')
        parser.add_argument('--keep-yaml', action='store_true')
        options = parser.parse_args()
        command = options.command
        profile = options.profile
        if options.keep_yaml:
            sys.argv.remove('--keep-yaml')
        result = templating.render(
            'skaffold.jinja2', 'skaffold.yaml',
            variables={
                'skaffold_command': command,
                'current_profile': profile
            },
            keep_yaml=options.keep_yaml
        )
        with result['manager']:
            if result['profile']:
                sys.argv += ['-p', result['profile']]
            sys.exit(subprocess.call(['skaffold'] + sys.argv[1:]))
