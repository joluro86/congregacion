from django.shortcuts import redirect, render

class Carro_informe:
    def __init__(self, request):
        self.request=request
        self.session=request.session
        carro=self.session.get("carro")

        if not carro:
            carro=self.session["carro"]={}
        self.carro=carro

    def agregar(self, publicador, ):
        if(str(publicador.id) not in self.carro.keys()):
            print("entre a agregar")
            self.carro[publicador.id]={
                'grupo': publicador.grupo.numero,
                'mes': 'agosto',
                'año': 2022,
                'id':publicador.id,
                'nombre':publicador.nombre,
                'publicaciones':0,
                'videos':0,
                'horas':0,
                'revisitas':0,
                'revistas':0,
                'cursos':0,
                'estado':0,
                'observaciones':"",
            }
        self.guardar_carro()
    
    def agregar_grupo(self, grupo_numero):
        return self.carro.keys["grupo"].values

    def consultar_grupo(self, grupo_numero):
        if(grupo_numero not in self.carro.keys()):
            return 0
        else:
            return 1

    def agregar_producto_actualizar(self, producto):
        if(str(producto.id) not in self.carro.keys()):
            self.carro[producto.id]={
                'id':producto.producto.id,
                'descripcion':producto.producto.descripcion,
                'cantidad':producto.cantidad,
                'cantidad_inicial':producto.cantidad,
                'dias_alquiler':producto.dias,
                'valor_dia':producto.producto.valor_dia,
                'valor_producto':producto.producto.valor_producto,
                'subtotal':str(producto.subtotal),
                'iva': producto.iva,
                'valor_iva': producto.iva/100,
            }
        self.guardar_carro()
        
    def cambiar_cantidad_informe(self, id, p, v, h, r, c, o):
    
        for key, value in self.carro.items():
                print("entre a cambiar")
                if key==str(id):
                    value['horas']=h
                    value['publicaciones']=p
                    value['videos']=v
                    value['horas']=h
                    value['revisitas']=r
                    value['cursos']=c
                    value['observaciones']=o

                    try:
                        if int(value['horas'])>0:
                            value['estado']=1
                        if int(value['horas'])==0:
                            value['estado']=0    
                            value['observaciones']=''                    
                    except:
                        pass        
                    break
        self.guardar_carro()
    
    def cambiar_estado_informe(self, id, estado):
        
        for key, value in self.carro.items():
                print("aqui voy " + str(id))
                if key==str(id):
                    value['estado']=estado
                    if estado ==1:
                        value['observaciones']='Informó.'
                    if estado ==0:
                        value['observaciones']=''
                    print("estado nuevo: " + str(value['estado']))
                    break
        self.guardar_carro()
    
    def actualizar_cantidad(self, producto, cantidad):
    
        for key, value in self.carro.items():
                if str(value['id'])==str(producto.id):
                    value['cantidad']=cantidad
                    value['subtotal']= float(cantidad) * float(value['dias_alquiler']) * float(value['valor_dia'])
                    break
        self.guardar_carro()

    

    
    def total_venta(self):
        total_venta = 0
        for key, value in self.carro.items():
                total_venta = total_venta + (int(value['cantidad']) * float(value['valor_dia'])* float(value['dias_alquiler']) )    
        self.guardar_carro()            
        return float(total_venta) 

  
        
    def guardar_carro(self):
        self.session["carro"]=self.carro
        self.session.modified=True
    
    def eliminar_producto(self, producto):
        producto.id=str(producto.id)
        if producto.id in self.carro:
            del self.carro[producto.id]
            self.guardar_carro()

    def restar_producto(self, producto):
        for key, value in self.carro.items():
                if key==str(producto.id):
                    value['cantidad']=value['cantidad']-1
                    if value['cantidad']<1:
                        self.eliminar_producto(producto)
                    break
        self.guardar_carro()

    def limpiar_carro(self):
        self.session["carro"]={}
        self.session.modified=True



