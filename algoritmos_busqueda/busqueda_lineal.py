"""
Linear Search Algorithm - Library Management System

This module implements the Linear Search algorithm used to search for books
by Title or Author in the General Inventory (unsorted list). This algorithm
sequentially checks each element until a match is found or all elements
have been examined.

The Linear Search is appropriate for this use case because:
1. The General Inventory is unsorted (maintains load order)
2. We need to find ALL matches (not just one)
3. Search criteria (title/author) don't have a defined order
4. Simple and reliable for small to medium datasets

Algorithm Explanation:
    The algorithm iterates through each element in the list, comparing the
    search criterion with each element's attribute. All matches are collected
    and returned. This ensures no results are missed.

Time Complexity: O(n) - must potentially check every element
Space Complexity: O(k) - where k is the number of matches found

Author: [Your Name]
Date: December 2025
"""


def busqueda_lineal(lista_libros, clave, valor, coincidencia_exacta=False):
    """
    Perform a linear search on a list of books by a specified attribute.
    
    This is the main linear search function that can search by any attribute
    and supports both exact and partial matching.
    
    Args:
        lista_libros (list): List of book objects or dictionaries to search
        clave (str): Attribute/key to search by (e.g., 'titulo', 'autor')
        valor (str): Value to search for
        coincidencia_exacta (bool, optional): If True, requires exact match.
                                             If False, allows partial match.
                                             Defaults to False.
    
    Returns:
        list: List of all matching books (empty list if no matches)
        
    Example:
        >>> resultados = busqueda_lineal(inventario, 'autor', 'García', False)
        >>> # Returns all books where author contains 'García'
    """
    resultados = []
    
    # Normalize search value for comparison (case-insensitive)
    valor_busqueda = str(valor).strip().lower()
    
    # Iterate through each book in the list
    for libro in lista_libros:
        # Get the attribute value from the book
        if isinstance(libro, dict):
            valor_libro = str(libro.get(clave, ""))
        else:
            valor_libro = str(getattr(libro, clave, ""))
        
        # Normalize book value for comparison
        valor_libro = valor_libro.strip().lower()
        
        # Check if there's a match
        if coincidencia_exacta:
            # Exact match required
            if valor_libro == valor_busqueda:
                resultados.append(libro)
        else:
            # Partial match allowed (substring search)
            if valor_busqueda in valor_libro:
                resultados.append(libro)
    
    return resultados


def buscar_por_titulo(lista_libros, titulo, coincidencia_exacta=False):
    """
    Search for books by title in the General Inventory.
    
    This is a specialized function for searching by title, which is one of
    the main requirements of the project (search by Title or Author on the
    unsorted General Inventory).
    
    Args:
        lista_libros (list): List of books to search (General Inventory)
        titulo (str): Title or partial title to search for
        coincidencia_exacta (bool, optional): Require exact match. Defaults to False.
        
    Returns:
        list: All books matching the title criteria
        
    Example:
        >>> libros = buscar_por_titulo(inventario_general, "Cien Años")
        >>> # Returns books with "Cien Años" in the title
    """
    return busqueda_lineal(lista_libros, 'titulo', titulo, coincidencia_exacta)


def buscar_por_autor(lista_libros, autor, coincidencia_exacta=False):
    """
    Search for books by author in the General Inventory.
    
    This is a specialized function for searching by author, which is one of
    the main requirements of the project (search by Title or Author on the
    unsorted General Inventory).
    
    Args:
        lista_libros (list): List of books to search (General Inventory)
        autor (str): Author name or partial name to search for
        coincidencia_exacta (bool, optional): Require exact match. Defaults to False.
        
    Returns:
        list: All books matching the author criteria
        
    Example:
        >>> libros = buscar_por_autor(inventario_general, "García Márquez")
        >>> # Returns all books by authors matching "García Márquez"
    """
    return busqueda_lineal(lista_libros, 'autor', autor, coincidencia_exacta)


