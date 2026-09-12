import reflex as rx
from weathergpt_app.state.app_state import AppState

def weather_card() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Top row: Location & Pin
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.text("📍", font_size="1.2rem"),
                        rx.heading(AppState.location_name, font_size="1.5rem", font_weight="700", color="#F8FAFC"),
                        spacing="2",
                        align_items="center",
                    ),
                    rx.text(f"PIN Code: {AppState.current_pincode} • District: {AppState.district}", font_size="0.85rem", color="#94A3B8"),
                    spacing="0",
                    align_items="start",
                ),
                rx.spacer(),
                rx.box(
                    rx.vstack(
                        rx.text("IMD + ECMWF", font_size="0.75rem", font_weight="700", color="#38BDF8"),
                        rx.text("Live Synoptic Data", font_size="0.7rem", color="#94A3B8"),
                        spacing="0",
                        align_items="end",
                    ),
                    background="rgba(56, 189, 248, 0.1)",
                    border="1px solid rgba(56, 189, 248, 0.3)",
                    padding="6px 12px",
                    border_radius="10px",
                ),
                width="100%",
                align_items="center",
            ),
            # Main Temperature Display
            rx.hstack(
                rx.hstack(
                    rx.text(f"{AppState.temperature}", font_size="4.2rem", font_weight="800", color="#F8FAFC", line_height="1"),
                    rx.text("°C", font_size="2rem", font_weight="600", color="#FF9933", margin_top="8px"),
                    spacing="0",
                    align_items="start",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.badge(AppState.weather_condition, color_scheme="blue", variant="solid", font_size="0.9rem", padding="6px 12px", border_radius="8px"),
                    rx.text(f"Feels like {AppState.feels_like}°C", font_size="0.95rem", color="#CBD5E1"),
                    spacing="1",
                    align_items="end",
                ),
                width="100%",
                align_items="center",
                padding="12px 0",
            ),
            # Key Weather Stats Grid
            rx.grid(
                rx.box(
                    rx.hstack(
                        rx.text("🌧️", font_size="1.3rem"),
                        rx.vstack(
                            rx.text("Rain Chance", font_size="0.75rem", color="#94A3B8"),
                            rx.text(f"{AppState.rain_probability}%", font_size="1.1rem", font_weight="700", color="#F8FAFC"),
                            spacing="0",
                            align_items="start",
                        ),
                        spacing="2",
                    ),
                    background="rgba(30, 41, 59, 0.6)",
                    padding="12px 16px",
                    border_radius="12px",
                    border="1px solid rgba(255, 255, 255, 0.08)",
                ),
                rx.box(
                    rx.hstack(
                        rx.text("💧", font_size="1.3rem"),
                        rx.vstack(
                            rx.text("Humidity", font_size="0.75rem", color="#94A3B8"),
                            rx.text(f"{AppState.humidity}%", font_size="1.1rem", font_weight="700", color="#F8FAFC"),
                            spacing="0",
                            align_items="start",
                        ),
                        spacing="2",
                    ),
                    background="rgba(30, 41, 59, 0.6)",
                    padding="12px 16px",
                    border_radius="12px",
                    border="1px solid rgba(255, 255, 255, 0.08)",
                ),
                rx.box(
                    rx.hstack(
                        rx.text("💨", font_size="1.3rem"),
                        rx.vstack(
                            rx.text("Wind Speed", font_size="0.75rem", color="#94A3B8"),
                            rx.text(f"{AppState.wind_speed} km/h {AppState.wind_direction}", font_size="1.1rem", font_weight="700", color="#F8FAFC"),
                            spacing="0",
                            align_items="start",
                        ),
                        spacing="2",
                    ),
                    background="rgba(30, 41, 59, 0.6)",
                    padding="12px 16px",
                    border_radius="12px",
                    border="1px solid rgba(255, 255, 255, 0.08)",
                ),
                rx.box(
                    rx.hstack(
                        rx.text("☀️", font_size="1.3rem"),
                        rx.vstack(
                            rx.text("UV Index", font_size="0.75rem", color="#94A3B8"),
                            rx.text(f"UV {AppState.uv_index} (High)", font_size="1.1rem", font_weight="700", color="#F59E0B"),
                            spacing="0",
                            align_items="start",
                        ),
                        spacing="2",
                    ),
                    background="rgba(30, 41, 59, 0.6)",
                    padding="12px 16px",
                    border_radius="12px",
                    border="1px solid rgba(255, 255, 255, 0.08)",
                ),
                columns="4",
                spacing="4",
                width="100%",
            ),
            width="100%",
            spacing="3",
            align_items="start",
        ),
        padding="24px",
        background="linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%)",
        border="1px solid rgba(255, 255, 255, 0.12)",
        border_radius="20px",
        box_shadow="0 8px 32px rgba(0, 0, 0, 0.4)",
        backdrop_filter="blur(12px)",
        width="100%",
        margin_bottom="20px",
    )
