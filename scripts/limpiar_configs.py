"""Limpia los configs exportados de Packet Tracer: redacta hashes y revisa restos.

Uso (dentro de la carpeta con los .txt ya renombrados):
    python limpiar_configs.py
o indicando la carpeta:
    python limpiar_configs.py ruta/a/la/carpeta

Los resultados se guardan en la subcarpeta "limpios"; los originales no se tocan.
"""
import re
import sys
from pathlib import Path

# Hash o contraseña cifrada que sigue a "secret" o "password" (tipos 5, 7, 8 y 9)
PATRON_HASH = re.compile(r"\b((?:secret|password)\s+[5789])\s+\S+")
# Líneas con secret/password que quedaron sin redactar (para revisar a mano)
PATRON_REVISAR = re.compile(r"\b(?:secret|password)\s")
# Restos de las pruebas de QoS
PATRON_QOS = re.compile(r"mls qos|class-map|policy-map|service-policy")


def main():
    carpeta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    salida = carpeta / "limpios"
    salida.mkdir(exist_ok=True)

    archivos = sorted(carpeta.glob("*.txt"))
    if not archivos:
        print(f"No hay archivos .txt en {carpeta}")
        return

    for archivo in archivos:
        lineas = archivo.read_text(encoding="utf-8", errors="replace").splitlines()
        limpias = []
        cambios = []  # (número de línea, línea ya redactada)

        for numero, linea in enumerate(lineas, start=1):
            nueva = PATRON_HASH.sub(r"\1 <REDACTED>", linea)
            if nueva != linea:
                cambios.append((numero, nueva))
            limpias.append(nueva)

        with open(salida / archivo.name, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(limpias) + "\n")
        print(f"{archivo.name}: {len(cambios)} línea(s) redactada(s)")
        for numero, nueva in cambios:
            print(f"  línea {numero}: {nueva.strip()}")

        for numero, linea in enumerate(limpias, start=1):
            if PATRON_REVISAR.search(linea) and "<REDACTED>" not in linea:
                print(f"  REVISAR {archivo.name}:{numero}: {linea}")
            if PATRON_QOS.search(linea):
                print(f"  QOS {archivo.name}:{numero}: {linea}")

    print(f"\nListo. Resultados en: {salida}")


if __name__ == "__main__":
    main()
