# Catálogo 360 - Shiny + SQLite

Aplicación en **Python con Shiny** con formulario dinámico por opción del catálogo.

## Estructura de archivos

```text
.
├── app.py
├── schema.sql
├── requirements.txt
└── catalogo/
    ├── __init__.py
    ├── config.py    # Configuración de entidades y mapeos formulario->columna
    ├── db.py        # Conexión SQLite + CRUD/UPSERT
    ├── server.py    # Lógica reactiva de Shiny
    └── ui.py        # Definición de interfaz
```

## Qué hace

- Cambias la opción (`Diccionarios`, `Tablas Input`, `Módulos`, `Artefactos`, `Vistas`, `Historia`, `Reglas Historia`, `Variables (General)`, `Variaciones de Variables`).
- La app renderiza **solo los campos de esa entidad**.
- Guarda en su tabla correspondiente en SQLite.
- Usa **UPSERT por llave natural** para evitar duplicados de negocio.
- Permite cargar/editar/eliminar por ID interno (PK surrogate).
- Incluye vista para consultar tablas y estructura (`PRAGMA table_info`).

## Estructura de BD

- El archivo `schema.sql` crea todas las tablas y constraints.
- `catalogo.db` se crea automáticamente al iniciar la app.
- Se aplica patrón recomendado:
  - PK numérica autogenerada (surrogate key)
  - `UNIQUE` por llave natural de negocio.

## Ejecutar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
shiny run --reload app.py
```

## Notas de modelado

- Se omitieron columnas `Unnamed:*` de Excel para mantener un modelo limpio.
- Se conservaron nombres funcionales de columnas para mapear los formularios solicitados.
- Para cargas masivas puedes reutilizar la misma lógica de UPSERT por llave natural.
