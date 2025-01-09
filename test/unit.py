import unittest
from pathlib import Path

from qsave import QuickSave


test_db = QuickSave(Path(__file__).resolve().parent / "tests.json")


class QuickSaveTests(unittest.TestCase):
    def setUp(self):
        with test_db.session() as session:
            session.clear()

    def test_initial_state(self):
        with test_db.session() as session:
            self.assertEqual(len(session), 0)

    def test_commit(self):
        with test_db.session() as session:
            for index, value in enumerate(range(100, 110), 1):
                session[f"key_{index}"] = value
            self.assertEqual(len(session), 0)
            session.commit()
            self.assertGreater(len(session), 9)

    def test_rollback(self):
        with test_db.session() as session:
            session["rollback_this"] = "i will disappear"
            session.rollback()
            session.pop("key_1")
            session.pop("key_2")
            session.commit()
            self.assertLess(len(session), 9)

    def test_cases(self):
        with test_db.session() as session:
            session["some_key"] = "some_val"
            session.commit()
            self.assertTrue("some_key" in session)

    def test_closed_session(self):
        with test_db.session() as session:
            pass
        with self.assertRaises(ValueError):
            session.clear()


if __name__ == "__main__":
    unittest.main()
