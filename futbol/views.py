from django.shortcuts import render, redirect
from futbol.models import *
from django import forms

class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())
    # dades = forms.ChoiceField()

class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = "__all__"

def nou_jugador(request):
    if request.method == "POST":
        form = JugadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nou_jugador')
    else:
        form = JugadorForm()
    return render(request, "menu.html", {"form": form})

def menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            return redirect('classificacio', lliga.id)
    return render(request, "menu.html", {"form": form})

def classificacio(request, lliga_id):
    lliga = Lliga.objects.get(id=lliga_id)
    equips = lliga.equips.all()
    classi = []

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
            "golesAverage": golesAverage,
        })

    classi.sort(reverse=True, key=lambda x: x["punts"])
    return render(request, "classificacio.html", {
        "classificacio": classi,
        "nom_lliga": lliga.nom,
    })

def llista_jugadors_per_gols(request):
    # Obtener todos los jugadores
    jugadors = Jugador.objects.all()

    # Crear una lista de tuplas (jugador, goles_marcats)
    jugadors_amb_gols = []
    for jugador in jugadors:
        gols_marcats = Event.objects.filter(jugador=jugador, tipus_esdeveniment="gol").count()
        jugadors_amb_gols.append((jugador, gols_marcats))

    # Ordenar la lista por goles marcados (de mayor a menor)
    jugadors_amb_gols_ordenats = sorted(jugadors_amb_gols, key=lambda x: x[1], reverse=True)

    # Pasar los jugadores ordenados a la plantilla
    return render(request, 'llista_jugadors.html', {'jugadors_amb_gols': jugadors_amb_gols_ordenats})

def taula_partits(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            equips = list(lliga.equips.all())
            
            # Crear matriz de resultados
            resultats = []
            
            # Primera fila con nombres de equipos
            header = [""] + [equip.nom for equip in equips]
            resultats.append(header)
            
            # Generar matriz de resultados
            for equip_local in equips:
                fila = [equip_local.nom]
                for equip_visitant in equips:
                    if equip_local == equip_visitant:
                        fila.append("X")
                    else:
                        gols_local = 0
                        gols_visitant = 0
                        try:
                            partit = lliga.partits.get(equip_local=equip_local, equip_visitant=equip_visitant)
                            gols_local = partit.gols_local()
                            gols_visitant = partit.gols_visitant()
                        except Partit.DoesNotExist:
                            pass
                        fila.append(f"{gols_local} - {gols_visitant}")
                resultats.append(fila)
            
            return render(request, "taula_partits.html", {"resultats": resultats})
    else:
        form = MenuForm()
    
    return render(request, "menu.html", {"form": form})