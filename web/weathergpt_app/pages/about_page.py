import reflex as rx
from weathergpt_app.state.app_state import AppState
from weathergpt_app.components.navbar import navbar
from weathergpt_app.components.sidebar import sidebar

def about_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.heading("WeatherGPT — Architecture & Technical Specifications", font_size="1.6rem", font_weight="800", color="#F8FAFC"),
                    rx.text("Conversational Weather Decision Intelligence for India (SIH 2026)", font_size="0.9rem", color="#FF9933"),
                    rx.box(
                        rx.vstack(
                            rx.heading("Architecture Principles", font_size="1.2rem", font_weight="700", color="#38BDF8"),
                            rx.text("1. Fact-First Architecture: Meteorological data is retrieved directly from official IMD APIs and ECMWF/GFS NWP models. The LLM does not generate weather facts.", font_size="0.9rem", color="#E2E8F0"),
                            rx.text("2. Rule & Risk Engine: Threshold rules classify weather into IMD warning tiers (Red, Orange, Yellow, Green) and map risk factors.", font_size="0.9rem", color="#E2E8F0"),
                            rx.text("3. Occupation-Aware Personalization: Advisories are dynamically customized for Students, Farmers, Fishermen, Drivers, and Tourists.", font_size="0.9rem", color="#E2E8F0"),
                            rx.text("4. BHASHINI 22-Language Multilingual AI: Integrates India's official language models for STT, translation, and TTS in native scripts.", font_size="0.9rem", color="#E2E8F0"),
                            rx.text("5. WIS 2.0 Ready: Data ingestion pipeline designed for WMO Information System 2.0 MQTT/HTTP Earth-system topics.", font_size="0.9rem", color="#E2E8F0"),
                            spacing="2",
                            align_items="start",
                        ),
                        padding="24px",
                        background="rgba(30, 41, 59, 0.8)",
                        border="1px solid rgba(255, 255, 255, 0.12)",
                        border_radius="18px",
                        width="100%",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.heading("Primary Data Sources", font_size="1.2rem", font_weight="700", color="#34D399"),
                            rx.text("• India Meteorological Department (IMD) District Nowcast & Warnings", font_size="0.9rem", color="#E2E8F0"),
                            rx.text("• Government of India All India Pincode Directory & Geospatial Boundaries", font_size="0.9rem", color="#E2E8F0"),
                            rx.text("• Open-Meteo High-Resolution ECMWF IFS & NOAA GFS NWP Models", font_size="0.9rem", color="#E2E8F0"),
                            rx.text("• BHASHINI Anuvaad Multilingual Speech & Language Gateway", font_size="0.9rem", color="#E2E8F0"),
                            spacing="2",
                            align_items="start",
                        ),
                        padding="24px",
                        background="rgba(30, 41, 59, 0.8)",
                        border="1px solid rgba(255, 255, 255, 0.12)",
                        border_radius="18px",
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
