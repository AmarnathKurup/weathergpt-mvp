import reflex as rx
from weathergpt_app.state.app_state import AppState
from weathergpt_app.components.navbar import navbar
from weathergpt_app.components.sidebar import sidebar

SUBDIVISIONS = [
    {"name": "Gangetic West Bengal", "actual": "845 mm", "normal": "790 mm", "departure": "+7% (Normal)", "status": "normal"},
    {"name": "Sub-Himalayan West Bengal & Sikkim", "actual": "1420 mm", "normal": "1280 mm", "departure": "+11% (Normal)", "status": "normal"},
    {"name": "East Madhya Pradesh", "actual": "910 mm", "normal": "720 mm", "departure": "+26% (Excess)", "status": "excess"},
    {"name": "Rayalaseema", "actual": "310 mm", "normal": "420 mm", "departure": "-26% (Deficient)", "status": "deficient"},
]

def analytics_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.heading("Subdivision Rainfall Departures & Meteorological Analytics", font_size="1.5rem", font_weight="700", color="#F8FAFC"),
                    rx.text("IMD Meteorological Sub-Division Cumulative Rainfall Performance.", font_size="0.85rem", color="#94A3B8"),
                    rx.grid(
                        *[
                            rx.box(
                                rx.hstack(
                                    rx.heading(sub["name"], font_size="1.1rem", color="#F8FAFC"),
                                    rx.spacer(),
                                    rx.badge(sub["departure"], color_scheme="green" if sub["status"]=="normal" else ("blue" if sub["status"]=="excess" else "red")),
                                    width="100%",
                                    align_items="center",
                                ),
                                rx.hstack(
                                    rx.text(f"Actual Rainfall: {sub['actual']}", font_size="0.9rem", color="#38BDF8"),
                                    rx.spacer(),
                                    rx.text(f"Normal Standard: {sub['normal']}", font_size="0.9rem", color="#94A3B8"),
                                    width="100%",
                                    margin_top="10px",
                                ),
                                padding="20px",
                                background="rgba(30, 41, 59, 0.7)",
                                border="1px solid rgba(255, 255, 255, 0.1)",
                                border_radius="16px",
                                width="100%",
                            )
                            for sub in SUBDIVISIONS
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
