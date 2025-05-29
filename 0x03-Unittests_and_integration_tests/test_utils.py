#!/usr/bin/env python3


"""
Unit tests for utility functions used across the project.

This module contains unit tests for the following functions:
- access_nested_map
- get_json
- memoize

Each function is tested using the unittest framework, with parameterized
tests where applicable. Mocking is used to simulate external behavior,
especially for HTTP requests.
"""

from utils import access_nested_map, get_json, memoize
import unittest
from unittest.mock import patch
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function"""

    @parameterized.expand([
        (
            {"a": 1},
            ("a", ),
            1,
        ),
        (
            {"a": {"b": 2}},
            ("a", ),
            {"b": 2},
        ),
        (
            {"a": {"b": 2}},
            ("a", "b"),
            2,
        )
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Testing that access_nested_map returns correct value"""
        self.assertEqual(
            access_nested_map(nested_map, path),
            expected
        )

    @parameterized.expand([
        (
            {},
            ("a", ),
        ),
        (
            {"a": 1},
            ("a", "b"),
        )
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Ensure that KeyError is raised for invalid paths"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        self.assertEqual(
            str(context.exception),
            f"'{path[-1]}'"
        )


class TestGetJson(unittest.TestCase):
    """
    Mock tests for HTTP GET requests using get_json function.
    Ensures that the get_json function correctly handles mocked responses
    and returns expected payloads.
    """

    @parameterized.expand([
        (
            "http://example.com",
            {"payload": True},
        ),
        (
            "http://holberton.io",
            {"payload": False},
        )
    ])
    @patch("requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """Tests that get_json returns the expected result from a
        mocked request"""
        mock_get.return_value.json.return_value = test_payload
        result = get_json(test_url)
        self.assertEqual(
            result,
            test_payload
        )


class TestMemoize(unittest.TestCase):
    """
    Tests the behavior of the @memoize decorator.

    Ensures that a method decorated with @memoize is only called once,
    even when accessed multiple times on the same instance.
    """

    def test_memoize(self):
        """
        Test that the @memoize decorator caches the result of a method.

        Ensures that the method is only called once, even when accessed
        multiple times.
        """

        class TestClass:
            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                return self.a_method()

        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_method:
            test_instance = TestClass()

            # First call should invoke a_method
            result1 = test_instance.a_property

            # Second call should use cached value
            result2 = test_instance.a_property

            # Verify results
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure a_method was only called once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
