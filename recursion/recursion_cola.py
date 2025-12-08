"""
Tail Recursion - Library Management System

This module implements Tail Recursion to calculate the average weight of
all books by a specific author. This is an optimized recursive approach
where calculations are performed BEFORE the recursive call using accumulators.

PROJECT REQUIREMENT:
    Implement a recursive function that calculates the average weight of books
    by a specific author, demonstrating tail recursion logic in console.

Tail Recursion Explanation:
    In tail recursion, the recursive call is the LAST operation in the function.
    All calculations are done BEFORE making the recursive call, using accumulator
    parameters to carry intermediate results forward.
    
    Key characteristics:
    - Accumulator parameters carry running totals
    - No operations after the recursive call
    - The recursive call is in "tail position" (last operation)
    - Can be optimized to iterative code by compilers (not in Python)
    
    Example flow:
        calcular(lista, suma=0, count=0) 
        → calcular(lista[1:], suma=2.5, count=1)
        → calcular(lista[2:], suma=5.0, count=2)
        → calcular(lista[3:], suma=7.8, count=3)
        → BASE CASE: return suma/count = 7.8/3 = 2.6
    
    Notice: Each call has the updated accumulator values, and returns
    directly without further calculations.

Time Complexity: O(n) - must check every book
Space Complexity: O(n) - recursion depth (could be O(1) with optimization)

Author: [Your Name]
Date: December 2025
"""


def calcular_peso_promedio_por_autor(lista_libros, autor, mostrar_proceso=False):
    """
    Calculate the average weight of all books by a specific author.
    
    This is the MAIN function for the Tail Recursion requirement.
    It uses tail recursion with accumulators to calculate the average
    weight, demonstrating the logic in console if requested.
    
    PROJECT REQUIREMENT:
        Calculate average weight using tail recursion, show logic in console.
    
    Args:
        lista_libros (list): List of book objects or dictionaries
        autor (str): Author name to search for (case-insensitive partial match)
        mostrar_proceso (bool, optional): Show tail recursion steps. Defaults to False.
        
    Returns:
        float: Average weight in kg of books by the author (0 if no books found)
        
    Example:
        >>> promedio = calcular_peso_promedio_por_autor(inventario, "García Márquez", True)
        >>> print(f"Average weight: {promedio:.2f} kg")
    """
    # Normalize author name for comparison
    autor_busqueda = autor.strip().lower()
    
    # Call the tail recursive function with accumulators
    # suma_pesos: accumulator for total weight
    # contador: accumulator for number of books
    if mostrar_proceso:
        print("=== Tail Recursion - Average Weight Calculation ===")
        print(f"Author: '{autor}'")
        print(f"Total books to process: {len(lista_libros)}")
        print("\nStarting tail recursion with accumulators:")
        print("  suma_pesos = 0.0 (initial)")
        print("  contador = 0 (initial)")
        print()
    
    suma_total, contador_total = calcular_peso_recursivo_cola(
        lista_libros, 
        autor_busqueda, 
        0,  # indice inicial
        0.0,  # suma_pesos inicial
        0,  # contador inicial
        mostrar_proceso
    )
    
    if mostrar_proceso:
        print("=== Tail Recursion Complete ===")
        print(f"Final accumulated weight: {suma_total:.2f} kg")
        print(f"Final accumulated count: {contador_total}")
    
    # Calculate and return average
    if contador_total == 0:
        if mostrar_proceso:
            print("No books found for this author")
            print("Average: 0.0 kg")
        return 0.0
    
    promedio = suma_total / contador_total
    
    if mostrar_proceso:
        print(f"Average: {suma_total:.2f} / {contador_total} = {promedio:.2f} kg")
        print()
    
    return promedio


