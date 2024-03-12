# IN3110 strømpris
IN3110 Strømpris is an API and website you can use to check electricity prices.
The API allows the user to check prices for electricity in 5 locations, and also how 
expensive an activity is at a given time.

# Installation information
The program was developed on python 3.10.2 and requires the following dependencies to run:
- altair v4.*
- altair-viewer
- beautifulsoup4
- fastapi
- pandas
- pytest
- requests
- requests-cache
- uvicorn

These can be installed by running ```python3 -m pip install -r requirements.txt```\
**The program does not work on python versions older than 3.10[1]. This is due to | for different types not being implemented.**\
I figured this was okay seeing as we've used it in previous assignments.

# Running program
To run the main program the user should run ```python3 app.py```. \
To run the klima app the user must do the following:
- ```cd klima```
- ```python3 app.py```

Reference:
1: https://peps.python.org/pep-0604/
