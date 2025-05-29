#!/usr/bin/env python3

from utils import access_nested_map
import unittest
from parameterized import parameterized

""" Unit test for the function access_nested_map """

class TestAccessNestedMap(unittest.TestCase):
	
	""" Test cases for the access_nested_map fuction """

	@parameterized.expand([
		({"a": 1}, ("a",),1),
		({"a": {"b": 2}}, ("a",), {"b": 2}),
		({"a": {"b": 2}}, ("a", "b"),2),
		])
	
	def test_access_nested_map(self, nested_map, path, expected):

		""" Testing access_nested_map returns correct value for given path """

		self.assertEqual(access_nested_map(nested_map, path), expected)

	@parameterized.expand([
		({}, ("a",),),
		({"a": 1}, ("a", "b")),
	])
	def test_access_nested_map_exception(self, nested_map, path):
		""" Ensuring the correct error is raised """
		with self.assertRaises(KeyError) as context:
			access_nested_map(nested_map, path)

		self.assertEqual(str(context.exception), f"'{path[-1]}'")

class TestGetJson(unittest.TestCase):
	""" Mock tests for http calls """

	@parameterized.expad([
		("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
		])

	@patch('payload.requess.get')
	def test_get_json(self, test_url, tes_payload, mock_get):
		""" Tests that the correct json is returned """

		mock_get.return_value.json.return_value = test_payload
		result = get_json(test_url)
		self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
	""" Tests the result of memoize decorator """
	def test_memoize(self):
		""" Test that memoize caches the result of the method """
		class TestClass:
			def a_method(self) -> int:
				return 42

			@memoize
			def a_property(self) -> int:
				return self.a_method()

		with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
			test_instance = TestClass()

			# First call to a_property should call a_method
            result1 = test_instance.a_property()

            # Second call to a_property should use
            result2 = test_instance.a_property()

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()

if __name__ == "__main__":
    unittest.main()