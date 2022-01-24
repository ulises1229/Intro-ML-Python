import pandas as pd

# Leer reporte de movilidad de Google (original, ¡¡¡UNICAMENTE SI LO DESCARGASTE DESDE EL PROYECTO INICIAL!!!)
#google = pd.read_csv("GoogleMobility.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')

# Leer reporte de movilidad de Google (tamaño reducido, con menos datos)
google = pd.read_csv("GoogleMobilitysmall.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')

# Seleccionar datos de México únicamente
google = google.loc[google['country_region_code'] == 'MX']

google.to_csv("GoogleMobilitysmall.csv")

# Seleccionar columnas de interés
columnas = ['sub_region_1', 'date', 'retail_and_recreation_percent_change_from_baseline',
            'grocery_and_pharmacy_percent_change_from_baseline', 'parks_percent_change_from_baseline',
            'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline',
            'residential_percent_change_from_baseline']
google = google[columnas]

# Cambiar nombres de columnas a español
google = google.rename(columns={'sub_region_1': 'Estado', 'date': 'Fecha',
        'retail_and_recreation_percent_change_from_baseline': 'Tiendas y ocio',
       'grocery_and_pharmacy_percent_change_from_baseline': 'Supermercados y farmacias',
       'parks_percent_change_from_baseline': 'Parques',
       'transit_stations_percent_change_from_baseline': 'Estaciones de transporte',
       'workplaces_percent_change_from_baseline': 'Oficinas',
       'residential_percent_change_from_baseline': 'Hogares'})

# Estandarizar nombres de estados
google = google.replace(google["Estado"].unique(), ['NACIONAL', 'AGUASCALIENTES', 'BAJA CALIFORNIA',
'BAJA CALIFORNIA SUR', 'CAMPECHE', 'CHIAPAS', 'CHIHUAHUA', 'COAHUILA', 'COLIMA', 'DURANGO',
'GUANAJUATO', 'GUERRERO', 'HIDALGO', 'JALISCO', 'DISTRITO FEDERAL', 'MICHOACAN',
'MORELOS', 'NAYARIT', 'NUEVO LEON', 'OAXACA', 'PUEBLA', 'QUERETARO', 'QUINTANA ROO',
'SAN LUIS POTOSI', 'SINALOA', 'SONORA', 'MEXICO', 'TABASCO', 'TAMAULIPAS', 'TLAXCALA',
'VERACRUZ', 'YUCATAN', 'ZACATECAS'])

# Dar formato de fecha
google["Fecha"] = pd.to_datetime(google["Fecha"], format = "%Y-%m-%d")

# Ordenamos para una mejor apreciación (opcional)
google = google.sort_values(by=["Estado", "Fecha"])
###############################
### Google ya está completo ###
###############################

# Leer datos de contagios, muertes, negativos y sospechosos
conf_data = pd.read_csv("Confirmados.csv")
def_data = pd.read_csv("Defunciones.csv")
neg_data = pd.read_csv("Negativos.csv")
sos_data = pd.read_csv("Sospechosos.csv")

# Creamos nuevo df a rellenar
datos = pd.DataFrame()
# Obtenemos la lista de estados
estados = conf_data["nombre"].unique()

# Hacer un ciclo que recorra todas las fechas que hay en los sets.
#Genera un renglón por cada día por cada estado
for fecha in conf_data.columns[3:]:
    #Creamos un nuevo df
    tdatos = pd.DataFrame()
    # Para cada fecha hacemos la comparación para cada estado (el ciclo ya contiene los casos confirmados)
    for i, confv in enumerate(conf_data[fecha]):
        # Si hubo negativos ese día
        if fecha in neg_data.columns:
            negv = neg_data[fecha][i]
        else:
            confv = 0
        # Si hubo defunciones ese día
        if fecha in def_data.columns:
            defv = def_data[fecha][i]
        else:
            defv = 0
        # Si hubo sospechosos ese día
        if fecha in sos_data.columns:
            sosv = sos_data[fecha][i]
        else:
            sosv = 0
        # Unimos los resultados de cada estado con la lista de estados y lo guardamos para la fecha actual en el ciclo
        tdatos = pd.concat([tdatos, pd.DataFrame([pd.Series([estados[i], fecha, confv, negv, defv, sosv])])], ignore_index = True)
    # Unimos la nueva fecha al conjunto de fechas que ya teníamos
    datos = pd.concat([datos, tdatos])
# Cambiamos los títulos a las columnas
datos.columns = ["Estado", "Fecha", "Confirmados", "Negativos", "Defunciones", "Sospechosos"]
# Modificamos el formato de fecha
datos["Fecha"] = pd.to_datetime(datos["Fecha"], format = "%d-%m-%Y")
# Ponemos en mayúsculas todos los estados
datos['Estado'] = datos['Estado'].replace("Nacional", "NACIONAL")
# Ordenamos para una mejor apreciación (opcional)
datos = datos.sort_values(by=["Estado", "Fecha"])
###############################
### Datos ya está completo ####
###############################

# Unimos ambos datasets (datos y google) donde se intersecten (ambos contengan) el mismo estado y la misma fecha
dataset = pd.merge(datos, google, on=["Estado", "Fecha"])

# Podemos guardar nuestro dataset final en un CSV
dataset.to_csv("DatosMexico.csv", index=False)

############ CASO INETRESANTE ############
# Cuando hacemos el merge, únicamente se juntan donde en ambos datasets (datos y google) se tienen las mismas
# fechas para los mismos estados. Esto puede llevar a que se recorten los datasets, por ejemplo vamos a comparar
# el número de infectados en el nuevo dataset y el original de datos

# Casos en el dataset creado (¿¿¿error???)
sum(dataset['Confirmados'].loc[dataset['Estado'] != 'NACIONAL'])

# Casos antes del merge
sum(datos['Confirmados'].loc[datos['Estado'] != 'NACIONAL'])

# ¿De cuánto fue la diferencia? ¿Por qué sucedió eso? ¿Qué fechas no tienen en común?
