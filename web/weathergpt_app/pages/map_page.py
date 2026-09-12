import reflex as rx
from weathergpt_app.state.app_state import AppState
from weathergpt_app.components.navbar import navbar
from weathergpt_app.components.sidebar import sidebar
from weathergpt_app.components.leaflet_map import leaflet_map

def map_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Interactive GIS Weather & Warning Map", font_size="1.5rem", font_weight="700", color="#F8FAFC"),
                        rx.spacer(),
                        rx.badge("CartoDB Dark + IMD Synoptic Layers", color_scheme="orange"),
                        width="100%",
                        align_items="center",
                    ),
                    rx.text("Pan and zoom across 19,000+ Indian pincodes. Click markers for district warnings and station data.", font_size="0.85rem", color="#94A3B8"),
                    leaflet_map(height="650px"),
                    width="100%",
                    padding="24px",
                    spacing="3",
                ),
                width="calc(100vw - 240px)",
                background="#0B0F19",
                min_height="calc(100vh - 65px)",
            ),
            spacing="0",
            width="100%",
        ),
        background="#0B0F19",
        color="#F8FAFC",
    )
