from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def home():
    response = [requests.get("https://api.open5e.com/v2/spells/")]

    data = response.json()
    spell_list = data['results']
    
    spells = []
    
    for spell in spell_list:
        url = spell['school']
        parts = url.strip("/").split("/")
        school = parts[-1]

        url = spell['url']
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
            'id': id,
            'lvl': spell['level'],
            'school': school.capitalize(),
            'req' : req,
            'concentration': c,
            'ritual' : r
        })

    return render_template("home.html", spells=spells) 

@app.route("/spell-details/<id>")
def spell_detail(id):
    response = requests.get(f"https://api.open5e.com/v2/spells/{id}") 
    data = response.json()
    
    name = data.get('name')
    duration = data.get('duration')
    target = data.get('target_type')
    desc = data.get('desc')
    distance = data.get('range_text')

    save_throw = data.get('saving_throw_ability')
    if save_throw == "":
        save_throw = "N/A"
    else:
        save_throw = save_throw.capitalize()

    attack_roll = data.get('attack_roll')

    if attack_roll == True:
        dmg_roll = data.get('damage_roll')
    else:
        dmg_roll = "[This spell is not offensive]"

    url = data.get('school')
    parts = url.strip("/").split("/")
    school = parts[-1]
    
    req = []

    material = data.get('material')
    somatic = data.get('somatic')
    verbal = data.get('verbal')

    if material == True:
        req.append("M")
    if somatic == True:
        req.append("S")
    if verbal == True:
        req.append("V")

    concentration = data.get('concentration')
    ritual = data.get('ritual')

    if concentration == True:
        c = "Concentration"
    else:
        c = ""
    if ritual == True:
        r = "Ritual"
    else:
        r = ""

    return render_template("spell.html", spell={
        'name': name,
        'target': target.capitalize(),
        'duration': duration,
        'lvl': data.get('level'),
        'higher_level': data.get('higher_level'),
        'school': school.capitalize(),
        'req' : req,
        'range': distance,
        'concentration': c,
        'ritual' : r,
        'save_throw': save_throw,
        'dmg_roll':dmg_roll,
        'desc': desc
    })

if __name__ == '__main__':
    app.run(debug=True)