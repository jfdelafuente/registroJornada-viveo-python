import configD
import logging

def dia_validate(dia):
        mensaje = ''
        registrar = True
        hoy = dia.strftime("%d/%m/%Y")
        hoy_fanual = dia.strftime("%d/%m")

        # Evaluamos Vacaciones y Festivos
        if hoy in configD.festivosOtros:
            mensaje += f'\n{configD.VACACIONES}'
            registrar = False
            logging.debug("Evaluamos día --> Vacaciones : %s : %s" %
                          (configD.VACACIONES, str(registrar)))
        elif hoy_fanual in configD.festivosAnuales:
            mensaje += f'\n{configD.FESTIVO}'
            registrar = False
            logging.debug("Evaluamos día --> Festivos : %s : %s" %
                          (configD.FESTIVO, str(registrar)))
        else:
            logging.debug("Evaluamos día --> Ni vacas ni festivo")

        # Evaluamos Días de Teletrabajo
        if dia.isoweekday() not in configD.diasTeletrabajo:
            registrar = hoy in configD.novoy
            logging.debug("Evaluamos dias de la semana: %s : %s" %
                          (configD.TELETRABAJO, str(registrar)))
            mensaje += f'\n{configD.TELETRABAJO} : {registrar}'
        else:
            logging.debug(
                "Registramos el '%s', ya que corresponde a un día de teletrabajo y no he indicado Teletrabajo Ocasional." % dia)

        return mensaje, registrar

def dummy(dia):
        mensaje = ''
        registrar = True
        logging.debug("Evaluamos el día forzado %s" % str(dia))
        return mensaje
