import reflex as rx
from weathergpt_app.state.app_state import AppState

def alert_banner() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.text("🚨", font_size="1.5rem"),
                background="rgba(239, 68, 68, 0.2)",
                padding="10px",
                border_radius="12px",
            ),
            rx.vstack(
                rx.hstack(
                    rx.badge("IMD OFFICIAL WARNING", color_scheme="red", variant="solid", border_radius="6px"),
                    rx.badge(AppState.district.upper(), color_scheme="orange", variant="outline"),
                    rx.spacer(),
                    rx.text("Updated: 14:15 IST", font_size="0.75rem", color="#94A3B8"),
                    align_items="center",
                    width="100%",
                ),
                rx.heading(AppState.warning_title, font_size="1.05rem", font_weight="700", color="#FCA5A5"),
                rx.text(AppState.warning_desc, font_size="0.85rem", color="#CBD5E1"),
                spacing="1",
                align_items="start",
                width="100%",
            ),
            width="100%",
            spacing="4",
            align_items="center",
        ),
        padding="16px 20px",
        background="linear-gradient(135deg, rgba(220, 38, 38, 0.2) 0%, rgba(185, 28, 28, 0.1) 100%)",
        border="1px solid rgba(239, 68, 68, 0.4)",
        border_radius="16px",
        box_shadow="0 4px 20px rgba(220, 38, 38, 0.15)",
        width="100%",
        margin_bottom="16px",
    )
