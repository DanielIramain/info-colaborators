'''
Sistema de gestión de colaboradores

Requisitos:
1. Crear una clse base Colaborador con atributos como nombre, apellido, edad, salario, etc.
2. Definir clases derivadas para diferentes tipos de empleados (por ej. ColaboradorTiempoCompleto, ColaboradorTiempoParcial) con atributos y métodos específicos
3. Implementar operaciones tipo CRUD para gestionar los empleados
4. Manejar errores con bloques try-except para validar entradas y gestionar excepciones (por ej. salario negativo, longitud del DNI, etc.)
5. Persistir los datos en archivos JSON.  
'''

#Imports necesarios
import mysql.connector
from mysql.connector import Error
from decouple import config


#Clase base
class Colaborador: 
    '''
    Abstraccion: Constructor en el que abstraimos lo importante de una persona (colaborador) 
    
    Encapsulamiento: Con el encapsulamiento los atrbs y métodos pueden ser públicos, privados o protegidos
    Al encapsular nuestro código y hacerlo privado (con doble guión bajo) debemos establecer los métodos públicos para consultar
    y acceder a la información (getter y setter). 
    Esto lo hacemos mediante @Property para convertir en propiedad los atributos y modificamos los datos de manera
    controlada con los setters 

    '''
    def __init__(self, dni, nombre, apellido, edad, salario) -> None:
        self.__dni = self.validar_dni(dni)
        self.__nombre = nombre
        self.__apellido = apellido
        self.__edad = edad
        self.__salario = self.validar_salario(salario) ### Caso instanciación o creación de objeto
    
    ##Getters: hacer property (asimilable a los métodos de protocolo HTTP para consultar informcación => GET)
    '''
    Con property al atributo que figura en una función lo convertimos en una propiedad
    Esto significa que si instanciamos un objeto de la clase colaborador, podríamos acceder al
    dato que está guardado en el atributo, sin necesidad de utilizar los dos parentesis al llamar 
    por ej. persona1.dni
    '''
    @property
    def dni(self):
        return self.__dni
    
    @property
    def nombre(self):
        return self.__nombre.capitalize() ###En este caso ya se aplicó una modificación
    
    @property
    def apellido(self):
        return self.__apellido.capitalize()
    
    @property
    def edad(self):
        return self.__edad

    @property
    def salario(self):
        return self.__salario
    
    ## Setters: modificar la información (asimilable a POST) => decorador setter 
    '''
    Por ej. realizar una validación del salario, de manera que si no encapsulamos
    se accedería directamente a salario y como programador no tendría ningún control sobre
    ese cambio. Ya no va directamente al atributo salario si no que primero se realiza un chequeo.
    '''
    @salario.setter
    def salario(self, nuevo_salario):
        self.__salario = self.validar_salario(nuevo_salario) ### Caso validación de objeto al modificar

    @dni.setter
    def dni(self, dni_num):
        self.__dni = self.validar_dni(dni_num)

    def validar_salario(self, salario):
        try:
            salario_num = float(salario)
            if salario_num < 0: 
                raise ValueError('El salario debe ser mayor o igual a 0')
            return salario_num
        except ValueError:
            raise ValueError('El salario debe ser un número válido')
    
    def validar_dni(self, dni):
        try:
            dni_num = int(dni)
            if len(str(dni)) not in [7, 8]:
                raise ValueError('El DNI debe tener entre 7 y 8 dígitos')
            if dni_num <= 0:
                raise ValueError('El DNI debe ser un número positivo')
            return dni_num
        except ValueError:
            raise ValueError('El DNI debe ser numérico y estar completo')

    def to_dict(self):
        '''
        método para devolver un dicc porque vamos a trasladarlo a JSON
        '''
        return {
            'dni': self.dni,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'salario': self.salario
        }
    
    def __str__(self) -> str:
        '''
        Para que al imprimir el objeto veamos una cadena de texto
        '''
        return f'{self.nombre} {self.apellido}'

class ColaboradorTiempoCompleto(Colaborador):
    '''
    Herencia: llamamos al método __init__ de la clase base o superclase Colaborador y la instanciamos 
    con los valores que recibimos en la subclase ColaboradorTiempoCompleto (el atributo diferenciador es departamento)
    '''
    def __init__(self, dni, nombre, apellido, edad, salario, departamento) -> None:
        super().__init__(dni, nombre, apellido, edad, salario) 
        self.__departamento = departamento
    
    ## Getters
    @property
    def departamento(self):
        return self.__departamento
    
    ### Vamos a sobreescribir un método de la clase base
    def to_dict(self):
        '''
        Aquí se nota el polimorfismo: dependiendo de dónde provenga el objeto (clase base o subclase)
        Este método devolverá una u otra cosa
        '''
        data = super().to_dict()
        data['departamento'] = self.departamento
        return data

    def __str__(self) -> str:
        return f'{super().__str__()}' + f' departamento: {self.departamento}' ### Devuelve el str de la clase base y se le agrega el departamento.
    
