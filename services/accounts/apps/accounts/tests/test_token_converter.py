import re

from django.test import TestCase

from ..urls import TokenConverter


class TokenConverterTest(TestCase):
    def test_if_regex_is_matching_valid_token(self):
        pattern = re.compile(TokenConverter.regex)
        self.assertTrue(pattern.match("a9dfbde116af89e8a4ec46ce4e7fe94381dcd899"))
