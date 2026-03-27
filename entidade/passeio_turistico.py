class PasseioTuristico:
    def __init__(self, dia: str, cidade: str, atracao_turistica: str, horario_inc: str, horario_fim: str, valor_passeio: float):
        self.__dia = None
        self.__cidade = None
        self.__atracao_turistica = None
        self.__horario_inc = None
        self.__horario_fim = None
        self.__valor_passeio = None
        if isinstance(cidade, str):
            self.__cidade = cidade
        if isinstance(atracao_turistica, str):
            self.__atracao_turistica = atracao_turistica
        if isinstance(horario_inc, str):
            self.__horario_inc = horario_inc
        if isinstance(horario_fim, str):
            self.__horario_fim = horario_fim
        if isinstance(valor_passeio, float):
            self.__valor_passeio = valor_passeio
        if isinstance(dia, str):
            self.__dia = dia

    @property
    def dia(self):
        return self.__dia

    @dia.setter
    def dia(self, dia: str):
        if isinstance(dia, str):
            self.__dia = dia
            
    @property
    def cidade(self):
        return self.__cidade
        
    @cidade.setter
    def cidade(self, cidade: str):
        if isinstance(cidade, str):
            self.__cidade = cidade
            
    @property
    def atracao_turistica(self):
        return self.__atracao_turistica
        
    @atracao_turistica.setter
    def atracao_turistica(self, atracao_turistica: str):
        if isinstance(atracao_turistica, str):
            self.__atracao_turistica = atracao_turistica
            
    @property
    def horario_inc(self):
        return self.__horario_inc
        
    @horario_inc.setter
    def horario_inc(self, horario_inc: str):
        if isinstance(horario_inc, str):
            self.__horario_inc = horario_inc
            
    @property
    def horario_fim(self):
        return self.__horario_fim
        
    @horario_fim.setter
    def horario_fim(self, horario_fim: str):
        if isinstance(horario_fim, str):
            self.__horario_fim = horario_fim
            
    @property
    def valor_passeio(self):
        return self.__valor_passeio
        
    @valor_passeio.setter
    def valor_passeio(self, valor_passeio: float):
        if isinstance(valor_passeio, float):
            self.__valor_passeio = valor_passeio

    def __str__(self):
        return f'Dia: {self.__dia} | Cidade: {self.__cidade} | Atração Turística: {self.__atracao_turistica} | Início: {self.__horario_inc} | Fim: {self.__horario_fim} | Valor: {self.__valor_passeio:.2f}'
        
