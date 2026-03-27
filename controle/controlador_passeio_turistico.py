from entidade.passeio_turistico import PasseioTuristico
from limite.tela_passeio_turistico import TelaPasseioTuristico
from DAO.passeio_turistico_dao import PasseioTuristicoDAO

class ControladorPasseioTuristicos():
    def __init__(self, controlador_sistema):
        self.__tela_passeio_turistico = TelaPasseioTuristico(self)
        self.__passeio_turistico_DAO = PasseioTuristicoDAO()
        self.__controlador_sistema = controlador_sistema

    @property
    def passeio_turistico_DAO(self):
        return self.__passeio_turistico_DAO
    
    @property
    def controlador_sistema(self):
        return self.__controlador_sistema
    
    def find_passeio_by_atracao_na_viagem(self, viagem, atracao_turistica: str):
        for passeio in viagem.passeios_turisticos:
            if passeio.atracao_turistica == atracao_turistica:
                return passeio
        return None
    
    def _seleciona_viagem_obj(self):
        viagens = list(self.controlador_sistema.controlador_viagens.viagem_DAO.get_all())
        
        if not viagens:
            self.__tela_passeio_turistico.mostra_mensagem("ERRO: Não há nenhuma viagem cadastrada para gerenciar passeios.")
            return None

        lista_formatada = []
        for v in viagens:
            lista_formatada.append(f"Cód: {v.codigo} | Nome: {v.nome_viagem}")

        codigo = self.__tela_passeio_turistico.seleciona_viagem_integrada(lista_formatada)
        
        if codigo is None:
            return None
        
        viagem = self.controlador_sistema.controlador_viagens.find_viagem_by_codigo(codigo)
        if viagem is None:
            self.__tela_passeio_turistico.mostra_mensagem("ERRO: Viagem não encontrada.")
            return None
        return viagem

    def _seleciona_passeio_obj(self, viagem):
        passeios = viagem.passeios_turisticos
        if not passeios:
            self.__tela_passeio_turistico.mostra_mensagem("ERRO: Esta viagem não possui passeios cadastrados.")
            return None
        
        lista_formatada = []
        for p in passeios:
            lista_formatada.append(f"Atração: {p.atracao_turistica} | Cidade: {p.cidade}")
        
        atracao = self.__tela_passeio_turistico.seleciona_passeio_integrado(lista_formatada)
        
        if atracao is None:
            return None
        
        passeio = self.find_passeio_by_atracao_na_viagem(viagem, atracao)
        if passeio is None:
            self.__tela_passeio_turistico.mostra_mensagem("ERRO: Passeio não encontrado nesta viagem.")
            return None
        return passeio

    def incluir_passeio(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return

        dados_passeio = self.__tela_passeio_turistico.pega_dados_passeio()
        if dados_passeio is None:
            return

        atracao = dados_passeio['atracao_turistica']
        passeio = self.find_passeio_by_atracao_na_viagem(viagem, atracao)
        
        if passeio is None:
            novo_passeio = PasseioTuristico(
                dados_passeio['dia'],
                dados_passeio['cidade'],
                dados_passeio['atracao_turistica'],
                dados_passeio['horario_inc'],
                dados_passeio['horario_fim'],
                dados_passeio['valor_passeio']
            )
            viagem.passeios_turisticos.append(novo_passeio)
            self.controlador_sistema.controlador_viagens.atualiza_viagem(viagem)
            
            # Adiciona ao DAO global para persistência se necessário
            # Verifica duplicidade simples pela atração
            existe = False
            for p in self.__passeio_turistico_DAO.get_all():
                if p.atracao_turistica == novo_passeio.atracao_turistica:
                    existe = True
                    break
            if not existe:
                self.__passeio_turistico_DAO.add(novo_passeio)
                
            self.__tela_passeio_turistico.mostra_mensagem("Passeio cadastrado com sucesso!")
        else:
            self.__tela_passeio_turistico.mostra_mensagem("Erro: Essa atração já está cadastrada nesta viagem!")

    def excluir_passeio(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return

        passeio_a_remover = self._seleciona_passeio_obj(viagem)
        if passeio_a_remover is not None:
            # Tenta remover do DAO global primeiro (opcional, depende da regra de negócio)
            try:
                self.__passeio_turistico_DAO.remove(passeio_a_remover.atracao_turistica)
            except:
                pass # Se não estiver no DAO global, ignora

            viagem.passeios_turisticos.remove(passeio_a_remover)
            self.controlador_sistema.controlador_viagens.atualiza_viagem(viagem)
            self.__tela_passeio_turistico.mostra_mensagem('Passeio removido com sucesso!')
    
    def alterar_passeio(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return

        passeio = self._seleciona_passeio_obj(viagem)
        if passeio is not None:
            novos_dados = self.__tela_passeio_turistico.pega_dados_passeio()
            if novos_dados is None:
                return
            
            # Atualiza objeto
            passeio.dia = novos_dados['dia']
            passeio.cidade = novos_dados['cidade']
            passeio.atracao_turistica = novos_dados['atracao_turistica']
            passeio.horario_inc = novos_dados['horario_inc']
            passeio.horario_fim = novos_dados['horario_fim']
            passeio.valor_passeio = novos_dados['valor_passeio']
            
            # Persiste a alteração na viagem
            self.controlador_sistema.controlador_viagens.atualiza_viagem(viagem)
            
            # Persiste no DAO global se existir
            # (Assumindo que o DAO usa atracao_turistica como chave, update pode ser complexo se a chave mudar)
            # Aqui, simplificamos apenas atualizando a viagem
            
            self.listar_passeios(viagem)
        else:
            self.__tela_passeio_turistico.mostra_mensagem('Erro: passeio não encontrado')
    
    def listar_passeios_da_viagem(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return
        self.listar_passeios(viagem)
    
    def listar_passeios(self, viagem):
        titulo = f"--- Passeios da Viagem: {viagem.nome_viagem} ---"
        if not viagem.passeios_turisticos:
            self.__tela_passeio_turistico.mostra_mensagem("Nenhum passeio turístico registrado.")
            return
        
        lista_de_strings = [titulo]
        for passeio in viagem.passeios_turisticos:
            lista_de_strings.append(str(passeio))
        
        texto_completo = "\n\n".join(lista_de_strings)
        self.__tela_passeio_turistico.mostra_lista_scroll("Lista de Passeios", texto_completo)

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            0: self.retornar,
            1: self.incluir_passeio,
            2: self.excluir_passeio,
            3: self.alterar_passeio,
            4: self.listar_passeios_da_viagem
        }
        while True:
            opcao = self.__tela_passeio_turistico.mostra_tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao]
            funcao_escolhida()
