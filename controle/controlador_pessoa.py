from entidade.pessoa import Pessoa
from limite.tela_pessoa import TelaPessoa
from DAO.pessoa_dao import PessoaDAO

class ControladorPessoas():
    def __init__(self, controlador_sistema):
        self.__tela_pessoa = TelaPessoa(self)
        self.__pessoa_DAO = PessoaDAO()
        self.__controlador_sistema = controlador_sistema

    @property
    def pessoa_DAO(self):
        return self.__pessoa_DAO
    
    @property
    def controlador_sistema(self):
        return self.__controlador_sistema
    
    def find_pessoa_by_identificacao(self, identificacao: int):
        for pessoa in self.__pessoa_DAO.get_all():
            if pessoa.identificacao == identificacao:
                return pessoa
        return None
    
    def find_pessoa_by_identificacao_na_viagem(self, viagem, identificacao: int):
        for pessoa in viagem.pessoas:
            if pessoa.identificacao == identificacao:
                return pessoa
        return None
    
    def _seleciona_viagem_obj(self):
        viagens = list(self.controlador_sistema.controlador_viagens.viagem_DAO.get_all())

        if not viagens:
            self.__tela_pessoa.mostra_mensagem("ERRO: Não há nenhuma viagem cadastrada no sistema para selecionar.")
            return None

        lista_formatada = []
        for v in viagens:
            lista_formatada.append(f"Cód: {v.codigo} | Nome: {v.nome_viagem} | Início: {v.data_inc}")

        codigo = self.__tela_pessoa.seleciona_viagem_integrada(lista_formatada)
        
        if codigo is None:
            return None
        
        viagem = self.controlador_sistema.controlador_viagens.find_viagem_by_codigo(codigo)
        if viagem is None:
            self.__tela_pessoa.mostra_mensagem("ERRO: Viagem não encontrada.")
            return None
        return viagem

    def incluir_pessoa(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return

        dados_pessoa = self.__tela_pessoa.pega_dados_pessoa()
        if dados_pessoa is None:
            return

        identificacao = dados_pessoa['identificacao']
        nome = dados_pessoa['nome']
        celular = dados_pessoa['celular']
        idade = dados_pessoa['idade']

        pessoa_no_sistema = self.find_pessoa_by_identificacao(identificacao)
        if pessoa_no_sistema:
            if pessoa_no_sistema.nome == nome and pessoa_no_sistema.celular == celular and pessoa_no_sistema.idade == idade:
                pessoa = self.find_pessoa_by_identificacao_na_viagem(viagem, identificacao)
                if pessoa is None:
                    nova_pessoa = Pessoa(dados_pessoa['nome'], dados_pessoa['celular'],
                                       dados_pessoa['identificacao'], dados_pessoa['idade'])
                    viagem.pessoas.append(nova_pessoa)
                    self.controlador_sistema.controlador_viagens.atualiza_viagem(viagem)
                    self.__tela_pessoa.mostra_mensagem("Pessoa cadastrada com sucesso!")
                else:
                    self.__tela_pessoa.mostra_mensagem("Erro: Essa pessoa já está cadastrada!")
            else:
                self.__tela_pessoa.mostra_mensagem("Erro: Essa dentificação já está sendo usada para outro usuário!")
        else:
            pessoa = self.find_pessoa_by_identificacao_na_viagem(viagem, identificacao)
            if pessoa is None:
                nova_pessoa = Pessoa(dados_pessoa['nome'], dados_pessoa['celular'],
                                   dados_pessoa['identificacao'], dados_pessoa['idade'])
                viagem.pessoas.append(nova_pessoa)
                self.controlador_sistema.controlador_viagens.atualiza_viagem(viagem)
                self.__pessoa_DAO.add(nova_pessoa)
                self.__tela_pessoa.mostra_mensagem("Pessoa cadastrada com sucesso!")
                
        return None
    
    def excluir_pessoa_da_viagem(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return
        
        self.listar_pessoas(viagem)
        
        identificacao = self.__tela_pessoa.seleciona_pessoa()
        if identificacao is None:
            return

        pessoa_a_remover = self.find_pessoa_by_identificacao_na_viagem(viagem, identificacao)
        if pessoa_a_remover is not None:
            viagem.pessoas.remove(pessoa_a_remover)
            self.controlador_sistema.controlador_viagens.atualiza_viagem(viagem)
            self.__tela_pessoa.mostra_mensagem('Pessoa removida com sucesso!')
        else:
            self.__tela_pessoa.mostra_mensagem(f'Erro: essa pessoa NÃO está cadastrada!')
    
    def excluir_pessoa_do_sistema(self):
        self.listar_pessoas_no_sistema()
        
        identificacao = self.__tela_pessoa.seleciona_pessoa()
        if identificacao is None:
            return

        pessoa_a_remover = self.find_pessoa_by_identificacao(identificacao)
        if pessoa_a_remover is not None:
            self.__pessoa_DAO.remove(pessoa_a_remover.identificacao)
            self.__tela_pessoa.mostra_mensagem('Pessoa removida com sucesso!')
        else:
            self.__tela_pessoa.mostra_mensagem(f'Erro: essa pessoa NÃO está cadastrada!')
    
    def alterar_pessoa(self):
        self.listar_pessoas_no_sistema()
        
        identificacao_pessoa = self.__tela_pessoa.seleciona_pessoa()
        if identificacao_pessoa is None:
            return
        
        pessoa = self.find_pessoa_by_identificacao(identificacao_pessoa)
        if pessoa is not None:
            novos_dados = self.__tela_pessoa.pega_dados_pessoa()
            if novos_dados is None:
                return

            for viagem in self.controlador_sistema.controlador_viagens.viagem_DAO.get_all():
                for pes in viagem.pessoas:
                    if pes.nome == pessoa.nome and pes.celular == pessoa.celular and pes.identificacao == pessoa.identificacao and pes.idade == pessoa.idade:
                        pes.nome = novos_dados['nome']
                        pes.celular = novos_dados['celular']
                        pes.identificacao = novos_dados['identificacao']
                        pes.idade = novos_dados['idade']
                self.controlador_sistema.controlador_viagens.atualiza_viagem(viagem)
            
            pessoa.nome = novos_dados['nome']
            pessoa.celular = novos_dados['celular']
            pessoa.identificacao = novos_dados['identificacao']
            pessoa.idade = novos_dados['idade']
            self.__pessoa_DAO.update(pessoa)
            self.listar_pessoas_no_sistema()
        else:
            self.__tela_pessoa.mostra_mensagem('Erro: pessoa não está cadastrada')
    
    def listar_pessoas_no_sistema(self):
        pessoas = self.__pessoa_DAO.get_all()
        titulo = "--- Lista de Pessoas Registradas no Sistema ---"
        if not pessoas:
            self.__tela_pessoa.mostra_mensagem("Nenhuma pessoa registrada.")
            return

        lista_de_strings = [titulo]
        for pessoa in pessoas:
            lista_de_strings.append(str(pessoa))
        
        texto_completo = "\n\n".join(lista_de_strings)
        self.__tela_pessoa.mostra_lista_scroll("Pessoas no Sistema", texto_completo)
    
    def listar_pessoas_na_viagem(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None:
            return
        self.listar_pessoas(viagem)
    
    def listar_pessoas(self, viagem):
        titulo = "--- Lista de Pessoas Registradas na Viagem ---"
        if not viagem.pessoas:
            self.__tela_pessoa.mostra_mensagem("Nenhuma pessoa registrada.")
            return
        
        lista_de_strings = [titulo]
        for pessoa in viagem.pessoas:
            lista_de_strings.append(str(pessoa))
        
        texto_completo = "\n\n".join(lista_de_strings)
        self.__tela_pessoa.mostra_lista_scroll("Pessoas na Viagem", texto_completo)
    
    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            0: self.retornar,
            1: self.incluir_pessoa,
            2: self.excluir_pessoa_da_viagem,
            3: self.excluir_pessoa_do_sistema,
            4: self.alterar_pessoa,
            5: self.listar_pessoas_na_viagem,
            6: self.listar_pessoas_no_sistema
        }
        while True:
            opcao = self.__tela_pessoa.mostra_tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao]
            funcao_escolhida()
