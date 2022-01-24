import pandas as pd
import matplotlib.pyplot as plt

# Leer reporte de movilidad de Google
datos = pd.read_csv("DatosMexico.csv", index_col=False)
# Dar formato de fecha
datos["Fecha"] = pd.to_datetime(datos["Fecha"], format = "%Y-%m-%d")

# Obtener lista de estados
datos['Estado'].unique()

# Seleccionar estado
estado = 'NACIONAL'
datosEstado = datos.loc[datos['Estado'] == estado]
# Seleccionar únicamente datos de movilidad
movDatos = datosEstado.drop(["Casos", "Defunciones", "Negativos", "Sospechosos"], 1)

# Graficar en líneas los datos de movilidad
movDatos.plot(x='Fecha')
plt.ylabel('Cmabios en tendencia')
plt.title('Movilidad en ' + estado)

movDatos = movDatos.drop(["Estado", "Fecha"], 1)
proms = movDatos.mean(axis=1)
plt.plot(proms, datosEstado['Casos'], 'o', label="Confirmados")
plt.plot(proms, datosEstado['Defunciones'], 'o', label="Defunciones")
plt.plot(proms, datosEstado['Sospechosos'], 'o', label="Sospechosos")
plt.legend()
plt.title('Números diarios por promedio de movilidad en ' + estado)
plt.ylabel('Personas')
plt.xlabel('Promedio de movilidad')
