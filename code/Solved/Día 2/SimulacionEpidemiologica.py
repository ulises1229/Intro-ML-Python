from Ayudas import ObtenerNumeroEntero, ObtenerNumeroFlotante
import numpy as np

# Calculo del contagio de cada individuo dependiendo de sus alrededores
def CalcularContagio(i, j, caso):
    inicio_i = i-1; inicio_j = j-1; final_i = i+1; final_j = j+1;
    # Verificación de orillas
    if i == 0:
        inicio_i = i
    elif i == dimensiones[0]-1:
        final_i = i
    if j == 0:
        inicio_j = j
    elif j == dimensiones[1]-1:
        final_j = j

    # Si es susceptible
    if caso == 0:
        # Encontramos cuántos contagiados hay en los alrededores
        contagiados = np.sum(personas[inicio_i:final_i+1, inicio_j:final_j+1] == 1)
        # Para cada contagiado lanzamos la moneda cargada
        for contagiado in range(contagiados):
            if np.random.rand() <= beta:
                # Si sale la moneda cargada con probabilidad beta, se infecta
                return 1
        # Si no se contagió en ninguna interacción, sigue como susceptible
        return 0
    # Si está infectado
    elif caso == 1:
        # Lanzamos la moneda cargada, si se cumple, pasa al estado removido (2)
        return caso + 1 * (np.random.rand() <= gamma)
    # Si no se cumple ninguna de las anteriores es porque era removido, y por tanto se queda igual
    return caso

# Simular un día
def PasoSimulacion():
    global personas
    # Creamos una copia del arreglo antes de modificarlo
    siguientes_personas = personas.copy() ##diferencia entre asignar y copiar un arreglo
    for i in range(dimensiones[0]):
        for j in range(dimensiones[1]):
            siguientes_personas[i, j] = CalcularContagio(i, j, personas[i][j])
    personas = siguientes_personas

# Distribución de los casos iniciales
def CasosIniciales(iniciales):
    global personas
    # Por cada caso inicial
    for contagiado in range(iniciales):
        # Obtenemos dos índices random
        i = np.random.randint(dimension)
        j = np.random.randint(dimension)
        # Si la persona en ese índice ya está infectada repetimos el proceso
        while personas [i][j] == 1:
            i = np.random.randint(dimension)
            j = np.random.randint(dimension)
        # Asignamos el estado de infectado a la persona del elemento [i][j]
        personas[i][j] = 1


# Total de personas
dimension = ObtenerNumeroEntero(pregunta='¿Cuántas personas hay en la simulación? (Se tomará floor(sqrt)): ')

# Casos iniciales
iniciales = ObtenerNumeroEntero(pregunta='¿Cuántos contagiados iniciales hay?: ')

# Valor de factor beta (probabilidad de contagiarse)
beta = ObtenerNumeroFlotante(min=0, max=1, pregunta='¿Cuál es el valor de beta? (probabilidad de que un suceptible se contagie): ') ##entre 0 y 1

# Valor de factor gamma (probabilidad de recuperarse)
gamma = ObtenerNumeroFlotante(min=0, max=1, pregunta='¿Cuál es el valor de gamma? (probabilidad de que un infectado se recupere o muera): ') ##entre 0 y 1

# Raíz del número de personas (la forma es un cuadrado)
dimension = int(np.sqrt(dimension))
dimensiones = (dimension, dimension)

#Arreglo de personas inicial (todos susceptibles)
personas = np.zeros(dimensiones)

# Distribución de los caso iniciales
CasosIniciales(iniciales)
# Mostramos los casos iniciales (día 0)
dia = 0
print(f"\nDía {dia}")
print(personas)

# Simular hasta que deje de haber infectados
while sum(sum(personas == 1)) != 0:
    PasoSimulacion()
    # Mostramos la istribución de casos por día
    print(f"\nDía {dia + 1}")
    print(personas)
    dia += 1

print(f"\nFinal de la simulación en día {dia}.")
print(f"{sum(sum(personas == 0))} Susceptibles.\n{sum(sum(personas==2))} Removidos.")
