import json
from pathlib import Path
import tempfile
import unittest

from inputkit import convert, load_corpus, read_table


class InputTests(unittest.TestCase):
    def test_corpus_references_and_types(self):
        tables = load_corpus(Path(__file__).resolve().parents[1] / "data")
        self.assertGreaterEqual(len(tables), 5)
        self.assertTrue(all(tables.values()))

    def test_empty_is_distinct_from_zero(self):
        definition = {"name": "amount", "type": "int", "nullable": True}
        self.assertIsNone(convert("", definition))
        self.assertEqual(convert("0", definition), 0)
        with self.assertRaises(ValueError):
            convert("", {**definition, "nullable": False})

    def test_nonfinite_float_is_rejected(self):
        for value in ("nan", "inf", "-inf"):
            with self.assertRaises(ValueError):
                convert(value, {"name": "number", "type": "float", "nullable": False})

    def test_timestamp_requires_timezone(self):
        column = {"name": "at", "type": "datetime", "nullable": False}
        with self.assertRaises(ValueError):
            convert("2026-08-01T10:00:00", column)
        self.assertIsNotNone(convert("2026-08-01T10:00:00+08:00", column).tzinfo)

    def test_invalid_csv_is_rejected(self):
        definition = {"primary_key": "id", "columns": [{"name": "id", "type": "str", "nullable": False}, {"name": "count", "type": "int", "nullable": False}]}
        for body in ("count,id\n1,a\n", "id,count\na,1\na,2\n", "id,count\na,1,extra\n", "id,count\na\n"):
            with tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "rows.csv"
                path.write_text(body, encoding="utf-8")
                with self.assertRaises(ValueError):
                    read_table(path, definition)

    def test_text_csv_preserves_delimiters(self):
        definition = {"primary_key": "id", "columns": [{"name": "id", "type": "str", "nullable": False}, {"name": "text", "type": "str", "nullable": False}]}
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "rows.csv"
            path.write_text('id,text\na,"中文,保留"\n', encoding="utf-8")
            self.assertEqual(read_table(path, definition)[0]["text"], "中文,保留")


if __name__ == "__main__":
    unittest.main()
