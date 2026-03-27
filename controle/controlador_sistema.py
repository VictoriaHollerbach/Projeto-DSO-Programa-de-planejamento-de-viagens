from controle.controlador_empresa import ControladorEmpresas
from controle.controlador_local import ControladorLocais
from controle.controlador_pagamento import ControladorPagamentos
from controle.controlador_passeio_turistico import ControladorPasseioTuristicos
from controle.controlador_pessoa import ControladorPessoas
from controle.controlador_transporte import ControladorTransportes
from controle.controlador_trecho import ControladorTrechos
from controle.controlador_viagem import ControladorViagens
from controle.controlador_relatorio import ControladorRelatorios
from limite.tela_sistema import TelaSistema


class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = TelaSistema()
        self.__controlador_locais = ControladorLocais(self)
        self.__controlador_pessoas = ControladorPessoas(self)
        self.__controlador_transportes = ControladorTransportes(self)
        self.__controlador_empresas = ControladorEmpresas(self)
        self.__controlador_trechos = ControladorTrechos(self)
        self.__controlador_passeio_turisticos = ControladorPasseioTuristicos(self)
        self.__controlador_pagamentos = ControladorPagamentos(self)
        self.__controlador_viagens = ControladorViagens(self)
        self.__controlador_relatorios = ControladorRelatorios(self)
    
    @property
    def controlador_locais(self):
        return self.__controlador_locais

    @property
    def controlador_pessoas(self):
        return self.__controlador_pessoas

    @property
    def controlador_transportes(self):
        return self.__controlador_transportes

    @property
    def controlador_empresas(self):
        return self.__controlador_empresas

    @property
    def controlador_trechos(self):
        return self.__controlador_trechos

    @property
    def controlador_passeio_turisticos(self):
        return self.__controlador_passeio_turisticos 

    @property
    def controlador_pagamentos(self):
        return self.__controlador_pagamentos

    @property
    def controlador_viagens(self):
        return self.__controlador_viagens
    
    @property
    def controlador_relatorios(self):
        return self.__controlador_relatorios
    
    def inicializa_sistema(self):
        self.abre_tela()

    def encerra_sistema(self):
        self.__tela_sistema.mostra_mensagem('Sistema Encerrado! Volte Sempre!')
        exit(0)
    
    def abre_tela(self):
        lista_opcoes = {
            1: self.cadastra_viagens,
            2: self.cadastra_pessoas,
            3: self.cadastra_locais,
            4: self.cadastra_transportes,
            5: self.cadastra_empresas,
            6: self.cadastra_trechos,
            7: self.cadastra_passeios_turisticos,
            8: self.cadastra_pagamentos,
            9: self.fazer_relatorios,
            0: self.encerra_sistema
        }
        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()
    
    def cadastra_pessoas(self): 
        self.__controlador_pessoas.abre_tela()

    def cadastra_locais(self):
        self.__controlador_locais.abre_tela()

    def cadastra_transportes(self):
        self.__controlador_transportes.abre_tela()

    def cadastra_empresas(self):
        self.__controlador_empresas.abre_tela()

    def cadastra_trechos(self):
        self.__controlador_trechos.abre_tela()

    def cadastra_passeios_turisticos(self):
        self.__controlador_passeio_turisticos.abre_tela()

    def cadastra_pagamentos(self):
        self.__controlador_pagamentos.abre_tela()

    def cadastra_viagens(self):
        self.__controlador_viagens.abre_tela() 
    
    def fazer_relatorios(self):
        self.__controlador_relatorios.abre_tela()
