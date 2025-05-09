from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://api.open5e.com/v2/spells/")
    data = response.json()
    spell_list = data['results']
    
    spells = []
    
    for spell in spell_list:
        url = spell['school']
        parts = url.strip("/").split("/")
        school = parts[-1]
        req = []
        
        spells.append({
            'name': spell['name'].capitalize(),
            'lvl': spell['level'],
            'school': school.capitalize(),
            'req' : req
        })