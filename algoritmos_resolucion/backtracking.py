"""
Backtracking Algorithm - Library Management System

This module implements a Backtracking algorithm to find the optimal combination
of books that maximizes total value (COP) while respecting the weight constraint
of 8 kg. This is part of the Shelf Module (Optimal Shelf Configuration).

PROJECT REQUIREMENT:
    Implement a backtracking algorithm that finds the combination of books
    that maximizes the total value (COP) without exceeding the maximum weight
    capacity of 8 kg. The algorithm must demonstrate exploration and pruning.

Algorithm Explanation:
    Backtracking is a depth-first search with pruning. The algorithm explores
    possible combinations of books by recursively adding books to the current
    solution. When a constraint is violated (weight > 8 kg) or no better
    solution is possible, it backtracks and tries a different path.
    
    Key features:
    - Pruning: Stops exploring branches that cannot lead to better solutions
    - Constraint checking: Immediately rejects solutions exceeding weight limit
    - Optimization: Tracks the best solution found so far

Time Complexity: O(2^n) worst case, but pruning significantly reduces search space
Space Complexity: O(n) for the recursion stack

Use Case:
    Maximize the economic value of books on a shelf while maintaining
    structural safety (not exceeding 8 kg weight limit).

Author: [Your Name]
Date: December 2025
"""


# Project constant
CAPACIDAD_MAXIMA = 8.0  # Maximum weight capacity in kilograms


def optimizar_estante(lista_libros, capacidad_maxima=CAPACIDAD_MAXIMA, 
                     incluir_exploracion=False):
    """
    Find the optimal combination of books that maximizes value with weight constraint.
    
    This is the MAIN function for the Backtracking requirement. It finds the
    combination of books with maximum total value (COP) while ensuring the
    total weight does not exceed 8 kg.
    
    PROJECT REQUIREMENT:
        Find the combination that maximizes value without exceeding 8 kg capacity.
        Demonstrate exploration and pruning.
    
    Args:
        lista_libros (list): List of book objects or dictionaries
        capacidad_maxima (float, optional): Max weight in kg. Defaults to 8.0.
        incluir_exploracion (bool, optional): Track exploration stats. Defaults to False.
        
    Returns:
        dict: Optimal solution with:
              - 'libros': List of books in optimal combination
              - 'valor_total': Total value in COP
              - 'peso_total': Total weight in kg
              - 'num_libros': Number of books in combination
              - 'isbns': List of ISBNs
              - 'titulos': List of titles
              - 'exploracion': Exploration statistics (if incluir_exploracion=True)
              
    Example:
        >>> resultado = optimizar_estante(inventario)
        >>> print(f"Max value: ${resultado['valor_total']:,.0f} COP")
        >>> print(f"Total weight: {resultado['peso_total']:.2f} kg")
        >>> print(f"Books: {len(resultado['libros'])}")
    """
    # Prepare book data for easier processing
    libros_data = []
    for libro in lista_libros:
        if isinstance(libro, dict):
            libros_data.append({
                'objeto': libro,
                'isbn': libro.get('isbn', ''),
                'titulo': libro.get('titulo', ''),
                'autor': libro.get('autor', ''),
                'peso': float(libro.get('peso', 0)),
                'valor': float(libro.get('valor', 0))
            })
        else:
            libros_data.append({
                'objeto': libro,
                'isbn': getattr(libro, 'isbn', ''),
                'titulo': getattr(libro, 'titulo', ''),
                'autor': getattr(libro, 'autor', ''),
                'peso': float(getattr(libro, 'peso', 0)),
                'valor': float(getattr(libro, 'valor', 0))
            })
    
    # Sort by value/weight ratio for better pruning (greedy heuristic)
    libros_data.sort(key=lambda x: x['valor'] / x['peso'] if x['peso'] > 0 else 0, reverse=True)
    
    # Initialize tracking variables
    mejor_solucion = {
        'libros': [],
        'valor_total': 0,
        'peso_total': 0
    }
    
    exploracion = {
        'nodos_explorados': 0,
        'nodos_podados': 0,
        'soluciones_encontradas': 0,
        'max_profundidad': 0
    } if incluir_exploracion else None
    
    # Start backtracking
    _backtracking_recursivo(
        libros_data,
        0,
        [],
        0,
        0,
        capacidad_maxima,
        mejor_solucion,
        exploracion
    )
    
    # Format result
    resultado = {
        'libros': [libro['objeto'] for libro in mejor_solucion['libros']],
        'valor_total': round(mejor_solucion['valor_total'], 2),
        'peso_total': round(mejor_solucion['peso_total'], 2),
        'num_libros': len(mejor_solucion['libros']),
        'isbns': [libro['isbn'] for libro in mejor_solucion['libros']],
        'titulos': [libro['titulo'] for libro in mejor_solucion['libros']],
        'capacidad_maxima': capacidad_maxima,
        'espacio_restante': round(capacidad_maxima - mejor_solucion['peso_total'], 2)
    }
    
    if incluir_exploracion:
        resultado['exploracion'] = exploracion
    
    return resultado


