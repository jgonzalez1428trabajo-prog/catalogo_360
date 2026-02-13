from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from shiny import App, reactive, render, ui

DB_PATH = Path("catalogo.db")
SCHEMA_PATH = Path("schema.sql")


@dataclass(frozen=True)
class EntityConfig:
    table: str
    pk: str
    fields: list[tuple[str, str]]  # (form_label, db_column)
    natural_key: list[str]


CONFIGS: dict[str, EntityConfig] = {
    "Diccionarios": EntityConfig(
        table="dic_diccionarios",
        pk="diccionario_id",
        fields=[("Diccionario", "Diccionario"), ("Descripción", "Descripcion")],
        natural_key=["Diccionario"],
    ),
    "Tablas Input": EntityConfig(
        table="dic_tablas_input",
        pk="tabla_input_id",
        fields=[
            ("Tabla", "Tabla"),
            ("Descripción", "Descripcion"),
            ("Nivel Detalle", "Nivel Detalle"),
            ("Nivel Detalle Periódica", "Nivel Detalle Periodica"),
            ("Periodicidad de Actualización", "Periocidad de Actualizacion"),
            ("Tablas Origen SAS", "Tablas Origen SAS"),
            ("Tabla DWH", "Tabla DWH"),
        ],
        natural_key=["Tabla"],
    ),
    "Módulos": EntityConfig(
        table="dic_modulos",
        pk="modulo_id",
        fields=[("Módulo", "Modulo"), ("Descripción", "Descrpcion")],
        natural_key=["Modulo"],
    ),
    "Artefactos": EntityConfig(
        table="dic_artefactos",
        pk="artefacto_id",
        fields=[("Artefacto", "Artefacto"), ("Descripción", "Descripcion")],
        natural_key=["Artefacto"],
    ),
    "Vistas": EntityConfig(
        table="dic_vistas",
        pk="vista_id",
        fields=[
            ("Vista", "Vista"),
            ("Descripción", "Descripcion"),
            ("Aperturas Agrupación", "Aperturas Agrupacion"),
            ("Apertura Filtro 1", "Apertura Filtro 1"),
            ("Filtro 1", "Filtro1"),
            ("Apertura Filtro 2", "Apertura Filtro 2"),
            ("Filtro 2", "Filtro2"),
            ("Apertura Filtro 3", "Apertura Filtro 3"),
            ("Filtro 3", "Filtro3"),
        ],
        natural_key=["Vista"],
    ),
    "Historia": EntityConfig(
        table="dic_historia",
        pk="historia_id",
        fields=[("Nombre", "Nombre"), ("Descripción", "Descripcion"), ("Autor", "Autor")],
        natural_key=["Nombre", "Autor"],
    ),
    "Reglas Historia": EntityConfig(
        table="dic_reglas_historia",
        pk="regla_historia_id",
        fields=[
            ("Id Regla Historia", "Id Regla Historia"),
            ("Indicadores", "Indicadores"),
            ("Artefactos", "Artefactos"),
            ("Aperturas Agrupación", "Aperturas Agrupacion"),
            ("Apertura Filtro 1", "Apertura Filtro 1"),
            ("Filtro 1", "Filtro1"),
            ("Apertura Filtro 2", "Apertura Filtro 2"),
            ("Filtro 2", "Filtro2"),
            ("Apertura Filtro 3", "Apertura Filtro 3"),
            ("Filtro 3", "Filtro3"),
        ],
        natural_key=[
            "Indicadores",
            "Artefactos",
            "Aperturas Agrupacion",
            "Apertura Filtro 1",
            "Filtro1",
            "Apertura Filtro 2",
            "Filtro2",
            "Apertura Filtro 3",
            "Filtro3",
        ],
    ),
    "Variables (General)": EntityConfig(
        table="dic_variables_general",
        pk="variable_general_id",
        fields=[
            ("Id Padre", "Id_Padre"),
            ("Nombre", "Nombre"),
            ("Proyecto", "Proyecto"),
            ("Calculo o Dato", "Calculo o Dato"),
            ("Estatus Cubo General", "Estatus Cubo General"),
            ("Estatus 360 General", "Estatus 360 General"),
            ("Estatus Validación General", "Estatus Validacion General"),
            ("Resultado Validación General", "Resultado Validacion General"),
            ("Dato de validación", "Dato de validacion"),
            ("Tipo de Variable", "Tipo de Variable"),
            ("Comentario Validación", "Comentario Validacion"),
            ("Descripción", "Descripcion"),
        ],
        natural_key=["Proyecto", "Nombre", "Tipo de Variable"],
    ),
    "Variaciones de Variables": EntityConfig(
        table="dic_variaciones_variables",
        pk="variacion_id",
        fields=[
            ("Id_V", "Id_V"),
            ("Nombre", "Nombre"),
            ("Id_M", "Id_M"),
            ("Proyecto", "Proyecto"),
            ("Tipo Variable", "Tipo Variable"),
            ("Frec. Act", "Frec. Act"),
            ("Momento de actualización", "Momento de actualizacion"),
            ("Tabla Maestra", "Tabla Maestra"),
            ("Tabla output", "Tabla output"),
            ("Nivel de detalle", "Nivel de detalle"),
            ("Cuartiles", "Cuartiles"),
            ("Casos de uso", "Casos Usos"),
            ("Tabla Origen SAS", "Tabla Origen SAS"),
            ("Variable Origen SAS", "Variable Origen SAS"),
            ("Fórmula SAS", "Formulas SAS"),
            ("Tabla Origen DWH", "Tabla Origen DHW"),
            ("Variable Origen DWH", "Variable Origen DWH"),
            ("Fórmula DWH", "Formulas DWH"),
            ("Estatus Agregación DWH", "Estatus Agregacion DWH"),
            ("Estatus Migración DWH", "Estatus Migracion DWH"),
            ("Acumulado o independiente", "acumulado o independiente"),
            ("Nivel de profundidad", "Nivel de profundidad"),
            ("Estatus Cubo", "Estatus Cubo"),
            ("Estatus 360", "Estatus 360"),
            ("Estatus Validación", "Estatus Validacion"),
            ("Resultado % Validación", "Resultado % Validacion"),
            ("Dato de validación", "Dato de validacion"),
            ("Comentario Validación", "Comentario Validacion"),
            ("Descripción", "Descripcion"),
            ("Caso MDP", "Caso MDP"),
        ],
        natural_key=["Proyecto", "Nombre", "Tabla output", "Nivel de detalle", "Tipo Variable"],
    ),
}


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


