from __future__ import annotations

from shiny import ui

from .config import CONFIGS


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
