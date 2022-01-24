def ObtenerNumeroEntero(pregunta = ""):
    """

    Pide al usuario ingresar un número entero mostrando el texto en pregunta.
    Si el usuario no ingresa un número entero se vulve a repetir la pregunta.

    Parámetros
    ----------
    pregunta : string, opcional
        Pregunta mostrada al usuario.
        Si no se especifica no se muestra ninguna frase.

    Regresa
    -------
    numero : int
        Número entero ingresado por el usuario.
    """

    numero = input(pregunta)
    while not numero.isnumeric():
        numero = input(pregunta)
    return int(numero)


def ObtenerNumeroFlotante(pregunta="", min=None, max=None):
	"""

    Pide al usuario ingresar un número flotante (fraccional) mostrando el texto
	en pregunta. Si el usuario no ingresa un número que se pueda convertir a un
	punto flotante se repite la pregunta hasta que el usuario ingrese un número
	válido.

    Parámetros
    ----------
    pregunta : string, opcional
        Pregunta mostrada al usuario.
        Si no se especifica no se muestra ninguna frase.
	min : float, opcional
		Valor mínimo que debe de tener el valor ingresado por el usuario. Si no
		se ingresa se admite cualquier valor sin límite inferior por el usuario.
	max : float, opcional
		Valor máximo que debe de tener el valor ingresado por el usuario. Si no
		se ingresa se admite cualquier valor sin límite superior por el usuario.

    Regresa
    -------
    numero : float
        Número flotante ingresado por el usuario. Si se especifica un valor
		mínimo el valor regresado será mayor. Si e especifica un valor máximo,
		el valor regresado será menor.
    """

	while True:
		numero = input(pregunta)
		if not PruebaFloat(numero):
			continue
		numero = float(numero)
		if min != None:
			if numero < min:
				continue
		if max != None:
			if numero > max:
				continue
		return numero


def PruebaFloat(num):
	"""

    Prueba si un valor ingresado en una cadena de caracteres puede ser convertido
	a un número de punto flotante válido.

    Parámetros
    ----------
    num : string
        Cadena de caracteres que se intentará convertir a un número de punto
		flotante.

    Regresa
    -------
    out : bool
        Si num se pudo convertir a un número de punto flotante válido regresa True,
		de lo contrario regresa False.
    """
	try:
		float(num)
		return True
	except ValueError:
		return False
