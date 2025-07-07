def verificar_vlan(vlan):
    if 1 <= vlan <= 1005:
        return "VLAN estándar (normal)"
    elif 1006 <= vlan <= 4094:
        return "VLAN extendida"
    else:
        return "VLAN fuera de rango válido"

if __name__ == "__main__":
    try:
        numero_vlan = int(input("Ingrese el número de VLAN: "))
        resultado = verificar_vlan(numero_vlan)
        print("Resultado:", resultado)
    except ValueError:
        print("Por favor ingrese un número válido.")
