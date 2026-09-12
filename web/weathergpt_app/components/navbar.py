import reflex as rx
from weathergpt_app.state.app_state import AppState, INDIAN_LANGUAGES

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Brand & Logo
            rx.hstack(
                rx.box(
                    rx.text("⚡", font_size="1.5rem"),
                    background="linear-gradient(135deg, #FF9933 0%, #138808 100%)",
                    padding="8px 12px",
                    border_radius="12px",
                    box_shadow="0 0 12px rgba(255, 153, 51, 0.4)",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.heading("WeatherGPT", font_size="1.4rem", font_weight="800", color="#F8FAFC"),
                        rx.badge("SIH 2026", color_scheme="orange", variant="solid", border_radius="6px"),
                        spacing="2",
                        align_items="center",
                    ),
                    rx.text("Conversational Weather Intelligence for India", font_size="0.75rem", color="#94A3B8"),
                    spacing="0",
                    align_items="start",
                ),
                spacing="3",
                align_items="center",
            ),
            rx.spacer(),
            # PIN Code Search Box
            rx.hstack(
                rx.input(
                    placeholder="Enter PIN (e.g. 700001) or Location...",
                    value=AppState.search_query,
                    on_change=AppState.set_search_query,
                    width="280px",
                    background="rgba(30, 41, 59, 0.8)",
                    border="1px solid rgba(255, 255, 255, 0.15)",
                    color="#F8FAFC",
                    border_radius="10px",
                    padding="8px 14px",
                    font_size="0.85rem",
                    _focus={"border_color": "#FF9933", "box_shadow": "0 0 8px rgba(255, 153, 51, 0.3)"},
                ),
                rx.button(
                    "🔍 Search",
                    on_click=AppState.search_pincode_action,
                    background="linear-gradient(135deg, #FF9933, #D97706)",
                    color="#FFFFFF",
                    font_weight="600",
                    border_radius="10px",
                    padding="8px 16px",
                    font_size="0.85rem",
                    _hover={"transform": "translateY(-1px)", "box_shadow": "0 4px 12px rgba(255, 153, 51, 0.4)"},
                ),
                spacing="2",
                align_items="center",
            ),
            rx.spacer(),
            # Right Action controls
            rx.hstack(
                # Language Select Dropdown
                rx.select(
                    [f"{lang['native']} ({lang['name']})" for lang in INDIAN_LANGUAGES],
                    value=AppState.current_language,
                    on_change=AppState.set_language,
                    background="rgba(30, 41, 59, 0.9)",
                    color="#F8FAFC",
                    border="1px solid rgba(255, 255, 255, 0.15)",
                    border_radius="10px",
                    font_size="0.85rem",
                    padding="6px 12px",
                ),
                # Theme selector buttons
                rx.button(
                    "🌙",
                    on_click=lambda: AppState.set_theme("dark"),
                    background="rgba(255, 255, 255, 0.05)",
                    border_radius="8px",
                    padding="6px 10px",
                    font_size="0.9rem",
                ),
                rx.button(
                    "👁️ High Contrast",
                    on_click=lambda: AppState.set_theme("high_contrast"),
                    background="rgba(255, 255, 255, 0.05)",
                    color="#F8FAFC",
                    border_radius="8px",
                    font_size="0.75rem",
                    padding="6px 10px",
                ),
                # Accessibility modal trigger
                rx.button(
                    "♿ Accessibility",
                    on_click=AppState.toggle_accessibility_modal,
                    background="rgba(16, 185, 129, 0.2)",
                    color="#34D399",
                    border="1px solid #10B981",
                    border_radius="8px",
                    font_size="0.8rem",
                    padding="6px 12px",
                    _hover={"background": "rgba(16, 185, 129, 0.35)"},
                ),
                # Emergency Mode Toggle Button
                rx.button(
                    "🚨 Emergency Mode",
                    on_click=AppState.toggle_emergency_mode,
                    background="rgba(239, 68, 68, 0.2)",
                    color="#F87171",
                    border="1px solid #EF4444",
                    border_radius="8px",
                    font_size="0.8rem",
                    padding="6px 12px",
                    _hover={"background": "rgba(239, 68, 68, 0.35)"},
                ),
                spacing="3",
                align_items="center",
            ),
            width="100%",
            padding="12px 24px",
            align_items="center",
        ),
        background="rgba(15, 23, 42, 0.95)",
        backdrop_filter="blur(16px)",
        border_bottom="1px solid rgba(255, 255, 255, 0.1)",
        position="sticky",
        top="0",
        z_index="100",
        width="100%",
    )
