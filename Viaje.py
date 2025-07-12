import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "6380ddff-61d3-43a4-91f1-cb761bb01fdc"

def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")

        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name

        return json_status, lat, lng, new_loc
    else:
        print(f"Error al geocodificar {location}. Estado: {json_status}")
        return json_status, None, None, location

def obtener_ruta(origen, destino, key, vehicle):
    orig = geocoding(origen, key)
    dest = geocoding(destino, key)

    if orig[0] != 200 or dest[0] != 200:
        print("No se pudieron obtener las coordenadas para calcular la ruta.")
        return

    op = f"&point={orig[1]},{orig[2]}"
    dp = f"&point={dest[1]},{dest[2]}"
    vehicle_param = f"&vehicle={vehicle}"
    paths_url = route_url + urllib.parse.urlencode({"key": key}) + op + dp + vehicle_param
    response = requests.get(paths_url)
    paths_status = response.status_code
    paths_data = response.json()

    if paths_status == 200 and "paths" in paths_data and len(paths_data["paths"]) > 0:
        return paths_data
    else:
        print(f"No se encontraron rutas válidas entre {orig[3]} y {dest[3]}.")
        return None

def seleccionar_medio_transporte():
    while True:
        print("\nSeleccione el medio de transporte:")
        print("1. Automóvil")
        print("2. Bicicleta")
        print("3. A pie")
        choice = input("Ingrese el número correspondiente (1/2/3): ")

        if choice == "1":
            return "car"
        elif choice == "2":
            return "bike"
        elif choice == "3":
            return "foot"
        else:
            print("Opción no válida. Por favor, elija 1, 2 o 3.")

def convertir_duracion(segundos):
    minutos = segundos // 60000
    horas = minutos // 60
    minutos_restantes = minutos % 60
    return horas, minutos_restantes

def metros_a_km_mi(metros):
    km = metros / 1000
    millas = metros / 1609.34
    return km, millas

# Bucle principal
while True:
    print("\n=====================================")
    loc1 = input("Ciudad de origen (o 's' para salir): ")
    if loc1.lower() == "s":
        break

    loc2 = input("Ciudad de destino (o 's' para salir): ")
    if loc2.lower() == "s":
        break

    vehicle = seleccionar_medio_transporte()
    paths_data = obtener_ruta(loc1, loc2, key, vehicle)

    if paths_data:
        path = paths_data["paths"][0]
        distancia_metros = path["distance"]
        duracion_ms = path["time"]
        instrucciones = path["instructions"]

        km, millas = metros_a_km_mi(distancia_metros)
        horas, minutos = convertir_duracion(duracion_ms)

        print("\n=================================================")
        print(f"Ruta desde {loc1} hasta {loc2}")
        print("=================================================")
        print(f"Distancia: {km:.2f} km / {millas:.2f} millas")
        print(f"Duración estimada: {horas}h {minutos}min")
        print("-------------------------------------------------")
        print("Narrativa del viaje:")
        for paso in instrucciones:
            print(f" - {paso['text']} ({paso['distance']:.1f} m)")
        print("=================================================\n")
