from entidade.viagem import Viagem
from limite.tela_viagem import TelaViagem
from DAO.viagem_dao import ViagemDAO
from collections import defaultdict

class ControladorViagens():
    def __init__(self, controlador_sistema):
        self.__tela_viagem = TelaViagem(self)
        self.__viagem_DAO = ViagemDAO()
        self.__controlador_sistema = controlador_sistema

    @property
    def viagem_DAO(self):
        return self.__viagem_DAO
    
    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    def atualiza_viagem(self, viagem):
        self.__viagem_DAO.update(viagem)
    
    def find_viagem_by_codigo(self, codigo: int):
        for viagem in self.__viagem_DAO.get_all():
            if viagem.codigo == codigo:
                return viagem
        return None
    
    def _seleciona_viagem_obj(self):
        viagens = list(self.__viagem_DAO.get_all())
        
        if not viagens:
            self.__tela_viagem.mostra_mensagem("ERRO: Não há nenhuma viagem cadastrada no sistema.")
            return None

        lista_formatada = []
        for v in viagens:
            lista_formatada.append(f"Cód: {v.codigo} | Nome: {v.nome_viagem} | Início: {v.data_inc}")

        codigo = self.__tela_viagem.seleciona_viagem_integrada(lista_formatada)
        
        if codigo is None:
            return None
        
        viagem = self.find_viagem_by_codigo(codigo)
        if viagem is None:
            self.__tela_viagem.mostra_mensagem("ERRO: Viagem não encontrada.")
            return None
        return viagem

    def incluir_viagem(self):
        dados_viagem = self.__tela_viagem.pega_dados_viagem()
        if dados_viagem is None:
            return

        codigo = dados_viagem['codigo']
        viagem = self.find_viagem_by_codigo(codigo)
        if viagem is None:
            nova_viagem = Viagem(dados_viagem['codigo'], dados_viagem['nome_viagem'],
                                   dados_viagem['data_inc'], dados_viagem['data_fim'])
            self.__viagem_DAO.add(nova_viagem)
            self.__tela_viagem.mostra_mensagem("Viagem cadastrada com sucesso!")
        else:
            self.__tela_viagem.mostra_mensagem("Erro: Essa viagem já está cadastrada!")
        return None
    
    def excluir_viagem(self):
        viagem_a_remover = self._seleciona_viagem_obj()
        if viagem_a_remover is not None:
            self.__viagem_DAO.remove(viagem_a_remover.codigo)
            self.__tela_viagem.mostra_mensagem('Viagem removida com sucesso!')
    
    def alterar_viagem(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is not None:
            novos_dados = self.__tela_viagem.pega_dados_viagem()
            if novos_dados is None:
                return

            viagem.codigo = novos_dados['codigo']
            viagem.nome_viagem = novos_dados['nome_viagem']
            viagem.data_inc = novos_dados['data_inc']
            viagem.data_fim = novos_dados['data_fim']
            self.atualiza_viagem(viagem)
            self.listar_viagens()

    def listar_viagens(self):
        viagens = self.__viagem_DAO.get_all()
        titulo = "Lista de Viagens Registradas"
        if not viagens:
            self.__tela_viagem.mostra_mensagem("Nenhuma viagem registrada.")
            return

        lista_de_strings = [titulo]
        for viagem in viagens:
            lista_de_strings.append(str(viagem))
        
        texto_completo = "\n\n".join(lista_de_strings)
        self.__tela_viagem.mostra_lista_scroll("Lista de Viagens", texto_completo)

    def valor_total_por_pessoa(self, viagem):
        total_por_pessoa = 0.0
        for trecho in viagem.trechos:
            total_por_pessoa += trecho.valor_trecho
        for passeio in viagem.passeios_turisticos:
            total_por_pessoa += passeio.valor_passeio
        return total_por_pessoa
    
    def exibir_valor_total_por_pessoa(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return

        total = self.valor_total_por_pessoa(viagem)
        self.__tela_viagem.mostra_mensagem(f'O valor do pacote para cada pessoa é R$ {total:.2f}')
        return total
    
    def valor_total(self, viagem):
        total_pessoa = self.valor_total_por_pessoa(viagem)
        numero_pessoas = len(viagem.pessoas)
        total = total_pessoa * numero_pessoas
        return total

    def exibir_valor_total(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return

        total = self.valor_total(viagem)
        numero_pessoas = len(viagem.pessoas)
        self.__tela_viagem.mostra_mensagem(
            f'Com um total de {numero_pessoas} participantes, o valor total da viagem é R$ {total:.2f}')
        return total
    
    def valor_pago(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return

        total_pago = sum(pagamento.valor for pagamento in viagem.pagamentos)
        total_viagem = self.valor_total(viagem)
        
        mensagens = ["Status de Pagamento Geral",
                     f'Total já pago por todos: R$ {total_pago:.2f}',
                     f'Valor total necessário: R$ {total_viagem:.2f}']

        if total_pago < total_viagem:
            mensagens.append(f'Falta pagar: R$ {total_viagem - total_pago:.2f}')
        elif total_pago > total_viagem:
            mensagens.append(f'Valor excedente pago: R$ {total_pago - total_viagem:.2f}')
        else:
            mensagens.append('O valor total da viagem foi integralmente pago!')

        self.__tela_viagem.mostra_mensagem("\n".join(mensagens))
        return total_pago
    
    def verificar_quem_pagou(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return []

        valor_por_pessoa = self.valor_total_por_pessoa(viagem)
        pagamentos_pessoa = defaultdict(float)
        for pagamento in viagem.pagamentos:
            identificacao = pagamento.pessoa.identificacao
            pagamentos_pessoa[identificacao] += pagamento.valor

        pessoas_pagaram = []
        pessoas_cadastradas = viagem.pessoas
        titulo = "Pessoas que Pagaram o Pacote Completo"
        
        if not pessoas_cadastradas:
            self.__tela_viagem.mostra_mensagem("Nenhuma pessoa cadastrada para verificar pagamentos.")
            return []

        lista_de_strings = [titulo]
        for pessoa in pessoas_cadastradas:
            total_pago = pagamentos_pessoa[pessoa.identificacao]
            if total_pago >= valor_por_pessoa:
                pessoas_pagaram.append(pessoa)
                lista_de_strings.append(f"- {pessoa.nome} (Pago: R$ {total_pago:.2f})")

        if not pessoas_pagaram:
            self.__tela_viagem.mostra_mensagem("Nenhuma pessoa pagou o valor completo do pacote ainda.")
            return []
        
        texto_completo = "\n\n".join(lista_de_strings)
        self.__tela_viagem.mostra_lista_scroll("Pagadores", texto_completo)
    
    def verificar_quem_nao_pagou(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return []

        valor_por_pessoa = self.valor_total_por_pessoa(viagem)
        pagamentos_pessoa = defaultdict(float)
        for pagamento in viagem.pagamentos:
            identificacao = pagamento.pessoa.identificacao
            pagamentos_pessoa[identificacao] += pagamento.valor

        pessoas_nao_pagaram = []
        pessoas_cadastradas = viagem.pessoas
        titulo = "Pessoas com Pagamento Pendente"

        if not pessoas_cadastradas:
            self.__tela_viagem.mostra_mensagem("Nenhuma pessoa cadastrada para verificar pagamentos.")
            return []
            
        lista_de_strings = [titulo]
        for pessoa in pessoas_cadastradas:
            total_pago = pagamentos_pessoa[pessoa.identificacao]

            if total_pago < valor_por_pessoa:
                falta_pagar = valor_por_pessoa - total_pago
                pessoas_nao_pagaram.append(pessoa)
                lista_de_strings.append(f"- {pessoa.nome} | Falta pagar: R$ {falta_pagar:.2f}")
        
        if not pessoas_nao_pagaram:
            self.__tela_viagem.mostra_mensagem("Todas as pessoas cadastradas pagaram o valor completo do pacote.")
            return []
        
        texto_completo = "\n\n".join(lista_de_strings)
        self.__tela_viagem.mostra_lista_scroll("Pagamentos Pendentes", texto_completo)
    
    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            0: self.retornar,
            1: self.incluir_viagem,
            2: self.excluir_viagem,
            3: self.alterar_viagem,
            4: self.listar_viagens,
            5: self.exibir_valor_total,
            6: self.exibir_valor_total_por_pessoa,
            7: self.valor_pago,
            8: self.verificar_quem_pagou,
            9: self.verificar_quem_nao_pagou
        }
        while True:
            opcao = self.__tela_viagem.mostra_tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao]
            funcao_escolhida()
