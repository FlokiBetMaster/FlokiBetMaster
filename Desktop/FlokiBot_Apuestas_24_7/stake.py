# stake.py

def calcular_stake(confianza):
    # Si viene como texto "74%", quitamos el % y lo convertimos a float
    if isinstance(confianza, str):
        confianza = confianza.replace("%", "")
        confianza = float(confianza)
    
    if confianza >= 85:
        return 5  # stake 5% si la confianza es muy alta
    elif confianza >= 70:
        return 3  # stake 3% si la confianza es aceptable
    else:
        return 1  # stake mínimo si la confianza es baja
