import reflex as rx

from weathergpt_app.pages.dashboard import dashboard_page
from weathergpt_app.pages.map_page import map_page
from weathergpt_app.pages.location_page import location_page
from weathergpt_app.pages.alerts_page import alerts_page
from weathergpt_app.pages.forecast_page import forecast_page
from weathergpt_app.pages.climate_page import climate_page
from weathergpt_app.pages.chat_page import chat_page
from weathergpt_app.pages.nwp_page import nwp_page
from weathergpt_app.pages.stations_page import stations_page
from weathergpt_app.pages.analytics_page import analytics_page
from weathergpt_app.pages.about_page import about_page

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        accent_color="amber",
    )
)

# Register all 11 pages
app.add_page(dashboard_page, route="/", title="WeatherGPT — Conversational Weather Intelligence")
app.add_page(map_page, route="/map", title="GIS Weather Map — WeatherGPT")
app.add_page(location_page, route="/location", title="PIN Weather Intelligence — WeatherGPT")
app.add_page(alerts_page, route="/alerts", title="IMD Warning Center — WeatherGPT")
app.add_page(forecast_page, route="/forecast", title="Extended Forecast — WeatherGPT")
app.add_page(climate_page, route="/climate", title="Climate Analytics — WeatherGPT")
app.add_page(chat_page, route="/chat", title="WeatherGPT Conversational Assistant")
app.add_page(nwp_page, route="/nwp", title="NWP Model Matrix — WeatherGPT")
app.add_page(stations_page, route="/stations", title="Automatic Weather Stations — WeatherGPT")
app.add_page(analytics_page, route="/analytics", title="Rainfall Analytics — WeatherGPT")
app.add_page(about_page, route="/about", title="About & Architecture — WeatherGPT")
