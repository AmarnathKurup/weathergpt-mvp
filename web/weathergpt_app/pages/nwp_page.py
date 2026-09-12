import reflex as rx
from weathergpt_app.state.app_state import AppState
from weathergpt_app.components.navbar import navbar
from weathergpt_app.components.sidebar import sidebar

MODELS_DATA = [
    {"name": "IMD Regional WRF", "res": "3.0 km", "cycles": "4 Runs/day", "accuracy": "94.2% (India)", "desc": "India Meteorological Department High-Resolution Weather Research & Forecasting Model calibrated specifically for Indian monsoons."},
    {"name": "ECMWF IFS (HRES)", "res": "9.0 km", "cycles": "00 & 12 UTC", "accuracy": "93.8% Global", "desc": "European Centre for Medium-Range Weather Forecasts flagship numerical prediction model."},
    {"name": "NOAA GFS (Global)", "res": "13.0 km", "cycles": "00, 06, 12, 18 UTC", "accuracy": "91.5% Global", "desc": "NOAA Operational Global Forecast System 16-day numerical prediction engine."},
    {"name": "DWD ICON (Global)", "res": "13.0 km", "cycles": "00, 06, 12, 18 UTC", "accuracy": "92.1% Global", "desc": "Deutscher Wetterdienst ICON non-hydrostatic global numerical atmosphere model."},
]

def nwp_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.heading("Numerical Weather Prediction (NWP) Model Matrix", font_size="1.5rem", font_weight="700", color="#F8FAFC"),
                    rx.text("Compare multi-model ensemble outputs for GFS, ECMWF, IMD WRF, and ICON.", font_size="0.85rem", color="#94A3B8"),
                    # Model Comparison Disclaimer
                    rx.box(
                        rx.hstack(
                            rx.text("⚠️ Note: Model comparison is informational and does not replace official IMD warnings.", font_size="0.85rem", font_weight="700", color="#FBBF24"),
                            width="100%",
                            align_items="center",
                        ),
                        padding="10px 16px",
                        background="rgba(245, 158, 11, 0.12)",
                        border="1px solid rgba(245, 158, 11, 0.3)",
                        border_radius="10px",
                        width="100%",
                        margin_bottom="12px",
                    ),
                    rx.grid(
                        *[
                            rx.box(
                                rx.hstack(
                                    rx.heading(model["name"], font_size="1.2rem", color="#38BDF8"),
                                    rx.spacer(),
                                    rx.badge(model["res"], color_scheme="green"),
                                    width="100%",
                                    align_items="center",
                                ),
                                rx.text(model["desc"], font_size="0.85rem", color="#CBD5E1", margin="8px 0"),
                                rx.hstack(
                                    rx.text(f"Cycles: {model['cycles']}", font_size="0.75rem", color="#94A3B8"),
                                    rx.spacer(),
                                    rx.text(f"India Accuracy: {model['accuracy']}", font_size="0.8rem", font_weight="700", color="#FF9933"),
                                    width="100%",
                                ),
                                padding="20px",
                                background="rgba(30, 41, 59, 0.7)",
                                border="1px solid rgba(255, 255, 255, 0.1)",
                                border_radius="16px",
                                width="100%",
                            )
                            for model in MODELS_DATA
                        ],
                        columns="2",
                        spacing="4",
                        width="100%",
                    ),
                    # Model Output Comparison Table for Current Location
                    rx.box(
                        rx.heading("Ensemble Live Comparison — PIN 700001 (Kolkata)", font_size="1.1rem", font_weight="700", color="#F8FAFC", margin_bottom="12px"),
                        rx.box(
                            rx.table.root(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell("Model Engine"),
                                        rx.table.column_header_cell("Temperature"),
                                        rx.table.column_header_cell("Rain Prob"),
                                        rx.table.column_header_cell("Expected Precip"),
                                        rx.table.column_header_cell("Wind"),
                                        rx.table.column_header_cell("Confidence"),
                                    )
                                ),
                                rx.table.body(
                                    rx.foreach(
                                        AppState.nwp_models,
                                        lambda item: rx.table.row(
                                            rx.table.cell(item["model"], font_weight="700", color="#38BDF8"),
                                            rx.table.cell(item["temp"]),
                                            rx.table.cell(item["rain_prob"]),
                                            rx.table.cell(item["precip"]),
                                            rx.table.cell(item["wind"]),
                                            rx.table.cell(rx.badge(item["confidence"], color_scheme="green")),
                                        )
                                    )
                                ),
                                width="100%",
                            ),
                            padding="16px",
                            background="rgba(15, 23, 42, 0.9)",
                            border="1px solid rgba(255, 255, 255, 0.1)",
                            border_radius="14px",
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
