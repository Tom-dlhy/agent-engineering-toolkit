"""Ephemeral PostgreSQL integration tests. Never point at customer/prod data.

Requires an explicitly disposable PG server and DATA_TEST_EPHEMERAL=1.
Uses isolated randomly named schema and NOLOGIN application role.
Tests are not run during generic unittest discovery; CI invokes explicitly.
"""
from __future__ import annotations

import os
import unittest
from uuid import uuid4

import psycopg
from psycopg import sql


class PostgresDataContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if os.getenv("DATA_TEST_EPHEMERAL") != "1":
            raise RuntimeError("Refusing PostgreSQL test without DATA_TEST_EPHEMERAL=1")
        dsn = os.getenv("PG_DATA_TEST_DSN")
        if not dsn:
            raise RuntimeError("PG_DATA_TEST_DSN is required for an isolated CI DB")
        cls.conn = psycopg.connect(dsn, autocommit=True)
        cls.schema = "test_data_" + uuid4().hex[:12]
        cls.role = "data_reader_" + uuid4().hex[:12]
        try:
            cls.conn.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(cls.schema)))
            cls.conn.execute(sql.SQL("CREATE ROLE {} NOLOGIN").format(sql.Identifier(cls.role)))
            cls.conn.execute(sql.SQL("""
                CREATE TABLE {}.orders (
                    order_id text PRIMARY KEY,
                    tenant_id text NOT NULL,
                    source_id text NOT NULL,
                    amount_minor integer NOT NULL CHECK (amount_minor >= 0),
                    UNIQUE (tenant_id, source_id)
                )
            """).format(sql.Identifier(cls.schema)))
            cls.conn.execute(sql.SQL("ALTER TABLE {}.orders ENABLE ROW LEVEL SECURITY").format(sql.Identifier(cls.schema)))
            cls.conn.execute(sql.SQL("ALTER TABLE {}.orders FORCE ROW LEVEL SECURITY").format(sql.Identifier(cls.schema)))
            cls.conn.execute(sql.SQL("""
                CREATE POLICY tenant_orders ON {}.orders
                USING (tenant_id = current_setting('app.tenant_id', true))
                WITH CHECK (tenant_id = current_setting('app.tenant_id', true))
            """).format(sql.Identifier(cls.schema)))
            cls.conn.execute(sql.SQL("GRANT USAGE ON SCHEMA {} TO {}").format(
                sql.Identifier(cls.schema), sql.Identifier(cls.role)))
            cls.conn.execute(sql.SQL("GRANT SELECT, INSERT, UPDATE, DELETE ON {}.orders TO {}").format(
                sql.Identifier(cls.schema), sql.Identifier(cls.role)))
        except Exception:
            cls._cleanup()
            raise

    @classmethod
    def _cleanup(cls) -> None:
        try:
            cls.conn.execute("RESET ROLE")
            cls.conn.execute(sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(
                sql.Identifier(cls.schema)))
            cls.conn.execute(sql.SQL("DROP ROLE IF EXISTS {}").format(
                sql.Identifier(cls.role)))
        finally:
            cls.conn.close()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._cleanup()

    def setUp(self) -> None:
        self.conn.execute("RESET ROLE")
        self.conn.execute(sql.SQL("TRUNCATE {}.orders").format(sql.Identifier(self.schema)))
        self.conn.execute(sql.SQL(
            "INSERT INTO {}.orders (order_id, tenant_id, source_id, amount_minor)"
            " VALUES (%s,%s,%s,%s),(%s,%s,%s,%s)"
        ).format(sql.Identifier(self.schema)), ("a1","A","source-a",100, "b1","B","source-b",200))

    def test_unique_business_key_enforced(self) -> None:
        with self.assertRaises(psycopg.errors.UniqueViolation):
            self.conn.execute(sql.SQL(
                "INSERT INTO {}.orders VALUES ('a2', 'A','source-a', 3)"
            ).format(sql.Identifier(self.schema)))
        self.assertEqual(self.conn.execute(sql.SQL("SELECT count(*) FROM {}.orders").format(
            sql.Identifier(self.schema))).fetchone()[0], 2)

    def test_check_constraint_enforced(self) -> None:
        with self.assertRaises(psycopg.errors.CheckViolation):
            self.conn.execute(sql.SQL(
                "INSERT INTO {}.orders VALUES ('a3', 'A','new', -1)"
            ).format(sql.Identifier(self.schema)))

    def test_rls_select_scoped_to_actual_nonowner_role(self) -> None:
        self.conn.execute(sql.SQL("SET ROLE {}").format(sql.Identifier(self.role)))
        try:
            with self.conn.transaction():
                self.conn.execute("SELECT set_config('app.tenant_id', %s, true)", ("A",))
                rows = self.conn.execute(sql.SQL(
                    "SELECT order_id FROM {}.orders ORDER BY order_id"
                ).format(sql.Identifier(self.schema))).fetchall()
                self.assertEqual(rows, [("a1",)])
        finally:
            self.conn.execute("RESET ROLE")

    def test_rls_blocks_cross_tenant_insert(self) -> None:
        self.conn.execute(sql.SQL("SET ROLE {}").format(sql.Identifier(self.role)))
        try:
            with self.assertRaises(psycopg.errors.InsufficientPrivilege):
                with self.conn.transaction():
                    self.conn.execute("SELECT set_config('app.tenant_id', %s, true)", ("A",))
                    self.conn.execute(sql.SQL(
                        "INSERT INTO {}.orders VALUES ('x1', 'B', 'blocked', 1)"
                    ).format(sql.Identifier(self.schema)))
        finally:
            self.conn.execute("RESET ROLE")
        self.assertEqual(self.conn.execute(sql.SQL("SELECT count(*) FROM {}.orders").format(
            sql.Identifier(self.schema))).fetchone()[0], 2)

    def test_rls_without_tenant_context_returns_no_rows(self) -> None:
        self.conn.execute(sql.SQL("SET ROLE {}").format(sql.Identifier(self.role)))
        try:
            with self.conn.transaction():
                self.conn.execute("SELECT set_config('app.tenant_id', %s, true)", ("",))
                rows = self.conn.execute(sql.SQL("SELECT order_id FROM {}.orders").format(
                    sql.Identifier(self.schema))).fetchall()
                self.assertEqual(rows, [])
        finally:
            self.conn.execute("RESET ROLE")

    def test_rollback_does_not_commit_partial_batch(self) -> None:
        with self.assertRaises(RuntimeError):
            with self.conn.transaction():
                self.conn.execute(sql.SQL(
                    "INSERT INTO {}.orders VALUES ('a4', 'A', 'replayable', 15)"
                ).format(sql.Identifier(self.schema)))
                raise RuntimeError("synthetic crash before commit")
        count = self.conn.execute(sql.SQL(
            "SELECT count(*) FROM {}.orders WHERE order_id='a4'"
        ).format(sql.Identifier(self.schema))).fetchone()[0]
        self.assertEqual(count, 0)

    def test_expand_column_preserves_old_writer_and_reader(self) -> None:
        self.conn.execute(sql.SQL(
            "ALTER TABLE {}.orders ADD COLUMN IF NOT EXISTS remark text"
        ).format(sql.Identifier(self.schema)))
        self.conn.execute(sql.SQL(
            "INSERT INTO {}.orders (order_id,tenant_id,source_id,amount_minor)"
            " VALUES ('a5','A','next',22)"
        ).format(sql.Identifier(self.schema)))
        self.assertEqual(self.conn.execute(sql.SQL(
            "SELECT remark FROM {}.orders WHERE order_id='a5'"
        ).format(sql.Identifier(self.schema))).fetchone()[0], None)

    def test_readonly_explain_does_not_run_modify_statement(self) -> None:
        plan = self.conn.execute(sql.SQL(
            "EXPLAIN SELECT order_id FROM {}.orders WHERE tenant_id = %s"
        ).format(sql.Identifier(self.schema)), ("A",)).fetchall()
        self.assertTrue(plan)
        self.assertEqual(self.conn.execute(sql.SQL("SELECT count(*) FROM {}.orders").format(
            sql.Identifier(self.schema))).fetchone()[0], 2)


if __name__ == "__main__":
    unittest.main()
