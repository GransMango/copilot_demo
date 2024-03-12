"""
Clima app entrypoint
"""

import uvicorn

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from klima import get_chart

app = FastAPI(title="Clima history",
              description="An API that provides a chart over clima histiory",
              summary="clima history",
              version="1.0"
              )
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_home(request: Request):
    """
    get the homepage
    Args:
        request (request): Contains http request

    Returns:
        _TemplateResponse: the html template for chosen html file.

    """

    return templates.TemplateResponse("klima.html", {"request": request})

@app.get("/climate.json")
async def get_plot(request: Request) -> dict:
    """
    Get the climate plot
    Args:
        request (request): Contains http request

    Returns:
        dict: the plot converted to a dict.

    """

    return get_chart().to_dict()


def main():
    uvicorn.run(app, host="localhost", port=5000)


if __name__ == "__main__":
    main()
