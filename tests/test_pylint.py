import unittest
from subprocess import Popen, PIPE


class ProductTestCase(unittest.TestCase):

    def test_with_PyLint(self):
        cmd = 'pylint', '-rn', '../sparrow_player'
        pylint = Popen(cmd, stdout=PIPE, stderr=PIPE)
        self.assertEqual(pylint.stdout.read(), '')


if __name__ == '__main__':
    unittest.main()
