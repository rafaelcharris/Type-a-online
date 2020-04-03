from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
This is a task that requires real effort from participants.
Subjects are shown two images of incomprehensible text.
Subjects are required to transcribe (copy) the text into a text entry field.
The quality of a subject's transcription is measured by the
<a href="http://en.wikipedia.org/wiki/Levenshtein_distance">Levenshtein distance</a>.
"""


def levenshtein(a, b):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]


def distance_and_ok(transcribed_text, reference_text, max_error_rate):
    error_threshold = len(reference_text) * max_error_rate
    distance = levenshtein(transcribed_text, reference_text)
    ok = distance <= error_threshold
    return distance, ok


class Constants(BaseConstants):
    name_in_url = 'real_effort'
    players_per_group = None
    #Fuente del texto: https://www.thelatinlibrary.com/petronius1.html
    reference_texts = [
        "Revealed preference",
        "Hex ton satoha egavecen. Loh ta receso minenes da linoyiy xese coreliet ocotine! Senuh asud tu bubo tixorut sola",
        "bo ipacape le rorisin lesiku etutale saseriec niyacin ponim na. Ri arariye senayi esoced behin?",
        "Tefid oveve duk mosar rototo buc: Leseri binin nolelar sise etolegus ibosa farare. Desac eno titeda res vab no mes!",
        "Qui inter haec nutriuntur, non magis sapere possunt quam bene olere qui in culina habitant.Pace vestra liceat",
        "dixisse, primi omnium eloquentiam perdidistis.Levibus enim atque inanibus sonis ludibria quaedam excitando",
        "effecistis ut corpus orationis enervaretur et caderet.Nondum iuvenes declamationibus continebantur",
        "Sophocles aut Euripides invenerunt verba quibus deberent loqui.Nondum umbraticus doctor ingenia deleverat",
        "Pindarus novemque lyrici Homericis versibus canere timuerunt.Et ne poetas quidem ad testimonium citem, certe"
        "neque Platona neque Demosthenen ad hoc genus exercitationis accessisse video.Grandis et, ut ita dicam, pudica",
        "oratio non est maculosa nec turgida, sed naturali pulchritudine exsurgit.Nuper ventosa istaec et enormis",
        "loquacitas Athenas ex Asia commigravit animosque iuvenum ad magna surgentes veluti pestilenti quodam sidere",
        "adflavit, semelque corrupta regula eloquentia stetit et obmutuit.Ad summam, quis postea Thucydidis, quis Hyperidis ad famam processit?",
    ]

    num_rounds = len(reference_texts)
    print("This is the number of rounds " + str(num_rounds))
    allowed_error_rate = 0.03

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    transcribed_text = models.LongStringField()
    puntaje = models.IntegerField()

    def transcribed_text_error_message(self, transcribed_text):
        reference_text = Constants.reference_texts[self.round_number - 1]
        allowed_error_rate = Constants.allowed_error_rate
        distance, ok = distance_and_ok(transcribed_text, reference_text,
                                       allowed_error_rate)
        if ok:
            self.levenshtein_distance = distance
        else:
            if allowed_error_rate == 0:
                return "The transcription should be exactly the same as on the image."
            else:
                return "This transcription appears to contain too many errors."

    def payment(self):
        if self.round_number > 1:
            turno = self.round_number - 1
            if turno == 1:
                return self.puntaje
            else :
                self.puntaje += len(self.transcribed_text)
                turno -= 1
        else:
            self.puntaje = 0

    levenshtein_distance = models.IntegerField()
