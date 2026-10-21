import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDAnni(self):
        for a in self._model.getAnni():
            self._view._ddAnno1.options.append(ft.dropdown.Option(str(a)))
            self._view._ddAnno2.options.append(ft.dropdown.Option(str(a)))

    # ==================== PUNTO 1 ====================

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        # 1. leggo e controllo gli anni
        if self._view._ddAnno1.value is None or self._view._ddAnno2.value is None:
            self._errore("Selezionare entrambi gli anni!")
            return
        anno1 = int(self._view._ddAnno1.value)
        anno2 = int(self._view._ddAnno2.value)
        if anno1 > anno2:
            self._errore("L'anno di inizio non può essere successivo all'anno di fine!")
            return

        # 2. creo il grafo
        self._model.buildGraph(anno1, anno2)
        if self._model.getNumNodi() == 0:
            self._errore("Nessun circuito trovato nel periodo selezionato!")
            return

        # 3. stampo nodi e archi
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self._view._ddCostruttore.options.clear()
        self._view._ddCostruttore.value = None
        for c in self._model.getNodiOrdinati():
            self._view._ddCostruttore.options.append(ft.dropdown.Option(key=str(c.constructorId), text=c.name))
        self._view.update_page()

    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # a. i 3 archi di peso maggiore
        self._view._txt_result.controls.append(ft.Text("Top 3 archi di peso maggiore:"))
        for i, (u, v, peso) in enumerate(self._model.getTop3(), start=1):
            self._view._txt_result.controls.append(ft.Text(f"{i}. {u} -> {v} (peso: {peso})"))

        #b. componenti fortemente connesse
        best, valB = self._model.getEsportatore()
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(
            ft.Text(f"Maggior esportatore di piloti: {best} con : {valB}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di componenti debolmente connesse: {self._model.getNumComponentiDeboli()}"))
        self._view.update_page()

    def handleCarriera(self, e):
        self._view._txt_result.controls.clear()

        # 1. il grafo deve esistere
        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # 2. costruttore di partenza
        if self._view._ddCostruttore.value is None:
            self._errore("Selezionare un costruttore di partenza!")
            return
        partenza = self._model.getCostruttore(int(self._view._ddCostruttore.value))
        if partenza is None:
            self._errore("Costruttore non presente nel grafo, ricreare il grafo!")
            return

        # 3. ricorsione
        cammino, peso = self._model.getCammino(partenza)

        # 4. stampa
        self._view._txt_result.controls.append(
            ft.Text(f"Carriera in ascesa più lunga partendo da {partenza}:"))
        for i, c in enumerate(cammino, start=1):
            self._view._txt_result.controls.append(
                ft.Text(f"{i}. {c} - punti: {c.punti}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di costruttori: {len(cammino)}"))
        self._view._txt_result.controls.append(ft.Text(f"Somma dei pesi: {peso}"))

        self._view.update_page()

