import FreeSimpleGUI as sg
from controle.controlador_sistema import ControladorSistema

if __name__ == "__main__":
    sg.theme('DarkBlue14')
    ControladorSistema().inicializa_sistema()