def _backtracking_recursivo(libros, indice, solucion_actual, peso_actual, 
                            valor_actual, capacidad_maxima, mejor_solucion, 
                            exploracion):
    """
    Recursive backtracking function with pruning.
    
    This is the core recursive function that explores the solution space.
    It implements the backtracking algorithm with constraint checking and
    pruning for optimization.
    
    Args:
        libros (list): List of book data dictionaries
        indice (int): Current index in the book list
        solucion_actual (list): Current books in the solution
        peso_actual (float): Current total weight
        valor_actual (float): Current total value
        capacidad_maxima (float): Maximum weight allowed
        mejor_solucion (dict): Best solution found so far (modified in place)
        exploracion (dict): Exploration statistics (modified in place)
    """
    # Update exploration statistics
    if exploracion is not None:
        exploracion['nodos_explorados'] += 1
        exploracion['max_profundidad'] = max(exploracion['max_profundidad'], len(solucion_actual))
    
    # Check if current solution is better than best found
    if valor_actual > mejor_solucion['valor_total']:
        mejor_solucion['libros'] = solucion_actual.copy()
        mejor_solucion['valor_total'] = valor_actual
        mejor_solucion['peso_total'] = peso_actual
        
        if exploracion is not None:
            exploracion['soluciones_encontradas'] += 1
    
    # Base case: reached end of book list
    if indice >= len(libros):
        return
    
    # Calculate upper bound for pruning (optimistic estimate)
    # If we can't possibly beat the current best, prune this branch
    peso_restante = capacidad_maxima - peso_actual
    valor_potencial = valor_actual
    
    for i in range(indice, len(libros)):
        if libros[i]['peso'] <= peso_restante:
            valor_potencial += libros[i]['valor']
            peso_restante -= libros[i]['peso']
        else:
            # Fractional knapsack upper bound
            if peso_restante > 0:
                valor_potencial += (peso_restante / libros[i]['peso']) * libros[i]['valor']
            break
    
    # Pruning: if upper bound can't beat current best, stop exploring
    if valor_potencial <= mejor_solucion['valor_total']:
        if exploracion is not None:
            exploracion['nodos_podados'] += 1
        return
    
    # Try INCLUDING the current book
    libro_actual = libros[indice]
    if peso_actual + libro_actual['peso'] <= capacidad_maxima:
        # Include this book and explore
        solucion_actual.append(libro_actual)
        _backtracking_recursivo(
            libros,
            indice + 1,
            solucion_actual,
            peso_actual + libro_actual['peso'],
            valor_actual + libro_actual['valor'],
            capacidad_maxima,
            mejor_solucion,
            exploracion
        )
        # Backtrack: remove the book
        solucion_actual.pop()
    else:
        # Pruning: weight constraint violated
        if exploracion is not None:
            exploracion['nodos_podados'] += 1
    
    # Try EXCLUDING the current book
    _backtracking_recursivo(
        libros,
        indice + 1,
        solucion_actual,
        peso_actual,
        valor_actual,
        capacidad_maxima,
        mejor_solucion,
        exploracion
    )


