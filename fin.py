import time
import requests
import json
import urllib.parse
import browser_cookie3

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


def consultar_por_nombre():
    nombre = input("Ingrese apellidos, nombres: ")
    resultados = input("N° de sujetos: ")

    nombre_codificado = urllib.parse.quote(nombre.upper())

    url = f"https://srienlinea.sri.gob.ec/movil-servicios/api/v1.0/deudas/porDenominacion/{nombre_codificado}/?tipoPersona=N&resultados={resultados}&_=1749327249455"

    response = requests.get(url)

    try:
        data = response.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except ValueError:
        print("La respuesta no es JSON válida:")
        print(response.text)


def consultar_por_cedula():
    num = input("Ingrese el número de cédula: ")

    url = f"https://srienlinea.sri.gob.ec/movil-servicios/api/v1.0/deudas/porIdentificacion/{num}/?tipoPersona=N&_=1749334567532"

    response = requests.get(url)

    try:
        data = response.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except ValueError:
        print("La respuesta no es JSON válida:")
        print(response.text)


def main():
    while True:
        print("\n=== CONSULTAS DISPONIBLES ===")
        print("1. Consultar por PLACA")
        print("2. Consultar por NOMBRE COMPLETO")
        print("3. Consultar por NÚMERO DE CÉDULA")
        print("4. Salir")

        opcion = input("\nSeleccione una opción (1-4): ").strip()

        if opcion == "1":
            consultar_por_placa()
        elif opcion == "2":
            consultar_por_nombre()
        elif opcion == "3":
            consultar_por_cedula()
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("[!] Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()