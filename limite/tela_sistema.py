import FreeSimpleGUI as sg

class TelaSistema:

    def tela_opcoes(self):
        
        layout = [
            [sg.Text('Sistema de Viagens', justification='center', expand_x=True)],
            [sg.Text('Escolha uma opção:')],
            [sg.Button('Cadastro de Viagens e Informações', key=1, expand_x=True)],
            [sg.Button('Pessoas', key=2, expand_x=True)],
            [sg.Button('Locais', key=3, expand_x=True)],
            [sg.Button('Transporte', key=4, expand_x=True)],
            [sg.Button('Empresas de Transporte', key=5, expand_x=True)],
            [sg.Button('Trechos', key=6, expand_x=True)],
            [sg.Button('Passeios Turísticos', key=7, expand_x=True)],
            [sg.Button('Realizar Pagamentos', key=8, expand_x=True)],
            [sg.Button('Acessar Relátorios', key=9, expand_x=True)],
            [sg.Button('Finalizar sistema', key=0, expand_x=True, button_color=('white', 'darkred'))]
        ]

        window = sg.Window('Menu Principal', layout)
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return 0
            
        return event

    def mostra_mensagem(self, mensagem):
        sg.popup(mensagem, title="Aviso do Sistema")
