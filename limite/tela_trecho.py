import FreeSimpleGUI as sg

class TelaTrecho():
    def __init__(self, controlador):
        self.__controlador = controlador

    def mostra_tela_opcoes(self):
        layout = [
            [sg.Text('CADASTRO TRECHOS', justification='center', expand_x=True)],
            [sg.Button('Incluir Trecho', key=1, expand_x=True)],
            [sg.Button('Excluir Trecho', key=2, expand_x=True)],
            [sg.Button('Alterar Trecho', key=3, expand_x=True)],
            [sg.Button('Listar Trechos de uma Viagem', key=4, expand_x=True)],
            [sg.Button('Retornar', key=0, expand_x=True, button_color=('white', 'orange'))]
        ]
        window = sg.Window('Menu Trechos', layout)
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return 0
        return event

    def pega_dados_trecho_simples(self):
        layout = [
            [sg.Text('Dados do Trecho', justification='center', expand_x=True)],
            [sg.Text('Código:', size=(15, 1)), sg.Input(key='-CODIGO-')],
            [sg.Text('Data:', size=(15, 1)), sg.Input(key='-DATA-')],
            [sg.Text('Valor (R$):', size=(15, 1)), sg.Input(key='-VALOR-')],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]
        window = sg.Window('Dados Trecho', layout)

        while True:
            event, values = window.read()
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == 'Salvar':
                try:
                    data = values['-DATA-']
                    if not data:
                        self.mostra_mensagem('ERRO: A Data é obrigatória.')
                        continue

                    codigo = int(values['-CODIGO-'])
                    valor = float(values['-VALOR-'])

                    if codigo <= 0 or valor < 0:
                        self.mostra_mensagem('ERRO: Código deve ser positivo e Valor não negativo.')
                        continue
                    
                    window.close()
                    return {'codigo': codigo, 'data': data, 'valor_trecho': valor}
                
                except ValueError:
                    self.mostra_mensagem('ERRO: Verifique os tipos dos dados (Código inteiro, Valor numérico).')

    def seleciona_viagem_integrada(self, lista_formatada):
        layout = [
            [sg.Text('Selecione a Viagem:', font=('Helvetica', 10, 'bold'))],
            [sg.Listbox(values=lista_formatada, size=(60, 10), key='-LISTA-', enable_events=True)],
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
                try:
                    codigo_str = values['-LISTA-'][0].split('Cód: ')[1].split(' |')[0]
                    window['-CODIGO-'].update(codigo_str)
                except IndexError:
                    pass

            if event == 'Confirmar':
                try:
                    return int(values['-CODIGO-'])
                except ValueError:
                    self.mostra_mensagem('ERRO: Digite um Código numérico válido.')

    def seleciona_local_integrado(self, lista_formatada, titulo_janela="Selecionar Local"):
        layout = [
            [sg.Text(f'{titulo_janela}:', font=('Helvetica', 10, 'bold'))],
            [sg.Listbox(values=lista_formatada, size=(60, 10), key='-LISTA-', enable_events=True)],
            [sg.Text('Cidade:'), sg.Input(key='-CIDADE-', size=(20, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window(titulo_janela, layout)

        while True:
            event, values = window.read()
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == '-LISTA-' and values['-LISTA-']:
                try:
                    cidade_str = values['-LISTA-'][0].split('Cidade: ')[1].split(' |')[0]
                    window['-CIDADE-'].update(cidade_str)
                except IndexError:
                    pass

            if event == 'Confirmar':
                cidade = values['-CIDADE-'].capitalize()
                if cidade:
                    window.close()
                    return cidade
                self.mostra_mensagem('ERRO: Cidade inválida.')

    def seleciona_transporte_integrado(self, lista_formatada):
        layout = [
            [sg.Text('Selecione o Transporte:', font=('Helvetica', 10, 'bold'))],
            [sg.Listbox(values=lista_formatada, size=(60, 10), key='-LISTA-', enable_events=True)],
            [sg.Text('Tipo:'), sg.Input(key='-TIPO-', size=(20, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Selecionar Transporte', layout)

        while True:
            event, values = window.read()
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == '-LISTA-' and values['-LISTA-']:
                window['-TIPO-'].update(values['-LISTA-'][0])

            if event == 'Confirmar':
                tipo = values['-TIPO-'].capitalize()
                if tipo:
                    window.close()
                    return tipo
                self.mostra_mensagem('ERRO: Tipo inválido.')

    def seleciona_empresa_integrada(self, lista_formatada):
        layout = [
            [sg.Text('Selecione a Empresa:', font=('Helvetica', 10, 'bold'))],
            [sg.Listbox(values=lista_formatada, size=(60, 10), key='-LISTA-', enable_events=True)],
            [sg.Text('CNPJ:'), sg.Input(key='-CNPJ-', size=(20, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Selecionar Empresa', layout)

        while True:
            event, values = window.read()
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == '-LISTA-' and values['-LISTA-']:
                try:
                    cnpj_str = values['-LISTA-'][0].split('CNPJ: ')[1].split(' |')[0]
                    window['-CNPJ-'].update(cnpj_str)
                except IndexError:
                    pass

            if event == 'Confirmar':
                try:
                    return int(values['-CNPJ-'])
                except ValueError:
                    self.mostra_mensagem('ERRO: CNPJ inválido.')

    def seleciona_trecho_integrado(self, lista_formatada):
        layout = [
            [sg.Text('Selecione o Trecho:', font=('Helvetica', 10, 'bold'))],
            [sg.Listbox(values=lista_formatada, size=(80, 10), key='-LISTA-', enable_events=True)],
            [sg.Text('Código do Trecho:'), sg.Input(key='-CODIGO-', size=(10, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Selecionar Trecho', layout)

        while True:
            event, values = window.read()
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == '-LISTA-' and values['-LISTA-']:
                try:
                    # Formato esperado: "Trecho Cód: X | ..."
                    cod_str = values['-LISTA-'][0].split('Cód: ')[1].split(' |')[0]
                    window['-CODIGO-'].update(cod_str)
                except IndexError:
                    pass

            if event == 'Confirmar':
                try:
                    return int(values['-CODIGO-'])
                except ValueError:
                    self.mostra_mensagem('ERRO: Código inválido.')

    def mostra_lista_scroll(self, titulo, texto_completo):
        sg.popup_scrolled(texto_completo, 
                           title=titulo, 
                           font=('Helvetica', 12), 
                           size=(70, 15))

    def mostra_mensagem(self, mensagem):
        sg.popup(mensagem, title="Aviso do Sistema")