def buscar_por_atributo(lista_libros, **criterios):
    """
    Search for books matching multiple criteria using linear search.
    
    This function allows searching by multiple attributes simultaneously.
    All criteria must match for a book to be included in results.
    
    Args:
        lista_libros (list): List of books to search
        **criterios: Keyword arguments where key is attribute name and
                    value is the search value
    
    Returns:
        list: Books matching ALL specified criteria
        
    Example:
        >>> libros = buscar_por_atributo(
        ...     inventario,
        ...     autor="García",
        ...     genero="Ficción"
        ... )
        >>> # Returns books matching both author and genre
    """
    resultados = []
    
    for libro in lista_libros:
        coincide = True
        
        # Check each criterion
        for clave, valor_busqueda in criterios.items():
            # Get the attribute value from the book
            if isinstance(libro, dict):
                valor_libro = str(libro.get(clave, ""))
            else:
                valor_libro = str(getattr(libro, clave, ""))
            
            # Normalize for comparison
            valor_libro = valor_libro.strip().lower()
            valor_busqueda_norm = str(valor_busqueda).strip().lower()
            
            # Check if this criterion matches
            if valor_busqueda_norm not in valor_libro:
                coincide = False
                break
        
        # If all criteria match, add to results
        if coincide:
            resultados.append(libro)
    
    return resultados


def buscar_libros_disponibles(lista_libros, clave=None, valor=None):
    """
    Search for available books (stock > 0) with optional additional criteria.
    
    This function is useful for finding books that can be loaned immediately.
    
    Args:
        lista_libros (list): List of books to search
        clave (str, optional): Additional attribute to filter by
        valor (str, optional): Value for additional filter
        
    Returns:
        list: Available books matching criteria
        
    Example:
        >>> disponibles = buscar_libros_disponibles(inventario, 'autor', 'García')
        >>> # Returns available books by García
    """
    resultados = []
    
    for libro in lista_libros:
        # Check if book is available (stock > 0)
        if isinstance(libro, dict):
            stock = libro.get('stock', 0)
        else:
            stock = getattr(libro, 'stock', 0)
        
        if stock <= 0:
            continue
        
        # If no additional criteria, add to results
        if clave is None or valor is None:
            resultados.append(libro)
            continue
        
        # Check additional criteria
        if isinstance(libro, dict):
            valor_libro = str(libro.get(clave, ""))
        else:
            valor_libro = str(getattr(libro, clave, ""))
        
        valor_libro = valor_libro.strip().lower()
        valor_busqueda = str(valor).strip().lower()
        
        if valor_busqueda in valor_libro:
            resultados.append(libro)
    
    return resultados


def contar_libros_por_autor(lista_libros, autor):
    """
    Count how many books by a specific author exist in the inventory.
    
    This function uses linear search to count occurrences.
    
    Args:
        lista_libros (list): List of books to search
        autor (str): Author name to search for
        
    Returns:
        int: Number of books by the specified author
        
    Example:
        >>> cantidad = contar_libros_por_autor(inventario, "García Márquez")
        >>> print(f"Found {cantidad} books by García Márquez")
    """
    libros = buscar_por_autor(lista_libros, autor, coincidencia_exacta=False)
    return len(libros)


def obtener_autores_unicos(lista_libros):
    """
    Get a list of all unique authors in the inventory using linear search.
    
    This function scans the entire list and collects unique author names.
    
    Args:
        lista_libros (list): List of books to analyze
        
    Returns:
        list: Sorted list of unique author names
        
    Example:
        >>> autores = obtener_autores_unicos(inventario)
        >>> print(f"The library has books from {len(autores)} different authors")
    """
    autores = set()
    
    for libro in lista_libros:
        if isinstance(libro, dict):
            autor = libro.get('autor', '').strip()
        else:
            autor = getattr(libro, 'autor', '').strip()
        
        if autor:
            autores.add(autor)
    
    return sorted(list(autores))


