from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class cuestionario_intro(Page):
    pass

class Cuestionario(Page):
    form_model = 'player'
    form_fields = ['sexo', 'edad', 'e_civil', 'facultad','carrera',
                   'veces_matriculado', 'ed_padre', 'ed_madre','estrato',
                   'localidad', 'peso', 'altura']
class Medidas(Page):
    form_model = 'player'
    form_fields = ['riesgo_1', 'riesgo_2', 'gasto_no_plan', 'asalto_fisico', 'asalto_fisico_numero', 'asalto_fisico_familiar',
                   'asalto_fisico_numero_familiar','confrontacion', 'confrontacion_numero', 'violencia', 'prob_atraco', 'barrio_violento', 'barrio_ayuda',
                   'barrio_seguro', 'estrato_esperado', 'elecciones', 'botella',
                   'self_perception_justicia']


page_sequence = [
    cuestionario_intro,
    Cuestionario,
    Medidas,
]
