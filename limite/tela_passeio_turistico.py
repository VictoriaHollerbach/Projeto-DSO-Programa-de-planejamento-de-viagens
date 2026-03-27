import FreeSimpleGUI as sg

class TelaPasseioTuristico():
    def __init__(self, controlador):
        self.__controlador = controlador

    def mostra_tela_opcoes(self):
        layout = [
            [sg.Text('CADASTRO PASSEIOS', justification='center', expand_x=True)],
            [sg.Button('Incluir Passeio Turístico', key=1, expand_x=True)],
            [sg.Button('Excluir Passeio Turístico', key=2, expand_x=True)],
            [sg.Button('Alterar Passeio Turístico', key=3, expand_x=True)],
            [sg.Button('Listar Passeios Turísticos de uma Viagem', key=4, expand_x=True)],
            [sg.Button('Retornar', key=0, expand_x=True, button_color=('white', 'orange'))]
        ]
        window = sg.Window('Menu Passeios', layout)
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return 0
        return event

    def seleciona_viagem_integrada(self, lista_viagens_formatada):
        layout = [
            [sg.Text('Selecione a Viagem:', font=('Helvetica', 10, 'bold'))],
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
                    self.mostra_mensagem('ERRO: Digite um Código numérico válido.')

    def seleciona_passeio_integrado(self, lista_passeios_formatada):
        layout = [
            [sg.Text('Selecione o Passeio:', font=('Helvetica', 10, 'bold'))],
            [sg.Listbox(values=lista_passeios_formatada, size=(60, 10), key='-LISTA-', enable_events=True)],
            [sg.Text('Atração Turística:'), sg.Input(key='-ATRACAO-', size=(30, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Selecionar Passeio', layout)

        while True:
            event, values = window.read()
            
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == '-LISTA-' and values['-LISTA-']:
                linha_selecionada = values['-LISTA-'][0]
                try:
                    # Assume formato: "Atração: X | Cidade: Y"
                    atracao_str = linha_selecionada.split('Atração: ')[1].split(' |')[0]
                    window['-ATRACAO-'].update(atracao_str)
                except IndexError:
                    pass

            if event == 'Confirmar':
                atracao = values['-ATRACAO-'].capitalize()
                if not atracao:
                    self.mostra_mensagem('ERRO: O campo Atração não pode estar vazio.')
                    continue
                window.close()
                return atracao

    def pega_dados_passeio(self):
        layout = [
            [sg.Text('Dados Passeio', justification='center', expand_x=True)],
            [sg.Text('Dia:'), sg.Input(key='-DIA-')],
            [sg.Text('Cidade:'), sg.Input(key='-CIDADE-')],
            [sg.Text('Atração Turística:'), sg.Input(key='-ATRACAO-')],
            [sg.Text('Horário Início:'), sg.Input(key='-H_INC-')],
            [sg.Text('Horário Fim:'), sg.Input(key='-H_FIM-')],
            [sg.Text('Valor Passeio (R$):'), sg.Input(key='-VALOR-')],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]
        window = sg.Window('Dados do Passeio', layout)

        while True:
            event, values = window.read()
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == 'Salvar':
                try:
                    dia = values['-DIA-']
                    cidade = values['-CIDADE-'].capitalize()
                    atracao = values['-ATRACAO-'].capitalize()
                    h_inc = values['-H_INC-']
                    h_fim = values['-H_FIM-']
                    valor = float(values['-VALOR-'])

                    if not dia or not cidade or not atracao or not h_inc or not h_fim:
                        self.mostra_mensagem('ERRO: Todos os campos de texto são obrigatórios.')
                        continue
                    
                    if valor < 0:
                        self.mostra_mensagem('ERRO: O valor do passeio não pode ser negativo.')
                        continue

                    window.close()
                    return {
                        'dia': dia,
                        'cidade': cidade,
                        'atracao_turistica': atracao,
                        'horario_inc': h_inc,
                        'horario_fim': h_fim,
                        'valor_passeio': valor
                    }
                except ValueError:
                    self.mostra_mensagem('ERRO: Valor do Passeio deve ser um número válido (use ponto para decimais).')

    def mostra_lista_scroll(self, titulo, texto_completo):
        sg.popup_scrolled(texto_completo, 
                           title=titulo, 
                           font=('Helvetica', 12), 
                           size=(60, 15))

    def mostra_mensagem(self, mensagem):
        sg.popup(mensagem, title="Aviso do Sistema")
