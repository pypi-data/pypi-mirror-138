from basedatosRho.ConectorBD import BDMySQL as bd


myconexion=bd("proxy17.rt3.io",39704)
cantidadsStock=myconexion.getStock("203601400005")
cantidadAbastecida=myconexion.getAbastecido("203601400005","CVT","")
cantidadAbastecidaPro=myconexion.getAbastecidoPro("203601400005","CVT",'','2021')
res=myconexion.getAbastecidoSerie("203601400296","LB1905748")
categoria = myconexion.getEquipoCatalogo("203601400296")


print(cantidadsStock)
print("-------------")
print(cantidadAbastecida)
print("-------------")
print(cantidadAbastecida)
print("-------------")
print(cantidadAbastecidaPro)
print("-------------")
print(res)
print("-------------")
print(categoria)
