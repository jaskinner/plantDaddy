import os, requests

import openai
from flask import Flask, redirect, render_template, request, url_for, Markup

# def create_app(*args, **kwargs):
app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        plant = request.form["plant"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(plant),
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    result = result if result else ""
    return render_template("index.html", result=Markup(result))
    
def generate_prompt(plant):
    return "Tell me how to care for a {} plant, which three are very similar in care instructions? send the answer in html format so it's easy to read please.".format(plant)
