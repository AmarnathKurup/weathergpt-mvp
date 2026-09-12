import reflex as rx
from weathergpt_app.state.app_state import AppState
from weathergpt_app.components.navbar import navbar
from weathergpt_app.components.sidebar import sidebar
from weathergpt_app.components.weather_card import weather_card

def location_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.heading("PIN Code Intelligence & Location Weather", font_size="1.5rem", font_weight="700", color="#F8FAFC"),
                    rx.text("Lookup location details using 6-digit Indian PIN code or district coordinates.", font_size="0.85rem", color="#94A3B8"),
                    weather_card(),
                    # Location details card
                    rx.box(
                        rx.heading("Geospatial & Postal Hierarchy", font_size="1.1rem", font_weight="700", color="#F8FAFC", margin_bottom="12px"),
                        rx.grid(
                            rx.box(rx.text("PIN Code", color="#94A3B8", font_size="0.8rem"), rx.heading(AppState.current_pincode, font_size="1.2rem", color="#38BDF8")),
                            rx.box(rx.text("District", color="#94A3B8", font_size="0.8rem"), rx.heading(AppState.district, font_size="1.2rem", color="#F8FAFC")),
                            rx.box(rx.text("State", color="#94A3B8", font_size="0.8rem"), rx.heading(AppState.state_name, font_size="1.2rem", color="#F8FAFC")),
                            rx.box(rx.text("Coordinates", color="#94A3B8", font_size="0.8rem"), rx.heading(f"{AppState.lat:.2f}°N, {AppState.lon:.2f}°E", font_size="1.2rem", color="#FF9933")),
                            columns="4",
                            spacing="4",
                            width="100%",
                        ),
                        padding="20px",
                        background="rgba(30, 41, 59, 0.6)",
                        border="1px solid rgba(255, 255, 255, 0.1)",
                        border_radius="16px",
                        width="100%",
                    ),
                    # My Places Section (Home, Office, Farm, College)
                    rx.box(
                        rx.heading("📍 MY PLACES — SAVED LOCATIONS & ADVISORIES", font_size="1.1rem", font_weight="700", color="#F8FAFC", margin_bottom="12px"),
                        rx.grid(
                            rx.foreach(
                                AppState.saved_places,
                                lambda place: rx.box(
                                    rx.hstack(
                                        rx.vstack(
                                            rx.hstack(
                                                rx.heading(place["name"], font_size="1.1rem", color="#F8FAFC"),
                                                rx.badge(place["pincode"], color_scheme="blue", variant="soft"),
                                                spacing="2",
                                                align_items="center",
                                            ),
                                            rx.text(place["location"], font_size="0.8rem", color="#94A3B8"),
                                            spacing="0",
                                            align_items="start",
                                        ),
                                        rx.spacer(),
                                        rx.vstack(
                                            rx.text(place["temp"], font_size="1.2rem", font_weight="800", color="#FF9933"),
                                            rx.text(f"Rain: {place['rain']}", font_size="0.75rem", color="#CBD5E1"),
                                            spacing="0",
                                            align_items="end",
                                        ),
                                        width="100%",
                                        align_items="center",
                                    ),
                                    rx.hstack(
                                        rx.text(f"Condition: {place['cond']}", font_size="0.8rem", color="#E2E8F0"),
                                        rx.spacer(),
                                        rx.badge(f"Alert: {place['alert'].upper()}", color_scheme=rx.cond(place["alert"] == "orange", "orange", rx.cond(place["alert"] == "yellow", "yellow", "green"))),
                                        width="100%",
                                        align_items="center",
                                        margin_top="10px",
                                    ),
                                    padding="16px",
                                    background="rgba(30, 41, 59, 0.7)",
                                    border="1px solid rgba(255, 255, 255, 0.1)",
                                    border_radius="14px",
                                    width="100%",
                                )
                            ),
                            columns="2",
                            spacing="4",
                            width="100%",
                        ),
                        width="100%",
                        margin_top="16px",
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
