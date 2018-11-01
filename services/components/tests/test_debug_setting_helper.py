from unittest import TestCase, main

from settings.helpers import get_debug


class DebugSettingTest(TestCase):

    def test_debug_on(self):
        self.assertEqual(True, get_debug('true'))

    def test_debug_off(self):
        for value in ('No', 'nO', 'N', 'n', 'false', 'False', 'off', 'oFF', 'Yes', 'YES', 'Y', 'On', '', '1', '0'):
            self.assertEqual(False, get_debug(value))


if __name__ == '__main__':
    main()
