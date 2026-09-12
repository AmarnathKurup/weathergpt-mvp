import reflex as rx
from weathergpt_app.state.app_state import AppState
from weathergpt_app.components.navbar import navbar
from weathergpt_app.components.sidebar import sidebar

CLIMATE_FACTS = [
    {"title": "20-Year Temperature Shift", "value": "+1.2°C", "sub": "Above 1990-2010 baseline for Gangetic West Bengal"},
    {"title": "Monsoon Departure Index", "value": "+14% Heavy Events", "sub": "Increased frequency of intense short-duration rainfall"},
    {"title": "Heatwave Frequency", "value": "18 Days/Year", "sub": "Average high heat threshold (>40°C) recorded in Eastern plains"},
    {"title": "Cyclonic Intensity Trend", "value": "Category 3+", "sub": "Bay of Bengal warm SST fostering rapid intensification"},
]

def climate_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.heading("Historical Climate Intelligence & Trend Analytics", font_size="1.5rem", font_weight="700", color="#F8FAFC"),
                    rx.text("Long-term meteorological statistical analysis based on IMD 50-year dataset and ECMWF ERA5 Reanalysis.", font_size="0.85rem", color="#94A3B8"),
                    rx.grid(
                        *[
                            rx.box(
                                rx.text(item["title"], font_size="0.85rem", font_weight="600", color="#94A3B8"),
                                rx.heading(item["value"], font_size="1.6rem", font_weight="800", color="#34D399", margin="8px 0"),
                                rx.text(item["sub"], font_size="0.8rem", color="#CBD5E1"),
                                padding="20px",
                                background="rgba(30, 41, 59, 0.6)",
                                border="1px solid rgba(255, 255, 255, 0.1)",
                                border_radius="16px",
                                width="100%",
                            )
                            for item in CLIMATE_FACTS
                        ],
                        columns="2",
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    padding="24px",
                    spacing="4",
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
