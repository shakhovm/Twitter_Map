#This program runs the server

from flask import Flask, render_template, request
import folium
import twitter_map

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map", methods=["POST"])
def map():
    try:
        account = request.form.get("account")
        twitter_map.create_twitter_json(account, "account_data.json")
        locations = twitter_map.find_locations("account_data.json")
        coordinates = twitter_map.check_coordinates(locations)
        mapa = folium.Map()
        twitter_map.add_locations_to_map(mapa, coordinates)
        mapa.save("templates/Map.html")
        return render_template("Map.html")
    except:
        return render_template("Failure.html")


if __name__ == "__main__":
    app.run(debug=True)
