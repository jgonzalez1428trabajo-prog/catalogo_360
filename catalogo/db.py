from __future__ import annotations

import sqlite3

from .config import DB_PATH, SCHEMA_PATH, EntityConfig


# Escapa identificadores (tabla/columna) para SQL dinámico seguro con nombres que tienen espacios.
def qident(identifier: str) -> str:
    return f'"{identifier.replace(chr(34), chr(34) * 2)}"'


# Crea una conexión SQLite con acceso por nombre de columna (sqlite3.Row).
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Ejecuta el schema al inicio para garantizar que existan tablas e índices únicos.
def init_db() -> None:
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError("No se encontró schema.sql")
    with get_connection() as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


# Lista tablas de negocio (excluye tablas internas de SQLite).
def list_tables() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()


# Devuelve estructura de columnas de una tabla usando PRAGMA.
def table_info(table: str) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(f"PRAGMA table_info({qident(table)})").fetchall()


# Consulta registros de la entidad activa, ordenando por PK descendente.
def fetch_table(config: EntityConfig, limit: int = 100) -> list[sqlite3.Row]:
    with get_connection() as conn:
        sql = f"SELECT * FROM {qident(config.table)} ORDER BY {qident(config.pk)} DESC LIMIT ?"
        return conn.execute(sql, (limit,)).fetchall()


# Valida si ya existe otro registro con la misma llave natural.
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


# Inserta o actualiza por llave natural (UPSERT), evitando duplicados de negocio.
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


# Actualiza un registro específico por su PK interna.
def update_entity(config: EntityConfig, row_id: int, values: dict[str, str]) -> None:
    cols = [col for _, col in config.fields]
    set_clause = ", ".join([f"{qident(c)} = ?" for c in cols])
    sql = f"UPDATE {qident(config.table)} SET {set_clause} WHERE {qident(config.pk)} = ?"
    with get_connection() as conn:
        conn.execute(sql, [values.get(c, "").strip() for c in cols] + [row_id])


# Elimina un registro por su PK.
def delete_entity(config: EntityConfig, row_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            f"DELETE FROM {qident(config.table)} WHERE {qident(config.pk)} = ?",
            (row_id,),
        )


# Carga un registro por PK para poblar el formulario en modo edición.
def get_by_id(config: EntityConfig, row_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            f"SELECT * FROM {qident(config.table)} WHERE {qident(config.pk)} = ?",
            (row_id,),
        ).fetchone()
