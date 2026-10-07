"""Exercise sealing and resuming through the installed CLI."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/songmai/scripts/songmai.py'


class SongmaiCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'งาน ตัวอย่าง'
        self.root.mkdir()
        self.file = self.root / 'หน้า เว็บ.py'
        self.file.write_text('private source content\n', encoding='utf-8')
        self.handoff = self.root / 'HANDOFF.md'
        self.handoff.write_text('## ไฟล์อ้างอิง\n- `หน้า เว็บ.py` — หน้าหลัก\n', encoding='utf-8')
        self.snapshot = self.root / 'HANDOFF.songmai.json'

    def run_cli(self, command, *args, root=None):
        workspace = root or self.root
        return subprocess.run(
            [sys.executable, str(SCRIPT), command, str(workspace/'HANDOFF.md'), *args],
            capture_output=True, text=True, encoding='utf-8', cwd=self.temp.name,
        )

    def seal(self):
        result = self.run_cli('seal')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def test_seal_is_portable_and_resume_is_read_only(self):
        before = self.file.read_bytes()
        self.seal()
        saved = self.snapshot.read_text(encoding='utf-8')
        self.assertNotIn('private source content', saved)
        self.assertNotIn(str(self.root), saved)
        self.assertEqual(self.file.read_bytes(), before)
        moved = Path(self.temp.name) / 'ย้ายงาน'
        shutil.copytree(self.root, moved)
        before_resume = {p.name: p.read_bytes() for p in moved.iterdir()}
        result = self.run_cli('resume', root=moved)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('UNCHANGED', result.stdout)
        self.assertEqual({p.name: p.read_bytes() for p in moved.iterdir()}, before_resume)

    def test_resume_detects_content_change_even_with_same_size_and_mtime(self):
        self.seal()
        stat = self.file.stat()
        self.file.write_text('changed source content\n', encoding='utf-8')
        self.assertEqual(self.file.stat().st_size, stat.st_size)
        os.utime(self.file, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        result = self.run_cli('resume')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('CHANGED: หน้า เว็บ.py', result.stdout)
        self.assertIn('ตรวจใหม่', result.stdout)
        self.assertNotIn('UNCHANGED:', result.stdout)

    @unittest.skipUnless(shutil.which('git'), 'git unavailable')
    def test_git_detects_branch_commit_and_dirty_changes_without_storing_patch(self):
        def git(*args):
            return subprocess.run(['git', '-C', str(self.root), *args], check=True,
                                  capture_output=True, text=True, encoding='utf-8')
        git('init')
        git('config', 'user.name', 'Songmai Test')
        git('config', 'user.email', 'songmai@example.invalid')
        other = self.root / 'other.py'
        other.write_text('initial\n', encoding='utf-8')
        git('add', '.')
        git('commit', '-m', 'initial')
        # Dirty before sealing: changing an already dirty file must still be detected.
        other.write_text('private uncommitted content\n', encoding='utf-8')
        self.seal()
        self.assertNotIn('private uncommitted content', self.snapshot.read_text(encoding='utf-8'))
        self.assertEqual(self.run_cli('resume').returncode, 0)
        other.write_text('private uncommitted content   \n', encoding='utf-8')
        result = self.run_cli('resume')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('GIT_WORKTREE_CHANGED', result.stdout)
        git('switch', '-c', 'next-agent')
        result = self.run_cli('resume')
        self.assertEqual(result.returncode, 1)
        self.assertIn('GIT_BRANCH_CHANGED', result.stdout)
        git('add', 'other.py')
        git('commit', '-m', 'later')
        self.assertIn('GIT_HEAD_CHANGED', self.run_cli('resume').stdout)

    def test_resealing_is_explicit_and_never_overwrites_project_files(self):
        self.seal()
        original = self.snapshot.read_bytes()
        self.file.write_text('new content\n', encoding='utf-8')
        refused = self.run_cli('seal')
        self.assertEqual(refused.returncode, 1)
        self.assertEqual(self.snapshot.read_bytes(), original)
        result = self.run_cli('seal', '--replace')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.run_cli('resume').returncode, 0)
        self.assertEqual(self.file.read_text(encoding='utf-8'), 'new content\n')

    def test_invalid_snapshots_never_report_unchanged(self):
        self.seal()
        saved = json.loads(self.snapshot.read_text(encoding='utf-8'))
        malformed = [[], {'version': 99}, dict(saved, version=True),
                     {key: value for key, value in saved.items() if key != 'git'},
                     dict(saved, files=[]), dict(saved, handoff_sha256='bad'),
                     dict(saved, git={'branch': 'main'})]
        for value in malformed:
            with self.subTest(value=value):
                self.snapshot.write_text(json.dumps(value), encoding='utf-8')
                result = self.run_cli('resume')
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn('FAIL:', result.stdout)
                self.assertNotIn('UNCHANGED:', result.stdout)
                self.assertNotIn('Traceback', result.stderr)

    def test_document_reference_changes_and_missing_files_require_review(self):
        self.seal()
        self.handoff.write_text(self.handoff.read_text(encoding='utf-8') + '\n## งานถัดไป\nเปลี่ยนเป้าหมาย\n', encoding='utf-8')
        result = self.run_cli('resume')
        self.assertEqual(result.returncode, 1)
        self.assertIn('HANDOFF_CHANGED', result.stdout)
        self.file.unlink()
        result = self.run_cli('resume')
        self.assertEqual(result.returncode, 1)
        self.assertIn('missing file: หน้า เว็บ.py', result.stdout)
        self.assertNotIn('UNCHANGED:', result.stdout)

    def test_unsealed_and_unsafe_inputs_fail_without_writing(self):
        result = self.run_cli('resume')
        self.assertEqual(result.returncode, 1)
        self.assertIn('UNSEALED', result.stdout)
        self.assertFalse(self.snapshot.exists())
        self.handoff.write_text('## ไฟล์อ้างอิง\n- `../private.txt`\n', encoding='utf-8')
        result = self.run_cli('seal')
        self.assertEqual(result.returncode, 1)
        self.assertIn('unsafe path', result.stdout)
        self.assertFalse(self.snapshot.exists())

    def test_snapshot_cannot_reference_itself_or_replace_an_unrelated_file(self):
        self.seal()
        original = self.snapshot.read_bytes()
        self.handoff.write_text('## ไฟล์อ้างอิง\n- `HANDOFF.songmai.json`\n', encoding='utf-8')
        result = self.run_cli('seal', '--replace')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('snapshot cannot be a file reference', result.stdout)
        self.assertEqual(self.snapshot.read_bytes(), original)
        self.handoff.write_text('## ไฟล์อ้างอิง\n- `หน้า เว็บ.py`\n', encoding='utf-8')
        self.snapshot.write_text('unrelated user data\n', encoding='utf-8')
        result = self.run_cli('seal', '--replace')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.snapshot.read_text(encoding='utf-8'), 'unrelated user data\n')

    def test_explicit_root_and_snapshot_symlink(self):
        (self.root/'docs').mkdir()
        original = self.handoff
        self.handoff = self.root/'docs/HANDOFF.md'
        original.rename(self.handoff)
        self.snapshot = self.handoff.with_suffix('.songmai.json')
        result = subprocess.run([sys.executable, str(SCRIPT), 'seal', str(self.handoff), '--root', str(self.root)],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        result = subprocess.run([sys.executable, str(SCRIPT), 'resume', str(self.handoff), '--root', str(self.root)],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        outside = Path(self.temp.name)/'outside.json'
        outside.write_bytes(self.snapshot.read_bytes())
        before = outside.read_bytes()
        self.snapshot.unlink()
        try:
            self.snapshot.symlink_to(outside)
        except OSError as error:
            self.skipTest(f'symlink permission unavailable: {error}')
        for command in ('seal', 'resume'):
            result = subprocess.run([sys.executable, str(SCRIPT), command, str(self.handoff), '--root', str(self.root)],
                                    capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 1)
            self.assertIn('snapshot must not be a symlink', result.stdout)
        self.assertEqual(outside.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
