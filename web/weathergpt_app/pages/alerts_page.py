import reflex as rx
from weathergpt_app.state.app_state import AppState
from weathergpt_app.components.navbar import navbar
from weathergpt_app.components.sidebar import sidebar

ALERTS_LIST = [
    {"level": "red", "title": "🔴 Red Warning — Heavy Monsoonal Downpour & Tidal Surge", "district": "Mumbai & Palghar", "state": "Maharashtra", "time": "Valid till 23:59 IST", "desc": "Extremely heavy rainfall exceeding 200mm expected in coastal areas. Flash flooding and urban waterlogging probable."},
    {"level": "orange", "title": "🟠 Orange Alert — Severe Thunderstorm & Lightning", "district": "Kolkata & Howrah", "state": "West Bengal", "time": "Valid till 20:00 IST", "desc": "Convective thunderstorm activity with wind gusts up to 45 km/h and localized intense rain (25-50mm/hr)."},
    {"level": "orange", "title": "🟠 Orange Alert — Heavy Rainfall Warning", "district": "Bhubaneswar & Cuttack", "state": "Odisha", "time": "Valid till 18:00 IST", "desc": "Depression over Westcentral Bay of Bengal moving NW. Squally winds up to 55 km/h near coastal sea zones."},
    {"level": "yellow", "title": "🟡 Yellow Watch — Heatwave & High Humidity", "district": "New Delhi & NCR", "state": "Delhi", "time": "Valid till 17:00 IST", "desc": "Maximum temperatures hovering around 38°C with heat index feeling like 44°C. Stay hydrated."},
    {"level": "green", "title": "🟢 Green Normal — No Weather Warning", "district": "Bengaluru Urban", "state": "Karnataka", "time": "Valid 24 hours", "desc": "Pleasant monsoon weather with light isolated drizzles expected."},
]

def alerts_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading("National Weather Warning & Alert Center", font_size="1.5rem", font_weight="700", color="#F8FAFC"),
                        rx.spacer(),
                        rx.badge("IMD Official Severity Standards", color_scheme="red"),
                        width="100%",
                        align_items="center",
                    ),
                    rx.text("Live warnings published by India Meteorological Department (IMD) categorized into 4 severity tiers.", font_size="0.85rem", color="#94A3B8"),
                    rx.vstack(
                        *[
                            rx.box(
                                rx.hstack(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.badge(item["level"].upper(), color_scheme="red" if item["level"]=="red" else ("orange" if item["level"]=="orange" else ("yellow" if item["level"]=="yellow" else "green")), variant="solid", font_weight="700"),
                                            rx.heading(item["title"], font_size="1.1rem", font_weight="700", color="#F8FAFC"),
                                            spacing="3",
                                            align_items="center",
                                        ),
                                        rx.text(f"Region: {item['district']}, {item['state']} • {item['time']}", font_size="0.8rem", color="#94A3B8"),
                                        rx.text(item["desc"], font_size="0.9rem", color="#CBD5E1", margin_top="4px"),
                                        spacing="1",
                                        align_items="start",
                                    ),
                                    width="100%",
                                ),
                                padding="16px 20px",
                                background="rgba(30, 41, 59, 0.7)",
                                border=f"1px solid {'#EF4444' if item['level']=='red' else ('#F97316' if item['level']=='orange' else ('#EAB308' if item['level']=='yellow' else '#10B981'))}",
                                border_radius="14px",
                                width="100%",
                                margin_bottom="12px",
                            )
                            for item in ALERTS_LIST
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
