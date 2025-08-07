import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import random
import browser_cookie3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Cabeceras para simular navegador real
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Referer": "https://www.ecuadorlegalonline.com/",
    "Origin": "https://www.ecuadorlegalonline.com",
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Language": "es-EC,es;q=0.9,en;q=0.8"
}

# --- Consulta por Nombre -> Cédula ---
def consultar_cedula_por_nombre(nombre, limite):
    nombre_cod = urllib.parse.quote(nombre.upper().strip())
    timestamp = str(int(time.time() * 1000))
    url = f"https://apps.ecuadorlegalonline.com/modulo/consultar-cedulanombre.php?nombres={nombre_cod}&_={timestamp}"

    with requests.Session() as s:
        s.headers.update(HEADERS)
        r = s.get(url, timeout=10)
        if r.status_code != 200:
            print(f"[!] Error HTTP {r.status_code}")
            return
        try:
            data = r.json()
            if data and isinstance(data, list):
                if limite > 0:
                    data = data[:limite]
                print("\n[✔] Resultados encontrados:")
                for i, persona in enumerate(data, start=1):
                    cedula = persona.get("identificacion", "N/A")
                    nombre_completo = persona.get("nombreCompleto", "N/A")
                    print(f"{i}. Cédula: {cedula} | Nombre: {nombre_completo}")
            else:
                print("[✘] No se encontró resultado.")
        except Exception as e:
            print(f"[!] Error al decodificar JSON: {e}")

# --- Consulta por Nombre desde archivo ---
def consultar_cedula_por_nombre_desde_archivo(ruta_archivo, limite):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            nombres = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] Error al leer archivo: {e}")
        return

    for nombre in nombres:
        print(f"\nConsultando cédula para nombre: {nombre}")
        consultar_cedula_por_nombre(nombre, limite)
        time.sleep(random.uniform(1, 2))

# --- Consulta por Cédula -> Nombre (requests) ---
def consultar_nombre_por_cedula(cedula):
    url_post = "https://www.ecuadorlegalonline.com/modulo/consultar-cedula.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Origin": "https://www.ecuadorlegalonline.com",
        "Referer": "https://www.ecuadorlegalonline.com/consultas/registro-civil/consultar-el-nombre-con-el-numero-de-cedula/",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {"ci": cedula}

    with requests.Session() as s:
        r = s.post(url_post, data=data, headers=headers, timeout=10)
        if r.status_code != 200:
            print(f"[!] Error HTTP {r.status_code}")
            return

        with open("respuesta.html", "w", encoding="utf-8") as f:
            f.write(r.text)
        print("[*] Respuesta guardada en respuesta.html")

# --- Consulta por Placa ---
def consultar_por_placa():
    placa = input("Ingrese la placa del vehículo: ").strip().upper()
    timestamp = int(time.time() * 1000)
    url = f"https://www.ecuadorlegalonline.com/modulo/sri/matriculacion/consultar-dueno.php?placa={placa}&_={timestamp}"

    try:
        cookies = browser_cookie3.firefox(domain_name="ecuadorlegalonline.com")
    except Exception as e:
        print("[!] No se pudo obtener cookies desde Firefox.")
        print(f"Error: {e}")
        return

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.ecuadorlegalonline.com/consultas/agencia-nacional-de-transito/consultar-a-quien-pertenece-un-vehiculo-por-placa-ant/",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "*/*",
        "Accept-Language": "es-EC,es;q=0.9,en;q=0.8"
    }

    print(f"\n[+] Consultando datos para la placa: {placa}...\n")
    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code == 200:
        print("Resultado:")
        print(response.text)
    else:
        print(f"[!] Error al consultar: Código HTTP {response.status_code}")

# --- Menú principal ---
def main():
    while True:
        print("\n=== CONSULTAS DISPONIBLES ===")
        print("1. Buscar CÉDULA por NOMBRE")
        print("2. Buscar NOMBRE por CÉDULA")
        print("3. Buscar PROPIETARIO por PLACA")
        print("4. Salir")
        print("5. Buscar CÉDULA por NOMBRES desde archivo")

        opcion = input("\nSeleccione una opción (1-5): ").strip()

        if opcion == "1":
            nombre = input("Ingrese apellidos y nombres: ").strip()
            try:
                limite = int(input("¿Cuántos resultados mostrar? (0 = todos): ").strip())
            except:
                limite = 0
            consultar_cedula_por_nombre(nombre, limite)

        elif opcion == "2":
            cedula = input("Ingrese número de cédula: ").strip()
            consultar_nombre_por_cedula(cedula)

        elif opcion == "3":
            consultar_por_placa()

        elif opcion == "5":
            ruta = input("Ingrese ruta del archivo con nombres: ").strip()
            try:
                limite = int(input("¿Cuántos resultados mostrar por nombre? (0 = todos): ").strip())
            except:
                limite = 0
            consultar_cedula_por_nombre_desde_archivo(ruta, limite)

        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("[!] Opción inválida. Intente de nuevo.")

        time.sleep(random.uniform(1, 2))

if __name__ == "__main__":
    main()
