import os
import tempfile
import unittest

from j2skaffold import templating


class TemplatingTest(unittest.TestCase):

    def _test_render(self, input, output):

        with tempfile.NamedTemporaryFile() as f:
            os.chdir(os.path.dirname(f.name))
            f.write(input)
            f.flush()
            out_name = f.name + '.yaml'
            with templating.render(
                os.path.basename(f.name), out_name, {'cmd': 'test'}
            )['manager']:
                with open(out_name, 'r') as f_out:
                    result = f_out.read()
                self.assertEqual(result, output)
            self.assertFalse(os.path.exists(out_name))

    def test_simple_render(self):
        self._test_render(b'foo: {{ cmd }}', 'foo: test')
