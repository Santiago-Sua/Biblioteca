"""
Brute Force Algorithm - Library Management System

This module implements a Brute Force algorithm to find ALL combinations of
four books that exceed the risk threshold of 8 kg when placed together on
a shelf. This is part of the Shelf Module (Deficient Shelf Analysis).

PROJECT REQUIREMENT:
    Implement a brute force algorithm that finds and lists ALL combinations
    of 4 books that, when their weights are summed, exceed a risk threshold
    of 8 kg. The algorithm must exhaustively explore all combinations.

Algorithm Explanation:
    The algorithm uses nested loops (or itertools.combinations) to generate
    all possible combinations of 4 books from the inventory. For each
    combination, it calculates the total weight and checks if it exceeds
    the 8 kg threshold. All risky combinations are collected and returned.

Time Complexity: O(n^4) - explores all 4-element combinations
Space Complexity: O(k) - where k is the number of risky combinations found

Use Case:
    Safety inspection to identify potentially dangerous shelf configurations
    that could cause structural failure or accidents.

Author: [Your Name]
Date: December 2025
"""

from itertools import combinations


# Project constant
UMBRAL_RIESGO = 8.0  # Risk threshold in kilograms


def encontrar_combinaciones_riesgosas(lista_libros, umbral=UMBRAL_RIESGO, 
                                      num_libros=4, incluir_detalles=True):
    """
    Find all combinations of books that exceed the weight risk threshold.
    
    This is the MAIN function for the Brute Force requirement. It exhaustively
    explores all possible combinations of 4 books and identifies those that
    exceed the 8 kg safety limit.
    
    PROJECT REQUIREMENT:
        Find and list ALL combinations of 4 books that exceed 8 kg total weight.
    
    Args:
        lista_libros (list): List of book objects or dictionaries
        umbral (float, optional): Risk threshold in kg. Defaults to 8.0.
        num_libros (int, optional): Number of books per combination. Defaults to 4.
        incluir_detalles (bool, optional): Include detailed book info. Defaults to True.
        
    Returns:
        list: List of dictionaries, each containing:
              - 'libros': List of books in the combination
              - 'peso_total': Total weight of the combination
              - 'exceso': How much over the threshold
              - 'isbns': List of ISBNs (if incluir_detalles=True)
              - 'titulos': List of titles (if incluir_detalles=True)
              
    Example:
        >>> riesgosas = encontrar_combinaciones_riesgosas(inventario)
        >>> print(f"Found {len(riesgosas)} risky combinations")
        >>> for combo in riesgosas[:5]:  # Show first 5
        ...     print(f"Weight: {combo['peso_total']} kg")
    """
    combinaciones_riesgosas = []
    total_combinaciones = 0
    
    # Generate all combinations of num_libros books
    for combinacion in combinations(lista_libros, num_libros):
        total_combinaciones += 1
        
        # Calculate total weight for this combination
        peso_total = 0.0
        for libro in combinacion:
            if isinstance(libro, dict):
                peso_total += float(libro.get('peso', 0))
            else:
                peso_total += float(getattr(libro, 'peso', 0))
        
        # Check if this combination exceeds the risk threshold
        if peso_total > umbral:
            resultado = {
                'libros': list(combinacion),
                'peso_total': round(peso_total, 2),
                'exceso': round(peso_total - umbral, 2),
                'num_libros': num_libros
            }
            
            # Include detailed information if requested
            if incluir_detalles:
                isbns = []
                titulos = []
                autores = []
                
                for libro in combinacion:
                    if isinstance(libro, dict):
                        isbns.append(libro.get('isbn', 'N/A'))
                        titulos.append(libro.get('titulo', 'N/A'))
                        autores.append(libro.get('autor', 'N/A'))
                    else:
                        isbns.append(getattr(libro, 'isbn', 'N/A'))
                        titulos.append(getattr(libro, 'titulo', 'N/A'))
                        autores.append(getattr(libro, 'autor', 'N/A'))
                
                resultado['isbns'] = isbns
                resultado['titulos'] = titulos
                resultado['autores'] = autores
            
            combinaciones_riesgosas.append(resultado)
    
    # Add statistics
    return {
        'combinaciones_riesgosas': combinaciones_riesgosas,
        'total_encontradas': len(combinaciones_riesgosas),
        'total_exploradas': total_combinaciones,
        'umbral_usado': umbral,
        'num_libros': num_libros
    }


def generar_combinaciones_cuatro_libros(lista_libros):
    """
    Generate all possible combinations of exactly 4 books.
    
    This is a helper function that demonstrates the exhaustive exploration
    of the brute force approach. It generates all 4-book combinations
    regardless of weight.
    
    Args:
        lista_libros (list): List of books
        
    Returns:
        list: List of all 4-book combinations
        
    Example:
        >>> combos = generar_combinaciones_cuatro_libros(inventario)
        >>> print(f"Total combinations: {len(combos)}")
    """
    todas_combinaciones = []
    
    for combo in combinations(lista_libros, 4):
        todas_combinaciones.append(list(combo))
    
    return todas_combinaciones


