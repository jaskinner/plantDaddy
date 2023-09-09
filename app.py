import os, requests
import openai
from flask import Flask, redirect, render_template, request, url_for, Markup

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        plant = request.form["plant"]
        temp = request.form["temp"]
        humidity = request.form["humidity"]
        temp_unit = request.form.get("temp_unit", "F")  # assuming you have a field named "temp_unit" in your form

        if temp and humidity:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=plant_env(plant, temp, humidity, temp_unit),
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.1
            )
        else:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=plant_rec(plant),
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.1
            )

        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    result = result if result else ""
    return render_template("index.html", result=Markup(result))
    
def plant_rec(plant):
    return """Based on the following criteria, if the Name represents a plant, what are care instructions for it?
                If it's not a plant, ask to repeat.
                Please respond in a block of html/css for readability

Plant Name: {}
""".format(plant)

def plant_env(plant, temp, humidity, temp_unit):
    return """Based on the following criteria, is this a good plant for my home environment?
                Please respond in a block of html/css for readability

Plant Name: {}
Average Home Temperature: {}°{}
Average Home Humidity: {}%
""".format(plant, temp, temp_unit, humidity)

# Run this at the bottom to execute the app when this script is run
if __name__ == '__main__':
    app.run()
