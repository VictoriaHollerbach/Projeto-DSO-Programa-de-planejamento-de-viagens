from limite.tela_pagamento import TelaPagamento
from entidade.pix import Pix
from entidade.dinheiro import Dinheiro
from entidade.cartao import Cartao
from entidade.pagamento import Pagamento
from DAO.pagamento_dao import PagamentoDAO

class ControladorPagamentos():
    def __init__(self, controlador_sistema):
        self.__tela_pagamento = TelaPagamento(self)
        self.__pagamento_DAO = PagamentoDAO()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_pessoas = controlador_sistema.controlador_pessoas

    @property
    def pagamento_DAO(self):
        return self.__pagamento_DAO
    
    @property
    def controlador_sistema(self):
        return self.__controlador_sistema
    
    def _seleciona_viagem_obj(self):
        viagens = list(self.controlador_sistema.controlador_viagens.viagem_DAO.get_all())
        
        if not viagens:
            self.__tela_pagamento.mostra_mensagem("ERRO: Não há nenhuma viagem cadastrada para registrar pagamentos.")
            return None

        lista_formatada = []
        for v in viagens:
            lista_formatada.append(f"Cód: {v.codigo} | Nome: {v.nome_viagem}")

        codigo = self.__tela_pagamento.seleciona_viagem_integrada(lista_formatada)
        
        if codigo is None:
            return None
        
        viagem = self.controlador_sistema.controlador_viagens.find_viagem_by_codigo(codigo)
        if viagem is None:
            self.__tela_pagamento.mostra_mensagem("ERRO: Viagem não encontrada.")
            return None
        return viagem

    def _seleciona_pessoa_pagadora(self, viagem):
        pessoas = viagem.pessoas
        if not pessoas:
            self.__tela_pagamento.mostra_mensagem("ERRO: Esta viagem não tem pessoas cadastradas.")
            return None
        
        lista_formatada = []
        for p in pessoas:
            lista_formatada.append(f"Nome: {p.nome} | ID: {p.identificacao}")
        
        identificacao = self.__tela_pagamento.seleciona_pessoa_integrada(lista_formatada)
        
        if identificacao is None:
            return None
        
        # Busca pessoa na lista da viagem
        for p in pessoas:
            if p.identificacao == identificacao:
                return p
        
        self.__tela_pagamento.mostra_mensagem("ERRO: Pessoa não encontrada nesta viagem.")
        return None

    def incluir_pagamento(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return

        pessoa_selecionada = self._seleciona_pessoa_pagadora(viagem)
        if pessoa_selecionada is None:
            return

        dados_pagamento = self.__tela_pagamento.pega_dados_pagamento(pessoa_selecionada.nome)
        if dados_pagamento is None:
            return

        try:
            novo_pagamento = None
            # Adiciona dados comuns
            dados_pagamento['pessoa'] = pessoa_selecionada
            dados_pagamento['cpf'] = pessoa_selecionada.identificacao

            if dados_pagamento['tipo'] == 'PIX':
                novo_pagamento = Pix(
                    dados_pagamento['codigo'], dados_pagamento['valor'],
                    dados_pagamento['pessoa'], dados_pagamento['data'],
                    dados_pagamento['cpf']
                )
            elif dados_pagamento['tipo'] == 'DINHEIRO':
                novo_pagamento = Dinheiro(
                    dados_pagamento['codigo'], dados_pagamento['valor'],
                    dados_pagamento['pessoa'], dados_pagamento['data'],
                    dados_pagamento['cpf']
                )
            elif dados_pagamento['tipo'] == 'CARTAO':
                novo_pagamento = Cartao(
                    dados_pagamento['codigo'], dados_pagamento['valor'],
                    dados_pagamento['pessoa'], dados_pagamento['data'],
                    dados_pagamento['numero_cartao'], dados_pagamento['bandeira']
                )

            if novo_pagamento:
                viagem.pagamentos.append(novo_pagamento)
                self.controlador_sistema.controlador_viagens.atualiza_viagem(viagem)
                
                # Adiciona ao DAO global se necessário, ou apenas mantém na viagem
                # Verificando duplicação simples pelo código
                existe = False
                for p in self.__pagamento_DAO.get_all():
                    if p.codigo == novo_pagamento.codigo:
                        existe = True
                        break
                
                if not existe:
                    self.__pagamento_DAO.add(novo_pagamento)
                
                self.__tela_pagamento.mostra_mensagem(f"Pagamento registrado com sucesso!")

        except Exception as e:
            self.__tela_pagamento.mostra_mensagem(f"Erro ao registrar pagamento: {e}")
    
    def listar_pagamentos(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return

        titulo = f"--- Pagamentos da Viagem: {viagem.nome_viagem} ---"
        if not viagem.pagamentos:
            self.__tela_pagamento.mostra_mensagem("Nenhum pagamento registrado nesta viagem.")
            return
        
        lista_de_strings = [titulo]
        for pagamento in viagem.pagamentos:
            lista_de_strings.append(str(pagamento))
        
        texto_completo = "\n\n".join(lista_de_strings)
        self.__tela_pagamento.mostra_lista_scroll("Lista de Pagamentos", texto_completo)
    
    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            0: self.retornar,
            1: self.incluir_pagamento,
            2: self.listar_pagamentos
        }

        while True:
            opcao = self.__tela_pagamento.mostra_tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao]
            funcao_escolhida()