def calcular_peso_recursivo_cola(lista_libros, autor_busqueda, indice, 
                                 suma_pesos, contador, mostrar_proceso=False):
    """
    Tail recursive function to calculate total weight and count.
    
    This function demonstrates TAIL RECURSION where:
    1. All calculations are done BEFORE the recursive call
    2. Accumulators (suma_pesos, contador) carry intermediate results
    3. The recursive call is the LAST operation (tail position)
    4. No operations occur after the recursive call returns
    
    The key characteristic is that we pass updated accumulator values
    to the next call, and simply return whatever that call returns.
    
    Args:
        lista_libros (list): List of books
        autor_busqueda (str): Normalized author name to search for
        indice (int): Current position in the list
        suma_pesos (float): Accumulator for total weight
        contador (int): Accumulator for number of books
        mostrar_proceso (bool): Whether to print steps
        
    Returns:
        tuple: (suma_total, contador_total) - accumulated values
    """
    # BASE CASE: Reached end of list
    if indice >= len(lista_libros):
        if mostrar_proceso:
            print(f"[BASE CASE] Reached end of list")
            print(f"[BASE CASE] Final accumulators: suma={suma_pesos:.2f}, count={contador}")
            print(f"[BASE CASE] Returning: ({suma_pesos:.2f}, {contador})")
            print()
        return (suma_pesos, contador)
    
    # Get current book
    libro_actual = lista_libros[indice]
    
    # Extract author and weight from current book
    if isinstance(libro_actual, dict):
        autor_libro = str(libro_actual.get('autor', '')).strip().lower()
        peso_libro = float(libro_actual.get('peso', 0))
        isbn = libro_actual.get('isbn', 'N/A')[:15]
    else:
        autor_libro = str(getattr(libro_actual, 'autor', '')).strip().lower()
        peso_libro = float(getattr(libro_actual, 'peso', 0))
        isbn = getattr(libro_actual, 'isbn', 'N/A')[:15]
    
    # TAIL RECURSION: Update accumulators BEFORE recursive call
    if autor_busqueda in autor_libro:
        # Book matches - update both accumulators
        nueva_suma = suma_pesos + peso_libro
        nuevo_contador = contador + 1
        
        if mostrar_proceso:
            print(f"[Step {indice}] Book: {isbn}...")
            print(f"[Step {indice}] Author matches! Weight: {peso_libro:.2f} kg")
            print(f"[Step {indice}] BEFORE call: suma={suma_pesos:.2f}, count={contador}")
            print(f"[Step {indice}] UPDATING accumulators:")
            print(f"[Step {indice}]   suma_pesos: {suma_pesos:.2f} + {peso_libro:.2f} = {nueva_suma:.2f}")
            print(f"[Step {indice}]   contador: {contador} + 1 = {nuevo_contador}")
            print(f"[Step {indice}] Making TAIL CALL with updated accumulators")
            print()
        
        # TAIL CALL: Recursive call is the LAST operation
        # We return DIRECTLY what the recursive call returns (no further operations)
        return calcular_peso_recursivo_cola(
            lista_libros, 
            autor_busqueda, 
            indice + 1,
            nueva_suma,  # Updated accumulator
            nuevo_contador,  # Updated accumulator
            mostrar_proceso
        )
    else:
        # Book doesn't match - keep accumulators unchanged
        if mostrar_proceso:
            print(f"[Step {indice}] Book: {isbn}...")
            print(f"[Step {indice}] Author doesn't match, skipping")
            print(f"[Step {indice}] Accumulators unchanged: suma={suma_pesos:.2f}, count={contador}")
            print(f"[Step {indice}] Making TAIL CALL with same accumulators")
            print()
        
        # TAIL CALL: Pass unchanged accumulators
        return calcular_peso_recursivo_cola(
            lista_libros, 
            autor_busqueda, 
            indice + 1,
            suma_pesos,  # Unchanged accumulator
            contador,  # Unchanged accumulator
            mostrar_proceso
        )


def calcular_peso_recursivo_cola_alternativo(lista_libros, autor_busqueda, 
                                             suma_pesos=0.0, contador=0):
    """
    Alternative tail recursion using list slicing.
    
    This version processes the first element and recurses on the rest,
    demonstrating tail recursion with a different approach.
    
    Args:
        lista_libros (list): List of books
        autor_busqueda (str): Author name to search for
        suma_pesos (float, optional): Accumulator for weight. Defaults to 0.0.
        contador (int, optional): Accumulator for count. Defaults to 0.
        
    Returns:
        tuple: (suma_total, contador_total)
    """
    # BASE CASE: Empty list
    if not lista_libros:
        return (suma_pesos, contador)
    
    # Get first book
    primer_libro = lista_libros[0]
    
    # Extract author and weight
    if isinstance(primer_libro, dict):
        autor_libro = str(primer_libro.get('autor', '')).strip().lower()
        peso_libro = float(primer_libro.get('peso', 0))
    else:
        autor_libro = str(getattr(primer_libro, 'autor', '')).strip().lower()
        peso_libro = float(getattr(primer_libro, 'peso', 0))
    
    # Update accumulators BEFORE recursive call
    if autor_busqueda in autor_libro:
        nueva_suma = suma_pesos + peso_libro
        nuevo_contador = contador + 1
    else:
        nueva_suma = suma_pesos
        nuevo_contador = contador
    
    # TAIL CALL: Recursive call is the last operation
    return calcular_peso_recursivo_cola_alternativo(
        lista_libros[1:],  # Rest of the list
        autor_busqueda,
        nueva_suma,
        nuevo_contador
    )


