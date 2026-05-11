import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import import_posts


SCHEMA_PATH = Path(__file__).resolve().parents[2] / "application" / "schema.sql"


def _make_db():
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    conn = sqlite3.connect(db_path)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    return db_path, conn


def _write_draft(directory, name, slug, title="A Post", date="2026-05-10",
                 categories="blog", body="Body."):
    path = Path(directory) / name
    path.write_text(
        f"---\nslug: {slug}\ntitle: {title}\npublish_date: {date}\n"
        f"categories: {categories}\n---\n{body}\n",
        encoding="utf-8",
    )
    return path


class ParsePostTests(unittest.TestCase):
    def test_with_leading_separator(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("---\nslug: foo\ntitle: Foo\n---\nBody here.\n")
            path = f.name
        try:
            metadata, content = import_posts.parse_post(path)
            self.assertEqual(metadata["slug"], "foo")
            self.assertEqual(metadata["title"], "Foo")
            self.assertEqual(content, "Body here.")
        finally:
            os.unlink(path)

    def test_without_leading_separator(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("slug: foo\ntitle: Foo\n---\nBody here.\n")
            path = f.name
        try:
            metadata, content = import_posts.parse_post(path)
            self.assertEqual(metadata["slug"], "foo")
            self.assertEqual(content, "Body here.")
        finally:
            os.unlink(path)

    def test_missing_separator_raises(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("---\nslug: foo\ntitle: Foo\nNo closer.\n")
            path = f.name
        try:
            with self.assertRaises(Exception):
                import_posts.parse_post(path)
        finally:
            os.unlink(path)


class NormalizePublishDateTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(
            import_posts.normalize_publish_date("2026-05-10"),
            "2026-05-10 00:00:00",
        )

    def test_invalid_raises(self):
        with self.assertRaises(ValueError):
            import_posts.normalize_publish_date("May 10, 2026")


class GetCategoryIdTests(unittest.TestCase):
    def setUp(self):
        self.db_path, self.conn = _make_db()

    def tearDown(self):
        self.conn.close()
        os.unlink(self.db_path)

    def test_creates_when_missing(self):
        cat_id = import_posts.get_category_id(self.conn, "newcat")
        self.assertIsNotNone(cat_id)
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM categories WHERE id = ?", (cat_id,))
        self.assertEqual(cur.fetchone()[0], "newcat")

    def test_returns_existing(self):
        first = import_posts.get_category_id(self.conn, "blog")
        second = import_posts.get_category_id(self.conn, "blog")
        self.assertEqual(first, second)


class ImportPostTests(unittest.TestCase):
    def setUp(self):
        self.db_path, self.conn = _make_db()
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        self.conn.close()
        os.unlink(self.db_path)
        for f in Path(self.tmpdir).iterdir():
            f.unlink()
        os.rmdir(self.tmpdir)

    def test_insert_new_post(self):
        draft = _write_draft(self.tmpdir, "hello.md", slug="hello",
                             categories="blog, recipe")
        import_posts.import_post(draft, self.conn)
        cur = self.conn.cursor()
        cur.execute("SELECT title FROM posts WHERE slug='hello'")
        self.assertEqual(cur.fetchone()[0], "A Post")
        cur.execute(
            "SELECT COUNT(*) FROM post_categories pc "
            "JOIN posts p ON p.id = pc.post_id WHERE p.slug='hello'"
        )
        self.assertEqual(cur.fetchone()[0], 2)

    def test_update_replaces_categories(self):
        draft1 = _write_draft(self.tmpdir, "hello.md", slug="hello",
                              categories="blog, recipe")
        import_posts.import_post(draft1, self.conn)
        draft2 = _write_draft(self.tmpdir, "hello2.md", slug="hello",
                              title="Updated", categories="til")
        import_posts.import_post(draft2, self.conn)
        cur = self.conn.cursor()
        cur.execute("SELECT title FROM posts WHERE slug='hello'")
        self.assertEqual(cur.fetchone()[0], "Updated")
        cur.execute(
            "SELECT c.name FROM categories c "
            "JOIN post_categories pc ON pc.category_id = c.id "
            "JOIN posts p ON p.id = pc.post_id WHERE p.slug='hello'"
        )
        names = sorted(r[0] for r in cur.fetchall())
        self.assertEqual(names, ["til"])

    def test_slug_with_leading_slash_raises(self):
        draft = _write_draft(self.tmpdir, "bad.md", slug="/badslug")
        with self.assertRaises(ValueError):
            import_posts.import_post(draft, self.conn)

    def test_missing_slug_raises(self):
        draft = Path(self.tmpdir) / "noslug.md"
        draft.write_text(
            "---\ntitle: No Slug\npublish_date: 2026-05-10\n---\nBody.\n",
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            import_posts.import_post(draft, self.conn)


class CollectDraftsTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        for f in Path(self.tmpdir).rglob("*"):
            if f.is_file():
                f.unlink()
        for d in sorted(Path(self.tmpdir).rglob("*"), reverse=True):
            if d.is_dir():
                d.rmdir()
        os.rmdir(self.tmpdir)

    def test_returns_md_only_sorted(self):
        (Path(self.tmpdir) / "b.md").write_text("x", encoding="utf-8")
        (Path(self.tmpdir) / "a.md").write_text("x", encoding="utf-8")
        (Path(self.tmpdir) / "ignore.txt").write_text("x", encoding="utf-8")
        result = import_posts.collect_drafts(self.tmpdir)
        names = [p.name for p in result]
        self.assertEqual(names, ["a.md", "b.md"])

    def test_no_recursion(self):
        sub = Path(self.tmpdir) / "sub"
        sub.mkdir()
        (sub / "nested.md").write_text("x", encoding="utf-8")
        (Path(self.tmpdir) / "top.md").write_text("x", encoding="utf-8")
        result = import_posts.collect_drafts(self.tmpdir)
        names = [p.name for p in result]
        self.assertEqual(names, ["top.md"])


class MoveToImportedTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.imported = Path(self.tmpdir) / "imported"
        self.imported.mkdir()

    def tearDown(self):
        for f in Path(self.tmpdir).rglob("*"):
            if f.is_file():
                f.unlink()
        for d in sorted(Path(self.tmpdir).rglob("*"), reverse=True):
            if d.is_dir():
                d.rmdir()
        os.rmdir(self.tmpdir)

    def test_moves_with_timestamp(self):
        draft = Path(self.tmpdir) / "foo.md"
        draft.write_text("x", encoding="utf-8")
        dest = import_posts.move_to_imported(draft, self.imported)
        self.assertFalse(draft.exists())
        self.assertTrue(dest.exists())
        self.assertTrue(dest.name.startswith("foo."))
        self.assertTrue(dest.name.endswith(".md"))

    def test_collision_raises(self):
        draft = Path(self.tmpdir) / "foo.md"
        draft.write_text("x", encoding="utf-8")
        fixed = "20260510-213500"
        with patch("scripts.import_posts.datetime") as mock_dt:
            mock_dt.datetime.now.return_value.strftime.return_value = fixed
            import_posts.move_to_imported(draft, self.imported)
            draft.write_text("y", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                import_posts.move_to_imported(draft, self.imported)


class DumpDatabaseTests(unittest.TestCase):
    @patch("scripts.import_posts.subprocess.check_output")
    def test_invokes_docker(self, mock_check_output):
        mock_check_output.return_value = "FAKE DUMP\n"
        with tempfile.TemporaryDirectory() as tmp:
            db_path = os.path.join(tmp, "blog.db")
            Path(db_path).touch()
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                import_posts.dump_database(db_path)
                args = mock_check_output.call_args[0][0]
                self.assertEqual(args[0], "docker")
                self.assertIn("sqlite3-compat", args)
                self.assertIn(".dump", args)
                with open("blog.sql", "r", encoding="utf-8") as f:
                    self.assertEqual(f.read(), "FAKE DUMP\n")
            finally:
                os.chdir(old_cwd)


class MainTests(unittest.TestCase):
    def setUp(self):
        self.db_path, self.conn = _make_db()
        self.conn.close()
        self.tmpdir = tempfile.mkdtemp()
        self.drafts = Path(self.tmpdir) / "drafts"
        self.drafts.mkdir()
        self.imported = Path(self.tmpdir) / "drafts-imported"

    def tearDown(self):
        os.unlink(self.db_path)
        for f in Path(self.tmpdir).rglob("*"):
            if f.is_file():
                f.unlink()
        for d in sorted(Path(self.tmpdir).rglob("*"), reverse=True):
            if d.is_dir():
                d.rmdir()
        os.rmdir(self.tmpdir)

    def _run_main(self, argv):
        old_cwd = os.getcwd()
        os.chdir(self.tmpdir)
        try:
            return import_posts.main(
                argv,
                db_path=self.db_path,
                drafts_dir=str(self.drafts),
                imported_dir=str(self.imported),
            )
        finally:
            os.chdir(old_cwd)

    @patch("scripts.import_posts.subprocess.check_output")
    def test_batch_imports_all_and_moves(self, mock_check_output):
        mock_check_output.return_value = "FAKE\n"
        _write_draft(self.drafts, "a.md", slug="post-a")
        _write_draft(self.drafts, "b.md", slug="post-b")

        rc = self._run_main([])

        self.assertEqual(rc, 0)
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT slug FROM posts ORDER BY slug")
        self.assertEqual([r[0] for r in cur.fetchall()],
                         ["post-a", "post-b"])
        conn.close()

        moved = sorted(self.imported.iterdir())
        self.assertEqual(len(moved), 2)
        self.assertEqual(mock_check_output.call_count, 1)

    @patch("scripts.import_posts.subprocess.check_output")
    def test_single_path_imports_just_that_file(self, mock_check_output):
        mock_check_output.return_value = "FAKE\n"
        draft = _write_draft(self.drafts, "solo.md", slug="solo-post")
        _write_draft(self.drafts, "other.md", slug="other-post")

        rc = self._run_main([str(draft)])

        self.assertEqual(rc, 0)
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT slug FROM posts ORDER BY slug")
        self.assertEqual([r[0] for r in cur.fetchall()], ["solo-post"])
        conn.close()

        moved = sorted(self.imported.iterdir())
        self.assertEqual(len(moved), 1)

    @patch("scripts.import_posts.subprocess.check_output")
    def test_abort_keeps_committed_skips_remaining_no_dump_no_move(
        self, mock_check_output
    ):
        mock_check_output.return_value = "FAKE\n"
        _write_draft(self.drafts, "a.md", slug="a")
        bad = self.drafts / "b.md"
        bad.write_text("---\nslug: b\ntitle: B\nno-closer\n", encoding="utf-8")
        _write_draft(self.drafts, "c.md", slug="c")

        rc = self._run_main([])

        self.assertEqual(rc, 1)
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT slug FROM posts ORDER BY slug")
        slugs = [r[0] for r in cur.fetchall()]
        conn.close()
        self.assertEqual(slugs, ["a"])

        self.assertFalse(self.imported.exists() and any(self.imported.iterdir()))
        mock_check_output.assert_not_called()


if __name__ == "__main__":
    unittest.main()
