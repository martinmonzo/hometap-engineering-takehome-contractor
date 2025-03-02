from django.test import TestCase

from parameterized import parameterized

from properties.exceptions.property import PropertyException

class PropertyExceptionsTests(TestCase):
    @parameterized.expand([
        (PropertyException.ErrorCode.Address_Required, 400),
        (PropertyException.ErrorCode.Unauthorized, 401),
        (PropertyException.ErrorCode.Unknown_Error, 500),
        # Add more exceptions if needed
    ])
    def test_error_code_statuses(self, error_code, expected_status_code):
        exception = PropertyException(error_code)

        self.assertEqual(exception.status_code, expected_status_code)