def buscar_con_filtros(lista_libros, filtros):
    """
    Advanced search with multiple filters and conditions.
    
    This function supports complex filtering with range queries for
    numeric attributes and pattern matching for strings.
    
    Args:
        lista_libros (list): List of books to search
        filtros (dict): Dictionary of filters where:
                       - For strings: {'autor': 'García'} (substring match)
                       - For ranges: {'peso_min': 0.5, 'peso_max': 2.0}
                       - For exact: {'genero_exact': 'Fiction'}
        
    Returns:
        list: Books matching all filter conditions
        
    Example:
        >>> filtros = {
        ...     'autor': 'García',
        ...     'peso_min': 0.5,
        ...     'peso_max': 2.0,
        ...     'stock_min': 1
        ... }
        >>> resultados = buscar_con_filtros(inventario, filtros)
    """
    resultados = []
    
    for libro in lista_libros:
        cumple_filtros = True
        
        for filtro, valor in filtros.items():
            # Handle range filters (min/max)
            if filtro.endswith('_min'):
                atributo = filtro[:-4]  # Remove '_min' suffix
                if isinstance(libro, dict):
                    valor_libro = libro.get(atributo, 0)
                else:
                    valor_libro = getattr(libro, atributo, 0)
                
                if float(valor_libro) < float(valor):
                    cumple_filtros = False
                    break
                    
            elif filtro.endswith('_max'):
                atributo = filtro[:-4]  # Remove '_max' suffix
                if isinstance(libro, dict):
                    valor_libro = libro.get(atributo, float('inf'))
                else:
                    valor_libro = getattr(libro, atributo, float('inf'))
                
                if float(valor_libro) > float(valor):
                    cumple_filtros = False
                    break
                    
            elif filtro.endswith('_exact'):
                atributo = filtro[:-6]  # Remove '_exact' suffix
                if isinstance(libro, dict):
                    valor_libro = str(libro.get(atributo, "")).strip().lower()
                else:
                    valor_libro = str(getattr(libro, atributo, "")).strip().lower()
                
                if valor_libro != str(valor).strip().lower():
                    cumple_filtros = False
                    break
                    
            else:
                # Standard substring search
                if isinstance(libro, dict):
                    valor_libro = str(libro.get(filtro, "")).strip().lower()
                else:
                    valor_libro = str(getattr(libro, filtro, "")).strip().lower()
                
                if str(valor).strip().lower() not in valor_libro:
                    cumple_filtros = False
                    break
        
        if cumple_filtros:
            resultados.append(libro)
    
    return resultados


def demostrar_busqueda_lineal(lista_libros, clave, valor):
    """
    Demonstrate the linear search process step by step.
    
    This function shows how the algorithm checks each element sequentially.
    
    Args:
        lista_libros (list): List of books to search
        clave (str): Attribute to search by
        valor (str): Value to search for
        
    Note:
        This function prints to console for educational purposes.
    """
    print("=== Linear Search Demonstration ===")
    print(f"Searching for: {clave} = '{valor}'")
    print(f"Total elements to check: {len(lista_libros)}")
    print()
    
    valor_busqueda = str(valor).strip().lower()
    resultados = []
    comparaciones = 0
    
    for idx, libro in enumerate(lista_libros):
        comparaciones += 1
        
        if isinstance(libro, dict):
            valor_libro = str(libro.get(clave, ""))
        else:
            valor_libro = str(getattr(libro, clave, ""))
        
        valor_libro = valor_libro.strip().lower()
        
        print(f"Step {idx + 1}: Checking element at position {idx}")
        print(f"  Value: '{valor_libro}'")
        
        if valor_busqueda in valor_libro:
            print(f"  ✓ MATCH FOUND!")
            resultados.append(libro)
        else:
            print(f"  ✗ No match")
        print()
    
    print("=== Search Complete ===")
    print(f"Total comparisons: {comparaciones}")
    print(f"Matches found: {len(resultados)}")
    
    return resultados