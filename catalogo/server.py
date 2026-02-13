from __future__ import annotations

from shiny import reactive, render, ui

from .config import CONFIGS, EntityConfig
from .db import (
    delete_entity,
    exists_duplicate,
    fetch_table,
    get_by_id,
    list_tables,
    table_info,
    update_entity,
    upsert_entity,
)


# Controlador reactivo principal: coordina eventos UI y operaciones de base de datos.
def server(input, output, session):
    # Mensaje de estado para mostrar feedback al usuario.
    message = reactive.value("Base inicializada. Selecciona una opción.")

    @reactive.effect
    def _sync_schema_choices() -> None:
        # Mantiene actualizado el combo de tablas disponibles para inspección.
        names = [r["name"] for r in list_tables()]
        selected = input.schema_table() if input.schema_table() in names else (names[0] if names else None)
        ui.update_select("schema_table", choices=names, selected=selected)

    @output
    @render.ui
    def dynamic_form():
        # Renderiza inputs dinámicos según la opción elegida.
        conf = CONFIGS[input.opcion()]
        widgets = [ui.input_text(f"f_{col}", label) for label, col in conf.fields]
        return ui.TagList(*widgets)

    # Extrae valores actuales del formulario y los normaliza (strip).
    def collect_values(conf: EntityConfig) -> dict[str, str]:
        return {col: (input[f"f_{col}"]() or "").strip() for _, col in conf.fields}

    @reactive.effect
    @reactive.event(input.btn_upsert)
    def _upsert():
        # Guarda por llave natural: inserta si no existe, actualiza si existe.
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
        # Carga un registro por ID para editarlo en formulario.
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
        # Actualiza un registro por ID validando colisión de llave natural.
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
        # Borra un registro por ID interno.
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
        # Tabla principal: muestra datos de la entidad seleccionada.
        conf = CONFIGS[input.opcion()]
        return [dict(r) for r in fetch_table(conf)]

    @output
    @render.table
    def tables_table():
        # Lista todas las tablas disponibles en SQLite.
        return [dict(r) for r in list_tables()]

    @output
    @render.table
    def schema_table_view():
        # Muestra la estructura de la tabla elegida en el selector.
        table_name = input.schema_table()
        if not table_name:
            return []
        return [dict(r) for r in table_info(table_name)]
