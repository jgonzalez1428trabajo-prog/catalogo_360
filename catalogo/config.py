from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DB_PATH = Path("catalogo.db")
SCHEMA_PATH = Path("schema.sql")


@dataclass(frozen=True)
class EntityConfig:
    table: str
    pk: str
    fields: list[tuple[str, str]]
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