init_db()


app_ui = ui.page_fluid(
    ui.h2("Catálogo 360 - Formulario dinámico por opción"),
    ui.row(
        ui.column(
            4,
            ui.input_select("opcion", "Opción de catálogo", choices=list(CONFIGS.keys())),
            ui.input_numeric("row_id", "ID interno para editar/eliminar", min=1, value=None),
            ui.output_ui("dynamic_form"),
            ui.div(
                ui.input_action_button("btn_upsert", "Guardar (UPSERT)", class_="btn-primary me-2"),
                ui.input_action_button("btn_load", "Cargar por ID", class_="btn-secondary me-2"),
                ui.input_action_button("btn_update", "Editar", class_="btn-warning me-2"),
                ui.input_action_button("btn_delete", "Eliminar", class_="btn-danger"),
                class_="mb-3",
            ),
            ui.output_text_verbatim("msg"),
        ),
        ui.column(
            8,
            ui.h4("Datos de la opción seleccionada"),
            ui.output_table("data_table"),
            ui.hr(),
            ui.h4("Tablas disponibles en SQLite"),
            ui.output_table("tables_table"),
            ui.hr(),
            ui.input_select("schema_table", "Inspeccionar esquema", choices=[]),
            ui.output_table("schema_table_view"),
        ),
    ),
)


def server(input, output, session):
    message = reactive.value("Base inicializada. Selecciona una opción.")

    @reactive.effect
    def _sync_schema_choices() -> None:
        names = [r["name"] for r in list_tables()]
        selected = input.schema_table() if input.schema_table() in names else (names[0] if names else None)
        ui.update_select("schema_table", choices=names, selected=selected)

    @output
    @render.ui
    def dynamic_form():
        conf = CONFIGS[input.opcion()]
        widgets = [ui.input_text(f"f_{col}", label) for label, col in conf.fields]
        return ui.TagList(*widgets)

    def collect_values(conf: EntityConfig) -> dict[str, str]:
        return {col: (input[f"f_{col}"]() or "").strip() for _, col in conf.fields}

    @reactive.effect
    @reactive.event(input.btn_upsert)
    def _upsert():
        conf = CONFIGS[input.opcion()]
        values = collect_values(conf)
        if any(not values.get(col, "") for col in conf.natural_key):
            message.set(f"Completa los campos de llave natural: {', '.join(conf.natural_key)}")
            return
        upsert_entity(conf, values)
        message.set("UPSERT aplicado correctamente (inserta si no existe, actualiza si ya existe).")

    @reactive.effect
    @reactive.event(input.btn_load)
    def _load():
        if input.row_id() is None:
            message.set("Indica un ID para cargar.")
            return
        conf = CONFIGS[input.opcion()]
        row = get_by_id(conf, int(input.row_id()))
        if row is None:
            message.set("No existe ese ID en la tabla seleccionada.")
            return
        for _, col in conf.fields:
            ui.update_text(f"f_{col}", value=row[col] or "")
        message.set("Registro cargado en el formulario.")

    @reactive.effect
    @reactive.event(input.btn_update)
    def _update():
        if input.row_id() is None:
            message.set("Indica un ID para editar.")
            return
        conf = CONFIGS[input.opcion()]
        row_id = int(input.row_id())
        if get_by_id(conf, row_id) is None:
            message.set("No existe ese ID en la tabla seleccionada.")
            return

        values = collect_values(conf)
        if any(not values.get(col, "") for col in conf.natural_key):
            message.set(f"Completa los campos de llave natural: {', '.join(conf.natural_key)}")
            return

        if exists_duplicate(conf, values, exclude_id=row_id):
            message.set("Duplicado detectado: la llave natural ya existe en otro registro.")
            return

        update_entity(conf, row_id, values)
        message.set("Registro actualizado correctamente.")

    @reactive.effect
    @reactive.event(input.btn_delete)
    def _delete():
        if input.row_id() is None:
            message.set("Indica un ID para eliminar.")
            return
        conf = CONFIGS[input.opcion()]
        row_id = int(input.row_id())
        if get_by_id(conf, row_id) is None:
            message.set("No existe ese ID en la tabla seleccionada.")
            return
        delete_entity(conf, row_id)
        message.set("Registro eliminado correctamente.")

    @output
    @render.text
    def msg():
        return message.get()

    @output
    @render.table
    def data_table():
        conf = CONFIGS[input.opcion()]
        return [dict(r) for r in fetch_table(conf)]

    @output
    @render.table
    def tables_table():
        return [dict(r) for r in list_tables()]

    @output
    @render.table
    def schema_table_view():
        table_name = input.schema_table()
        if not table_name:
            return []
        return [dict(r) for r in table_info(table_name)]


app = App(app_ui, server)
