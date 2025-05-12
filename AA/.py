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
        part = url.strip("/").split("/")
        id = part[-1]
        req = []

        if spell["material"] == True:
            req.append("M")
        if spell["somatic"] == True:
            req.append("S")
        if spell["verbal"] == True:
            req.append("V")

        if spell["concentration"] == True:
            c = "Concentration"
        else:
            c = ""
        
        if spell["ritual"] == True:
            r = "Ritual"
        else:
            r = ""
        
        spells.append({
            'name': spell['name'].capitalize(),
            'lvl': spell['level'],
            'school': school.capitalize(),
            'req' : req,
            'concentration': c
            'ritual' : r
            'id' = id
        })

    render_template("index.html", spells=spells)

@app.route("/spell-details/<id>")
def spell_detail(id):
    response = requests.get(f"https://api.open5e.com/v2/spells/{id}")
    data = response.json()
    
    types = [t['type']['name'] for t in data['types']]
    duration = data.get('duration')
    target = data.get('target_type')
    desc = data.get('desc')
    school = data.get('school')
    name = data.get('name').capitalize()
    
    stat_names = [stat['stat']['name'] for stat in data['stats']]
    stat_values = [stat['base_stat'] for stat in data['stats']]
    
    req = []

    if data["material"] == True:
        req.append("M")
    if data["somatic"] == True:
        req.append("S")
    if data["verbal"] == True:
        req.append("V")

    if data["concentration"] == True:
        c = "Concentration"
    else:
        c = ""
    
    if data["ritual"] == True:
        r = "Ritual"
    else:
        r = ""

    render_template("spell.html", spell={
        'name': name,
        'desc': desc,
        'target': target,
        'duration': duration,
        'lvl': data['level'],
        'school': school.capitalize(),
        'req' : req,
        'concentration': c,
        'ritual' : r,
        'desc': desc,
    })

if __name__ == '__main__':
    app.run(debug=True)