# Catálogo 360 - Shiny + SQLite

Aplicación en **Python con Shiny** para gestionar estructuras con operaciones CRUD:

- Agregar registros
- Editar registros
- Eliminar registros
- Validar duplicados por `codigo`
- Consultar la estructura de la base SQLite y filtrar por ubicación

## Requisitos

- Python 3.10+
- Dependencias de `requirements.txt`

## Ejecución

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
shiny run --reload app.py
```

La app crea automáticamente la base `catalogo.db` con la tabla `estructuras`.

## Estructura de tabla principal

`estructuras`

- `id` (PK autoincremental)
- `codigo` (único)
- `nombre`
- `ubicacion`
- `descripcion`
- `estado`
