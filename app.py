from shiny import App

from catalogo import app_ui, init_db, server

# Inicializa/crea la base de datos al arrancar la aplicación.
init_db()
# Objeto principal que Shiny usa para ejecutar la app.
app = App(app_ui, server)
