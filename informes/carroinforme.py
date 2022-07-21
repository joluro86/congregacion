from django.shortcuts import redirect, render

class Carro_informe:
    def __init__(self, request):
        self.request=request
        self.session=request.session
        carro=self.session.get("carro")

        if not carro:
            carro=self.session["carro"]={}
        self.carro=carro

    def nuevo_informe(self, publicadores):

        for publicador in publicadores:  
            print(publicador.nombre)      
            self.carro[publicador.id]={
                'id':publicador.id,
                'nombre':publicador.nombre,
                'publicaciones': '',
                'videos': '',
                'horas': '',
                'revisitas': '',
                'cursos': '',
                'observaciones': '',
            }
        self.guardar_carro()

    # def agregar_producto_actualizar(self, producto):
    #     if(str(producto.id) not in self.carro.keys()):
    #         if producto.iva>0:
    #             iva=producto.iva
    #         else:
    #             iva=1
    #         self.carro[producto.id]={
    #             'id':producto.producto.id,
    #             'descripcion':producto.producto.descripcion,
    #             'cantidad':producto.cantidad,
    #             'cantidad_inicial':producto.cantidad,
    #             'dias_alquiler':producto.dias,
    #             'valor_dia':producto.producto.valor_dia,
    #             'valor_producto':producto.producto.valor_producto,
    #             'subtotal':str(producto.subtotal),
    #             'iva': producto.iva,
    #             'valor_iva': producto.iva/100,
    #         }
    #     self.guardar_carro()
        
    # def cambiar_cantidad(self, producto, cantidad):
    
    #     for key, value in self.carro.items():
    #             if key==str(producto.id):
    #                 value['cantidad']=cantidad
    #                 value['subtotal']= float(cantidad) * float(value['dias_alquiler']) * float(value['valor_dia'])
    #                 break
    #     self.guardar_carro()
    
    # def actualizar_cantidad(self, producto, cantidad):
    
    #     for key, value in self.carro.items():
    #             if str(value['id'])==str(producto.id):
    #                 value['cantidad']=cantidad
    #                 value['subtotal']= float(cantidad) * float(value['dias_alquiler']) * float(value['valor_dia'])
    #                 break
    #     self.guardar_carro()

    
    # def actualizar_carro_dias(self, producto, dias):
    #     for key, value in self.carro.items():
    #         if str(value['id'])==str(producto.id):
    #             value['dias_alquiler']=dias
    #             value['subtotal']= float(value['cantidad']) * float(value['dias_alquiler']) * float(value['valor_dia'])
    #             break
    #     self.guardar_carro()

    # def cambiar_cantidad_dias(self, producto, cantidad):
    #     for key, value in self.carro.items():
    #             if key==str(producto.id):
    #                 value['dias_alquiler']=cantidad
    #                 value['subtotal']=  float(value['cantidad']) * float(value['dias_alquiler']) * float(value['valor_dia'])
    #                 break
    #     self.guardar_carro()

    
    # def total_venta(self):
    #     total_venta = 0
    #     for key, value in self.carro.items():
    #             total_venta = total_venta + (int(value['cantidad']) * float(value['valor_dia'])* float(value['dias_alquiler']) )    
    #     self.guardar_carro()            
    #     return float(total_venta) 

    # def total_iva(self):
    #     total_iva = 0
    #     for key, value in self.carro.items():
    #         if value['iva']>0:
    #             total_iva = total_iva + (int(value['cantidad']) * float(value['valor_dia'])* float(value['dias_alquiler'])) * (float(value['iva'])/100)   
    #     self.guardar_carro()            
    #     return float(total_iva)     
        
    def guardar_carro(self):
        self.session["carro"]=self.carro
        self.session.modified=True
    
    # def eliminar_producto(self, producto):
    #     producto.id=str(producto.id)
    #     if producto.id in self.carro:
    #         del self.carro[producto.id]
    #         self.guardar_carro()

    # def restar_producto(self, producto):
    #     for key, value in self.carro.items():
    #             if key==str(producto.id):
    #                 value['cantidad']=value['cantidad']-1
    #                 if value['cantidad']<1:
    #                     self.eliminar_producto(producto)
    #                 break
    #     self.guardar_carro()

    def limpiar_carro(self):
        self.session["carro"]={}
        self.session.modified=True

    # def total_productos(self,):
    #     total=0
    #     for key, value in self.carro.items():
    #         total=total+int(value['cantidad'])             
    #     self.guardar_carro()
    #     return total