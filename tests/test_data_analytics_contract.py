"""Executable semantic model contracts using disposable in-memory SQLite.

This is a grain/metric demonstration, NOT a warehouse cost/DDL test.
"""
import sqlite3
import unittest


class AnalyticsGrainTests(unittest.TestCase):
    def setUp(self) -> None:
        self.db = sqlite3.connect(":memory:")
        self.db.executescript("""
          CREATE TABLE fct_orders(
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            order_day TEXT NOT NULL,
            amount_minor INTEGER NOT NULL
          );
          CREATE TABLE dim_customer(
            version_id INTEGER PRIMARY KEY,
            customer_id TEXT NOT NULL,
            region TEXT NOT NULL,
            valid_from TEXT NOT NULL,
            valid_to TEXT NOT NULL,
            CHECK(valid_from < valid_to)
          );
          INSERT INTO fct_orders VALUES
            ('o1','A','2026-01-15',100),
            ('o2','A','2026-04-01',200),
            ('o3','B','2026-04-01',100);
          INSERT INTO dim_customer VALUES
            (1,'A','north','2026-01-01','2026-03-01'),
            (2,'A','south','2026-03-01','9999-12-31'),
            (3,'B','west','2026-01-01','9999-12-31');
        """)

    def tearDown(self) -> None:
        self.db.close()

    def test_fact_grain_one_row_per_order(self) -> None:
        rows = self.db.execute("""
            SELECT order_id FROM fct_orders GROUP BY order_id HAVING COUNT(*) != 1
        """).fetchall()
        self.assertEqual(rows, [])

    def test_historical_scd2_join_preserves_fact_grain(self) -> None:
        rows = self.db.execute("""
            SELECT f.order_id, d.region, f.amount_minor
            FROM fct_orders f JOIN dim_customer d
              ON d.customer_id = f.customer_id
             AND f.order_day >= d.valid_from
             AND f.order_day < d.valid_to
            ORDER BY f.order_id
        """).fetchall()
        self.assertEqual(rows, [("o1","north",100),("o2","south",200),
                                ("o3","west",100)])
        self.assertEqual(sum(row[2] for row in rows), 400)

    def test_naive_join_double_counts_and_must_not_be_accepted(self) -> None:
        wrong = self.db.execute("""
            SELECT SUM(f.amount_minor)
            FROM fct_orders f JOIN dim_customer d USING (customer_id)
        """).fetchone()[0]
        correct = self.db.execute("SELECT SUM(amount_minor) FROM fct_orders").fetchone()[0]
        self.assertEqual(correct, 400)
        self.assertEqual(wrong, 700)
        self.assertNotEqual(correct, wrong)

    def test_scd2_overlaps_are_detectable(self) -> None:
        self.db.execute("""
            INSERT INTO dim_customer
            VALUES(4,'A','duplicate','2026-02-01','2026-05-01')
        """)
        conflicts = self.db.execute("""
            SELECT a.version_id,b.version_id
              FROM dim_customer a JOIN dim_customer b
                ON a.customer_id = b.customer_id
               AND a.version_id < b.version_id
               AND a.valid_from < b.valid_to
               AND b.valid_from < a.valid_to
        """).fetchall()
        self.assertEqual(conflicts, [(1,4),(2,4)])

    def test_weighted_rate_uses_underlying_numerator_denominator(self) -> None:
        self.db.executescript("""
          CREATE TABLE cohorts(conversions INTEGER, eligible INTEGER);
          INSERT INTO cohorts VALUES (1,1), (1,9);
        """)
        weighted = self.db.execute("""
          SELECT CAST(SUM(conversions) AS REAL)/SUM(eligible) FROM cohorts
        """).fetchone()[0]
        naive = self.db.execute("""
          SELECT AVG(CAST(conversions AS REAL)/eligible) FROM cohorts
        """).fetchone()[0]
        self.assertAlmostEqual(weighted, 0.2)
        self.assertNotAlmostEqual(weighted, naive)


if __name__ == "__main__":
    unittest.main()
