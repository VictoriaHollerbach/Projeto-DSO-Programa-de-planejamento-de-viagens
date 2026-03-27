import FreeSimpleGUI as sg

class TelaPessoa():
    def __init__(self, controlador):
        self.__controlador = controlador

    def mostra_tela_opcoes(self):
        layout = [
            [sg.Text('CADASTRO PESSOAS', justification='center', expand_x=True)],
            [sg.Button('Incluir Pessoa', key=1, expand_x=True)],
            [sg.Button('Excluir Pessoa de uma Viagem', key=2, expand_x=True)],
            [sg.Button('Excluir Pessoa do Sistema', key=3, expand_x=True)],
            [sg.Button('Editar dados da Pessoa', key=4, expand_x=True)],
            [sg.Button('Listar Pessoas de uma Viagem', key=5, expand_x=True)],
            [sg.Button('Listar Pessoas do Sistema', key=6, expand_x=True)],
            [sg.Button('Retornar', key=0, expand_x=True, button_color=('white', 'orange'))]
        ]
        window = sg.Window('Menu Pessoas', layout)
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return 0
        return event
    
    def pega_dados_pessoa(self):
        layout = [
            [sg.Text('Dados Pessoa', justification='center', expand_x=True)],
            [sg.Text('Nome:'), sg.Input(key='-NOME-')],
            [sg.Text('Celular:'), sg.Input(key='-CELULAR-')],
            [sg.Text('Identificação:'), sg.Input(key='-ID-')],
            [sg.Text('Idade:'), sg.Input(key='-IDADE-')],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]
        window = sg.Window('Dados da Pessoa', layout)

        while True:
            event, values = window.read()
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == 'Salvar':
                nome = values['-NOME-'].capitalize()
                
                if not nome:
                    self.mostra_mensagem('ERRO: O campo Nome não pode estar vazio.')
                    continue
                
                try:
                    celular = int(values['-CELULAR-'])
                    identificacao = int(values['-ID-'])
                    idade = int(values['-IDADE-'])

                    if celular <= 0 or identificacao <= 0:
                        self.mostra_mensagem('ERRO: Celular e Identificação devem ser números positivos.')
                        continue
                    
                    if idade <= 17:
                        self.mostra_mensagem('ERRO: A pessoa deve ter 18 anos ou mais.')
                        continue
                    
                    window.close()
                    return {'nome': nome, 'celular': celular, 'identificacao': identificacao, 'idade': idade}
                
                except ValueError:
                    self.mostra_mensagem('ERRO: Celular, Identificação e Idade devem ser números inteiros.')
                    continue
    
    def seleciona_pessoa(self):
        while True:
            valor_lido = sg.popup_get_text('Identificação da pessoa que deseja selecionar:', title="Selecionar Pessoa")
            
            if valor_lido is None:
                return None
            
            try:
                identificacao = int(valor_lido)
                if identificacao <= 0:
                    self.mostra_mensagem('ERRO: Identificação deve ser um número positivo.')
                    continue
                return identificacao
            
            except ValueError:
                self.mostra_mensagem('ERRO: Digite uma Identificação numérica válida.')

    def seleciona_viagem_integrada(self, lista_viagens_formatada):
        layout = [
            [sg.Text('Selecione uma Viagem da lista ou digite o código:', font=('Helvetica', 10, 'bold'))],
            [sg.Listbox(values=lista_viagens_formatada, size=(60, 10), key='-LISTA-', enable_events=True)],
            [sg.Text('Código da Viagem:'), sg.Input(key='-CODIGO-', size=(10, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Selecionar Viagem', layout)

        while True:
            event, values = window.read()
            
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == '-LISTA-' and values['-LISTA-']:
                linha_selecionada = values['-LISTA-'][0]
                try:
                    codigo_str = linha_selecionada.split('Cód: ')[1].split(' |')[0]
                    window['-CODIGO-'].update(codigo_str)
                except IndexError:
                    pass

            if event == 'Confirmar':
                valor_lido = values['-CODIGO-']
                try:
                    codigo = int(valor_lido)
                    if codigo <= 0:
                        self.mostra_mensagem('ERRO: O Código deve ser um número positivo.')
                        continue
                    window.close()
                    return codigo
                except ValueError:
                    self.mostra_mensagem('ERRO: Digite um Código numérico válido ou selecione na lista.')

    def mostra_lista_scroll(self, titulo, texto_completo):
        sg.popup_scrolled(texto_completo, 
                           title=titulo, 
                           font=('Helvetica', 12), 
                           size=(60, 15))

    def mostra_mensagem(self, mensagem):
        sg.popup(mensagem, title="Aviso do Sistema")