def analizar_seguridad_estantes(lista_libros, umbral=UMBRAL_RIESGO):
    """
    Comprehensive safety analysis of shelf configurations.
    
    This function performs a complete brute force analysis and provides
    detailed statistics about safe and risky combinations.
    
    Args:
        lista_libros (list): List of books to analyze
        umbral (float, optional): Risk threshold in kg. Defaults to 8.0.
        
    Returns:
        dict: Comprehensive analysis with:
              - 'total_libros': Number of books analyzed
              - 'total_combinaciones': Total 4-book combinations
              - 'combinaciones_riesgosas': List of risky combinations
              - 'combinaciones_seguras': Number of safe combinations
              - 'porcentaje_riesgo': Percentage of risky combinations
              - 'peso_promedio_riesgosas': Average weight of risky combinations
              - 'peso_maximo_encontrado': Heaviest combination found
              - 'combinacion_mas_riesgosa': Most dangerous combination
              
    Example:
        >>> analisis = analizar_seguridad_estantes(inventario)
        >>> print(f"Risk level: {analisis['porcentaje_riesgo']:.2f}%")
    """
    n_libros = len(lista_libros)
    
    # Calculate total possible combinations
    from math import comb
    total_combinaciones = comb(n_libros, 4) if n_libros >= 4 else 0
    
    # Find all risky combinations
    resultado_bruto = encontrar_combinaciones_riesgosas(
        lista_libros, 
        umbral=umbral,
        incluir_detalles=True
    )
    
    combinaciones_riesgosas = resultado_bruto['combinaciones_riesgosas']
    num_riesgosas = len(combinaciones_riesgosas)
    num_seguras = total_combinaciones - num_riesgosas
    
    # Calculate statistics
    analisis = {
        'total_libros': n_libros,
        'total_combinaciones': total_combinaciones,
        'combinaciones_riesgosas': combinaciones_riesgosas,
        'num_riesgosas': num_riesgosas,
        'combinaciones_seguras': num_seguras,
        'porcentaje_riesgo': (num_riesgosas / total_combinaciones * 100) if total_combinaciones > 0 else 0,
        'umbral_riesgo': umbral
    }
    
    # Additional statistics if risky combinations were found
    if num_riesgosas > 0:
        pesos = [combo['peso_total'] for combo in combinaciones_riesgosas]
        analisis['peso_promedio_riesgosas'] = round(sum(pesos) / len(pesos), 2)
        analisis['peso_maximo_encontrado'] = round(max(pesos), 2)
        analisis['peso_minimo_riesgoso'] = round(min(pesos), 2)
        
        # Find the most dangerous combination
        idx_max = pesos.index(max(pesos))
        analisis['combinacion_mas_riesgosa'] = combinaciones_riesgosas[idx_max]
    else:
        analisis['peso_promedio_riesgosas'] = 0
        analisis['peso_maximo_encontrado'] = 0
        analisis['peso_minimo_riesgoso'] = 0
        analisis['combinacion_mas_riesgosa'] = None
    
    return analisis


def encontrar_libros_pesados(lista_libros, peso_minimo=2.0):
    """
    Find books that individually contribute most to risky combinations.
    
    This helper function identifies heavy books that are likely to appear
    in many risky combinations.
    
    Args:
        lista_libros (list): List of books
        peso_minimo (float, optional): Minimum weight threshold. Defaults to 2.0 kg.
        
    Returns:
        list: Books exceeding the weight threshold, sorted by weight (descending)
        
    Example:
        >>> pesados = encontrar_libros_pesados(inventario, peso_minimo=2.5)
        >>> print(f"Found {len(pesados)} heavy books")
    """
    libros_pesados = []
    
    for libro in lista_libros:
        if isinstance(libro, dict):
            peso = float(libro.get('peso', 0))
        else:
            peso = float(getattr(libro, 'peso', 0))
        
        if peso >= peso_minimo:
            libros_pesados.append({
                'libro': libro,
                'peso': peso
            })
    
    # Sort by weight in descending order
    libros_pesados.sort(key=lambda x: x['peso'], reverse=True)
    
    return libros_pesados


def calcular_frecuencia_en_combinaciones(lista_libros, umbral=UMBRAL_RIESGO):
    """
    Calculate how frequently each book appears in risky combinations.
    
    This analysis helps identify which books are most problematic for
    shelf safety and should be distributed carefully.
    
    Args:
        lista_libros (list): List of books
        umbral (float, optional): Risk threshold. Defaults to 8.0.
        
    Returns:
        dict: Dictionary mapping ISBN to frequency count
        
    Example:
        >>> frecuencias = calcular_frecuencia_en_combinaciones(inventario)
        >>> libro_problematico = max(frecuencias, key=frecuencias.get)
        >>> print(f"Most problematic book: {libro_problematico}")
    """
    resultado = encontrar_combinaciones_riesgosas(lista_libros, umbral=umbral)
    combinaciones = resultado['combinaciones_riesgosas']
    
    frecuencias = {}
    
    for combo in combinaciones:
        for isbn in combo['isbns']:
            frecuencias[isbn] = frecuencias.get(isbn, 0) + 1
    
    return frecuencias


