"""Checks the public read-only CLI using real temporary workspaces."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_handoff.py'


class HandoffCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'งาน ตัวอย่าง'
        self.root.mkdir()
        self.handoff = self.root / 'HANDOFF.md'

    def run_check(self, text, *args):
        self.handoff.write_text(text, encoding='utf-8')
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.handoff), *args],
            capture_output=True, text=True, encoding='utf-8', cwd=self.temp.name,
        )

    def test_checks_thai_file_with_spaces_from_another_directory(self):
        target = self.root / 'หน้า เว็บ.py'
        target.write_text('print("hello")\n', encoding='utf-8')
        before = target.read_bytes()
        result = self.run_check('## ไฟล์อ้างอิง\n- `หน้า เว็บ.py` — หน้าหลัก\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('PASS: 1', result.stdout)
        self.assertEqual(target.read_bytes(), before)

    def test_rejects_unsafe_file_references(self):
        outside = Path(self.temp.name) / 'private.txt'
        outside.write_text('must not be read', encoding='utf-8')
        for path in ('../private.txt', str(outside), 'C:/private.txt', 'C:private.txt', '//server/share.txt'):
            with self.subTest(path=path):
                result = self.run_check(f'## ไฟล์อ้างอิง\n- `{path}`\n')
                self.assertEqual(result.returncode, 1)
                self.assertIn('unsafe path', result.stdout)
                self.assertNotIn('must not be read', result.stdout + result.stderr)

    def test_rejects_symlinks_outside_workspace(self):
        outside = Path(self.temp.name) / 'private.txt'
        outside.write_text('private', encoding='utf-8')
        try:
            (self.root / 'linked.txt').symlink_to(outside)
        except OSError as error:
            self.skipTest(f'symlink permission unavailable: {error}')
        result = self.run_check('## ไฟล์อ้างอิง\n- `linked.txt`\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn('outside workspace', result.stdout)

    def test_missing_file_is_reported(self):
        result = self.run_check('## ไฟล์อ้างอิง\n- `gone.py`\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn('gone.py', result.stdout)

    def test_rejects_directory_as_file(self):
        (self.root / 'src').mkdir()
        result = self.run_check('## ไฟล์อ้างอิง\n- `src`\n')
        self.assertEqual(result.returncode, 1)

    def test_rejects_missing_empty_duplicate_or_malformed_section(self):
        documents = (
            '# ไม่มีส่วนอ้างอิง\n',
            '## ไฟล์อ้างอิง\n\n## งานต่อไป\n- `fake.py`\n',
            '## ไฟล์อ้างอิง\n- ไม่มีไฟล์อ้างอิง\n## ไฟล์อ้างอิง\n- ไม่มีไฟล์อ้างอิง\n',
            '## ไฟล์อ้างอิง\n- missing-backticks.py\n',
            '## ไฟล์อ้างอิง\n- ``\n',
            '## ไฟล์อ้างอิง\n- `file.py` extra `second.py`\n',
            '## ไฟล์อ้างอิง\n- ไม่มีไฟล์อ้างอิง\n- `file.py`\n',
        )
        for document in documents:
            with self.subTest(document=document):
                result = self.run_check(document)
                self.assertEqual(result.returncode, 1)
                self.assertIn('FAIL:', result.stdout)
                self.assertNotIn('Traceback', result.stderr)

    def test_accepts_explicit_no_files(self):
        result = self.run_check('## ไฟล์อ้างอิง\n- ไม่มีไฟล์อ้างอิง\n')
        self.assertEqual(result.returncode, 0)
        self.assertIn('PASS: 0', result.stdout)

    def test_ignores_reference_heading_inside_code_fences(self):
        text = '```md\n## ไฟล์อ้างอิง\n- `fake.py`\n```\n## ไฟล์อ้างอิง\n- ไม่มีไฟล์อ้างอิง\n'
        result = self.run_check(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_explicit_root_with_handoff_in_a_subdirectory(self):
        (self.root / 'file.py').write_text('pass\n', encoding='utf-8')
        (self.root / 'docs').mkdir()
        self.handoff = self.root / 'docs/HANDOFF.md'
        result = self.run_check('## ไฟล์อ้างอิง\n- `file.py`\n', '--root', str(self.root))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_bad_inputs_fail_without_traceback(self):
        cases = (
            (b'\xff\xfe', ()),
            (b'## files\n', ()),
            ('## ไฟล์อ้างอิง\n- `bad\x00name`\n'.encode('utf-8'), ()),
            ('## ไฟล์อ้างอิง\n- ไม่มีไฟล์อ้างอิง\n'.encode('utf-8'), ('--root', str(self.root / 'gone'))),
        )
        for content, args in cases:
            with self.subTest(content=content, args=args):
                self.handoff.write_bytes(content)
                result = subprocess.run([sys.executable, str(SCRIPT), str(self.handoff), *args],
                                        capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(result.returncode, 1)
                self.assertIn('FAIL:', result.stdout)
                self.assertNotIn('Traceback', result.stderr)

    def test_bom_crlf_and_last_line_without_newline(self):
        self.handoff.write_bytes('\ufeff## ไฟล์อ้างอิง\r\n- ไม่มีไฟล์อ้างอิง'.encode('utf-8'))
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.handoff)],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_handoff_is_controlled(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.handoff)],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 1)
        self.assertIn('FAIL:', result.stdout)
        self.assertNotIn('Traceback', result.stderr)

    def test_help_and_invalid_usage(self):
        help_result = subprocess.run([sys.executable, str(SCRIPT), '--help'], capture_output=True)
        invalid = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True)
        self.assertEqual(help_result.returncode, 0)
        self.assertEqual(invalid.returncode, 2)





if __name__ == '__main__':
    unittest.main()
