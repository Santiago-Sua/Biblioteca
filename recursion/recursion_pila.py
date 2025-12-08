"""
Stack Recursion - Library Management System

This module implements Stack Recursion to calculate the total value (COP)
of all books by a specific author. This is a traditional recursive approach
where calculations are performed during the return phase of the recursion.

PROJECT REQUIREMENT:
    Implement a recursive function that calculates the total value of all
    books by a specific author. The function must NOT use loops.

Stack Recursion Explanation:
    In stack recursion, the function makes a recursive call and then performs
    operations with the result of that call. The calculation happens during
    the "unwinding" phase as the call stack collapses.
    
    Example flow:
        calcular(lista[0:5]) calls calcular(lista[1:5])
        calcular(lista[1:5]) calls calcular(lista[2:5])
        ...
        calcular(lista[4:5]) calls calcular(lista[5:5]) -> base case returns 0
        Then each call adds its value and returns up the stack
    
    The stack grows with each call, and results are combined as we return.

Time Complexity: O(n) - must check every book
Space Complexity: O(n) - recursion call stack depth

Author: [Your Name]
Date: December 2025
"""


def calcular_valor_total_por_autor(lista_libros, autor):
    """
    Calculate the total value (COP) of all books by a specific author.
    
    This is the MAIN function for the Stack Recursion requirement.
    It uses recursive calls (NO LOOPS) to sum the values of all books
    matching the specified author.
    
    PROJECT REQUIREMENT:
        Calculate total value of books by an author using recursion.
    
    Args:
        lista_libros (list): List of book objects or dictionaries
        autor (str): Author name to search for (case-insensitive partial match)
        
    Returns:
        float: Total value in COP of all books by the author
        
    Example:
        >>> total = calcular_valor_total_por_autor(inventario, "García Márquez")
        >>> print(f"Total value: ${total:,.0f} COP")
    """
    # Normalize author name for comparison
    autor_busqueda = autor.strip().lower()
    
    # Call the recursive helper function
    return calcular_valor_recursivo(lista_libros, autor_busqueda, 0)


def calcular_valor_recursivo(lista_libros, autor_busqueda, indice):
    """
    Recursive helper function to calculate total value.
    
    This function demonstrates STACK RECURSION where:
    1. Base case: When we've processed all books, return 0
    2. Recursive case: Check current book, then recurse on remaining books
    3. Calculation: Add current book's value (if matches) to the result
                   from the recursive call
    
    The key characteristic of stack recursion is that the operation
    (addition) happens AFTER the recursive call returns.
    
    Args:
        lista_libros (list): List of books
        autor_busqueda (str): Normalized author name to search for
        indice (int): Current position in the list
        
    Returns:
        float: Total value from current position to end of list
    """
    # BASE CASE: Reached end of list
    if indice >= len(lista_libros):
        return 0
    
    # Get current book
    libro_actual = lista_libros[indice]
    
    # Extract author and value from current book
    if isinstance(libro_actual, dict):
        autor_libro = str(libro_actual.get('autor', '')).strip().lower()
        valor_libro = float(libro_actual.get('valor', 0))
    else:
        autor_libro = str(getattr(libro_actual, 'autor', '')).strip().lower()
        valor_libro = float(getattr(libro_actual, 'valor', 0))
    
    # RECURSIVE CASE: Calculate value for the rest of the list
    # This is the recursive call that builds the stack
    valor_resto = calcular_valor_recursivo(lista_libros, autor_busqueda, indice + 1)
    
    # STACK OPERATION: Check if current book matches, add its value
    # This happens AFTER the recursive call (during stack unwinding)
    if autor_busqueda in autor_libro:
        return valor_libro + valor_resto
    else:
        return valor_resto


def calcular_valor_recursivo_alternativo(lista_libros, autor_busqueda):
    """
    Alternative stack recursion using list slicing.
    
    This version demonstrates stack recursion using a different approach:
    processing the first element and recursing on the rest of the list.
    
    Args:
        lista_libros (list): List of books
        autor_busqueda (str): Author name to search for
        
    Returns:
        float: Total value of books by the author
    """
    # BASE CASE: Empty list
    if not lista_libros:
        return 0
    
    # Get first book
    primer_libro = lista_libros[0]
    
    # Extract author and value
    if isinstance(primer_libro, dict):
        autor_libro = str(primer_libro.get('autor', '')).strip().lower()
        valor_libro = float(primer_libro.get('valor', 0))
    else:
        autor_libro = str(getattr(primer_libro, 'autor', '')).strip().lower()
        valor_libro = float(getattr(primer_libro, 'valor', 0))
    
    # RECURSIVE CALL on the rest of the list (lista_libros[1:])
    valor_resto = calcular_valor_recursivo_alternativo(lista_libros[1:], autor_busqueda)
    
    # Check if current book matches and add to result
    if autor_busqueda in autor_libro:
        return valor_libro + valor_resto
    else:
        return valor_resto


def contar_libros_por_autor_recursivo(lista_libros, autor, indice=0):
    """
    Count books by an author using stack recursion.
    
    This auxiliary function demonstrates another use of stack recursion:
    counting instead of summing.
    
    Args:
        lista_libros (list): List of books
        autor (str): Author to search for
        indice (int, optional): Current index. Defaults to 0.
        
    Returns:
        int: Number of books by the author
    """
    # BASE CASE
    if indice >= len(lista_libros):
        return 0
    
    # Get current book's author
    libro_actual = lista_libros[indice]
    if isinstance(libro_actual, dict):
        autor_libro = str(libro_actual.get('autor', '')).strip().lower()
    else:
        autor_libro = str(getattr(libro_actual, 'autor', '')).strip().lower()
    
    # RECURSIVE CALL
    contador_resto = contar_libros_por_autor_recursivo(lista_libros, autor, indice + 1)
    
    # STACK OPERATION: Add 1 if matches
    autor_busqueda = autor.strip().lower()
    if autor_busqueda in autor_libro:
        return 1 + contador_resto
    else:
        return contador_resto


