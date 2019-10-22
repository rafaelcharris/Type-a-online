from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield pages.cuestionario_intro
        yield pages.Cuestionario, dict(sexo=random.choice(["Masculino", "Femenino", "Otro"]),
                                       edad=random.randint(13, 70),
                                       e_civil=random.choice(['Soltera/o', 'Casada/o', 'Unión Marital de Hecho (Unión libre)', 'Viuda/o']),
                                       facultad="Facultad número " + str(random.randint(1, 100)),
                                       carrera="Carrera número " + str(random.randint(1, 100)),
                                       veces_matriculado=random.randint(1,15),
                                       ed_padre=random.choice(['Ninguno', 'Primaria', 'Bachillerato', 'Algún semestre universitario, pero no graduado', 'Técnico', 'Universitario', 'Posgrado']),
                                       ed_madre=random.choice(['Ninguno', 'Primaria', 'Bachillerato', 'Algún semestre universitario, pero no graduado', 'Técnico', 'Universitario', 'Posgrado']),
                                       estrato=random.randint(1, 6),
                                       localidad=random.choice(["No vivo en Bogotá", "Usaquén", "Chapinero", "Santa fé",
                                                                 "La Candelaria","Antonio Nariño", "San Cristobal",
                                                                 "Usme", "Sumapaz", "Suba", "Barrios Unidos", "Engativá",
                                                                 "Teusaquillo", "Fontibón", "Martires", "Puente Aranda",
                                                                 "Kennedy", "Bosa", "Rafael Uribe Uribe", "Tunjuelito", "Ciudad Bolivar"]),
                                       peso=random.randint(40,100),
                                       altura=random.randint(100, 220))
        yield pages.Medidas, dict(riesgo_1=random.randint(1, 5),
                                  riesgo_2=random.randint(1, 5),
                                  gasto_no_plan=random.choice(['No tendría dificultad', 'Tendría alguna dificultad, pero lo conseguiría', 'No sé si lo conseguiría', 'Definitivamente no lo conseguiría' ]),
                                  asalto_fisico=random.choice(['No', 'Sí, una vez', 'Sí, más de una vez']),
                                  asalto_fisico_numero=random.randint(1, 10),
                                  asalto_fisico_familiar=random.choice(['No', 'Sí, una vez', 'Sí, más de una vez']),
                                  asalto_fisico_numero_familiar=random.randint(1, 10),
                                  confrontacion=random.choice(['No', 'Sí, una vez', 'Sí, más de una vez']),
                                  confrontacion_numero=random.randint(1, 10),
                                  violencia=random.choice(['No', 'Sí, una vez', 'Sí, más de una vez']),
                                  prob_atraco=random.randint(1, 5),
                                  barrio_violento=random.randint(1, 5),
                                  barrio_ayuda=random.choice(["True", "False"]),
                                  barrio_seguro=random.choice(["True", "False"]),
                                  estrato_esperado=random.randint(1, 6),
                                  elecciones=random.choice(["Todas las veces", "Casi siempre", "Raramente", "Nunca"]),
                                  botella=random.choice(['Botella de 5.000 pesos', 'Botella de 10.000 pesos', 'Botella de 15.000 pesos', 'Botella de 20.000 pesos',
                                                          'Botella de 25.000 pesos', 'Botella de 30.000 pesos']),
                                  self_perception_justicia=random.randint(1, 10))
