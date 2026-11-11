"""Respaldo de configuraciones por SSH (Netmiko).

Lee inventario.csv (columnas: nombre, ip), se conecta a cada equipo por SSH y
guarda el "show running-config" en respaldos/AAAA-MM-DD/<nombre>.txt, con los
hashes de contraseñas reemplazados por <REDACTED>.

Uso:
    pip install netmiko
    python backup_configs.py

Notas:
- En este proyecto el SSH solo se acepta desde la VLAN 30 (ADMIN-IT), así que el
  script debe ejecutarse desde un equipo de esa VLAN.
- La contraseña se pide por teclado y no se guarda en ningún archivo. En el
  laboratorio el enable usa la misma contraseña que el usuario.
"""
import csv
import re
from datetime import date
from getpass import getpass
from pathlib import Path

# Hash o contraseña cifrada que sigue a "secret" o "password" (tipos 5, 7, 8 y 9)
PATRON_HASH = re.compile(r"\b((?:secret|password)\s+[5789])\s+\S+")


def redactar(texto):
    """Reemplaza los hashes de contraseñas por <REDACTED>."""
    return PATRON_HASH.sub(r"\1 <REDACTED>", texto)


def leer_inventario(ruta):
    """Devuelve una lista de diccionarios {"nombre": ..., "ip": ...}."""
    with open(ruta, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def respaldar(equipo, usuario, clave):
    """Se conecta al equipo por SSH y devuelve su running-config."""
    from netmiko import ConnectHandler  # se importa aquí para dar un error claro si falta

    with ConnectHandler(
        device_type="cisco_ios",
        host=equipo["ip"],
        username=usuario,
        password=clave,
        secret=clave,
    ) as conexion:
        # En los switches L2 del proyecto el usuario entra en modo usuario (>);
        # enable() no hace nada si ya está en modo privilegiado (#).
        conexion.enable()
        return conexion.send_command("show running-config")


def main():
    equipos = leer_inventario("inventario.csv")
    usuario = input("Usuario [admin]: ") or "admin"
    clave = getpass("Contraseña: ")

    carpeta = Path("respaldos") / date.today().isoformat()
    carpeta.mkdir(parents=True, exist_ok=True)

    correctos = 0
    for equipo in equipos:
        nombre = equipo["nombre"]
        try:
            config = respaldar(equipo, usuario, clave)
        except Exception as error:  # un equipo caído no debe detener el resto
            print(f"FALLO {nombre} ({equipo['ip']}): {error}")
            continue

        archivo = carpeta / f"{nombre.lower()}.txt"
        archivo.write_text(redactar(config) + "\n", encoding="utf-8")
        print(f"OK    {nombre} -> {archivo}")
        correctos += 1

    print(f"\n{correctos} de {len(equipos)} equipos respaldados en {carpeta}")


if __name__ == "__main__":
    main()
