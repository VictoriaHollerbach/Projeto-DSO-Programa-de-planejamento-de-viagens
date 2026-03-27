import FreeSimpleGUI as sg

class TelaRelatorio:
    def __init__(self, controlador):
        self.__controlador = controlador

    def mostra_tela_opcoes(self):
        layout = [
            [sg.Text('MENU DE RELATÓRIOS', justification='center', expand_x=True)],
            [sg.Button('Destinos Mais Visitados', key=1, expand_x=True)],
            [sg.Button('Destinos Mais Caros (Total Acumulado)', key=2, expand_x=True)],
            [sg.Button('Destinos Mais Baratos (Total Acumulado)', key=3, expand_x=True)],
            [sg.Button('Passeios Turísticos Mais Caros', key=4, expand_x=True)],
            [sg.Button('Retornar', key=0, expand_x=True, button_color=('white', 'orange'))]
        ]

        window = sg.Window('Menu Relatórios', layout)
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return 0
        return event

    def mostra_relatorio_destinos(self, titulo: str, relatorio: dict, tipo_dado: str = "Valor"):
        if not relatorio:
            self.mostra_mensagem("Não há dados para gerar este relatório.")
            return

        # Cria o texto formatado para o popup_scrolled
        linhas = [f"--- {titulo} ---\n"]
        linhas.append(f"{'Pos.':<5} | {'Destino':<30} | {tipo_dado}")
        linhas.append("-" * 50)
        
        for i, (local, dado) in enumerate(relatorio.items()):
            if isinstance(dado, float):
                valor_formatado = f"R$ {dado:.2f}"
            else:
                valor_formatado = str(dado)
            
            linhas.append(f"{i+1:<5} | {local:<30} | {valor_formatado}")

        texto_completo = "\n".join(linhas)
        self.mostra_lista_scroll(titulo, texto_completo)

    def mostra_relatorio_passeios(self, titulo: str, relatorio: dict):
        if not relatorio:
            self.mostra_mensagem("Não há dados para gerar este relatório.")
            return

        linhas = [f"--- {titulo} ---\n"]
        linhas.append(f"{'Pos.':<5} | {'Atração':<30} | {'Valor'}")
        linhas.append("-" * 50)
        
        for i, (atracao, valor) in enumerate(relatorio.items()):
            linhas.append(f"{i+1:<5} | {atracao:<30} | R$ {valor:.2f}")

        texto_completo = "\n".join(linhas)
        self.mostra_lista_scroll(titulo, texto_completo)

    def mostra_lista_scroll(self, titulo, texto_completo):
        sg.popup_scrolled(texto_completo, 
                           title=titulo, 
                           font=('Courier New', 11), # Fonte monoespaçada para alinhar colunas
                           size=(70, 20))

    def mostra_mensagem(self, mensagem):
        sg.popup(mensagem, title="Aviso do Sistema")
