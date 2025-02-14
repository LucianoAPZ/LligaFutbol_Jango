from django.shortcuts import render
from futbol.models import *

def classificacio(request):
    lliga = Lliga.objects.first()
    equips = lliga.equips.all()
    classi = []
 
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        victorias = 0
        derrotas = 0
        empates = 0
        golesAfavor = 0
        golesEncontra = 0
        for partit in lliga.partits.filter(equip_local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
                victorias += 1
                golesAfavor += partit.gols_local()
                golesEncontra += partit.gols_visitant()
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
                empates += 1
                golesAfavor += partit.gols_local()
                golesEncontra += partit.gols_visitant()
            else:
                derrotas += 1
                golesAfavor += partit.gols_local()
                golesEncontra += partit.gols_visitant()
        for partit in lliga.partits.filter(equip_visitant=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
                victorias += 1
                golesEncontra += partit.gols_local()
                golesAfavor += partit.gols_visitant()
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
                empates += 1
                golesEncontra += partit.gols_local()
                golesAfavor += partit.gols_visitant()
            else:
                derrotas += 1
                golesEncontra += partit.gols_local()
                golesAfavor += partit.gols_visitant()

        if golesEncontra > 0:
            golesAverage = round(golesAfavor / golesEncontra, 2)
        else:
            golesAverage = round(golesAfavor, 2) 

        classi.append({
            "equip": equip.nom,
            "punts": punts,
            "victorias": victorias,
            "empates": empates,
            "derrotas": derrotas,
            "golesAfavor": golesAfavor,
            "golesEncontra": golesEncontra,
            "golesAverage" : golesAverage,
        })
    # ordenem llista
    classi.sort(reverse=True, key=lambda x: x["punts"])
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                    "nom_lliga": lliga.nom,
                })

