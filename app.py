from __future__ import annotations

import sqlite3
from pathlib import Path

from shiny import App, reactive, render, ui

DB_PATH = Path("catalogo.db")


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS estructuras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    ubicacion TEXT NOT NULL,
    descripcion TEXT,
    estado TEXT NOT NULL
);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(SCHEMA_SQL)


def fetch_all() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT id, codigo, nombre, ubicacion, descripcion, estado
            FROM estructuras
            ORDER BY id DESC
            """
        ).fetchall()


def fetch_by_codigo(codigo: str) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM estructuras WHERE codigo = ?", (codigo.strip(),)
        ).fetchone()


def fetch_by_id(item_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM estructuras WHERE id = ?", (item_id,)).fetchone()


def insert_item(codigo: str, nombre: str, ubicacion: str, descripcion: str, estado: str) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO estructuras (codigo, nombre, ubicacion, descripcion, estado)
            VALUES (?, ?, ?, ?, ?)
            """,
            (codigo.strip(), nombre.strip(), ubicacion.strip(), descripcion.strip(), estado),
        )


def update_item(
    item_id: int,
    codigo: str,
    nombre: str,
    ubicacion: str,
    descripcion: str,
    estado: str,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE estructuras
            SET codigo = ?, nombre = ?, ubicacion = ?, descripcion = ?, estado = ?
            WHERE id = ?
            """,
            (codigo.strip(), nombre.strip(), ubicacion.strip(), descripcion.strip(), estado, item_id),
        )


def delete_item(item_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM estructuras WHERE id = ?", (item_id,))


def list_tables() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()


def table_info(table_name: str) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(f"PRAGMA table_info({table_name})").fetchall()


init_db()


app_ui = ui.page_fluid(
    ui.h2("Gestión de estructuras (SQLite + Shiny)", class_="mt-3 mb-4"),
    ui.navset_tab(
        ui.nav_panel(
            "Formulario y gestión",
            ui.row(
                ui.column(
                    4,
                    ui.input_numeric("item_id", "ID para editar/eliminar", min=1, value=None),
                    ui.input_text("codigo", "Código único"),
                    ui.input_text("nombre", "Nombre"),
                    ui.input_text("ubicacion", "Ubicación"),
                    ui.input_text_area("descripcion", "Descripción", rows=3),
                    ui.input_select(
                        "estado",
                        "Estado",
                        {
                            "pendiente": "Pendiente",
                            "en_proceso": "En proceso",
                            "finalizado": "Finalizado",
                        },
                    ),
                    ui.div(
                        ui.input_action_button("btn_add", "Agregar", class_="btn-primary me-2"),
                        ui.input_action_button("btn_load", "Cargar por ID", class_="btn-secondary me-2"),
                        ui.input_action_button("btn_update", "Editar", class_="btn-warning me-2"),
                        ui.input_action_button("btn_delete", "Eliminar", class_="btn-danger"),
                        class_="mb-3",
                    ),
                    ui.output_text_verbatim("msg"),
                ),
                ui.column(
                    8,
                    ui.h4("Registros"),
                    ui.output_table("tabla_registros"),
                ),
            ),
        ),
        ui.nav_panel(
            "Consulta de BD",
            ui.h4("Tablas disponibles"),
            ui.output_table("tabla_tablas"),
            ui.hr(),
            ui.input_text("tabla_objetivo", "Tabla para inspeccionar", value="estructuras"),
            ui.output_table("tabla_schema"),
            ui.hr(),
            ui.input_text("buscar_ubicacion", "Buscar por ubicación"),
            ui.output_table("tabla_filtro"),
        ),
    ),
)


def server(input, output, session):
    mensaje = reactive.value("Listo.")

    def required_fields() -> bool:
        return bool(input.codigo().strip() and input.nombre().strip() and input.ubicacion().strip())

    @reactive.effect
    @reactive.event(input.btn_add)
    def _():
        if not required_fields():
            mensaje.set("Completa código, nombre y ubicación.")
            return

        if fetch_by_codigo(input.codigo()):
            mensaje.set("Duplicado detectado: ya existe un registro con ese código.")
            return

        try:
            insert_item(
                input.codigo(),
                input.nombre(),
                input.ubicacion(),
                input.descripcion(),
                input.estado(),
            )
            mensaje.set("Registro agregado correctamente.")
        except sqlite3.IntegrityError:
            mensaje.set("No se pudo agregar: código duplicado.")

    @reactive.effect
    @reactive.event(input.btn_load)
    def _():
        if input.item_id() is None:
            mensaje.set("Debes indicar un ID para cargar.")
            return

        row = fetch_by_id(int(input.item_id()))
        if row is None:
            mensaje.set("No existe ese ID.")
            return

        ui.update_text("codigo", value=row["codigo"])
        ui.update_text("nombre", value=row["nombre"])
        ui.update_text("ubicacion", value=row["ubicacion"])
        ui.update_text_area("descripcion", value=row["descripcion"] or "")
        ui.update_select("estado", selected=row["estado"])
        mensaje.set(f"Registro {row['id']} cargado para edición.")

    @reactive.effect
    @reactive.event(input.btn_update)
    def _():
        if input.item_id() is None:
            mensaje.set("Debes indicar un ID para editar.")
            return

        if not required_fields():
            mensaje.set("Completa código, nombre y ubicación.")
            return

        existing_id = fetch_by_id(int(input.item_id()))
        if existing_id is None:
            mensaje.set("No existe ese ID para editar.")
            return

        repeated = fetch_by_codigo(input.codigo())
        if repeated is not None and repeated["id"] != int(input.item_id()):
            mensaje.set("Duplicado detectado: el código pertenece a otro registro.")
            return

        update_item(
            int(input.item_id()),
            input.codigo(),
            input.nombre(),
            input.ubicacion(),
            input.descripcion(),
            input.estado(),
        )
        mensaje.set("Registro actualizado correctamente.")

    @reactive.effect
    @reactive.event(input.btn_delete)
    def _():
        if input.item_id() is None:
            mensaje.set("Debes indicar un ID para eliminar.")
            return

        existing = fetch_by_id(int(input.item_id()))
        if existing is None:
            mensaje.set("No existe ese ID para eliminar.")
            return

        delete_item(int(input.item_id()))
        mensaje.set("Registro eliminado correctamente.")

    @output
    @render.text
    def msg():
        return mensaje.get()

    @output
    @render.table
    def tabla_registros():
        return [dict(row) for row in fetch_all()]

    @output
    @render.table
    def tabla_tablas():
        return [dict(row) for row in list_tables()]

    @output
    @render.table
    def tabla_schema():
        table_name = input.tabla_objetivo().strip() or "estructuras"
        valid_names = {row["name"] for row in list_tables()}
        if table_name not in valid_names:
            return [{"error": f"La tabla '{table_name}' no existe."}]
        return [dict(row) for row in table_info(table_name)]

    @output
    @render.table
    def tabla_filtro():
        query = input.buscar_ubicacion().strip()
        with get_connection() as conn:
            if not query:
                rows = conn.execute(
                    "SELECT id, codigo, nombre, ubicacion, estado FROM estructuras ORDER BY id DESC LIMIT 25"
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT id, codigo, nombre, ubicacion, estado
                    FROM estructuras
                    WHERE lower(ubicacion) LIKE lower(?)
                    ORDER BY id DESC
                    """,
                    (f"%{query}%",),
                ).fetchall()
        return [dict(row) for row in rows]


app = App(app_ui, server)
