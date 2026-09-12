import reflex as rx
from weathergpt_app.state.app_state import AppState
from weathergpt_app.components.navbar import navbar
from weathergpt_app.components.sidebar import sidebar

STATIONS = [
    {"id": "AWS-700001", "name": "Alipore IMD Observatory", "district": "Kolkata", "type": "Automatic Weather Station", "temp": "31.5°C", "humidity": "75%", "rain": "14.2 mm", "status": "ONLINE"},
    {"id": "AWS-110001", "name": "Safdarjung Observatory", "district": "New Delhi", "type": "Synoptic Surface Station", "temp": "35.2°C", "humidity": "58%", "rain": "0.0 mm", "status": "ONLINE"},
    {"id": "AWS-400001", "name": "Colaba Weather Telemetry", "district": "Mumbai", "type": "Coastal Radar Station", "temp": "29.8°C", "humidity": "88%", "rain": "42.0 mm", "status": "ONLINE"},
    {"id": "AWS-600001", "name": "Meenambakkam Station", "district": "Chennai", "type": "Agromet Station", "temp": "33.1°C", "humidity": "64%", "rain": "2.4 mm", "status": "ONLINE"},
]

def stations_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.heading("Automatic Weather Stations (AWS) & Telemetry Network", font_size="1.5rem", font_weight="700", color="#F8FAFC"),
                    rx.text("Real-time sensor telemetry from IMD AWS, ARG (Automatic Rain Gauge), and Agromet stations across India.", font_size="0.85rem", color="#94A3B8"),
                    rx.vstack(
                        *[
                            rx.box(
                                rx.hstack(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.heading(s["name"], font_size="1.1rem", color="#F8FAFC"),
                                            rx.badge(s["id"], color_scheme="blue"),
                                            rx.badge(s["status"], color_scheme="green", variant="solid"),
                                            spacing="2",
                                            align_items="center",
                                        ),
                                        rx.text(f"{s['type']} • District: {s['district']}", font_size="0.8rem", color="#94A3B8"),
                                        spacing="1",
                                        align_items="start",
                                    ),
                                    rx.spacer(),
                                    rx.hstack(
                                        rx.box(rx.text("Temp", font_size="0.7rem", color="#94A3B8"), rx.text(s["temp"], font_size="0.95rem", font_weight="700", color="#FF9933")),
                                        rx.box(rx.text("Humidity", font_size="0.7rem", color="#94A3B8"), rx.text(s["humidity"], font_size="0.95rem", font_weight="700", color="#38BDF8")),
                                        rx.box(rx.text("Rainfall (24h)", font_size="0.7rem", color="#94A3B8"), rx.text(s["rain"], font_size="0.95rem", font_weight="700", color="#34D399")),
                                        spacing="4",
                                    ),
                                    width="100%",
                                    align_items="center",
                                ),
                                padding="16px",
                                background="rgba(30, 41, 59, 0.7)",
                                border="1px solid rgba(255, 255, 255, 0.1)",
                                border_radius="14px",
                                width="100%",
                                margin_bottom="10px",
                            )
                            for s in STATIONS
                        ],
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
