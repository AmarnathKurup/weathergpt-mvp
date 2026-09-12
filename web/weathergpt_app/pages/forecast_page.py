import reflex as rx
from weathergpt_app.state.app_state import AppState
from weathergpt_app.components.navbar import navbar
from weathergpt_app.components.sidebar import sidebar

def render_daily_forecast(day: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(day["day"], font_size="1.1rem", font_weight="700", color="#F8FAFC"),
            rx.text(day["date"], font_size="0.8rem", color="#94A3B8"),
            rx.heading(day["max"], font_size="1.8rem", font_weight="800", color="#FF9933", margin="8px 0"),
            rx.text(day["min"], font_size="0.9rem", color="#CBD5E1"),
            rx.badge(day["pop"], color_scheme="blue", margin="8px 0"),
            rx.text(day["cond"], font_size="0.85rem", color="#E2E8F0", text_align="center"),
            align_items="center",
            spacing="1",
        ),
        padding="20px 16px",
        background="rgba(30, 41, 59, 0.7)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius="16px",
        width="100%",
    )

def forecast_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.heading(f"Extended Weather Forecast — {AppState.location_name}", font_size="1.5rem", font_weight="700", color="#F8FAFC"),
                    rx.text("High-precision 7-day numerical forecast powered by ECMWF IFS & GFS NWP models.", font_size="0.85rem", color="#94A3B8"),
                    rx.grid(
                        rx.foreach(AppState.daily_forecast, render_daily_forecast),
                        columns="4",
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
