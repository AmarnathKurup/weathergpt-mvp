from weathergpt_app.components.accessibility_modal import accessibility_modal

def render_pulse_item(item: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(item["city"], font_size="0.8rem", font_weight="700", color="#F8FAFC"),
                rx.text(item["cond"], font_size="0.7rem", color="#94A3B8"),
                spacing="0",
                align_items="start",
            ),
            rx.spacer(),
            rx.text(item["temp"], font_size="1.1rem", font_weight="800", color="#FF9933"),
            align_items="center",
            width="100%",
        ),
        padding="10px 14px",
        background="rgba(30, 41, 59, 0.6)",
        border="1px solid rgba(255, 255, 255, 0.08)",
        border_radius="12px",
    )

def render_hourly_forecast(item: dict) -> rx.Component:
    return rx.hstack(
        rx.text(item["time"], font_size="0.85rem", font_weight="600", color="#94A3B8", width="50px"),
        rx.text(item["cond"], font_size="0.85rem", color="#E2E8F0", width="130px"),
        rx.badge(item["pop"], color_scheme="blue", variant="soft", font_size="0.75rem"),
        rx.spacer(),
        rx.text(item["temp"], font_size="0.95rem", font_weight="700", color="#FF9933"),
        width="100%",
        padding="8px 12px",
        background="rgba(30, 41, 59, 0.5)",
        border_radius="10px",
        margin_bottom="6px",
    )

def dashboard_page() -> rx.Component:
    return rx.box(
        accessibility_modal(),
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    alert_banner(),
                    # Emergency Weather Banner when mode active
                    rx.cond(
                        AppState.emergency_mode,
                        rx.box(
                            rx.hstack(
                                rx.text("🚨 EMERGENCY WEATHER MODE ACTIVE — RED ALERT ISSUED FOR HEAVY THUNDERSTORM / FLASH FLOOD RISK", font_size="0.9rem", font_weight="800", color="#FFFFFF"),
                                rx.spacer(),
                                rx.button("Exit Emergency Mode", on_click=AppState.toggle_emergency_mode, background="rgba(0,0,0,0.3)", color="#FFFFFF", font_size="0.75rem", padding="4px 10px", border_radius="6px"),
                                width="100%",
                                align_items="center",
                            ),
                            padding="12px 20px",
                            background="linear-gradient(90deg, #DC2626, #EF4444)",
                            border_radius="12px",
                            margin_bottom="16px",
                        ),
                        rx.fragment()
                    ),
                    weather_card(),
                    
                    # AI Intelligent Advisory Card
                    rx.box(
                        rx.hstack(
                            rx.box(
                                rx.text("🤖", font_size="1.5rem"),
                                padding="10px",
                                background="linear-gradient(135deg, #FF9933, #10B981)",
                                border_radius="12px",
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.text("WeatherGPT Intelligent Advisory", font_size="0.85rem", font_weight="700", color="#FF9933", letter_spacing="0.5px"),
                                    rx.badge(f"For {AppState.selected_occupation.title()}", color_scheme="green", variant="solid", font_size="0.7rem"),
                                    spacing="2",
                                ),
                                rx.text(
                                    f"Rain probability is {AppState.rain_probability}% after 5:00 PM IST in {AppState.location_name}. Thunderstorms and lightning expected. If travelling, carry waterproof gear.",
                                    font_size="0.95rem",
                                    color="#F8FAFC",
                                    font_weight="500",
                                ),
                                spacing="1",
                                align_items="start",
                            ),
                            align_items="center",
                            spacing="4",
                        ),
                        padding="16px 20px",
                        background="linear-gradient(135deg, rgba(255, 153, 51, 0.12) 0%, rgba(16, 185, 129, 0.12) 100%)",
                        border="1px solid rgba(255, 153, 51, 0.3)",
                        border_radius="16px",
                        width="100%",
                        margin_bottom="16px",
                    ),

                    # Occupation Personalization Bar
                    rx.box(
                        rx.hstack(
                            rx.text("👤 Personalize Advisory:", font_size="0.85rem", font_weight="700", color="#F8FAFC"),
                            rx.button("🎓 Student", on_click=lambda: AppState.set_occupation("student"), background=rx.cond(AppState.selected_occupation == "student", "rgba(59, 130, 246, 0.3)", "rgba(255,255,255,0.05)"), color="#60A5FA", border_radius="8px", padding="6px 12px", font_size="0.8rem"),
                            rx.button("🌾 Farmer", on_click=lambda: AppState.set_occupation("farmer"), background=rx.cond(AppState.selected_occupation == "farmer", "rgba(16, 185, 129, 0.3)", "rgba(255,255,255,0.05)"), color="#34D399", border_radius="8px", padding="6px 12px", font_size="0.8rem"),
                            rx.button("⛵ Fisherman", on_click=lambda: AppState.set_occupation("fisherman"), background=rx.cond(AppState.selected_occupation == "fisherman", "rgba(14, 165, 233, 0.3)", "rgba(255,255,255,0.05)"), color="#38BDF8", border_radius="8px", padding="6px 12px", font_size="0.8rem"),
                            rx.button("🚗 Driver", on_click=lambda: AppState.set_occupation("driver"), background=rx.cond(AppState.selected_occupation == "driver", "rgba(245, 158, 11, 0.3)", "rgba(255,255,255,0.05)"), color="#FBBF24", border_radius="8px", padding="6px 12px", font_size="0.8rem"),
                            rx.button("🧳 Tourist", on_click=lambda: AppState.set_occupation("tourist"), background=rx.cond(AppState.selected_occupation == "tourist", "rgba(168, 85, 247, 0.3)", "rgba(255,255,255,0.05)"), color="#C084FC", border_radius="8px", padding="6px 12px", font_size="0.8rem"),
                            spacing="2",
                            align_items="center",
                        ),
                        padding="12px 16px",
                        background="rgba(30, 41, 59, 0.6)",
                        border="1px solid rgba(255, 255, 255, 0.08)",
                        border_radius="14px",
                        width="100%",
                        margin_bottom="20px",
                    ),

                    # India Weather Pulse Section
                    rx.box(
                        rx.heading("🇮🇳 INDIA WEATHER PULSE — REGIONAL OBSERVED INTELLIGENCE", font_size="0.85rem", font_weight="700", color="#94A3B8", letter_spacing="1px", margin_bottom="12px"),
                        rx.grid(
                            rx.foreach(AppState.pulse_locations, render_pulse_item),
                            columns="3",
                            spacing="3",
                            width="100%",
                        ),
                        width="100%",
                        margin_bottom="24px",
                    ),

                    # Grid: Map + Hourly Forecast
                    rx.grid(
                        rx.box(
                            rx.heading("National Weather GIS Map & Active Radar", font_size="1.1rem", font_weight="700", color="#F8FAFC", margin_bottom="12px"),
                            leaflet_map(height="360px"),
                            width="100%",
                        ),
                        rx.box(
                            rx.heading("24-Hour Synoptic Forecast Timeline", font_size="1.1rem", font_weight="700", color="#F8FAFC", margin_bottom="12px"),
                            rx.vstack(
                                rx.foreach(AppState.hourly_forecast, render_hourly_forecast),
                                width="100%",
                                spacing="1",
                            ),
                            padding="16px",
                            background="rgba(15, 23, 42, 0.9)",
                            border="1px solid rgba(255, 255, 255, 0.08)",
                            border_radius="16px",
                            width="100%",
                        ),
                        columns="2",
                        spacing="6",
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
        min_height="100vh",
    )

