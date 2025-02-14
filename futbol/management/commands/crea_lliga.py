from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint, choice

from futbol.models import *

faker = Faker(["es_CA", "es_ES"])

class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'

    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)

    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga = Lliga.objects.filter(nom=titol_lliga)
        if lliga.count() > 0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return

        print("Creem la nova lliga: {}".format(titol_lliga))
        lliga = Lliga(nom=titol_lliga)
        lliga.save()

        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[randint(0, len(prefixos) - 1)]
            if prefix:
                prefix += " "
            nom = prefix + ciutat
            any_fundacio = randint(1900, 2010)
            equip = Equip(ciutat=ciutat, nom=nom, lliga=lliga, any_fundacio=any_fundacio)
            equip.save()

            print("Creem jugadors de l'equip " + nom)
            for j in range(25):
                nom = faker.name()
                posicio = choice(['PT', 'DF', 'MC', 'DL'])
                dorsal = randint(1, 99)
                nacionalitat = faker.country()
                jugador = Jugador(nom=nom, posicio=posicio, equip=equip, dorsal=dorsal, nacionalitat=nacionalitat)
                jugador.save()

        print("Creem partits de la lliga")
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local != visitant:
                    partit = Partit(equip_local=local, equip_visitant=visitant, lliga=lliga)
                    partit.save()

                    print(f"Afegint gols al partit {partit.equip_local.nom} vs {partit.equip_visitant.nom}")
                    num_gols_local = randint(0, 5)
                    num_gols_visitant = randint(0, 5)

                    for _ in range(num_gols_local):
                        jugador_local = choice(list(partit.equip_local.jugadors.all()))
                        minut = randint(1, 90)
                        event = Event(partit=partit, jugador=jugador_local, tipus_esdeveniment="gol", minut=minut)
                        event.save()
                        print(f"GOL LOCAL: {jugador_local.nom} al minut {minut}")

                    for _ in range(num_gols_visitant):
                        jugador_visitant = choice(list(partit.equip_visitant.jugadors.all()))
                        minut = randint(1, 90)
                        event = Event(partit=partit, jugador=jugador_visitant, tipus_esdeveniment="gol", minut=minut)
                        event.save()
                        print(f"GOL VISITANT: {jugador_visitant.nom} al minut {minut}")
