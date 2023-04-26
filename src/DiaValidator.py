import configD
import logging

def validate(dia):
        mensaje = ''
        registrar = True
        TELETRABAJO = "No es dia de teletrabajo, tengo teletrabajo ocasional ? "
        FESTIVO = "Hoy es festivo/vacaciones, no cargamos registro de Jornada."
        VACACIONES = "Hoy estás de vacaciones. Disfruta del día."
        hoy = dia.strftime("%d/%m/%Y")
        hoy_fanual = dia.strftime("%d/%m")

        # Evaluamos Vacaciones y Festivos
        if hoy in configD.festivosOtros:
            mensaje += f'\n{VACACIONES}'
            registrar = False
            logging.debug("Evaluamos día --> Vacaciones : %s : %s" %
                          (VACACIONES, str(registrar)))
        elif hoy_fanual in configD.festivosAnuales:
            mensaje += f'\n{FESTIVO}'
            registrar = False
            logging.debug("Evaluamos día --> Festivos : %s : %s" %
                          (FESTIVO, str(registrar)))
        else:
            logging.debug("Evaluamos día --> Ni vacas ni festivo")

        # Evaluamos Días de Teletrabajo
        if dia.isoweekday() not in configD.diasTeletrabajo:
            registrar = hoy in configD.novoy
            logging.debug("Evaluamos dias de la semana: %s : %s" %
                          (TELETRABAJO, str(registrar)))
            mensaje += f'\n{TELETRABAJO} : {registrar}'
        else:
            logging.debug(
                "Registramos el '%s', ya que corresponde a un día de teletrabajo y no he indicado Teletrabajo Ocasional." % dia)

        return mensaje, registrar

def dummy(dia):
        mensaje = ''
        registrar = True
        logging.debug("Evaluamos el día forzado %s" % str(dia))
        return mensaje