def encontrar_mejor_combinacion(lista_libros, capacidad_maxima=CAPACIDAD_MAXIMA):
    """
    Simplified interface to find the best book combination.
    
    This is a convenience wrapper around optimizar_estante that returns
    just the essential information.
    
    Args:
        lista_libros (list): List of books
        capacidad_maxima (float, optional): Max weight. Defaults to 8.0.
        
    Returns:
        dict: Optimal combination details
    """
    return optimizar_estante(lista_libros, capacidad_maxima, incluir_exploracion=False)


def backtracking_con_demostracion(lista_libros, capacidad_maxima=CAPACIDAD_MAXIMA, 
                                  mostrar_pasos=True):
    """
    Demonstrate the backtracking algorithm with detailed step-by-step output.
    
    This function shows how the algorithm explores the solution space,
    demonstrates pruning, and tracks the decision tree.
    
    Args:
        lista_libros (list): List of books (recommend small list for demo)
        capacidad_maxima (float, optional): Max weight. Defaults to 8.0.
        mostrar_pasos (bool, optional): Print each step. Defaults to True.
        
    Returns:
        dict: Optimal solution with exploration details
        
    Note:
        Use a small list (5-10 books) for clearer demonstration.
    """
    print("=== Backtracking Algorithm Demonstration ===")
    print(f"Goal: Maximize value without exceeding {capacidad_maxima} kg")
    print(f"Total books available: {len(lista_libros)}")
    print()
    
    # Prepare book data
    libros_data = []
    for i, libro in enumerate(lista_libros):
        if isinstance(libro, dict):
            peso = float(libro.get('peso', 0))
            valor = float(libro.get('valor', 0))
            isbn = libro.get('isbn', f'Book-{i}')
        else:
            peso = float(getattr(libro, 'peso', 0))
            valor = float(getattr(libro, 'valor', 0))
            isbn = getattr(libro, 'isbn', f'Book-{i}')
        
        libros_data.append({
            'id': i,
            'isbn': isbn,
            'peso': peso,
            'valor': valor,
            'ratio': valor / peso if peso > 0 else 0
        })
        
        if mostrar_pasos:
            print(f"Book {i}: ISBN={isbn[:15]}... Weight={peso:.2f}kg Value=${valor:,.0f} Ratio={valor/peso:.2f}" if peso > 0 else f"Book {i}: Weight=0")
    
    print("\n" + "="*80 + "\n")
    
    # Sort by value/weight ratio
    libros_data.sort(key=lambda x: x['ratio'], reverse=True)
    
    if mostrar_pasos:
        print("Books sorted by value/weight ratio (greedy heuristic):")
        for libro in libros_data[:5]:
            print(f"  {libro['isbn'][:15]}... Ratio: {libro['ratio']:.2f}")
        print()
    
    # Initialize for demonstration
    mejor = {'libros': [], 'valor': 0, 'peso': 0}
    stats = {'nodos': 0, 'podados': 0, 'profundidad_max': 0}
    
    def _demo_backtrack(idx, actual, peso_act, valor_act, nivel):
        stats['nodos'] += 1
        stats['profundidad_max'] = max(stats['profundidad_max'], nivel)
        
        indent = "  " * nivel
        
        if mostrar_pasos and stats['nodos'] <= 30:  # Limit output
            print(f"{indent}[Level {nivel}] Exploring node {stats['nodos']}")
            print(f"{indent}Current: {len(actual)} books, ${valor_act:,.0f}, {peso_act:.2f}kg")
        
        # Update best
        if valor_act > mejor['valor']:
            mejor['libros'] = actual.copy()
            mejor['valor'] = valor_act
            mejor['peso'] = peso_act
            if mostrar_pasos and stats['nodos'] <= 30:
                print(f"{indent}✓ NEW BEST SOLUTION! Value: ${valor_act:,.0f}")
        
        if idx >= len(libros_data):
            return
        
        # Pruning check
        peso_rest = capacidad_maxima - peso_act
        valor_pot = valor_act + sum(l['valor'] for l in libros_data[idx:] if l['peso'] <= peso_rest)
        
        if valor_pot <= mejor['valor']:
            stats['podados'] += 1
            if mostrar_pasos and stats['nodos'] <= 30:
                print(f"{indent}✗ PRUNED (can't beat current best)")
            return
        
        libro = libros_data[idx]
        
        # Try including
        if peso_act + libro['peso'] <= capacidad_maxima:
            if mostrar_pasos and stats['nodos'] <= 30:
                print(f"{indent}→ Including book {libro['id']}")
            actual.append(libro)
            _demo_backtrack(idx+1, actual, peso_act+libro['peso'], valor_act+libro['valor'], nivel+1)
            actual.pop()  # Backtrack
            if mostrar_pasos and stats['nodos'] <= 30:
                print(f"{indent}← Backtracking from book {libro['id']}")
        else:
            stats['podados'] += 1
            if mostrar_pasos and stats['nodos'] <= 30:
                print(f"{indent}✗ PRUNED (weight constraint)")
        
        # Try excluding
        if mostrar_pasos and stats['nodos'] <= 30:
            print(f"{indent}→ Excluding book {libro['id']}")
        _demo_backtrack(idx+1, actual, peso_act, valor_act, nivel+1)
    
    _demo_backtrack(0, [], 0, 0, 0)
    
    print("\n" + "="*80)
    print("=== Backtracking Complete ===")
    print(f"Nodes explored: {stats['nodos']}")
    print(f"Nodes pruned: {stats['podados']}")
    print(f"Pruning efficiency: {(stats['podados']/stats['nodos']*100):.1f}%")
    print(f"Maximum depth: {stats['profundidad_max']}")
    print()
    print(f"OPTIMAL SOLUTION:")
    print(f"  Books in combination: {len(mejor['libros'])}")
    print(f"  Total value: ${mejor['valor']:,.0f} COP")
    print(f"  Total weight: {mejor['peso']:.2f} kg")
    print(f"  Space remaining: {capacidad_maxima - mejor['peso']:.2f} kg")
    print()
    print("Books in optimal combination:")
    for libro in mejor['libros']:
        print(f"  - {libro['isbn'][:20]}... (${libro['valor']:,.0f}, {libro['peso']:.2f}kg)")
    
    return {
        'libros': mejor['libros'],
        'valor_total': mejor['valor'],
        'peso_total': mejor['peso'],
        'estadisticas': stats
    }


