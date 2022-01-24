def ObtenerNumeroPacientes(pregunta = "¿Cuántos pacientes hay hoy?: "):
    """

    Pide al usuario ingresar el número de pacientes
    que va a atender con el código actual. Se despliega
    al usuario el mensaje en pregunta.

    Parámetros
    ----------
    pregunta : string, opcional
        Pregunta mostrada al usuario para saber el número de pacientes.
        Si no se especifica se muestra la pregunta por default '¿Cuántos pacientes hay hoy?'.

    Regresa
    -------
    respuesta : int
        Número de pacientes.
    """

    respuesta = input(pregunta)
    while not respuesta.isnumeric():
        respuesta = input(pregunta)
    return int(respuesta)

def PacienteTiene(sintoma):
    """

    Pregunta al usuario si padece del síntoma especificado
    en la variable 'sintoma', siendo 1 sí y 0 no. Cualquier
    otra respuesta hace que se vuelva a hacer la pregunta.

    Parámetros
    ----------
    síntoma : string
        Síntoma que se le va a preguntar al paciente.

    Regresa
    -------
    out : bool
        Regresa True si el paciente presenta el síntoma
        y False si no lo presenta.
    """
    sintom = int(input(sintoma + ": "))
    while sintom != 0 and sintom != 1:
        print("Respuesta no válida, recuerda 1 es sí, 0 es no.")
        sintom = int(input(sintoma + ": "))
    if sintom == 0:
        return False
    return True