def calcular_suma_pesos_por_autor(lista_libros, autor, indice=0, suma=0.0):
    """
    Calculate total weight using tail recursion (without count).
    
    This simpler function demonstrates tail recursion with a single accumulator.
    
    Args:
        lista_libros (list): List of books
        autor (str): Author to search for
        indice (int, optional): Current index. Defaults to 0.
        suma (float, optional): Accumulator for weight. Defaults to 0.0.
        
    Returns:
        float: Total weight of books by the author
    """
    # BASE CASE
    if indice >= len(lista_libros):
        return suma
    
    # Get current book
    libro = lista_libros[indice]
    autor_busqueda = autor.strip().lower()
    
    if isinstance(libro, dict):
        autor_libro = str(libro.get('autor', '')).strip().lower()
        peso = float(libro.get('peso', 0))
    else:
        autor_libro = str(getattr(libro, 'autor', '')).strip().lower()
        peso = float(getattr(libro, 'peso', 0))
    
    # Update accumulator and make TAIL CALL
    if autor_busqueda in autor_libro:
        return calcular_suma_pesos_por_autor(lista_libros, autor, indice + 1, suma + peso)
    else:
        return calcular_suma_pesos_por_autor(lista_libros, autor, indice + 1, suma)


def demostrar_recursion_cola(lista_libros, autor):
    """
    Comprehensive demonstration of tail recursion logic.
    
    This function provides a detailed walkthrough of tail recursion,
    showing how accumulators work and why the recursive call is in
    tail position (no operations after it).
    
    Args:
        lista_libros (list): List of books (recommend small list for demo)
        autor (str): Author to calculate average weight for
        
    Returns:
        float: Average weight calculated
        
    Note:
        This function prints detailed output for educational purposes.
        Use a small list (5-10 books) for clearer demonstration.
    """
    print("=" * 80)
    print("TAIL RECURSION DEMONSTRATION - Average Weight Calculation")
    print("=" * 80)
    print()
    print("CONCEPT:")
    print("  Tail recursion performs calculations BEFORE the recursive call.")
    print("  Accumulators carry intermediate results forward.")
    print("  The recursive call is the LAST operation (tail position).")
    print("  No calculations occur AFTER the recursive call returns.")
    print()
    print("-" * 80)
    print()
    
    # Calculate with detailed output
    promedio = calcular_peso_promedio_por_autor(lista_libros, autor, mostrar_proceso=True)
    
    print("-" * 80)
    print()
    print("KEY OBSERVATIONS:")
    print("  1. Accumulators (suma_pesos, contador) are updated BEFORE each call")
    print("  2. The recursive call is the LAST line (tail position)")
    print("  3. We return DIRECTLY what the recursive call returns")
    print("  4. No operations happen AFTER the recursive call")
    print()
    print("COMPARISON WITH STACK RECURSION:")
    print("  Stack Recursion: value = current_value + recursive_call()")
    print("                   ↑ Operation AFTER recursive call")
    print()
    print("  Tail Recursion:  return recursive_call(accumulated_value)")
    print("                   ↑ No operation after, just return directly")
    print()
    print("=" * 80)
    
    return promedio


def comparar_recursiones(lista_libros, autor):
    """
    Compare stack recursion vs tail recursion side by side.
    
    This function demonstrates the difference between the two approaches
    by showing their execution patterns.
    
    Args:
        lista_libros (list): List of books
        autor (str): Author to analyze
        
    Returns:
        dict: Comparison results
    """
    from recursion.recursion_pila import calcular_valor_total_por_autor
    
    print("=" * 80)
    print("COMPARISON: Stack Recursion vs Tail Recursion")
    print("=" * 80)
    print()
    
    print("1. STACK RECURSION (Value Calculation):")
    print("   - Operations AFTER recursive call")
    print("   - Results combined during unwinding")
    print()
    valor_total = calcular_valor_total_por_autor(lista_libros, autor)
    print(f"   Result: ${valor_total:,.0f} COP")
    print()
    
    print("-" * 80)
    print()
    
    print("2. TAIL RECURSION (Weight Average):")
    print("   - Operations BEFORE recursive call")
    print("   - Accumulators carry results forward")
    print()
    peso_promedio = calcular_peso_promedio_por_autor(lista_libros, autor, mostrar_proceso=False)
    print(f"   Result: {peso_promedio:.2f} kg")
    print()
    
    print("=" * 80)
    
    return {
        'valor_total': valor_total,
        'peso_promedio': peso_promedio,
        'autor': autor
    }


def calcular_estadisticas_completas(lista_libros, autor):
    """
    Calculate comprehensive statistics using tail recursion.
    
    Args:
        lista_libros (list): List of books
        autor (str): Author to analyze
        
    Returns:
        dict: Complete statistics
    """
    # Calculate average weight (tail recursion)
    peso_promedio = calcular_peso_promedio_por_autor(lista_libros, autor)
    
    # Calculate total weight (tail recursion with single accumulator)
    peso_total = calcular_suma_pesos_por_autor(lista_libros, autor)
    
    # Calculate count from the recursive function
    suma, contador = calcular_peso_recursivo_cola(
        lista_libros,
        autor.strip().lower(),
        0,
        0.0,
        0,
        False
    )
    
    return {
        'autor': autor,
        'peso_total': peso_total,
        'peso_promedio': peso_promedio,
        'cantidad_libros': contador,
        'peso_maximo': peso_total if contador > 0 else 0,
        'peso_minimo': peso_promedio if contador > 0 else 0
    }