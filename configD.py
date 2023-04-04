#!/usr/bin/python3

# Dias teletrabajo (Lunes=1, Martes=2, Miercoles=3, Jueves=4, Viernes=5)
diasTeletrabajo = [1,2]
# Horas
hinicio = "8:00"
hfin = "18:00"
hinicioV = "7:30"
hfinV = "15:00"
# Programa
urlVO = 'https://newvo.orange.es'
urlOAMBase = 'https://applogin.orange.es'
urlRegistroJ = 'https://newvo.orange.es/group/viveorange/registro-de-jornada'
urlRegistroJC = 'https://newvo.orange.es/api/jsonws/invoke'
urlRJAccion = 'https://www.registratujornadaorange.com/RealizarAccion'
urlRJInforme = 'https://www.registratujornadaorange.com/ObtenerContenidoInformeGeneral'

# Festivos que se repiten todos los años
festivosAnuales = []
festivosAnuales.append("01/01")
festivosAnuales.append("06/01")
festivosAnuales.append("15/08")
festivosAnuales.append("12/10")
festivosAnuales.append("01/11")
festivosAnuales.append("09/11")
festivosAnuales.append("06/12")
festivosAnuales.append("08/12")

# festivosOtros festivos y vacaciones (año completo)
festivosOtros = []
festivosOtros.append("01/01/2022")
festivosOtros.append("26/12/2022")
festivosOtros.append("02/12/2022")
festivosOtros.append("27/12/2022")
festivosOtros.append("28/12/2022")
festivosOtros.append("29/12/2022")
festivosOtros.append("30/12/2022")
festivosOtros.append("25/01/2022")
festivosOtros.append("02/02/2023")
festivosOtros.append("20/03/2023")
festivosOtros.append("06/04/2023")
festivosOtros.append("07/04/2023")
festivosOtros.append("15/03/2023")
festivosOtros.append("21/03/2023")
festivosOtros.append("22/03/2023")
festivosOtros.append("23/03/2023")
festivosOtros.append("24/03/2023")

# Dias que teletrabjo fuera de los planificados ( X,J )
novoy = []
novoy.append("05/03/2023")
novoy.append("11/08/2023")
novoy.append("16/08/2023")