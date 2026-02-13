from __future__ import annotations

import sqlite3

from .config import DB_PATH, SCHEMA_PATH, EntityConfig


def qident(identifier: str) -> str:
    return f'"{identifier.replace(chr(34), chr(34) * 2)}"'


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError("No se encontró schema.sql")
    with get_connection() as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def list_tables() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()


def table_info(table: str) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(f"PRAGMA table_info({qident(table)})").fetchall()


def fetch_table(config: EntityConfig, limit: int = 100) -> list[sqlite3.Row]:
    with get_connection() as conn:
        sql = f"SELECT * FROM {qident(config.table)} ORDER BY {qident(config.pk)} DESC LIMIT ?"
        return conn.execute(sql, (limit,)).fetchall()


def exists_duplicate(config: EntityConfig, values: dict[str, str], exclude_id: int | None = None) -> bool:
    where_key = " AND ".join([f"{qident(col)} = ?" for col in config.natural_key])
    params: list[object] = [values.get(col, "").strip() for col in config.natural_key]
    sql = f"SELECT {qident(config.pk)} FROM {qident(config.table)} WHERE {where_key}"
    if exclude_id is not None:
        sql += f" AND {qident(config.pk)} <> ?"
        params.append(exclude_id)

    with get_connection() as conn:
        row = conn.execute(sql, params).fetchone()
    return row is not None


def upsert_entity(config: EntityConfig, values: dict[str, str]) -> None:
    cols = [col for _, col in config.fields]
    assignments = ", ".join([f"{qident(col)} = excluded.{qident(col)}" for col in cols])
    sql = f'''
        INSERT INTO {qident(config.table)} ({", ".join(qident(c) for c in cols)})
        VALUES ({", ".join(["?"] * len(cols))})
        ON CONFLICT ({", ".join(qident(c) for c in config.natural_key)})
        DO UPDATE SET {assignments}
    '''
    with get_connection() as conn:
        conn.execute(sql, [values.get(c, "").strip() for c in cols])


def update_entity(config: EntityConfig, row_id: int, values: dict[str, str]) -> None:
    cols = [col for _, col in config.fields]
    set_clause = ", ".join([f"{qident(c)} = ?" for c in cols])
    sql = f"UPDATE {qident(config.table)} SET {set_clause} WHERE {qident(config.pk)} = ?"
    with get_connection() as conn:
        conn.execute(sql, [values.get(c, "").strip() for c in cols] + [row_id])


def delete_entity(config: EntityConfig, row_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            f"DELETE FROM {qident(config.table)} WHERE {qident(config.pk)} = ?",
            (row_id,),
        )


def get_by_id(config: EntityConfig, row_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            f"SELECT * FROM {qident(config.table)} WHERE {qident(config.pk)} = ?",
            (row_id,),
        ).fetchone()
