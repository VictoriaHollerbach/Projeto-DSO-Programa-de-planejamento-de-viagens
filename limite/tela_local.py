import FreeSimpleGUI as sg

class TelaLocal:
    def __init__(self, controlador):
        self.__controlador = controlador

    def seleciona_local_integrado(self, lista_locais_formatada):
        layout = [
            [sg.Text('Selecione um Local da lista ou digite a Cidade:', font=('Helvetica', 10, 'bold'))],
            [sg.Listbox(values=lista_locais_formatada, size=(60, 10), key='-LISTA-', enable_events=True)],
            [sg.Text('Cidade:'), sg.Input(key='-CIDADE-', size=(20, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Selecionar Local', layout)

        while True:
            event, values = window.read()
            
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            # Auto-preenchimento ao clicar na lista
            # Assumindo formato "Cidade: X | País: Y"
            if event == '-LISTA-' and values['-LISTA-']:
                linha_selecionada = values['-LISTA-'][0]
                try:
                    cidade_str = linha_selecionada.split('Cidade: ')[1].split(' |')[0]
                    window['-CIDADE-'].update(cidade_str)
                except IndexError:
                    pass

            if event == 'Confirmar':
                cidade = values['-CIDADE-'].capitalize()
                if not cidade:
                    self.mostra_mensagem('ERRO: O campo Cidade não pode estar vazio.')
                    continue
                
                window.close()
                return cidade

    def mostra_tela_opcoes(self):
        layout = [
            [sg.Text('CADASTRO LOCAIS', justification='center', expand_x=True)],
            [sg.Button('Incluir Local', key=1, expand_x=True)],
            [sg.Button('Excluir Local', key=2, expand_x=True)],
            [sg.Button('Alterar Local', key=3, expand_x=True)],
            [sg.Button('Listar Locais', key=4, expand_x=True)],
            [sg.Button('Retornar', key=0, expand_x=True, button_color=('white', 'orange'))]
        ]

        window = sg.Window('Menu Locais', layout)
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return 0
        return event
    
    def pega_dados_local(self):
        layout = [
            [sg.Text('Dados Local', justification='center', expand_x=True)],
            [sg.Text('Cidade:'), sg.Input(key='-CIDADE-')],
            [sg.Text('País:'), sg.Input(key='-PAIS-')],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]

        window = sg.Window('Dados do Local', layout)

        while True:
            event, values = window.read()
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            elif event == 'Salvar':
                cidade = values['-CIDADE-'].capitalize()
                pais = values['-PAIS-'].capitalize()

                if not cidade or not pais:
                    self.mostra_mensagem('ERRO: Todos os campos são obrigatórios.')
                    continue

                window.close()
                return {'cidade': cidade, 'pais': pais}

    def mostra_lista_scroll(self, titulo, texto_completo):
        sg.popup_scrolled(texto_completo, 
                           title=titulo, 
                           font=('Helvetica', 12), 
                           size=(60, 15))

    def mostra_mensagem(self, mensagem):
        sg.popup(mensagem, title="Aviso do Sistema")
