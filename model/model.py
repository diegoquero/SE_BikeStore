import networkx as nx
import datetime
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.DiGraph()

    def get_date_range(self):
        return DAO.get_date_range()

    def get_dizio_category(self):
        return DAO.getCategory()

    def get_dizio_product(self):
        return DAO.getProducts()

    def get_dizio_order(self):
        return DAO.getOrder()

    def get_lista_orderItem(self):
        return DAO.getOrderItem()

    def get_product_for_category(self, category):
        dizioProducts = DAO.getProducts()
        listaProductCategory = []
        for id in dizioProducts.keys():
            if dizioProducts[id].category_id == category:
                listaProductCategory.append(dizioProducts[id].id)
        return listaProductCategory

    def get_numero_di_vendite_per_prodotto_in_range_data(self, start, end, category):
        listaProdottiFiltrata = self.get_product_for_category(category)
        listaOrderItem = self.get_lista_orderItem()
        dizioOrder = self.get_dizio_order()
        dizio_prodotti_per_numero_vendite_filtrati = {}
        listaOrdiniFiltrata = []
        for id_order in dizioOrder.keys():
            d = dizioOrder[id_order].order_date.date()
            if start<=d<=end:
                    listaOrdiniFiltrata.append(dizioOrder[id_order].id)
        for order_item in listaOrderItem:
                if order_item.order_id in listaOrdiniFiltrata:
                    if order_item.product_id in listaProdottiFiltrata:
                        if dizio_prodotti_per_numero_vendite_filtrati.get(order_item.product_id):
                            dizio_prodotti_per_numero_vendite_filtrati[order_item.product_id] += 1
                        else:
                            dizio_prodotti_per_numero_vendite_filtrati[order_item.product_id] = 1

        print('finito')
        print("Prodotti in categoria:", len(listaProdottiFiltrata))
        print("Prodotti venduti nel range:", len(dizio_prodotti_per_numero_vendite_filtrati.keys()))
        return dizio_prodotti_per_numero_vendite_filtrati




    def getGrafo(self, category, start, end):
        listaProdottiFiltrata = self.get_product_for_category(category)
        self.G.add_nodes_from(listaProdottiFiltrata)
        dizioQuantitaProdottiVenduti = self.get_numero_di_vendite_per_prodotto_in_range_data(start, end, category)
        for id_product in dizioQuantitaProdottiVenduti.keys():
            for id_product2 in dizioQuantitaProdottiVenduti.keys():
                if id_product != id_product2:
                    peso = dizioQuantitaProdottiVenduti[id_product]+dizioQuantitaProdottiVenduti[id_product2]
                    if dizioQuantitaProdottiVenduti[id_product]>dizioQuantitaProdottiVenduti[id_product2]:
                            self.G.add_edge(id_product, id_product2, weight=peso)
                    elif dizioQuantitaProdottiVenduti[id_product2]>dizioQuantitaProdottiVenduti[id_product]:
                            self.G.add_edge(id_product2, id_product, weight=peso)
                    elif dizioQuantitaProdottiVenduti[id_product2]==dizioQuantitaProdottiVenduti[id_product]:
                            self.G.add_edge(id_product, id_product2, weight=peso)
                            self.G.add_edge(id_product2, id_product, weight=peso)
        print(self.G)

    def getProdottiVenduti(self):
        PesiNodi = []
        for nodo in self.G.nodes():
            pesiArchiEntranti = []
            pesiArchiUscenti = []

            for _,_,data in self.G.out_edges(nodo, data=True):
                print()
                peso = data['weight']
                pesiArchiUscenti.append(peso)
            for _,_,data in self.G.in_edges(nodo, data=True):
                peso = data['weight']
                pesiArchiEntranti.append(peso)
            pesoNodo= sum(pesiArchiUscenti)-sum(pesiArchiEntranti)
            PesiNodi.append((nodo,pesoNodo))
        PesiNodi.sort(key=lambda x: x[1], reverse=True)
        pesiNodiFinal = PesiNodi[:5]
        print('PesiNodi:', pesiNodiFinal)
        return pesiNodiFinal




    def getPercorsoOttimo(self, nodo_start, nodo_end, lunghezza):
        self.bestPercorso = []
        self.bestPeso = 0
        self.ricorsione([nodo_start], 0, nodo_end, lunghezza)

    def ricorsione(self, parziale, peso_parziale, nodo_end, lunghezza):
        if len(parziale)>lunghezza:
            return

        if len(parziale)==lunghezza:
            if parziale[-1]==nodo_end:
                if peso_parziale>self.bestPeso:
                    self.bestPeso = peso_parziale
                    self.bestPercorso = parziale.copy()
        nodo_corrente = parziale[-1]
        for nodo in self.G.neighbors(nodo_corrente):
            if nodo not in parziale:
                    peso = self.G[nodo_corrente][nodo]['weight']
                    parziale.append(nodo)

                    self.ricorsione(parziale, peso_parziale + peso, nodo_end, lunghezza)
                    parziale.pop()









