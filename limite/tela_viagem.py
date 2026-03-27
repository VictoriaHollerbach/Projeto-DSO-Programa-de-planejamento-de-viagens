import FreeSimpleGUI as sg

class TelaViagem():
    def __init__(self, controlador):
        self.__controlador = controlador

    def mostra_tela_opcoes(self):
        layout = [
            [sg.Text('CADASTRO VIAGENS', justification='center', expand_x=True)],
            [sg.Button('Incluir Viagem', key=1, expand_x=True)],
            [sg.Button('Excluir Viagem', key=2, expand_x=True)],
            [sg.Button('Editar dados da Viagem', key=3, expand_x=True)],
            [sg.Button('Listar Viagens', key=4, expand_x=True)],
            [sg.Button('Verificar valor total da viagem', key=5, expand_x=True)],
            [sg.Button('Verificar valor total por pessoa', key=6, expand_x=True)],
            [sg.Button('Verificar quanto já foi pago', key=7, expand_x=True)],
            [sg.Button('Verificar quem pagou', key=8, expand_x=True)],
            [sg.Button('Verificar quem não pagou', key=9, expand_x=True)],
            [sg.Button('Retornar', key=0, expand_x=True, button_color=('white', 'orange'))]
        ]
        window = sg.Window('Menu Viagens', layout)
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return 0
        return event
    
    def pega_dados_viagem(self):
        layout = [
            [sg.Text('Dados Viagem', justification='center', expand_x=True)],
            [sg.Text('Código:'), sg.Input(key='-CODIGO-')],
            [sg.Text('Nome da Viagem:'), sg.Input(key='-NOME-')],
            [sg.Text('Data de Início:'), sg.Input(key='-DATA_INC-')],
            [sg.Text('Data Fim:'), sg.Input(key='-DATA_FIM-')],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]
        window = sg.Window('Dados da Viagem', layout)

        while True:
            event, values = window.read()
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == 'Salvar':
                nome_viagem = values['-NOME-'].capitalize()
                data_inc = values['-DATA_INC-']
                data_fim = values['-DATA_FIM-']

                if not nome_viagem or not data_inc or not data_fim:
                    self.mostra_mensagem('ERRO: Todos os campos são obrigatórios.')
                    continue
                
                try:
                    codigo = int(values['-CODIGO-'])
                    if codigo <= 0:
                        self.mostra_mensagem('ERRO: O Código deve ser um número positivo.')
                        continue
                    
                    window.close()
                    return {'codigo': codigo, 'nome_viagem': nome_viagem, 'data_inc': data_inc, 'data_fim': data_fim}
                
                except ValueError:
                    self.mostra_mensagem('ERRO: O Código deve ser um número inteiro.')
                    continue

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
