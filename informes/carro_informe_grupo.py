from django.shortcuts import redirect, render


class Carro_informe:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get("carro")

        if not carro:
            carro = self.session["carro"] = {}
        self.carro = carro

    def agregar(self, publicador, ):
        if (str(publicador.id) not in self.carro.keys()):
            self.carro[publicador.id] = {
                'grupo': publicador.grupo.numero,
                'mes': 'agosto',
                'año': 2022,
                'id': publicador.id,
                'nombre': publicador.nombre,
                'publicaciones': 0,
                'videos': 0,
                'horas': 0,
                'revisitas': 0,
                'revistas': 0,
                'cursos': 0,
                'estado': 0,
                'observaciones': "",
            }
        self.guardar_carro()

    def agregar_grupo(self, grupo_numero):
        return self.carro.keys["grupo"].values

    def consultar_grupo(self, grupo_numero):
        if (grupo_numero not in self.carro.keys()):
            return 0
        else:
            return 1


    def cambiar_cantidad_informe(self, id, p, v, h, r, c, o):

        for key, value in self.carro.items():
            if key == str(id):
                value['horas'] = h
                value['publicaciones'] = p
                value['videos'] = v
                value['horas'] = h
                value['revisitas'] = r
                value['cursos'] = c
                value['observaciones'] = o

                try:
                    if int(value['horas']) > 0:
                        value['estado'] = 1
                    if int(value['horas']) == 0:
                        value['estado'] = 0
                        value['observaciones'] = ''
                except:
                    pass
                break
        self.guardar_carro()

    def cambiar_estado_informe(self, id, estado):

        for key, value in self.carro.items():
            if key == str(id):
                value['estado'] = estado
                if estado == 1:
                    value['observaciones'] = 'Informó.'
                if estado == 0:
                    value['observaciones'] = ''
                break
        self.guardar_carro()

    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True

    def limpiar_carro(self):
        self.session["carro"] = {}
        self.session.modified = True
