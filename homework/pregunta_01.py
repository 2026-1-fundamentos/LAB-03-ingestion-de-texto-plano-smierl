"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    filas = []

    with open("files/input/clusters_report.txt", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    patron = re.compile(
        r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s+%\s+(.*)"
    )

    cluster = None
    cantidad = None
    porcentaje = None
    palabras = ""

    for linea in lineas:

        coincidencia = patron.match(linea)

        if coincidencia:

            # Guardar el registro anterior
            if cluster is not None:
                palabras = re.sub(r"\s+", " ", palabras)
                palabras = re.sub(r"\s*,\s*", ", ", palabras).strip(" ,.")

                filas.append(
                    [
                        int(cluster),
                        int(cantidad),
                        float(porcentaje.replace(",", ".")),
                        palabras,
                    ]
                )

            # Nuevo registro
            cluster = coincidencia.group(1)
            cantidad = coincidencia.group(2)
            porcentaje = coincidencia.group(3)
            palabras = coincidencia.group(4)

        elif cluster is not None:
            # Continuación de palabras clave
            palabras += " " + linea.strip()

    # Guardar último registro
    palabras = re.sub(r"\s+", " ", palabras)
    palabras = re.sub(r"\s*,\s*", ", ", palabras).strip(" ,.")

    filas.append(
        [
            int(cluster),
            int(cantidad),
            float(porcentaje.replace(",", ".")),
            palabras,
        ]
    )

    df = pd.DataFrame(
        filas,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )

    return df