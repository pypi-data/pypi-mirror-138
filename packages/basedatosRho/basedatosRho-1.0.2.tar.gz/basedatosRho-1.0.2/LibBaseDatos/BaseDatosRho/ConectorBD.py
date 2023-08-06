from libbasedatos.basedatosRho.Equipo import EquipoRes as eqRes
from libbasedatos.basedatosRho.Equipo import EquipoAbastecido as eqAbastecido
from libbasedatos.basedatosRho.Equipo import EquipoCatalogo as eqCatalogo
import mysql.connector
from unittest import result
import pymysql
import pandas as pd
import datetime


class BDMySQL:

    def __init__(self,db_host,db_port):
        self.host = db_host
        self.port = db_port
        self.user = "root"
        self.password = "4dm1n"
        self.db = "almacen"

    def __connect__(self):
        self.con = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()
    
    def getFullStock(self):
        res=0
        x='Stock'
        sheet='Interlomas'
        now = datetime.datetime.now()
        try:
            self.__connect__()
            result =self.cur.execute("SELECT tb1.Codigo,tb1.Concepto,Inventario,Cantidad FROM tb_equipo tb2 LEFT JOIN tb_catalogo tb1 ON tb1.Idcatalogo=tb2.Idcatalogo WHERE Inventario='OK'")
            result = self.cur.fetchall()
            df=pd.DataFrame(result)
            df=df.set_index('Codigo')
            df=df.groupby(['Codigo','Concepto','Inventario'])['Concepto'].count()
            df.to_excel('Res'+x+'_'+str(now.year)+'.xlsx',sheet)
            self.__disconnect__()
            res=1
            return res
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

    def getStock(self,codigo):
        try:
            resultado=0
            listaRes=[]
            listaauxiliar=[]
            self.__connect__()
            result =self.cur.execute("SELECT tb1.Codigo,tb1.Concepto,Inventario,Cantidad FROM tb_equipo tb2 LEFT JOIN tb_catalogo tb1 ON tb1.Idcatalogo=tb2.Idcatalogo WHERE tb1.Codigo='"+codigo+"' and Inventario = 'ok'")
            if result > 0:
                result = self.cur.fetchall()
            else:
                self.__disconnect__()
                return resultado
            df=pd.DataFrame(result)
            for i in df.index:
                #print(df['Codigo'][i]+'|'+df['Concepto'][i]+'|'+df['Cantidad'][i])
                codigo = df['Codigo'][i]
                if codigo not in listaauxiliar:
                    cantidad=int(df['Cantidad'][i])
                    concepto = df['Concepto'][i]
                    listaauxiliar.append(codigo)
                    eq=eqRes(codigo, concepto, cantidad)
                    listaRes.append(eq)
                else:
                    for e in listaRes:
                        if codigo == e.codigo:
                            e.cantidad += cantidad
            self.__disconnect__()
            resultado=listaRes[0].cantidad
            return resultado
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

    def getAbastecido(self,codigo,autopista,plazaCobro):
        try:
            resultado=0
            listaRes=[]
            listaauxiliar=[]
            self.__connect__()
            if not autopista:
                result =self.cur.execute("SELECT tb1.Codigo,tb1.Concepto,Inventario,Cantidad FROM tb_equipo tb2 LEFT JOIN tb_catalogo tb1 ON tb1.Idcatalogo=tb2.Idcatalogo WHERE tb1.Codigo='"+codigo+"' and PlazaCobro='"+plazaCobro+"' and Inventario = 'Abastecido'")
            if not plazaCobro:
                result =self.cur.execute("SELECT tb1.Codigo,tb1.Concepto,Inventario,Cantidad FROM tb_equipo tb2 LEFT JOIN tb_catalogo tb1 ON tb1.Idcatalogo=tb2.Idcatalogo WHERE tb1.Codigo='"+codigo+"' and UbicacionActual='"+autopista+"' and Inventario = 'Abastecido'")
            if result > 0:
                result = self.cur.fetchall()
            else:
                self.__disconnect__()
                return resultado
            df=pd.DataFrame(result)
            for i in df.index:
                codigo = df['Codigo'][i]
                if codigo not in listaauxiliar:
                    cantidad=int(df['Cantidad'][i])
                    concepto = df['Concepto'][i]
                    listaauxiliar.append(codigo)
                    eq=eqRes(codigo, concepto, cantidad)
                    listaRes.append(eq)
                else:
                    for e in listaRes:
                        if codigo == e.codigo:
                            e.cantidad += cantidad
            self.__disconnect__()
            resultado=listaRes[0].cantidad
            return resultado
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

    def getAbastecidoPro(self,codigo,autopista,plazaCobro,year):
        try:
            resultado=0
            listaRes=[]
            listaauxiliar=[]
            self.__connect__()
            if not autopista:
                result =self.cur.execute("SELECT tb1.Codigo,tb1.Concepto,Inventario,Cantidad FROM tb_equipo tb2 LEFT JOIN tb_catalogo tb1 ON tb1.Idcatalogo=tb2.Idcatalogo WHERE tb1.Codigo='"+codigo+"' and PlazaCobro='"+plazaCobro+"' and Inventario = 'Abastecido' and FechaSalida LIKE '%"+year+"'")
            if not plazaCobro:
                result =self.cur.execute("SELECT tb1.Codigo,tb1.Concepto,Inventario,Cantidad FROM tb_equipo tb2 LEFT JOIN tb_catalogo tb1 ON tb1.Idcatalogo=tb2.Idcatalogo WHERE tb1.Codigo='"+codigo+"' and UbicacionActual='"+autopista+"' and Inventario = 'Abastecido' and FechaSalida LIKE '%"+year+"'")
            if result > 0:
                result = self.cur.fetchall()
            else:
                self.__disconnect__()
                return resultado
            df=pd.DataFrame(result)
            for i in df.index:
                codigo = df['Codigo'][i]
                if codigo not in listaauxiliar:
                    cantidad=int(df['Cantidad'][i])
                    concepto = df['Concepto'][i]
                    listaauxiliar.append(codigo)
                    eq=eqRes(codigo, concepto, cantidad)
                    listaRes.append(eq)
                else:
                    for e in listaRes:
                        if codigo == e.codigo:
                            e.cantidad += cantidad
            self.__disconnect__()
            resultado=listaRes[0].cantidad
            return resultado
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

    def getAbastecidoSerie(self,codigo,serie):
        try:
            resultado=''
            listaRes=[]
            listaauxiliar=[]
            self.__connect__()
            result =self.cur.execute("SELECT tb1.Codigo,tb1.Concepto,UbicacionActual,PlazaCobro,Cantidad FROM tb_equipo tb2 LEFT JOIN tb_catalogo tb1 ON tb1.Idcatalogo=tb2.Idcatalogo WHERE tb1.Codigo='"+codigo+"' and IDLAB='"+serie+"' and Inventario = 'Abastecido'")
            if result > 0:
                result = self.cur.fetchall()
            else:
                self.__disconnect__()
                return resultado
            df=pd.DataFrame(result)
            for i in df.index:
                codigo = df['Codigo'][i]
                if codigo not in listaauxiliar:
                    cantidad=int(df['Cantidad'][i])
                    concepto = df['Concepto'][i]
                    autopista = df['UbicacionActual'][i]
                    plaza = df['PlazaCobro'][i]
                    listaauxiliar.append(codigo)
                    eq=eqAbastecido(codigo, concepto, autopista, plaza, cantidad)
                    listaRes.append(eq)
                else:
                    for e in listaRes:
                        if codigo == e.codigo:
                            e.cantidad += cantidad
            self.__disconnect__()
            resultado= listaRes[0].codigo+'|'+listaRes[0].concepto+'|'+listaRes[0].autopista+'|'+listaRes[0].plaza+'|'+str(listaRes[0].cantidad)
            return resultado
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

    def getEquipoCatalogo(self,codigo):
        try:
            resultado=''
            listaRes=[]
            listaauxiliar=[]
            self.__connect__()
            query="SELECT Codigo,Concepto,CategoriaDos FROM tb_catalogo WHERE Codigo='"+codigo+"'"
            print(query)
            result =self.cur.execute(query)
            if result > 0:
                result = self.cur.fetchall()
            else:
                self.__disconnect__()
                return resultado
            df=pd.DataFrame(result)
            for i in df.index:
                codigo = df['Codigo'][i]
                if codigo not in listaauxiliar:
                    concepto = df['Concepto'][i]
                    categoria = df['CategoriaDos'][i]
                    listaauxiliar.append(codigo)
                    eq=eqCatalogo(codigo, concepto, categoria)
                    listaRes.append(eq)
            self.__disconnect__()
            if not listaRes[0].etiquetable:
                resultado = listaRes[0].codigo+'|'+listaRes[0].concepto+'|'
            else:
                resultado = listaRes[0].codigo+'|'+listaRes[0].concepto+'|'+listaRes[0].etiquetable
            return resultado
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)