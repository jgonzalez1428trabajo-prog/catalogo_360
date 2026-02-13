PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS dic_diccionarios (
  diccionario_id INTEGER PRIMARY KEY AUTOINCREMENT,
  Diccionario TEXT NOT NULL,
  Descripcion TEXT,
  UNIQUE (Diccionario)
);

CREATE TABLE IF NOT EXISTS dic_tablas_input (
  tabla_input_id INTEGER PRIMARY KEY AUTOINCREMENT,
  Tabla TEXT NOT NULL,
  Descripcion TEXT,
  "Nivel Detalle" TEXT,
  "Nivel Detalle Periodica" TEXT,
  "Periocidad de Actualizacion" TEXT,
  "Tablas Origen SAS" TEXT,
  "Tabla DWH" TEXT,
  UNIQUE (Tabla)
);

CREATE TABLE IF NOT EXISTS dic_modulos (
  modulo_id INTEGER PRIMARY KEY AUTOINCREMENT,
  Modulo TEXT NOT NULL,
  Descrpcion TEXT,
  UNIQUE (Modulo)
);

CREATE TABLE IF NOT EXISTS dic_artefactos (
  artefacto_id INTEGER PRIMARY KEY AUTOINCREMENT,
  Artefacto TEXT NOT NULL,
  Descripcion TEXT,
  UNIQUE (Artefacto)
);

CREATE TABLE IF NOT EXISTS dic_vistas (
  vista_id INTEGER PRIMARY KEY AUTOINCREMENT,
  Vista TEXT NOT NULL,
  Descripcion TEXT,
  "Aperturas Agrupacion" TEXT,
  "Apertura Filtro 1" TEXT,
  Filtro1 TEXT,
  "Apertura Filtro 2" TEXT,
  Filtro2 TEXT,
  "Apertura Filtro 3" TEXT,
  Filtro3 TEXT,
  UNIQUE (Vista)
);

CREATE TABLE IF NOT EXISTS dic_historia (
  historia_id INTEGER PRIMARY KEY AUTOINCREMENT,
  Nombre TEXT NOT NULL,
  Descripcion TEXT,
  Autor TEXT,
  UNIQUE (Nombre, Autor)
);

CREATE TABLE IF NOT EXISTS dic_reglas_historia (
  regla_historia_id INTEGER PRIMARY KEY AUTOINCREMENT,
  "Id Regla Historia" TEXT,
  Indicadores TEXT,
  Artefactos TEXT,
  "Aperturas Agrupacion" TEXT,
  "Apertura Filtro 1" TEXT,
  Filtro1 TEXT,
  "Apertura Filtro 2" TEXT,
  Filtro2 TEXT,
  "Apertura Filtro 3" TEXT,
  Filtro3 TEXT,
  UNIQUE (
    Indicadores,
    Artefactos,
    "Aperturas Agrupacion",
    "Apertura Filtro 1",
    Filtro1,
    "Apertura Filtro 2",
    Filtro2,
    "Apertura Filtro 3",
    Filtro3
  )
);

CREATE TABLE IF NOT EXISTS dic_variables_general (
  variable_general_id INTEGER PRIMARY KEY AUTOINCREMENT,
  Id_Padre TEXT,
  Nombre TEXT NOT NULL,
  Proyecto TEXT NOT NULL,
  "Calculo o Dato" TEXT,
  "Estatus Cubo General" TEXT,
  "Estatus 360 General" TEXT,
  "Estatus Validacion General" TEXT,
  "Resultado Validacion General" TEXT,
  "Dato de validacion" TEXT,
  "Tipo de Variable" TEXT,
  "Comentario Validacion" TEXT,
  Descripcion TEXT,
  UNIQUE (Proyecto, Nombre, "Tipo de Variable")
);

CREATE TABLE IF NOT EXISTS dic_variaciones_variables (
  variacion_id INTEGER PRIMARY KEY AUTOINCREMENT,
  Id_V TEXT,
  Nombre TEXT NOT NULL,
  Id_M TEXT,
  Proyecto TEXT NOT NULL,
  "Tipo Variable" TEXT,
  "Frec. Act" TEXT,
  "Momento de actualizacion" TEXT,
  "Tabla Maestra" TEXT,
  "Tabla output" TEXT,
  "Nivel de detalle" TEXT,
  "Cuartiles" TEXT,
  "Casos Usos" TEXT,
  "Tabla Origen SAS" TEXT,
  "Variable Origen SAS" TEXT,
  "Formulas SAS" TEXT,
  "Tabla Origen DHW" TEXT,
  "Variable Origen DWH" TEXT,
  "Formulas DWH" TEXT,
  "Estatus Agregacion DWH" TEXT,
  "Estatus Migracion DWH" TEXT,
  "acumulado o independiente" TEXT,
  "Nivel de profundidad" TEXT,
  "Estatus Cubo" TEXT,
  "Estatus 360" TEXT,
  "Estatus Validacion" TEXT,
  "Resultado % Validacion" TEXT,
  "Dato de validacion" TEXT,
  "Comentario Validacion" TEXT,
  Descripcion TEXT,
  "Caso MDP" TEXT,
  UNIQUE (Proyecto, Nombre, "Tabla output", "Nivel de detalle", "Tipo Variable")
);
