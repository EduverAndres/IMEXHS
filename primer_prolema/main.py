# Función principal para resolver el problema con validación de colores
def hanoi_colores(n, discos):
    """
    Resuelve el problema de mover discos en la Torre de Hanoi con restricciones adicionales:
    discos del mismo color no pueden apilarse y un disco grande no puede colocarse sobre uno pequeño.

    Args:
        n (int): Número de discos (1 ≤ n ≤ 8).
        discos (list): Lista de tuplas (tamaño, color), donde cada disco está ordenado de mayor a menor tamaño.

    Returns:
        list: La secuencia de movimientos como [(tamaño, origen, destino)].
        int: Retorna -1 si no se puede resolver por violar las reglas.
    """
    # Validación inicial: verificar si hay discos consecutivos con el mismo color
    for i in range(1, n):
        if discos[i][1] == discos[i - 1][1]:  # Si dos discos consecutivos tienen el mismo color
            return -1  # No se puede resolver desde el inicio

    # Lista para almacenar la secuencia de movimientos
    movimientos = []

    # Estado inicial de las varillas: A (origen) tiene todos los discos, B y C están vacías
    estado_varillas = {"A": discos[:], "B": [], "C": []}

    # Función recursiva principal para mover los discos
    def mover_discos(num_discos, origen, auxiliar, destino):
        """
        Lógica recursiva para trasladar `num_discos` entre varillas, respetando las reglas del problema.

        Args:
            num_discos (int): Número de discos a mover.
            origen (str): Varilla de donde se mueven los discos.
            auxiliar (str): Varilla auxiliar para la transición.
            destino (str): Varilla final a la que se llevan los discos.
        """
        if num_discos == 0:
            return  # Caso base: si no hay discos que mover, terminamos aquí

        # Paso 1: Mueve los primeros n-1 discos a la varilla auxiliar
        mover_discos(num_discos - 1, origen, destino, auxiliar)

        # Paso 2: Mueve el disco más grande al destino
        disco_a_mover = estado_varillas[origen].pop()  # Retiramos el disco superior de la varilla origen

        # Antes de colocarlo en el destino, verificamos las reglas
        if estado_varillas[destino]:  # Si la varilla destino no está vacía
            disco_superior_destino = estado_varillas[destino][-1]  # Tomamos el disco en la cima del destino
            # Regla de tamaño: el disco movido debe ser más pequeño que el disco en el destino
            if disco_a_mover[0] > disco_superior_destino[0]:
                raise ValueError("Movimiento inválido: un disco grande no puede ir sobre uno más pequeño.")
            # Regla de color: los discos del mismo color no pueden apilarse
            if disco_a_mover[1] == disco_superior_destino[1]:
                raise ValueError("Movimiento inválido: discos del mismo color no pueden apilarse.")

        # Si pasa las validaciones, registramos el movimiento
        movimientos.append((disco_a_mover[0], origen, destino))  # Añadimos a la lista de movimientos
        estado_varillas[destino].append(disco_a_mover)  # Colocamos el disco en el destino

        # Paso 3: Mueve los n-1 discos de la varilla auxiliar al destino
        mover_discos(num_discos - 1, auxiliar, origen, destino)

    try:
        # Inicia la recursión para mover todos los discos de "A" a "C"
        mover_discos(n, "A", "B", "C")
    except ValueError:
        # Si en algún momento violamos una regla, devolvemos -1
        return -1

    return movimientos  # Al final devolvemos la secuencia completa de movimientos


# Aquí empieza el uso real de la función, con un ejemplo
n = 3  # Número de discos
discos = [(3, "rojo"), (2, "azul"), (1, "rojo")]  # Discos con tamaño y color

# Llamamos a la función principal y evaluamos el resultado
resultado = hanoi_colores(n, discos)
if resultado == -1:
    # Si el resultado es -1, significa que no se pudo resolver el problema
    print(resultado)
else:
    # Si obtenemos una lista de movimientos, los imprimimos
    for movimiento in resultado:
        print(movimiento)
