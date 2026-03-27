import FreeSimpleGUI as sg

class TelaTransporte():
    def __init__(self, controlador):
        self.__controlador = controlador
    
    def mostra_tela_opcoes(self):
        layout = [
            [sg.Text('GESTÃO DE TRANSPORTES', justification='center', expand_x=True)],
            [sg.Button('Cadastrar Transporte', key=1, expand_x=True)],
            [sg.Button('Excluir Transporte', key=2, expand_x=True)],
            [sg.Button('Listar Transportes', key=3, expand_x=True)],
            [sg.Button('Retornar', key=0, expand_x=True, button_color=('white', 'orange'))]
        ]
        window = sg.Window('Menu Transportes', layout)
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return 0
        return event
    
    def pega_dados_transporte(self):
        layout = [
            [sg.Text('Dados Transporte', justification='center', expand_x=True)],
            [sg.Text('Tipo:'), sg.Input(key='-TIPO-')],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]
        window = sg.Window('Dados do Transporte', layout)

        while True:
            event, values = window.read()
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == 'Salvar':
                tipo = values['-TIPO-'].capitalize()
                if not tipo:
                    self.mostra_mensagem('ERRO: O campo Tipo não pode estar vazio.')
                    continue
                
                window.close()
                return {'tipo': tipo}

    def seleciona_transporte_integrado(self, lista_transportes_formatada):
        layout = [
            [sg.Text('Selecione um Transporte da lista ou digite o Tipo:', font=('Helvetica', 10, 'bold'))],
            [sg.Listbox(values=lista_transportes_formatada, size=(60, 10), key='-LISTA-', enable_events=True)],
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
                linha_selecionada = values['-LISTA-'][0]
                window['-TIPO-'].update(linha_selecionada)

            if event == 'Confirmar':
                tipo = values['-TIPO-'].capitalize()
                if not tipo:
                    self.mostra_mensagem('ERRO: O campo Tipo não pode estar vazio.')
                    continue
                
                window.close()
                return tipo

    def mostra_lista_scroll(self, titulo, texto_completo):
        sg.popup_scrolled(texto_completo, 
                           title=titulo, 
                           font=('Helvetica', 12), 
                           size=(60, 15))

    def mostra_mensagem(self, mensagem):
        sg.popup(mensagem, title="Aviso do Sistema")
