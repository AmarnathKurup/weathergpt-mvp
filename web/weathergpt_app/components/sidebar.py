import reflex as rx
from weathergpt_app.state.app_state import AppState

NAV_ITEMS = [
    {"label": "Dashboard", "route": "/", "icon": "📊"},
    {"label": "Weather Map", "route": "/map", "icon": "🗺️"},
    {"label": "PIN Weather", "route": "/location", "icon": "📍"},
    {"label": "Warning Center", "route": "/alerts", "icon": "🚨"},
    {"label": "Forecast", "route": "/forecast", "icon": "🌤️"},
    {"label": "Climate AI", "route": "/climate", "icon": "📈"},
    {"label": "WeatherGPT Chat", "route": "/chat", "icon": "💬"},
    {"label": "NWP Models", "route": "/nwp", "icon": "🌐"},
    {"label": "Weather Stations", "route": "/stations", "icon": "📡"},
    {"label": "Analytics", "route": "/analytics", "icon": "📉"},
    {"label": "About & Architecture", "route": "/about", "icon": "ℹ️"},
]

def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("NAVIGATION", font_size="0.7rem", font_weight="700", color="#64748B", padding="12px 16px 4px 16px", letter_spacing="1px"),
            *[
                rx.link(
                    rx.hstack(
                        rx.text(item["icon"], font_size="1.1rem"),
                        rx.text(item["label"], font_size="0.9rem", font_weight="500", color="#E2E8F0"),
                        spacing="3",
                        align_items="center",
                        padding="10px 16px",
                        border_radius="10px",
                        width="100%",
                        _hover={"background": "rgba(255, 153, 51, 0.15)", "color": "#FF9933"},
                        transition="all 0.2s ease",
                    ),
                    href=item["route"],
                    width="100%",
                    text_decoration="none",
                )
                for item in NAV_ITEMS
            ],
            rx.spacer(),
            # Bottom Indian Weather Intelligence Badge
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("🇮🇳", font_size="1.2rem"),
                        rx.vstack(
                            rx.text("IMD + NWP Core", font_size="0.8rem", font_weight="700", color="#F8FAFC"),
                            rx.text("BHASHINI 22 Languages", font_size="0.7rem", color="#94A3B8"),
                            spacing="0",
                            align_items="start",
                        ),
                        spacing="2",
                        align_items="center",
                    ),
                    padding="12px",
                    background="rgba(30, 41, 59, 0.8)",
                    border="1px solid rgba(255, 255, 255, 0.1)",
                    border_radius="12px",
                    width="100%",
                ),
                padding="12px",
                width="100%",
            ),
            width="100%",
            height="100%",
            spacing="1",
            align_items="start",
        ),
        width="240px",
        min_width="240px",
        background="rgba(15, 23, 42, 0.98)",
        border_right="1px solid rgba(255, 255, 255, 0.1)",
        height="calc(100vh - 65px)",
        position="sticky",
        top="65px",
    )
