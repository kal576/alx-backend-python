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

from typing import Mapping, Sequence, Any
import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand([
        (
            {"a": 1},
            ("a",),
            1,
        ),
        (
            {"a": {"b": 2}},
            ("a",),
            {"b": 2},
        ),
        (
            {"a": {"b": 2}},
            ("a", "b"),
            2,
        )
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """Test that access_nested_map returns correct value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        (
            {},
            ("a",),
        ),
        (
            {"a": 1},
            ("a", "b"),
        )
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence) -> None:
        """Test that KeyError is raised for invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{path[-1]}'")


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
    def test_get_json(self, test_url: str, test_payload: dict, mock_get) -> None:
        """Test that get_json returns expected result from mocked request."""
        mock_get.return_value.json.return_value = test_payload
        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    Unit tests for the memoize decorator.

    Ensures that a method decorated with @memoize is only called once,
    even when accessed multiple times on the same instance.
    """

    def test_memoize(self) -> None:
        """
        Test that the @memoize decorator caches the result of a method.

        Ensures that the method is only called once, even when accessed
        multiple times.
        """

        class TestClass:
            """Test class with a memoized property."""

            def a_method(self) -> int:
                """Returns a constant integer."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Returns result of a_method, memoized."""
                return self.a_method()

        with patch.object(
            TestClass, "a_method", return_value=42
        ) as mock_method:
            test_instance = TestClass()
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