class ColaboradorTiempoParcial(Colaborador):
    def __init__(self, dni, nombre, apellido, edad, salario, horas_semanales) -> None:
        super().__init__(dni, nombre, apellido, edad, salario)
        self.__horas_semanales = horas_semanales

    @property
    def horas_semanales(self):
        return self.__horas_semanales
    
    def to_dict(self):
        data = super().to_dict()
        data['horas semanales'] = self.horas_semanales
        return data
    
    def __str__(self) -> str:
        return f'{super().__str__()} + horas semanales: {self.horas_semanales}' 

#Gestion
class GestionColaboradores:
    def __init__(self) -> None:
        '''
        Settea las variables necesarias para crear una conexión
        al instanciar un objeto de clase GestionColaboradores
        '''
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.port = config('DB_PORT')
    
    def connect(self):
        '''
        Método para establecer la conexión con la BBDD
        '''
        try:
            connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,  
                password = self.password,
                port = self.port
            )

            if connection.is_connected():
                return connection
            
        except Error as e:
            print(f'Error al conectarse a la BBDD: {e}')
            return None

    def crear_colaborador(self, colaborador):
        '''
        Este método va a recibir una instancia de Colaborador cuando llamemos desde main.py. Es decir, recibirá un input desde el usuario
        Dicha instancia será un colaborador parcial o de tiempo completo
        Ese objeto con esos datos pasa a este método para crear el colaborador
        El parámetro colaborador del método es a su vez una instancia de las subclases
        '''
        try:
            connection = self.connect() ### Crea (recibe) una conexión del método antes definido
            with connection.cursor() as cursor: ### El método cursor() permite realizar consultas a la BBDD
                ## Verificar si el DNI ya existe
                cursor.execute('SELECT dni FROM colaboradores WHERE dni = %s', (colaborador.dni, )) ### Con el comando (comodín) evitamos inyecciones SQL /// Se le pone una coma al final porque el método espera una tupla
                if cursor.fetchone(): ### Trae el primer registro encontrado (los DNI son únicos)
                    print(f'Ya existe el colaborador con el dni: {colaborador.dni}')
                    return 
                ## Insertar colaborador dependiendo del tipo
                if isinstance(colaborador, ColaboradorTiempoCompleto):
                    query = '''
                    INSERT INTO colaboradores (dni, nombre, apellido, edad, salario)
                    VALUES (%s, %s, %s, %s, %s)
                    '''

                    cursor.execute(query, (colaborador.dni, colaborador.nombre, colaborador.apellido,
                                           colaborador.edad, colaborador.salario))
                    
                    query = '''
                    INSERT INTO colaboradortiempocompleto (dni, departamento)
                    VALUES (%s, %s)
                    '''

                    cursor.execute(query, (colaborador.dni, colaborador.departamento))
                elif isinstance(colaborador, ColaboradorTiempoParcial):
                    query = '''
                    INSERT INTO colaboradores (dni, nombre, apellido, edad, salario)
                    VALUES (%s, %s, %s, %s, %s)
                    '''

                    cursor.execute(query, (colaborador.dni, colaborador.nombre, colaborador.apellido,
                                           colaborador.edad, colaborador.salario))
                    
                    query = '''
                    INSERT INTO colaboradortiempoparcial (dni, Horas_semanales)
                    VALUES (%s, %s)
                    '''

                    cursor.execute(query, (colaborador.dni, colaborador.horas_semanales))
                ## Guardar la consulta en la BBDD
                connection.commit()
                print(f'Colaborador {colaborador.nombre} {colaborador.apellido} creado con éxito')
        except Exception as e:
            print(f'Error inesperado al crear colaborador: {e}')

    def leer_colaborador(self, dni):
        '''
        Método para buscar el colaborador mediante CRUD
        '''
        try:
            '''
            Hace una consulta con un DNI dado
            Si la encuentro, crea una variable para guardar los datos 
            Evalua si está presente departamento, si es así, crea una 
            instancia de ColaboradorTiempoCompleto
            '''
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor: ### Cuando el cursor devuelve la consulta lo hará en formato diccionario
                    cursor.execute('SELECT * FROM colaboradores WHERE dni = %s', (dni,)) ### Para que Python "entienda" que es una estructura de datos tipo tupla de un solo elemento se le agrega ","
                    colaborador_data = cursor.fetchone()

                    if colaborador_data:
                        cursor.execute('SELECT departamento FROM colaboradortiempocompleto WHERE dni = %s', (dni,))
                        departamento = cursor.fetchone()

                        if departamento:
                            colaborador_data['departamento'] = departamento['departamento'] ### Agrega al diccionario del colaborador la información 'departamento' si la hubiese (consulta anterior)
                            colaborador = ColaboradorTiempoCompleto(**colaborador_data) ### Pasamos todos los datos para instanciar un colaborador
                        else: ### Quiere decir que es de tiempo parcial
                            cursor.execute('SELECT horas_semanales FROM colaboradortiempoparcial WHERE dni = %s', (dni,))
                            horas_semanales = cursor.fetchone()
                            if horas_semanales:
                                colaborador_data['horas_semanales'] = horas_semanales['horas_semanales'] ### Agrega al diccionario del colaborador la información 'departamento' si la hubiese (consulta anterior)
                                colaborador = ColaboradorTiempoParcial(**colaborador_data)
                            else:
                                colaborador = Colaborador(**colaborador_data)
                        print(f'Colaborador encontrado: {colaborador}')
                    else:
                        print(f'No se encontró el colaborador con DNI: {dni}')
        except Error as e:
            print(f'Error al leer colaborador: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def actualizar_colaborador(self, dni, nuevo_salario):
        '''
        Actualizar el salario del colaborador en la BBDD
        '''
        try:
            connection = self.connect()
            if  connection: ### Chequeamos que exista la conexión
                with connection.cursor() as cursor:
                    ### Verificar si existe DNI
                    cursor.execute('SELECT * FROM colaboradores WHERE dni = %s', (dni,))
                    if not cursor.fetchone(): ### Si no se encontró información es porque no existe ese DNI
                        print(f'No se encontró colaborador con DNI: {dni}')
                        return
                    
                    ### Actualizar el salario (si encuentra)
                    cursor.execute('UPDATE colaboradores SET salario = %s WHERE dni = %s', (nuevo_salario, dni))

                    if cursor.rowcount > 0: ### Si no tiene filas vacías es porque encontró un dato (es una validación)
                        connection.commit()
                        print(f'El nuevo salario {nuevo_salario} se actualizó correctamente para el colaborador con DNI {dni}')
                    else:
                        print(f'No se encontró colaborador con DNI {dni}')

        except Exception as e:
            print(f'Error al actualizar el colaborador: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def eliminar_colaborador(self, dni):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    ### Verificar si existe el DNI
                    cursor.execute('SELECT * FROM colaboradores WHERE dni = %s', (dni,))
                    if not cursor.fetchone():
                        print(f'No se encontró colaborador con DNI {dni}')
                        return 
                    
                    ### Eliminar colaborador
                    cursor.execute('DELETE FROM colaboradortiempocompleto WHERE dni = %s', (dni,))
                    cursor.execute('DELETE FROM colaboradortiempoparcial WHERE dni = %s', (dni,))
                    cursor.execute('DELETE FROM colaboradores WHERE dni = %s', (dni,))
                    
                    if cursor.rowcount > 0: ### Retorna la respuesta a la última consulta realizada
                        connection.commit()
                        print(f'El colaborador con DNI {dni} se eliminó correctamente')
                    else:
                        print(f'No se encontró colaborador con el siguiente DNI: {dni}')
        except Exception as e:
            print(f'Error al eliminar el colaborador: {e}')
        finally:
            if connection.is_connected():
                connection.close()
        
    def leer_todos_los_colaboradores(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM colaboradores')
                    colaboradores_data = cursor.fetchall()
                    colaboradores = []
                    for colaborador_data in colaboradores_data:
                        dni = colaborador_data['dni']
                        cursor.execute('SELECT departamento FROM colaboradortiempocompleto WHERE dni = %s', (dni,))
                        departamento = cursor.fetchone()
                        if departamento:
                            colaborador_data['departamento'] = departamento['departamento']
                            colaborador = ColaboradorTiempoCompleto(**colaborador_data)
                        else:
                            cursor.execute('SELECT horas_semanales FROM colaboradortiempoparcial WHERE dni = %s', (dni,))
                            horas_semanales = cursor.fetchone()
                            colaborador_data['horas_semanales'] = horas_semanales['horas_semanales']
                            colaborador = ColaboradorTiempoParcial(**colaborador_data)
                        colaboradores.append(colaborador)
        except Exception as e:
            print(f'Error al mostrar los colaboradores: {e}')
        else:
            return colaboradores
        finally:
            if connection.is_connected():
                connection.close()