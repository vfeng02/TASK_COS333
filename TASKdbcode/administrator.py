#!/usr/bin/env python

#-----------------------------------------------------------------------
# administrator.py
# Author: Andres Blanco Bonilla
# Test
#-----------------------------------------------------------------------

from flask import Flask
from flask import current_app as app
from flask import render_template


app = Flask(__name__, template_folder="templates")
with app.app_context():
        from dashboard import init_dashboard
        app = init_dashboard(app)


@app.route("/")
def home():
    """Landing page."""
    return render_template(
        "index.html",
        title="Test",
        description="Embed Plotly Dash into your Flask applications.",
        template="home-template",
        body="This is a homepage served with Flask.",
    )