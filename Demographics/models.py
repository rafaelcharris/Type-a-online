from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Rafael'

doc = """
Encuesta demográfica
"""

class Constants(BaseConstants):
    name_in_url = 'Demographics'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

def preg_likert(label):
    return models.IntegerField(
        label = label,
        min  = 1, max = 5,
        widget=widgets.Slider,
    )
def preg_cuatro(label):
    return models.StringField(
        label = label,
        choices = ['No', 'Sí, una vez', 'Sí, más de una vez']
    )

class Player(BasePlayer):

    sexo =models.StringField(
        label= '¿Cuál es su sexo',
        choices =["Masculino", "Femenino", "Otro"],
        widget = widgets.RadioSelectHorizontal
    )
    edad = models.PositiveIntegerField(
        label = '¿Cuál es su edad?',
        min = 13, max = 70
    )
    e_civil = models.CharField(
        choices=['Soltera/o', 'Casada/o', 'Unión Marital de Hecho (Unión libre)', 'Viuda/o'],
        verbose_name='¿Cuál es su estado civil?',
    )
    facultad = models.StringField(label = '¿ En que facultad está usted matriculado?')
    carrera = models.StringField(label = '¿En que carrera está usted matriculado?')
    veces_matriculado = models.IntegerField(label = "¿Cuantas matrículas ha pagado contando la de este semestre?")
    ed_padre = models.CharField(
        choices=['Ninguno', 'Primaria', 'Bachillerato', 'Algún semestre universitario, pero no graduado', 'Técnico', 'Universitario', 'Posgrado'],
        verbose_name='¿Cuál es el nivel de educación de su padre?',
    )
    ed_madre = models.CharField(
        choices=['Ninguno', 'Primaria', 'Bachillerato', 'Algún semestre universitario, pero no graduado', 'Técnico', 'Universitario', 'Posgrado'],
        verbose_name='¿Cuál es el nivel de educación de su madre?',
    )
    estrato = models.IntegerField(
        label = "De acuerdo con las facturas de sus servicios públicos, ¿cuál es el estrato de la vivienda actual donde reside?",
        choices = [1,2,3,4,5,6],
        widget = widgets.RadioSelectHorizontal
    )
    ingresos = models.IntegerField( #dar choices?
        label = "¿Cuál es el valor aproximado de sus ingresos mensuales en Salarios Mínimos (SMMLV=COP 828,116)? "
                "(ej. 1 salario mínimo mensual, 2 SMMLV, etc.)"
    )
    localidad = models.StringField(
        label = '¿Cuál es la localidad en la que usted reside?',
        choices = ["No vivo en Bogotá", "Usaquén", "Chapinero", "Santa fé", "La Candelaria",
                   "Antonio Nariño", "San Cristobal", "Usme", "Sumapaz", "Suba", "Barrios Unidos", "Engativá",
                   "Teusaquillo", "Fontibón", "Martires", "Puente Aranda", "Kennedy", "Bosa", "Rafael Uribe Uribe", "Tunjuelito",
                   "Ciudad Bolivar"
                   ]
    )
    peso = models.IntegerField(label = "¿Cuál es su peso en kilogramos?")
    altura = models.IntegerField(label = "¿Cuál es su altura en centímetros?",
                                 min = 50, max = 240)
    riesgo_1 = preg_likert(label = '¿Cómo se considera usted? Normalmente ¿es usted una persona totalmente dispuesta a tomar riesgos o intenta evitar tomar riesgos? Por favor conteste usando la siguiente escala de uno a cinco, '
                                   'donde uno indica “totalmente dispuesto a tomar riesgos” y cinco '
                                   '“Totalmente contrario a tomar riesgos”. ')
    riesgo_2 = preg_likert(label = 'Normalmente ¿es usted una persona totalmente dispuesta a tomar riesgos de carácter financiero o intenta evitar tomar riesgos financieros? Por favor conteste usando la siguiente escala de uno a cinco,'
                                   ' donde uno indica “totalmente dispuesto a tomar riesgos” y cinco “Totalmente contrario a tomar riesgos”.')
    gasto_no_plan = models.StringField(
        label = 'Si tuviera que conseguir COP 600.000 en una semana para enfrentar un gasto no planeado, ¿qué tanta dificultad cree que tendría en conseguir el dinero?',
        choices = ['No tendría dificultad', 'Tendría alguna dificultad, pero lo conseguiría', 'No sé si lo conseguiría', 'Definitivamente no lo conseguiría' ]
    )
    asalto_fisico = preg_cuatro(
        label = '¿Ha sido objeto de asalto físico en los últimos doce meses?'
    )
    asalto_fisico_numero = models.IntegerField(
        label = 'Por favor, indique cuántas veces:',
        blank=True
    )
    asalto_fisico_familiar = preg_cuatro(
        label = "¿Algún familiar suyo ha sido objeto de asalto físico en los últimos doce meses?"
    )
    asalto_fisico_numero_familiar = models.IntegerField(
        label='Por favor indique cuántas veces:',
        blank = True
    )
    confrontacion = preg_cuatro(
        label = '¿Se ha encontrado en medio de una confrontación que involucre el uso de pistolas u otras armas de fuego en los últimos cinco años?'
    )
    confrontacion_numero = models.IntegerField(
        label = 'Por favor, indique cuántas veces:',
        blank = True
    )
    violencia = preg_cuatro(
        label = '¿Ha sido objeto de violencia directa (física o psicológica) en los últimos doce meses?'
    )
    prob_atraco = preg_likert(
        label = 'Cuál cree que es su probabilidad de ser víctima de un atraco en los próximos 12 meses?' 
                'Por favor conteste usando la siguiente escala de uno a cinco, donde uno indica “no muy probable” y 5 indica “muy probable”.'
    )
    barrio_violento = preg_likert(
        label = '¿Está de acuerdo con la afirmación “el barrio donde vivo es violento”?'
                'Por favor, conteste usando la siguiente escala de uno a cinco, donde uno indica “estoy totalmente en desacuerdo” y 5 indica “estoy totalmente de acuerdo”.'
    )
    barrio_ayuda = models.BooleanField(
        label = 'Si usted llegara a necesitar ayuda, ¿acudiría a alguien desconocido de su mismo barrio?'
    )
    barrio_seguro = models.BooleanField(
        label = '¿Se siente seguro mientras camina en la tarde en su barrio?'
    )
    estrato_esperado = models.IntegerField(
        label = '¿Cuál es el estrato de la vivienda donde usted espera vivir a lo largo de su vida?',
        choices = [1,2,3,4,5,6],
        widget = widgets.RadioSelectHorizontal
    )

    elecciones = models.StringField(
        label = '¿Con qué frecuencia vota en las elecciones políticas?',
        choices = ["Todas las veces", "Casi siempre", "Raramente", "Nunca"],
        widget= widgets.RadioSelectHorizontal
    )
    botella = models.StringField(
        label = 'Imagine la siguiente situación: usted está de compras en una ciudad que no es familiar para usted y se da cuenta de que perdió el camino. Usted decide preguntarle a un extraño por indicaciones. El extraño ofrece llevarlo en su carro al destino que usted tenía. El viaje dura cerca de 20 minutos y le cuesta al extraño 20.000 pesos. El extraño no desea dinero por haberlo llevado. Usted lleva seis botellas de vino con usted. La botella más barata cuesta 5.000 pesos, la botella más cara cuesta 30.000 pesos. '
                'Usted decide darle una de sus botellas al extraño como agradecimiento por el favor. ¿Cuál botella le daría?', #separar las preguntas para que sea más fácil de leer
        choices = ['Botella de 5.000 pesos', 'Botella de 10.000 pesos', 'Botella de 15.000 pesos', 'Botella de 20.000 pesos',
                   'Botella de 25.000 pesos', 'Botella de 30.000 pesos'],
        widget=widgets.RadioSelect
    )
    self_perception_justicia = models.IntegerField(
        label = '¿Cómo se ve a usted mismo? ¿Es una persona que generalmente está dispuesta a castigar comportamientos injustos, incluso, si esto es costoso para usted?'
                'Por favor use una escala de 0 a 10, donde 0 significa que usted “no está dispuesto a incurrir en costos para castigar comportamientos injustos” y 10 significa que usted “está muy dispuesto a incurrir en costos para castigar comportamientos injustos”. '
                'También puede usar los valores intermedios para indicar dónde se encuentra en la escala.',
        min = 1,
        max = 10,
        widget= widgets.Slider #todo agregar otra función para el step?
    )

    impuesto = preg_likert(
        label = "¿Qué tan de acuerdo está con que el Gobierno tenga que reducir las diferencias entre ricos y pobres, de pronto subiendo los impuestos para los ricos o proveyendo asistencia a los ingresos de los más pobres?"
                " Por favor, indique que tan de acuerdo está marcando un número de uno a cinco en la escala de abajo, donde uno indica “estoy totalmente en desacuerdo” y cinco indica “estoy totalmente de acuerdo”."
                                   )