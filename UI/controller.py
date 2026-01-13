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
        if self._view.dp1.value is None or self._view.dp2.value is None:
            self._view.show_alert("Seleziona entrambe le date")
            return
        start = self._view.dp1.value.date()
        end = self._view.dp2.value.date()
        dictProdotti = self._model.get_dizio_product()

        if self._view.dd_category.value is None:
            self._view.show_alert("Seleziona una categoria")
            return

        category = int(self._view.dd_category.value)


        self._model.getGrafo(category,start, end)
        numNodi = self._model.G.number_of_nodes()
        numArchi = self._model.G.number_of_edges()
        self._view.txt_risultato.clean()
        self._view.txt_risultato.controls.append(ft.Text(f'start date: {start}'))
        self._view.txt_risultato.controls.append(ft.Text(f'end date: {end}'))
        self._view.txt_risultato.controls.append(ft.Text(f'grafo correttamente creato:'))
        self._view.txt_risultato.controls.append(ft.Text(f'numero di nodi: {numNodi}'))
        self._view.txt_risultato.controls.append(ft.Text(f'numero di archi: {numArchi}'))


        for node in self._model.G.nodes():
            nome = dictProdotti[node].product_name
            self._view.dd_prodotto_iniziale.options.append(ft.dropdown.Option(text=f'{nome}', key=node))
            self._view.dd_prodotto_finale.options.append(ft.dropdown.Option(text=f'{nome}', key=node))
        self._view.dd_prodotto_iniziale.disabled = False
        self._view.dd_prodotto_finale.disabled = False
        self._view.txt_lunghezza_cammino.disabled = False
        self._view.pulsante_best_prodotti.disabled = False
        self._view.pulsante_cerca_cammino.disabled = False
        self._view.update()

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        listaPiuVenduti = self._model.getProdottiVenduti()
        dictProdotti = self._model.get_dizio_product()
        self._view.txt_risultato.controls.append(ft.Text('i cinque prodotti piu venduti:'))
        for piuVenduto_id,peso in listaPiuVenduti:
            nomeProdotto = dictProdotti[piuVenduto_id].product_name
            self._view.txt_risultato.controls.append(ft.Text(f'{nomeProdotto} with score {peso}'))
        self._view.update()




    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        print(type(self._view.txt_lunghezza_cammino.value))
        if self._view.txt_lunghezza_cammino.value == '':
            self._view.show_alert("Scrivi la lunghezza del cammino")
            return
        lunghezza = int(self._view.txt_lunghezza_cammino.value)
        dictProdotti = self._model.get_dizio_product()

        if type(lunghezza) is not int:
            self._view.show_alert("Scrivi un numero")
            return
        if self._view.dd_prodotto_iniziale.value == self._view.dd_prodotto_finale.value:
            self._view.show_alert('nodo iniziale e finale devono essere diversi')
            return
        if self._view.dd_prodotto_iniziale.value is None:
            self._view.show_alert('selezionare un nodo iniziale')
            return
        if self._view.dd_prodotto_finale.value is None:
            self._view.show_alert('selezionare un nodo finale')
            return
        nodo_start = int(self._view.dd_prodotto_iniziale.value)
        nodo_final = int(self._view.dd_prodotto_finale.value)
        self._model.getPercorsoOttimo(nodo_start, nodo_final, lunghezza)
        self._view.txt_risultato.clean()
        listaPercorso = self._model.bestPercorso
        pesomigliore = self._model.bestPeso
        self._view.txt_risultato.controls.append(ft.Text(f'Cammino migliore:'))
        for percorso in listaPercorso:
            nome_prodotto = dictProdotti[percorso].product_name
            self._view.txt_risultato.controls.append(ft.Text(f'{nome_prodotto}'))
        self._view.txt_risultato.controls.append(ft.Text(f'score: {pesomigliore}'))
        self._view.update()

