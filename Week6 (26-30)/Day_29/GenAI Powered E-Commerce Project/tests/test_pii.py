import unittest

from app.security.pii import sanitize_text_for_llm


class PiiSanitizerTests(unittest.TestCase):
    def test_masks_email_phone_and_ssn(self) -> None:
        text = (
            "Email me at alice.smith@example.com, call (555) 123-4567, "
            "and note SSN 123-45-6789."
        )

        result = sanitize_text_for_llm(text)

        self.assertNotIn("alice.smith@example.com", result.sanitized_text)
        self.assertNotIn("(555) 123-4567", result.sanitized_text)
        self.assertNotIn("123-45-6789", result.sanitized_text)
        self.assertIn("<EMAIL_ADDRESS>", result.sanitized_text)
        self.assertIn("<PHONE_NUMBER>", result.sanitized_text)
        self.assertIn("<US_SSN>", result.sanitized_text)

    def test_leaves_non_pii_text_unchanged(self) -> None:
        text = "Find me a protein bar under 20 dollars."

        result = sanitize_text_for_llm(text)

        self.assertEqual(text, result.sanitized_text)
        self.assertFalse(result.detected_entities)


if __name__ == "__main__":
    unittest.main()
