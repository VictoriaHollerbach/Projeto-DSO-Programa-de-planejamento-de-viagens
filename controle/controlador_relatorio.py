from limite.tela_relatorio import TelaRelatorio
from collections import defaultdict

class ControladorRelatorios():
    def __init__(self, controlador_sistema):
        self.__tela_relatorio = TelaRelatorio(self)
        self.__controlador_sistema = controlador_sistema
        self.__controlador_viagens = controlador_sistema.controlador_viagens

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            0: self.retornar,
            1: self.destinos_mais_visitados,
            2: self.destinos_mais_caros,
            3: self.destinos_mais_baratos,
            4: self.passeios_turisticos_mais_caros
        }
        while True:
            try:
                opcao = self.__tela_relatorio.mostra_tela_opcoes()
                funcao_escolhida = lista_opcoes[opcao]
                funcao_escolhida()
            except Exception as e:
                self.__tela_relatorio.mostra_mensagem(f"Ocorreu um erro: {e}")

    def get_todos_trechos(self):
        todos_trechos = []
        for viagem in self.__controlador_viagens.viagem_DAO.get_all():
            todos_trechos.extend(viagem.trechos)
        return todos_trechos

    def get_todos_passeios(self):
        todos_passeios = []
        for viagem in self.__controlador_viagens.viagem_DAO.get_all():
            todos_passeios.extend(viagem.passeios_turisticos)
        return todos_passeios

    def destinos_mais_visitados(self):
        todos_trechos = self.get_todos_trechos()
        contagem_destinos = defaultdict(int)

        if not todos_trechos:
            self.__tela_relatorio.mostra_mensagem("Nenhum trecho cadastrado no sistema.")
            return

        for trecho in todos_trechos:
            contagem_destinos[trecho.destino] += 1
        
        top_destinos = sorted(
            contagem_destinos.items(),
            key=lambda x: x[1], 
            reverse=True
        )[:5]

        relatorio = {str(local): contagem for local, contagem in top_destinos}
        
        self.__tela_relatorio.mostra_relatorio_destinos(
            "Destinos Mais Visitados (Top 5)", 
            relatorio,
            tipo_dado="Visitas"
        )

    def destinos_mais_caros(self):
        todos_trechos = self.get_todos_trechos()
        soma_valores_destinos = defaultdict(float)

        if not todos_trechos:
            self.__tela_relatorio.mostra_mensagem("Nenhum trecho cadastrado no sistema.")
            return
            
        for trecho in todos_trechos:
            soma_valores_destinos[trecho.destino] += trecho.valor_trecho
        
        top_destinos_caros = sorted(
            soma_valores_destinos.items(),
            key=lambda x: x[1], 
            reverse=True
        )[:5]

        relatorio = {str(local): valor for local, valor in top_destinos_caros}
        
        self.__tela_relatorio.mostra_relatorio_destinos(
            "Destinos Mais Caros (Top 5 Acumulado)", 
            relatorio
        )
        
    def destinos_mais_baratos(self):
        todos_trechos = self.get_todos_trechos()
        soma_valores_destinos = defaultdict(float)

        if not todos_trechos:
            self.__tela_relatorio.mostra_mensagem("Nenhum trecho cadastrado no sistema.")
            return
            
        for trecho in todos_trechos:
            soma_valores_destinos[trecho.destino] += trecho.valor_trecho
        
        top_destinos_baratos = sorted(
            soma_valores_destinos.items(),
            key=lambda x: x[1], 
            reverse=False
        )[:5]

        relatorio = {str(local): valor for local, valor in top_destinos_baratos}
        
        self.__tela_relatorio.mostra_relatorio_destinos(
            "Destinos Mais Baratos (Top 5 Acumulado)", 
            relatorio
        )

    def passeios_turisticos_mais_caros(self):
        todos_passeios = self.get_todos_passeios()
        valores_passeios = {}

        if not todos_passeios:
            self.__tela_relatorio.mostra_mensagem("Nenhum passeio turístico cadastrado.")
            return

        for passeio in todos_passeios:
            atracao = passeio.atracao_turistica
            valor = passeio.valor_passeio
            valores_passeios[atracao] = valor
        
        top_passeios_caros = sorted(
            valores_passeios.items(),
            key=lambda x: x[1], 
            reverse=True
        )[:5]

        relatorio = dict(top_passeios_caros)
        
        self.__tela_relatorio.mostra_relatorio_passeios(
            "Passeios Turísticos Mais Caros (Top 5)", 
            relatorio
        )
