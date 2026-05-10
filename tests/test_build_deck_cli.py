import unittest

import build_deck


class BuildDeckCliTests(unittest.TestCase):
    def test_skip_png_export_disables_contact_sheet_generation(self):
        options = build_deck.parse_args(["--skip-png-export"])

        self.assertTrue(options.skip_png_export)
        self.assertTrue(options.skip_contact_sheet)


if __name__ == "__main__":
    unittest.main()
