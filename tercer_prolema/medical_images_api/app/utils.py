def normalize_data(data: list):
    """
    Normaliza los valores de una lista de datos y calcula el promedio antes y después de la normalización.

    Args:
        data (list): Lista de listas que contiene números. Ejemplo:
                     [
                        [78, 83, 21],
                        [68, 96, 46],
                        [40, 11, 1]
                     ]

    Returns:
        tuple: (avg_before, avg_after, data_size)
            - avg_before (float): Promedio de los valores antes de la normalización.
            - avg_after (float): Promedio de los valores después de la normalización.
            - data_size (int): Tamaño total de los datos (cantidad de números).
    """
    # "Aplanamos" los datos: convertimos una lista de listas en una sola lista.
    # Ejemplo: [[1, 2], [3, 4]] se convierte en [1, 2, 3, 4].
    flat_data = [num for sublist in data for num in sublist]

    # Encontramos el valor máximo en la lista aplanada. Esto se usa para la normalización.
    max_value = max(flat_data)

    # Normalizamos los datos dividiendo cada número por el valor máximo.
    normalized = [num / max_value for num in flat_data]

    # Calculamos el promedio antes de la normalización.
    avg_before = sum(flat_data) / len(flat_data)

    # Calculamos el promedio después de la normalización.
    avg_after = sum(normalized) / len(normalized)

    # Devolvemos el promedio antes, el promedio después, y el tamaño total de los datos.
    return avg_before, avg_after, len(flat_data)
