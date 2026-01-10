from UI.view import View
from database.dao import DAO
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def handle_dd_category(self):
        dictCategory = self._model.get_dizio_category()
        result =[]
        for id in dictCategory.keys():
            nome = dictCategory[id].category_name
            id = dictCategory[id].id
            result.append(ft.dropdown.Option(text=nome, key=id))
        return result


    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        self._model.G.clear()
        start = self._view.dp1.value.date()
        end = self._view.dp2.value.date()
        print(type(start), type(end))
        if start is None or end is None:
            self._view.show_alert("Seleziona entrambe le date")
            return
        category = int(self._view.dd_category.value)
        self._model.getGrafo(category,start, end)

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        # TODO

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
