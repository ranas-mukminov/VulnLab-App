import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lab"))
import fixed  # noqa: E402
import vuln  # noqa: E402


class TestSQLInjection(unittest.TestCase):
    def test_vuln_returns_all_on_injection(self):
        rows = vuln.search_users_vuln("' OR '1'='1")
        self.assertEqual(len(rows), 3)

    def test_fixed_returns_none_on_injection(self):
        rows = fixed.search_users_fixed("' OR '1'='1")
        self.assertEqual(rows, [])

    def test_fixed_finds_real_name(self):
        self.assertEqual(len(fixed.search_users_fixed("lab-alice")), 1)


class TestXSS(unittest.TestCase):
    def test_vuln_renders_raw_script(self):
        self.assertIn("<script>alert(1)</script>", vuln.render_greeting_vuln("<script>alert(1)</script>"))

    def test_fixed_escapes_script(self):
        out = fixed.render_greeting_fixed("<script>alert(1)</script>")
        self.assertNotIn("<script>", out)
        self.assertIn("&lt;script&gt;", out)


class TestIDOR(unittest.TestCase):
    def test_vuln_returns_others_record(self):
        self.assertEqual(vuln.get_record_vuln("lab-bob", "lab-alice"), "bob-lab-record")

    def test_fixed_blocks_others_record(self):
        with self.assertRaises(PermissionError):
            fixed.get_record_fixed("lab-bob", "lab-alice")

    def test_fixed_allows_own_record(self):
        self.assertEqual(fixed.get_record_fixed("lab-alice", "lab-alice"), "alice-lab-record")


if __name__ == "__main__":
    unittest.main()