def obtener_libros_por_autor_recursivo(lista_libros, autor, indice=0):
    """
    Get all books by an author using stack recursion.
    
    This function returns a list of books instead of a numeric value,
    demonstrating how stack recursion can build complex results.
    
    Args:
        lista_libros (list): List of books
        autor (str): Author to search for
        indice (int, optional): Current index. Defaults to 0.
        
    Returns:
        list: List of books by the specified author
    """
    # BASE CASE
    if indice >= len(lista_libros):
        return []
    
    # Get current book
    libro_actual = lista_libros[indice]
    if isinstance(libro_actual, dict):
        autor_libro = str(libro_actual.get('autor', '')).strip().lower()
    else:
        autor_libro = str(getattr(libro_actual, 'autor', '')).strip().lower()
    
    # RECURSIVE CALL
    libros_resto = obtener_libros_por_autor_recursivo(lista_libros, autor, indice + 1)
    
    # STACK OPERATION: Add current book to list if matches
    autor_busqueda = autor.strip().lower()
    if autor_busqueda in autor_libro:
        return [libro_actual] + libros_resto
    else:
        return libros_resto


def demostrar_recursion_pila(lista_libros, autor, max_profundidad=10):
    """
    Demonstrate stack recursion with detailed console output.
    
    This function shows how the recursion stack builds up and then
    unwinds, performing calculations during the unwinding phase.
    
    Args:
        lista_libros (list): List of books (recommend small list for demo)
        autor (str): Author to calculate total value for
        max_profundidad (int, optional): Max depth to show. Defaults to 10.
        
    Returns:
        float: Total value calculated
        
    Note:
        This function prints to console for educational purposes.
        Use a small list (5-10 books) for clearer demonstration.
    """
    print("=== Stack Recursion Demonstration ===")
    print(f"Calculating total value for author: '{autor}'")
    print(f"Total books to process: {len(lista_libros)}")
    print()
    
    autor_busqueda = autor.strip().lower()
    
    def _recursivo_demo(indice, nivel):
        indent = "  " * nivel
        
        # BASE CASE
        if indice >= len(lista_libros):
            if nivel < max_profundidad:
                print(f"{indent}[Level {nivel}] BASE CASE: No more books")
                print(f"{indent}[Level {nivel}] Returning: 0")
            return 0
        
        # Get current book
        libro = lista_libros[indice]
        if isinstance(libro, dict):
            autor_libro = str(libro.get('autor', '')).strip().lower()
            valor_libro = float(libro.get('valor', 0))
            isbn = libro.get('isbn', 'N/A')[:15]
        else:
            autor_libro = str(getattr(libro, 'autor', '')).strip().lower()
            valor_libro = float(getattr(libro, 'valor', 0))
            isbn = getattr(libro, 'isbn', 'N/A')[:15]
        
        if nivel < max_profundidad:
            print(f"{indent}[Level {nivel}] Processing book {indice}")
            print(f"{indent}[Level {nivel}] ISBN: {isbn}...")
            print(f"{indent}[Level {nivel}] Author: {autor_libro[:30]}...")
            print(f"{indent}[Level {nivel}] Value: ${valor_libro:,.0f}")
            
            if autor_busqueda in autor_libro:
                print(f"{indent}[Level {nivel}] ✓ MATCH! Will add this value")
            else:
                print(f"{indent}[Level {nivel}] ✗ No match, skipping")
            
            print(f"{indent}[Level {nivel}] → Making recursive call for book {indice + 1}")
            print()
        
        # RECURSIVE CALL (stack grows here)
        valor_resto = _recursivo_demo(indice + 1, nivel + 1)
        
        # CALCULATION DURING UNWINDING
        if autor_busqueda in autor_libro:
            resultado = valor_libro + valor_resto
            if nivel < max_profundidad:
                print(f"{indent}[Level {nivel}] ← Returning from recursion")
                print(f"{indent}[Level {nivel}] Current book value: ${valor_libro:,.0f}")
                print(f"{indent}[Level {nivel}] Rest of list value: ${valor_resto:,.0f}")
                print(f"{indent}[Level {nivel}] Total: ${resultado:,.0f}")
                print()
        else:
            resultado = valor_resto
            if nivel < max_profundidad:
                print(f"{indent}[Level {nivel}] ← Returning from recursion")
                print(f"{indent}[Level {nivel}] Passing through: ${resultado:,.0f}")
                print()
        
        return resultado
    
    total = _recursivo_demo(0, 0)
    
    print("=== Recursion Complete ===")
    print(f"Final Result: ${total:,.0f} COP")
    print()
    
    # Show number of books by author
    cantidad = contar_libros_por_autor_recursivo(lista_libros, autor)
    print(f"Books by '{autor}': {cantidad}")
    if cantidad > 0:
        print(f"Average value per book: ${total/cantidad:,.0f} COP")
    
    return total


def calcular_estadisticas_por_autor(lista_libros, autor):
    """
    Calculate comprehensive statistics for an author using recursion.
    
    This function demonstrates multiple recursive calculations working together.
    
    Args:
        lista_libros (list): List of books
        autor (str): Author to analyze
        
    Returns:
        dict: Statistics including total value, count, and book list
    """
    return {
        'autor': autor,
        'valor_total': calcular_valor_total_por_autor(lista_libros, autor),
        'cantidad_libros': contar_libros_por_autor_recursivo(lista_libros, autor),
        'libros': obtener_libros_por_autor_recursivo(lista_libros, autor)
    }