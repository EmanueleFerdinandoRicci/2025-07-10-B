import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDCategory(self):
        categories = self._model.getCategories()
        for c in categories:
            #da usare così dal momento in cui la stringa visualizzata non è il valore che ci serve
            self._view._ddcategory.options.append(
                ft.dropdown.Option(key=str(c.category_id), text=c.category_name)
            )
        self._view.update_page()

    def handleCreaGrafo(self, e):
        cat = self._view._ddcategory.value
        date1 = self._view._dp1.value
        date2 = self._view._dp2.value
        self._model.buildGraph(cat, date1, date2)
        n, a = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Date selezionate:")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Start date:{self._view._dp1.value.date()}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"End date:{self._view._dp2.value.date()}")
        )
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato:")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi:{n}, numero di archi:{a}")
        )
        self._view.update_page()

    def handleBestProdotti(self, e):
        bestProdotti = self._model.getNodiPiuProfittevoli()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Di seguito i 5 nodi più profittevoli:")
        )
        for p in bestProdotti:
            self._view.txt_result.controls.append(
                ft.Text(f"{p[0]} - score: {p[1]}")
            )
        self._view.update_page()

        self.fillDDProdotti()

    def handleCercaCammino(self, e):
        if self._view._txtInLun == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore numerico in lun", color="red")
            )
            self._view.update_page()
            return

        try:
            lun = int(self._view._txtInLun.value)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore numerico in lun", color="red")
            )
            self._view.update_page()
            return

        path, score = self._model.getBestPath(lun, self._view._ddProdStart.value, self._view._ddProdEnd.value)

        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Non ho trovato un cammino tra {self._view._ddProdStart.value} e {self._view._ddProdEnd.value}")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ecco il cammino migliore tra {self._view._ddProdStart.value} e {self._view._ddProdEnd.value}")
        )
        for p in path:
            self._view.txt_result.controls.append(
                ft.Text(f"{p}")
            )
        self._view.txt_result.controls.append(
            ft.Text(f"Score: {score}")
        )
        self._view.update_page()
        return



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)

    def fillDDProdotti(self):
        nodes = self._model.getAllNodes()
        for n in nodes:
            self._view._ddProdStart.options.append(
                ft.dropdown.Option(key=str(n.product_id), text=n.product_name)
            )
            self._view._ddProdEnd.options.append(
                ft.dropdown.Option(key=str(n.product_id), text=n.product_name)
            )
        self._view.update_page()
