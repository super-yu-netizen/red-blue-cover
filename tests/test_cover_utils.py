import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "cover_utils.py"


class CoverUtilsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def image(self, name, size):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", size, "#173653").save(path)
        return path

    def run_cli(self, *args):
        env = dict(os.environ)
        env.pop("RED_BLUE_COVER_PHOTOS", None)
        process = subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            capture_output=True, text=True, env=env,
        )
        return process.returncode, json.loads(process.stdout)

    def test_check_correct_ratios_and_preserves_sources(self):
        for name, size, aspect in [("wide.png", (400, 300), "4:3"), ("tall.png", (300, 400), "3:4")]:
            path = self.image(name, size)
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            code, report = self.run_cli("check", path, "--aspect", aspect, "--review-dir", self.root / "review")
            self.assertEqual(code, 0)
            self.assertTrue(report["aspect_ok"])
            self.assertEqual(report["display_size"], list(size))
            self.assertTrue(Path(report["preview"]).is_file())
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before)

    def test_wrong_aspect_returns_one(self):
        path = self.image("wide.png", (400, 300))
        code, report = self.run_cli("check", path, "--aspect", "3:4")
        self.assertEqual(code, 1)
        self.assertFalse(report["aspect_ok"])

    def test_invalid_aspect_returns_input_error(self):
        path = self.image("wide.png", (400, 300))
        for aspect in ["0:3", "4:0", "broken", "4:3:2"]:
            code, report = self.run_cli("check", path, "--aspect", aspect)
            self.assertEqual(code, 2)
            self.assertIn("error", report)

    def test_unreadable_input_returns_input_error(self):
        path = self.root / "broken.png"
        path.write_bytes(b"not a valid image")
        code, report = self.run_cli("check", path)
        self.assertEqual(code, 2)
        self.assertIn("error", report)

    def test_requires_explicit_library(self):
        code, report = self.run_cli("photos")
        self.assertEqual(code, 2)
        self.assertIn("--library", report["error"])

    def test_exclusion_cache_and_deleted_photo(self):
        library, cache = self.root / "photos", self.root / "cache"
        first = self.image("photos/allowed-a.png", (100, 150))
        second = self.image("photos/allowed-b.png", (100, 150))
        blocked = self.image("photos/do-not-use.png", (100, 150))
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [first, second, blocked]}
        args = ("photos", "--library", library, "--cache-dir", cache, "--exclude", "do-not-*")
        code, result = self.run_cli(*args)
        self.assertEqual(code, 0)
        self.assertEqual(result["count"], 2)
        manifest = json.loads(Path(result["manifest"]).read_text())
        self.assertNotIn(str(blocked), [entry["path"] for entry in manifest["photos"]])
        self.assertTrue(Path(result["sheet"]).is_file())
        code, cached = self.run_cli(*args)
        self.assertEqual(code, 0)
        self.assertTrue(cached["cached"])
        for path in [first, second, blocked]:
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before[path.name])
        second.unlink()
        code, changed = self.run_cli(*args)
        self.assertEqual(code, 0)
        self.assertEqual(changed["count"], 1)
        self.assertNotEqual(changed["manifest"], result["manifest"])

    def test_empty_library_after_exclusion(self):
        self.image("photos/skip.png", (100, 150))
        code, report = self.run_cli("photos", "--library", self.root / "photos", "--exclude", "*")
        self.assertEqual(code, 2)
        self.assertIn("No supported photos", report["error"])


if __name__ == "__main__":
    unittest.main()

