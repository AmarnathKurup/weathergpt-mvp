import reflex as rx
from weathergpt_app.state.app_state import AppState

def accessibility_modal() -> rx.Component:
    return rx.cond(
        AppState.show_accessibility_modal,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.hstack(
                            rx.text("♿", font_size="1.4rem"),
                            rx.heading("Accessibility & Vision Settings", font_size="1.2rem", color="#F8FAFC"),
                            spacing="2",
                            align_items="center",
                        ),
                        rx.spacer(),
                        rx.button(
                            "✕",
                            on_click=AppState.toggle_accessibility_modal,
                            background="transparent",
                            color="#94A3B8",
                            font_size="1.1rem",
                            padding="4px 8px",
                            _hover={"color": "#FFFFFF"},
                        ),
                        width="100%",
                        align_items="center",
                        margin_bottom="16px",
                    ),
                    
                    # Text Size Selector
                    rx.text("TEXT SIZE SCALING", font_size="0.75rem", font_weight="700", color="#94A3B8", letter_spacing="1px"),
                    rx.hstack(
                        rx.button("Small", on_click=lambda: AppState.set_font_size("small"), background=rx.cond(AppState.font_size == "small", "#FF9933", "rgba(255,255,255,0.08)"), color="#FFFFFF", font_size="0.8rem", padding="6px 14px", border_radius="8px"),
                        rx.button("Normal", on_click=lambda: AppState.set_font_size("normal"), background=rx.cond(AppState.font_size == "normal", "#FF9933", "rgba(255,255,255,0.08)"), color="#FFFFFF", font_size="0.8rem", padding="6px 14px", border_radius="8px"),
                        rx.button("Large", on_click=lambda: AppState.set_font_size("large"), background=rx.cond(AppState.font_size == "large", "#FF9933", "rgba(255,255,255,0.08)"), color="#FFFFFF", font_size="0.8rem", padding="6px 14px", border_radius="8px"),
                        rx.button("Extra Large", on_click=lambda: AppState.set_font_size("xlarge"), background=rx.cond(AppState.font_size == "xlarge", "#FF9933", "rgba(255,255,255,0.08)"), color="#FFFFFF", font_size="0.8rem", padding="6px 14px", border_radius="8px"),
                        spacing="2",
                        width="100%",
                        margin_bottom="16px",
                    ),

                    # Theme & High Contrast Mode
                    rx.text("HIGH CONTRAST & VISUAL MODE", font_size="0.75rem", font_weight="700", color="#94A3B8", letter_spacing="1px"),
                    rx.hstack(
                        rx.button("Standard Dark", on_click=lambda: AppState.set_theme("dark"), background=rx.cond(AppState.theme_mode == "dark", "#3B82F6", "rgba(255,255,255,0.08)"), color="#FFFFFF", font_size="0.8rem", padding="6px 14px", border_radius="8px"),
                        rx.button("High Contrast (Yellow/Black)", on_click=lambda: AppState.set_theme("high_contrast"), background=rx.cond(AppState.theme_mode == "high_contrast", "#F59E0B", "rgba(255,255,255,0.08)"), color="#FFFFFF", font_size="0.8rem", padding="6px 14px", border_radius="8px"),
                        spacing="2",
                        width="100%",
                        margin_bottom="16px",
                    ),

                    # Audio Read Aloud
                    rx.text("AUDIO ASSISTANT", font_size="0.75rem", font_weight="700", color="#94A3B8", letter_spacing="1px"),
                    rx.hstack(
                        rx.text("Read Aloud AI Advisories automatically", font_size="0.9rem", color="#E2E8F0"),
                        rx.spacer(),
                        rx.button(
                            rx.cond(AppState.read_aloud_enabled, "ON 🔊", "OFF 🔇"),
                            on_click=AppState.toggle_read_aloud,
                            background=rx.cond(AppState.read_aloud_enabled, "#10B981", "rgba(255,255,255,0.1)"),
                            color="#FFFFFF",
                            font_size="0.8rem",
                            padding="6px 16px",
                            border_radius="8px",
                        ),
                        width="100%",
                        align_items="center",
                        margin_bottom="16px",
                    ),

                    # Close Button
                    rx.button(
                        "Apply Settings",
                        on_click=AppState.toggle_accessibility_modal,
                        background="linear-gradient(135deg, #FF9933, #D97706)",
                        color="#FFFFFF",
                        font_weight="700",
                        width="100%",
                        padding="10px",
                        border_radius="10px",
                    ),
                    spacing="2",
                    align_items="start",
                ),
                padding="24px",
                background="#0F172A",
                border="1px solid rgba(255, 255, 255, 0.2)",
                border_radius="16px",
                width="90%",
                max_width="480px",
                box_shadow="0 20px 50px rgba(0, 0, 0, 0.8)",
            ),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background="rgba(0, 0, 0, 0.75)",
            backdrop_filter="blur(8px)",
            z_index="999",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        rx.fragment()
    )
