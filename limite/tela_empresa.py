import FreeSimpleGUI as sg

class TelaEmpresa:
    def __init__(self, controlador): 
        self.__controlador = controlador

    def mostra_tela_opcoes(self):
        layout = [
            [sg.Text('Sistema de Empresas', justification='center', expand_x=True)],
            [sg.Button('Incluir Empresa', key=1, expand_x=True)],
            [sg.Button('Excluir Empresa', key=2, expand_x=True)],
            [sg.Button('Alterar Dados da Empresa', key=3, expand_x=True)],
            [sg.Button('Listar Empresas', key=4, expand_x=True)],
            [sg.Button('Retornar ao Menu Principal', key=0, expand_x=True, button_color=('white', 'orange'))]
        ]

        window = sg.Window('Menu de Empresas', layout)
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return 0
        return event
    
    def pega_dados_empresa(self):
        layout = [
            [sg.Text('Dados Empresa', justification='center', expand_x=True)],
            [sg.Text('Nome:', size=(8,1)), sg.Input(key='-NOME-')],
            [sg.Text('CNPJ:', size=(8,1)), sg.Input(key='-CNPJ-')],
            [sg.Text('Telefone:', size=(8,1)), sg.Input(key='-TELEFONE-')],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]

        window = sg.Window('Dados da Empresa', layout)

        while True:
            event, values = window.read()
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            elif event == 'Salvar':
                nome = values['-NOME-'].capitalize()

                if not nome:
                    self.mostra_mensagem('ERRO: O campo Nome não pode estar vazio.')
                    continue

                try:
                    cnpj = int(values['-CNPJ-'])
                    telefone = int(values['-TELEFONE-'])

                    if cnpj <= 0 or telefone <= 0:
                        self.mostra_mensagem('ERRO: CNPJ e Telefone devem ser números positivos.')
                        continue

                    window.close()
                    return {'nome': nome, 'cnpj': cnpj, 'telefone': telefone}
                
                except ValueError:
                    self.mostra_mensagem('ERRO: CNPJ e Telefone devem conter apenas números.')
                    continue
    
    def seleciona_empresa_integrada(self, lista_empresas_formatada):
        layout = [
            [sg.Text('Selecione uma Empresa da lista ou digite o CNPJ:', font=('Helvetica', 10, 'bold'))],
            [sg.Listbox(values=lista_empresas_formatada, size=(60, 10), key='-LISTA-', enable_events=True)],
            [sg.Text('CNPJ da Empresa:'), sg.Input(key='-CNPJ-', size=(15, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Selecionar Empresa', layout)

        while True:
            event, values = window.read()
            
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == '-LISTA-' and values['-LISTA-']:
                linha_selecionada = values['-LISTA-'][0]
                try:
                    cnpj_str = linha_selecionada.split('CNPJ: ')[1].split(' |')[0]
                    window['-CNPJ-'].update(cnpj_str)
                except IndexError:
                    pass

            if event == 'Confirmar':
                valor_lido = values['-CNPJ-']
                try:
                    cnpj = int(valor_lido)
                    if cnpj <= 0:
                        self.mostra_mensagem('ERRO: O CNPJ deve ser um número positivo.')
                        continue
                    window.close()
                    return cnpj
                except ValueError:
                    self.mostra_mensagem('ERRO: Digite um CNPJ numérico válido ou selecione na lista.')

    def mostra_lista_scroll(self, titulo, texto_completo):
        sg.popup_scrolled(texto_completo, 
                           title=titulo, 
                           font=('Helvetica', 12), 
                           size=(60, 15))

    def mostra_mensagem(self, mensagem):
        sg.popup(mensagem, title="Aviso do Sistema")
