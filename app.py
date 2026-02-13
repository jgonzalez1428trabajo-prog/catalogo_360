from shiny import App

from catalogo import app_ui, init_db, server

init_db()
app = App(app_ui, server)
