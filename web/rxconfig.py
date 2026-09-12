import reflex as rx

config = rx.Config(
    app_name="weathergpt_app",
    cors_allowed_origins=["*"],
    tailwind=None,
    disable_plugins=["SitemapPlugin"],  # Suppresses your duplicate warnings
)
