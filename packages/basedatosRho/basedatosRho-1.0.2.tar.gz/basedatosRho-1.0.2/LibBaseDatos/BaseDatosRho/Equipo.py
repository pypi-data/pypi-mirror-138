

class EquipoRes(object):
    def __init__(self, codigo, concepto, cantidad):
        self.codigo = codigo
        self.concepto = concepto
        self.cantidad= cantidad
    def __str__(self) -> str:
        return f"{self.codigo}|{self.concepto}|{self.cantidad}"

class EquipoAbastecido(object):
    def __init__(self, codigo, concepto, autopista, plazaCobro, cantidad):
        self.codigo = codigo
        self.concepto = concepto
        self.autopista = autopista
        self.plaza = plazaCobro
        self.cantidad = cantidad

class EquipoCatalogo(object):
    def __init__(self,codigo,concepto,etiquetable):
        self.codigo = codigo
        self.concepto = concepto
        self.etiquetable = etiquetable
        