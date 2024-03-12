"""
strompris fastapi app entrypoint
"""
import datetime
import os
from typing import List

import fastapi.openapi.docs
import uvicorn

from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_prices,
)

app = FastAPI(title="FastAPI Strompris",
              description="An API that provides electricity prices through FastAPI",
              summary="Electricity price API",
              version="1.0",
              )
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_prices(request: Request):
    """
    Get_prices returns the strompris html template that's filled in with location codes and todays date.
    Args:
        request (request): Contains http request

    Returns:
        _TemplateResponse: containing template for chosen html file.

    """
    location_codes = LOCATION_CODES
    today = datetime.date.today()
    return templates.TemplateResponse("strompris.html", {"request": request, "locations": location_codes, "today":today})

@app.get("/plot_prices.json")
async def get_plot(locations: List[str] = Query(None), end: datetime.date = None, days: int = 7) -> dict:
    """
    Function that gets the chart by taking in the users choice of values. If user does not pass value default values are given.
    Args:
        locations (List[str]): Locations to check
        end (datetime.date): Last day to check
        days (int): Days before last day to check

    Returns:
        dict: containing chart

    """
    if not end:
        end = datetime.date.today()
    if not locations:
        locations = LOCATION_CODES
    df = fetch_prices(end_date=end, days=days, locations=locations)
    chart = plot_prices(df)
    return chart.to_dict()

# Task 5.6 (bonus):
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date


...
@app.get("/activity")
async def render_activity_page(request: Request):
    """
    render_activity_page returns the activity html template that's filled in with location codes and todays date.
    Args:
        request (request): Contains http request

    Returns:
        _TemplateResponse: the template object for the chosen html
    """
    activities = ACTIVITIES
    location_codes = LOCATION_CODES
    today = datetime.date.today()
    return templates.TemplateResponse("activity.html", {"request": request, "locations": location_codes, "today":today, "activities":activities})


@app.get("/plot_activity.json")
async def get_plot(location: str = "NO1", activity : str = "shower", minutes: int = 10) -> dict:
    """
    Function that gets the chart by taking in the users choice of values. If user does not pass value default values are given.
    Args:
        locations (List[str]): Locations to check
        end (datetime.date): Last day to check
        days (int): Days before last day to check

    Returns:
        dict: containing chart

    """
    df = fetch_day_prices(datetime.date.today(), location)
    chart = plot_activity_prices(df, activity, minutes)
    return chart.to_dict()

# mount your docs directory as static files at `/help`

app.mount("/help", StaticFiles(directory=os.getcwd() + "/docs/_build/html", html=True), name="help")

def main():
    uvicorn.run(app, host="localhost", port=5000)


if __name__ == "__main__":
    main()