def demostrar_fuerza_bruta(lista_libros, max_mostrar=10, umbral=UMBRAL_RIESGO):
    """
    Demonstrate the brute force algorithm step by step.
    
    This function shows the exhaustive exploration process, printing
    information about the search as it progresses.
    
    Args:
        lista_libros (list): List of books (recommend small list for demo)
        max_mostrar (int, optional): Max combinations to display. Defaults to 10.
        umbral (float, optional): Risk threshold. Defaults to 8.0.
        
    Note:
        This function prints to console for educational purposes.
        Use a small list (5-10 books) for clearer demonstration.
    """
    print("=== Brute Force Algorithm Demonstration ===")
    print(f"Finding all 4-book combinations exceeding {umbral} kg")
    print(f"Total books to analyze: {len(lista_libros)}")
    print()
    
    from math import comb
    total_combinaciones = comb(len(lista_libros), 4) if len(lista_libros) >= 4 else 0
    print(f"Total combinations to explore: {total_combinaciones}")
    print()
    
    print("Starting exhaustive search...")
    print("-" * 80)
    
    contador = 0
    encontradas = 0
    combinaciones_riesgosas = []
    
    for combinacion in combinations(lista_libros, 4):
        contador += 1
        
        # Calculate total weight
        peso_total = 0.0
        isbns = []
        
        for libro in combinacion:
            if isinstance(libro, dict):
                peso_total += float(libro.get('peso', 0))
                isbns.append(libro.get('isbn', 'N/A'))
            else:
                peso_total += float(getattr(libro, 'peso', 0))
                isbns.append(getattr(libro, 'isbn', 'N/A'))
        
        # Show progress for first few
        if contador <= max_mostrar or (peso_total > umbral and encontradas < max_mostrar):
            print(f"Combination {contador}:")
            print(f"  ISBNs: {isbns}")
            print(f"  Total Weight: {peso_total:.2f} kg")
            
            if peso_total > umbral:
                print(f"  ⚠️  RISKY! Exceeds threshold by {peso_total - umbral:.2f} kg")
                encontradas += 1
                combinaciones_riesgosas.append({
                    'isbns': isbns,
                    'peso': peso_total
                })
            else:
                print(f"  ✓ Safe")
            print()
    
    print("=" * 80)
    print("=== Search Complete ===")
    print(f"Total combinations explored: {contador}")
    print(f"Risky combinations found: {encontradas}")
    print(f"Safe combinations: {contador - encontradas}")
    print(f"Risk percentage: {(encontradas/contador*100):.2f}%" if contador > 0 else "N/A")
    print()
    
    if combinaciones_riesgosas:
        print("Top 5 most risky combinations:")
        combinaciones_riesgosas.sort(key=lambda x: x['peso'], reverse=True)
        for i, combo in enumerate(combinaciones_riesgosas[:5], 1):
            print(f"{i}. Weight: {combo['peso']:.2f} kg - ISBNs: {combo['isbns']}")


def generar_reporte_combinaciones_riesgosas(lista_libros, archivo_salida=None, umbral=UMBRAL_RIESGO):
    """
    Generate a comprehensive report of all risky combinations.
    
    This function performs the brute force analysis and can optionally
    save the results to a file for documentation purposes.
    
    Args:
        lista_libros (list): List of books to analyze
        archivo_salida (str, optional): Path to save report. Defaults to None.
        umbral (float, optional): Risk threshold. Defaults to 8.0.
        
    Returns:
        dict: Complete analysis report
        
    Example:
        >>> reporte = generar_reporte_combinaciones_riesgosas(
        ...     inventario,
        ...     archivo_salida="reports/risky_combinations.json"
        ... )
    """
    import json
    from datetime import datetime
    
    # Perform complete analysis
    analisis = analizar_seguridad_estantes(lista_libros, umbral)
    
    # Create report structure
    reporte = {
        'fecha_analisis': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'parametros': {
            'total_libros': analisis['total_libros'],
            'umbral_riesgo': umbral,
            'num_libros_por_combinacion': 4
        },
        'resultados': {
            'total_combinaciones_exploradas': analisis['total_combinaciones'],
            'combinaciones_riesgosas': analisis['num_riesgosas'],
            'combinaciones_seguras': analisis['combinaciones_seguras'],
            'porcentaje_riesgo': analisis['porcentaje_riesgo']
        },
        'estadisticas': {
            'peso_promedio_riesgosas': analisis.get('peso_promedio_riesgosas', 0),
            'peso_maximo_encontrado': analisis.get('peso_maximo_encontrado', 0),
            'peso_minimo_riesgoso': analisis.get('peso_minimo_riesgoso', 0)
        },
        'combinaciones_riesgosas': []
    }
    
    # Add detailed combinations (limit to avoid huge files)
    for combo in analisis['combinaciones_riesgosas'][:100]:  # First 100
        reporte['combinaciones_riesgosas'].append({
            'isbns': combo['isbns'],
            'titulos': combo['titulos'],
            'peso_total': combo['peso_total'],
            'exceso': combo['exceso']
        })
    
    # Save to file if requested
    if archivo_salida:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        print(f"Report saved to: {archivo_salida}")
    
    return reporte