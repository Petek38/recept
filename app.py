from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    global call
    call=requests.get("https://www.themealdb.com/api/json/v1/1/random.php").json()
    
    return render_template("index.html", title=call["meals"][0]["strMeal"], slika=call["meals"][0]["strMealThumb"], backColor=pridobi_barvo(call["meals"][0]["strMealThumb"],1),ingredients=ingredients())

def ingredients():
    ingredient_list = [] 
    # This will create a list of ingredients with their measurements as HTML
    ingredient_list = []
    for i in range(1, 21):
        ingredient = call["meals"][0].get(f"strIngredient{i}")
        measurement = call["meals"][0].get(f"strMeasure{i}")
        if ingredient and measurement:
            ingredient_list.append(f"<li>{ingredient} - {measurement}</li>")

    # Convert the list to an HTML unordered list
    ingredient_list = "<ul>" + "".join(ingredient_list) + "</ul>"
    return ingredient_list



def pridobi_barvo(url_slike: str, st_barv: int = 2) -> list:
    """Funkcija za pridobivanje dominantnih barv iz slike.
    
    Primer uporabe:
    barve = pridobi_barvo("https://example.com/slika.jpg")
    print(barve[0])  # prva (najbolj dominantna) barva
    """
    from dominantcolors import get_image_dominant_colors
    import urllib.request
    
    temp_slika = "static/temp_slika.jpg"
    try:
        urllib.request.urlretrieve(url_slike, temp_slika)
        return get_image_dominant_colors(image_path=temp_slika, num_colors=st_barv)
    except Exception as e:
        print(f"Napaka: {e}")
        return [(255, 255, 255)]  # Vrnemo belo barvo v primeru napake



app.run(debug=True, port=5002)
