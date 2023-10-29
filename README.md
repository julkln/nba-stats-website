## Presentation of the projet

Here is the link of the website : https://kjules75.pythonanywhere.com/

On this website, we can check NBA results, standings, statictics from all players, season averages...

There is a filter on date to get results from games only played on the date selected.

## How to run this project

```
python3 runner.py
```
This file runs an app, based on Flask.

Before lauching the app, we run some computation, with functions created in the file services/nba.py
The function render_template from Flask enables us to return an HTML file, in templates/home.html, with some CSS and JS files in the static folder.

## API
This website is mainly based on an API, and you can find the documentation right here if you are interested : https://www.balldontlie.io/home.html#introduction