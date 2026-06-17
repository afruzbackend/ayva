from decimal import Decimal
from .models import Mahsulot

SAVATCHA_KEY = 'savatcha'


class Savatcha:
    def __init__(self, request):
        self.session = request.session
        savatcha = self.session.get(SAVATCHA_KEY)
        if not savatcha:
            savatcha = self.session[SAVATCHA_KEY] = {}
        self.savatcha = savatcha

    def qoshish(self, mahsulot_id, soni=1):
        mahsulot_id = str(mahsulot_id)
        if mahsulot_id in self.savatcha:
            self.savatcha[mahsulot_id] += soni
        else:
            self.savatcha[mahsulot_id] = soni
        self.saqla()

    def yangila(self, mahsulot_id, soni):
        mahsulot_id = str(mahsulot_id)
        if soni <= 0:
            self.ochirish(mahsulot_id)
        else:
            self.savatcha[mahsulot_id] = soni
            self.saqla()

    def ochirish(self, mahsulot_id):
        mahsulot_id = str(mahsulot_id)
        if mahsulot_id in self.savatcha:
            del self.savatcha[mahsulot_id]
            self.saqla()

    def tozala(self):
        self.session[SAVATCHA_KEY] = {}
        self.saqla()

    def saqla(self):
        self.session.modified = True

    def __iter__(self):
        mahsulot_ids = self.savatcha.keys()
        mahsulotlar = Mahsulot.objects.filter(id__in=mahsulot_ids)
        savatcha = self.savatcha.copy()
        for mahsulot in mahsulotlar:
            soni = savatcha[str(mahsulot.id)]
            yield {
                'mahsulot': mahsulot,
                'soni': soni,
                'narxi': mahsulot.narxi,
                'jami': mahsulot.narxi * soni,
            }

    def __len__(self):
        return sum(self.savatcha.values())

    def jami_narx(self):
        ids = list(self.savatcha.keys())
        if not ids:
            return Decimal('0')
        return sum(
            Mahsulot.objects.get(id=int(mid)).narxi * soni
            for mid, soni in self.savatcha.items()
        )