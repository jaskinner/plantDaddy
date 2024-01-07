import os, requests

import openai
from flask import Flask, redirect, render_template, request, url_for, Markup

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        foods = request.form["foods"].split(",")  # Assuming ingredients are comma-separated
        meal = request.form["meal"]

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=meal_rec(meal, foods),
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.1
        )

        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    result = result if result else ""
    return render_template("index.html", result=Markup(result))

def meal_rec(meal, ingredients):
    ingredient_list = ", ".join(ingredients)  # Assuming 'ingredients' is a list
    return f"""Based on the following ingredients: {ingredient_list}, what are some {meal} recipes I can make with what I have in the pantry? send in html format"""

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
