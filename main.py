'''
Mientras que en main implementamos los métodos, en el otro archivo tenemos las clases y los mencionados métodos
'''

import os
import platform

from poo import (
    ColaboradorTiempoCompleto,
    ColaboradorTiempoParcial,
    GestionColaboradores
)

def limpiar_pantalla():
    '''
    Limpiar la pantalla según OS
    Todos se limpian de una manera excepto Windows
    '''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') #Para Linux/MacOS

def mostrar_menu():
    print('Menu de gestion de colaboradores')
    print('1. Crear colaborador tiempo completo')
    print('2. Crear colaborador tiempo parcial')
    print('3. Buscar colaborador')
    print('4. Actualizar colaborador')
    print('5. Eliminar colaborador')
    print('6. Mostrar todos los colaboradores')
    print('7. Salir')

def agregar_colaborador(gestion: GestionColaboradores, tipo_colaborador):
    '''
    Recibe una instancia de colaborador 
    (necesitamos los datos del colaborador)
    '''
    try:
        dni = int(input('Ingrese dni: '))
        nombre = input('Ingrese nombre: ')
        apellido = input('Ingrese apellido: ')
        edad = int(input('Ingrese edad: '))
        salario = float(input('Ingrese salario: '))

        if tipo_colaborador == '1':
            departamento = input('Ingrese departamento: ')
            colaborador = ColaboradorTiempoCompleto(dni, nombre, apellido, 
                                                edad, salario, departamento)
        elif tipo_colaborador == '2':
            horas_semanales = int(input('Ingrese horas semanales: '))
            colaborador = ColaboradorTiempoParcial(dni, nombre, apellido, 
                                                edad, salario, horas_semanales)
        else:
            print('Opción inválida')
            return


        # Instancia
        gestion.crear_colaborador(colaborador)
        input('Presione enter para continuar...') #Por limpiado de pantalla 

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_colaborador_por_dni(gestion):
    dni = input('Ingrese el DNI del colaborador a buscar: ')
    gestion.leer_colaborador(dni)
    input('Presione una tecla para continuar...')

def actualizar_salario_colaborador(gestion):
    dni = input('Ingrese el DNI del colaborador a actualizar: ')
    salario = float(input('Ingrese el salario del colaborador: '))
    gestion.actualizar_colaborador(dni, salario)
    input('Presione una tecla para continuar...')

def eliminar_colaborador_por_dni(gestion):
    dni = input('Ingrese el DNI del colaborador a eliminar: ')
    gestion.eliminar_colaborador(dni)
    input('Presione una tecla para continuar...')

def mostrar_todos_los_colaboradores(gestion):
    print('=== Listado completo de colaboradores ===')
    for colaborador in gestion.leer_datos().values():
        if 'departamento' in colaborador:
            print(f"{colaborador['nombre']} - Departamento: {colaborador['departamento']}")
        else:
            print(f"{colaborador['nombre']} - Horas semanales: {colaborador['horas semanales']}")
    print('=== /// === /// ===')
    input('Presione una tecla para continuar')

'''
Cuando 'detecta' que se está ejecutando este archivo, 
corre esta porción de código:
'''
if __name__ == '__main__':
    archivo_colaboradores = 'colaboradores_db.json' # De momento este archivo no existe, vamos a crearlo via código
    gestion_colaboradores = GestionColaboradores(archivo_colaboradores) # Instancia de la clase que implementa el CRUD // la búsqueda en JSON

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_colaborador(gestion_colaboradores, opcion)
        
        if opcion == '3':
            buscar_colaborador_por_dni(gestion_colaboradores)
        
        if opcion == '4':
            actualizar_salario_colaborador(gestion_colaboradores)
        
        if opcion == '5':
            eliminar_colaborador_por_dni(gestion_colaboradores)
        
        if opcion == '6':
            mostrar_todos_los_colaboradores(gestion_colaboradores)
        
        if opcion == '7':
            print('Saliendo del programa...')
            break
        
        else:
            print('Opcion no válida. Seleccione una opción válida (1-7)')