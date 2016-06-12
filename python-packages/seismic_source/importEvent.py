def str2Attrib(strg):
	'''	
	:param strg: cadena que representa el atributo a convertir
	'''
	try:
		# tratar de convertir el dato a entero
		return(int(strg))

	except ValueError:

		# tratar de convertir el dato a flotante
		try:

			return(float(strg))

		except ValueError:
			# usar el string para almacenar la informacion
			return(strg)

