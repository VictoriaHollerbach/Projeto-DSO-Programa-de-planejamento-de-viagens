import FreeSimpleGUI as sg

class TelaPagamento:
    def __init__(self, controlador):
        self.__controlador = controlador

    def mostra_tela_opcoes(self):
        layout = [
            [sg.Text('GESTÃO DE PAGAMENTOS', justification='center', expand_x=True)],
            [sg.Button('Registrar Novo Pagamento', key=1, expand_x=True)],
            [sg.Button('Listar Pagamentos', key=2, expand_x=True)],
            [sg.Button('Retornar', key=0, expand_x=True, button_color=('white', 'orange'))]
        ]
        window = sg.Window('Menu Pagamentos', layout)
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return 0
        return event

    def seleciona_viagem_integrada(self, lista_viagens_formatada):
        layout = [
            [sg.Text('Selecione a Viagem para o Pagamento:', font=('Helvetica', 10, 'bold'))],
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

    def seleciona_pessoa_integrada(self, lista_pessoas_formatada):
        layout = [
            [sg.Text('Selecione o Pagador:', font=('Helvetica', 10, 'bold'))],
            [sg.Listbox(values=lista_pessoas_formatada, size=(60, 10), key='-LISTA-', enable_events=True)],
            [sg.Text('ID da Pessoa:'), sg.Input(key='-ID-', size=(10, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Selecionar Pagador', layout)

        while True:
            event, values = window.read()
            
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == '-LISTA-' and values['-LISTA-']:
                linha_selecionada = values['-LISTA-'][0]
                try:
                    id_str = linha_selecionada.split('ID: ')[1]
                    window['-ID-'].update(id_str)
                except IndexError:
                    pass

            if event == 'Confirmar':
                valor_lido = values['-ID-']
                try:
                    identificacao = int(valor_lido)
                    if identificacao <= 0:
                        self.mostra_mensagem('ERRO: O ID deve ser um número positivo.')
                        continue
                    window.close()
                    return identificacao
                except ValueError:
                    self.mostra_mensagem('ERRO: Digite um ID numérico válido.')

    def pega_dados_pagamento(self, nome_pessoa):
        layout = [
            [sg.Text(f'Dados do Pagamento para: {nome_pessoa}', justification='center', expand_x=True)],
            [sg.Text('Código Pagamento:'), sg.Input(key='-CODIGO-')],
            [sg.Text('Data (DD/MM/AAAA):'), sg.Input(key='-DATA-')],
            [sg.Text('Valor (R$):'), sg.Input(key='-VALOR-')],
            [sg.Text('Método:')],
            [sg.Radio('PIX', "RADIO1", default=True, key='-PIX-'), 
             sg.Radio('Dinheiro', "RADIO1", key='-DINHEIRO-'),
             sg.Radio('Cartão', "RADIO1", key='-CARTAO-')],
            [sg.Frame('Dados do Cartão (Apenas se selecionar Cartão)', [
                [sg.Text('Número:'), sg.Input(key='-NUM_CARTAO-')],
                [sg.Text('Bandeira:'), sg.Input(key='-BANDEIRA-')]
            ])],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]
        window = sg.Window('Registrar Pagamento', layout)

        while True:
            event, values = window.read()
            if event == 'Cancelar' or event == sg.WIN_CLOSED:
                window.close()
                return None
            
            if event == 'Salvar':
                try:
                    codigo = int(values['-CODIGO-'])
                    valor = float(values['-VALOR-'])
                    data = values['-DATA-']
                    
                    if codigo <= 0 or valor <= 0:
                        self.mostra_mensagem('ERRO: Código e Valor devem ser positivos.')
                        continue
                    if not data:
                        self.mostra_mensagem('ERRO: Data obrigatória.')
                        continue

                    dados = {'codigo': codigo, 'valor': valor, 'data': data}

                    if values['-PIX-']:
                        dados['tipo'] = 'PIX'
                    elif values['-DINHEIRO-']:
                        dados['tipo'] = 'DINHEIRO'
                    elif values['-CARTAO-']:
                        dados['tipo'] = 'CARTAO'
                        dados['numero_cartao'] = values['-NUM_CARTAO-']
                        dados['bandeira'] = values['-BANDEIRA-']
                        
                        if not dados['numero_cartao'] or not dados['bandeira']:
                            self.mostra_mensagem('ERRO: Para pagamento em Cartão, preencha Número e Bandeira.')
                            continue

                    window.close()
                    return dados

                except ValueError:
                    self.mostra_mensagem('ERRO: Código deve ser inteiro e Valor deve ser número.')
                    continue

    def mostra_lista_scroll(self, titulo, texto_completo):
        sg.popup_scrolled(texto_completo, 
                           title=titulo, 
                           font=('Helvetica', 12), 
                           size=(60, 15))

    def mostra_mensagem(self, mensagem):
        sg.popup(mensagem, title="Aviso do Sistema")