def comparar_con_greedy(lista_libros, capacidad_maxima=CAPACIDAD_MAXIMA):
    """
    Compare backtracking solution with greedy algorithm.
    
    This demonstrates why backtracking is superior to a simple greedy
    approach for the knapsack-like problem.
    
    Args:
        lista_libros (list): List of books
        capacidad_maxima (float, optional): Max weight. Defaults to 8.0.
        
    Returns:
        dict: Comparison of both approaches
    """
    # Backtracking (optimal)
    resultado_backtracking = optimizar_estante(lista_libros, capacidad_maxima)
    
    # Greedy (by value/weight ratio)
    libros_data = []
    for libro in lista_libros:
        if isinstance(libro, dict):
            peso = float(libro.get('peso', 0))
            valor = float(libro.get('valor', 0))
        else:
            peso = float(getattr(libro, 'peso', 0))
            valor = float(getattr(libro, 'valor', 0))
        
        if peso > 0:
            libros_data.append({
                'libro': libro,
                'peso': peso,
                'valor': valor,
                'ratio': valor / peso
            })
    
    libros_data.sort(key=lambda x: x['ratio'], reverse=True)
    
    greedy_libros = []
    greedy_peso = 0
    greedy_valor = 0
    
    for item in libros_data:
        if greedy_peso + item['peso'] <= capacidad_maxima:
            greedy_libros.append(item['libro'])
            greedy_peso += item['peso']
            greedy_valor += item['valor']
    
    return {
        'backtracking': {
            'valor': resultado_backtracking['valor_total'],
            'peso': resultado_backtracking['peso_total'],
            'num_libros': resultado_backtracking['num_libros']
        },
        'greedy': {
            'valor': greedy_valor,
            'peso': greedy_peso,
            'num_libros': len(greedy_libros)
        },
        'diferencia_valor': resultado_backtracking['valor_total'] - greedy_valor,
        'porcentaje_mejora': ((resultado_backtracking['valor_total'] - greedy_valor) / greedy_valor * 100) if greedy_valor > 0 else 0
    }