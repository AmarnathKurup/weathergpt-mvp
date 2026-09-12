import reflex as rx
from weathergpt_app.state.app_state import AppState
from weathergpt_app.components.navbar import navbar
from weathergpt_app.components.sidebar import sidebar

PRESET_PROMPTS = [
    "Will it rain when I leave college at 5 PM?",
    "Agromet advice for Paddy crops under current rainfall",
    "Is it safe for fishermen to venture into Bay of Bengal?",
    "Why is Kolkata currently under an Orange Alert?",
]

def render_message(msg: dict, index: int) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.badge(rx.cond(msg["sender"] == "user", "YOU", "WEATHERGPT AI"), color_scheme=rx.cond(msg["sender"] == "user", "orange", "blue"), variant="solid", font_size="0.75rem"),
                rx.spacer(),
                rx.text(msg["timestamp"], font_size="0.7rem", color="#64748B"),
                width="100%",
                align_items="center",
                margin_bottom="6px",
            ),
            rx.text(msg["text"], font_size="0.95rem", color="#F8FAFC", line_height="1.5"),
            # Explainable AI "Why?" view for Assistant messages
            rx.cond(
                msg["sender"] != "user",
                rx.box(
                    rx.hstack(
                        rx.button(
                            "💡 Why this recommendation?",
                            on_click=lambda: AppState.toggle_why(index),
                            background="rgba(255, 153, 51, 0.15)",
                            color="#FF9933",
                            font_size="0.75rem",
                            padding="4px 10px",
                            border_radius="6px",
                        ),
                        rx.button(
                            "🔊 Read Aloud",
                            background="rgba(59, 130, 246, 0.15)",
                            color="#60A5FA",
                            font_size="0.75rem",
                            padding="4px 10px",
                            border_radius="6px",
                        ),
                        spacing="2",
                        margin_top="10px",
                    ),
                    rx.cond(
                        msg["show_why"],
                        rx.box(
                            rx.vstack(
                                rx.text("EXPLAINABLE AI REASONING CORE", font_size="0.7rem", font_weight="700", color="#FF9933"),
                                rx.text(rx.cond(msg["facts"]["source"], "Source: " + msg["facts"]["source"], "Source: IMD NWP"), font_size="0.75rem", color="#CBD5E1"),
                                rx.text(rx.cond(msg["facts"]["model"], "Reasoning Engine: " + msg["facts"]["model"], "Reasoning Engine: WeatherGPT Rules"), font_size="0.75rem", color="#CBD5E1"),
                                rx.text(rx.cond(msg["facts"]["rain_prob"], "Rain Forecast: " + msg["facts"]["rain_prob"], "Rain Forecast: 78%"), font_size="0.75rem", color="#CBD5E1"),
                                rx.text(rx.cond(msg["facts"]["risk"], "IMD Risk Tier: " + msg["facts"]["risk"], "IMD Risk Tier: Orange Alert"), font_size="0.75rem", color="#CBD5E1"),
                                spacing="1",
                                align_items="start",
                            ),
                            padding="12px",
                            background="rgba(15, 23, 42, 0.9)",
                            border="1px solid rgba(255, 153, 51, 0.3)",
                            border_radius="10px",
                            margin_top="8px",
                            width="100%",
                        ),
                    ),
                ),
            ),
            align_items="start",
            width="100%",
        ),
        padding="16px 20px",
        background=rx.cond(msg["sender"] == "user", "rgba(30, 41, 59, 0.8)", "rgba(15, 23, 42, 0.9)"),
        border=rx.cond(msg["sender"] == "user", "1px solid rgba(255, 153, 51, 0.3)", "1px solid rgba(56, 189, 248, 0.2)"),
        border_radius="16px",
        margin_bottom="12px",
        width="100%",
    )

def chat_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading("WeatherGPT — Conversational Decision Intelligence", font_size="1.4rem", font_weight="700", color="#F8FAFC"),
                        rx.spacer(),
                        rx.badge("BHASHINI 22 Languages Enabled", color_scheme="green"),
                        width="100%",
                        align_items="center",
                    ),
                    rx.text("Ask conversational queries in English, Hindi, Bengali, Tamil, Telugu, Marathi, or any Indian language.", font_size="0.85rem", color="#94A3B8"),
                    # Preset Chips
                    rx.hstack(
                        *[
                            rx.button(
                                prompt,
                                on_click=lambda p=prompt: AppState.set_chat_input(p),
                                background="rgba(30, 41, 59, 0.6)",
                                color="#CBD5E1",
                                border="1px solid rgba(255, 255, 255, 0.1)",
                                border_radius="20px",
                                font_size="0.75rem",
                                padding="6px 12px",
                                _hover={"background": "rgba(255, 153, 51, 0.2)", "color": "#FF9933"},
                            )
                            for prompt in PRESET_PROMPTS
                        ],
                        spacing="2",
                        width="100%",
                        overflow_x="auto",
                        padding_bottom="4px",
                    ),
                    # Messages List
                    rx.box(
                        rx.vstack(
                            rx.foreach(AppState.chat_history, render_message),
                            width="100%",
                        ),
                        max_height="480px",
                        overflow_y="auto",
                        width="100%",
                        padding_right="8px",
                    ),
                    # Input Box Row
                    rx.hstack(
                        rx.input(
                            placeholder="Type or speak weather query (e.g. Will it rain in Kolkata today?)...",
                            value=AppState.chat_input,
                            on_change=AppState.set_chat_input,
                            width="100%",
                            background="rgba(30, 41, 59, 0.9)",
                            color="#F8FAFC",
                            border="1px solid rgba(255, 255, 255, 0.2)",
                            border_radius="12px",
                            padding="12px 16px",
                            font_size="0.9rem",
                        ),
                        rx.button(
                            "🎤 Voice",
                            background="rgba(16, 185, 129, 0.2)",
                            color="#34D399",
                            border="1px solid #10B981",
                            border_radius="12px",
                            padding="12px 16px",
                            font_size="0.9rem",
                        ),
                        rx.button(
                            "Send ➔",
                            on_click=AppState.send_chat,
                            background="linear-gradient(135deg, #FF9933, #D97706)",
                            color="#FFFFFF",
                            font_weight="700",
                            border_radius="12px",
                            padding="12px 24px",
                            font_size="0.9rem",
                        ),
                        width="100%",
                        spacing="3",
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
