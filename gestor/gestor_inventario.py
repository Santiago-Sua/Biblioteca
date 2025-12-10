"""
Inventory Manager - Library Management System

This module implements the GestorInventario class which manages all book
inventory operations in the library system. It maintains two master lists
as required by the project and integrates sorting and searching algorithms.

PROJECT REQUIREMENTS:
    - Maintain General Inventory (unsorted, reflects load order)
    - Maintain Sorted Inventory (sorted by ISBN in ascending order)
    - Use Insertion Sort to maintain sorted inventory when adding books
    - Integrate Linear Search for title/author queries
    - Integrate Binary Search for ISBN queries
    - Load initial data from CSV/JSON file

Classes:
    GestorInventario: Main manager class for book inventory

Author: [Your Name]
Date: December 2025
"""

import json
import csv
from models.libro import Libro
from algoritmos_ordenamiento.insercion import insertar_ordenado, ordenamiento_insercion
from algoritmos_ordenamiento.merge_sort import generar_reporte_ordenado
from algoritmos_busqueda.busqueda_lineal import buscar_por_titulo, buscar_por_autor, buscar_libros_disponibles
from algoritmos_busqueda.busqueda_binaria import buscar_libro_por_isbn


class GestorInventario:
    """
    Manager class for book inventory operations.
    
    This class manages the two master lists required by the project:
    - General Inventory: Unsorted, maintains load order
    - Sorted Inventory: Always sorted by ISBN (ascending)
    
    Attributes:
        inventario_general (list): Unsorted list of books (load order)
        inventario_ordenado (list): Sorted list of books (by ISBN)
        archivo_handler: Utility for file operations
        ruta_datos (str): Path to book data file
    """
    
    def __init__(self, archivo_handler, ruta_datos="data/libros/libros.json"):
        """
        Initialize the inventory manager.
        
        Args:
            archivo_handler: ArchivoHandler instance for file operations
            ruta_datos (str, optional): Path to data file. Defaults to "data/libros/libros.json".
        """
        self.archivo_handler = archivo_handler
        self.ruta_datos = ruta_datos
        
        # PROJECT REQUIREMENT: Two master lists
        self.inventario_general = []  # Unsorted - reflects load order
        self.inventario_ordenado = []  # Sorted by ISBN (ascending)
        
        # Load initial data
        self.cargar_inventario()
    
    def cargar_inventario(self):
        """
        Load book inventory from file (CSV or JSON).
        
        PROJECT REQUIREMENT: Load initial inventory from CSV/JSON file.
        The system supports both formats for flexibility.
        """
        try:
            # Try loading from JSON first
            datos = self.archivo_handler.cargar_json(self.ruta_datos)
            
            if datos:
                # Load into General Inventory (unsorted)
                self.inventario_general = [Libro.from_dict(libro_dict) for libro_dict in datos]
                
                # Create Sorted Inventory (sorted by ISBN)
                self.inventario_ordenado = self.inventario_general.copy()
                ordenamiento_insercion(self.inventario_ordenado, clave='isbn')
                
                print(f"✓ Loaded {len(self.inventario_general)} books from {self.ruta_datos}")
            else:
                print(f"No data found in {self.ruta_datos}. Starting with empty inventory.")
                
        except Exception as e:
            print(f"Error loading inventory: {e}")
            self.inventario_general = []
            self.inventario_ordenado = []
    
    def cargar_desde_csv(self, ruta_csv):
        """
        Load inventory from a CSV file.
        
        PROJECT REQUIREMENT: Support CSV format for initial data.
        
        Expected CSV format:
        ISBN,Titulo,Autor,Peso,Valor,Stock,Genero,Editorial,AnioPublicacion
        
        Args:
            ruta_csv (str): Path to CSV file
            
        Returns:
            int: Number of books loaded
        """
        try:
            libros_cargados = []
            
            with open(ruta_csv, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        libro = Libro(
                            isbn=row['ISBN'],
                            titulo=row['Titulo'],
                            autor=row['Autor'],
                            peso=float(row['Peso']),
                            valor=float(row['Valor']),
                            stock=int(row.get('Stock', 1)),
                            genero=row.get('Genero', 'General'),
                            editorial=row.get('Editorial', 'Unknown'),
                            anio_publicacion=int(row.get('AnioPublicacion', 2024))
                        )
                        libros_cargados.append(libro)
                    except Exception as e:
                        print(f"Error loading book from row: {e}")
                        continue
            
            # Add to inventories
            for libro in libros_cargados:
                self.agregar_libro(libro)
            
            print(f"✓ Loaded {len(libros_cargados)} books from CSV")
            return len(libros_cargados)
            
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return 0
    
    def agregar_libro(self, libro):
        """
        Add a new book to both inventories.
        
        PROJECT REQUIREMENT: Use Insertion Sort to maintain sorted inventory.
        
        Args:
            libro (Libro): Book object to add
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        try:
            # Check if book already exists (by ISBN)
            if self.buscar_por_isbn(libro.isbn):
                print(f"Book with ISBN {libro.isbn} already exists")
                return False
            
            # Add to General Inventory (unsorted - just append)
            self.inventario_general.append(libro)
            
            # Add to Sorted Inventory using Insertion Sort
            # PROJECT REQUIREMENT: Use insertar_ordenado for maintaining order
            insertar_ordenado(self.inventario_ordenado, libro, clave='isbn')
            
            # Save to file
            self.guardar_inventario()
            
            print(f"✓ Book added: {libro.titulo}")
            return True
            
        except Exception as e:
            print(f"Error adding book: {e}")
            return False
    
    def actualizar_libro(self, isbn, datos_actualizados):
        """
        Update a book's information.
        
        Args:
            isbn (str): ISBN of the book to update
            datos_actualizados (dict): Dictionary with fields to update
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            # Find book in both inventories
            libro_general = None
            libro_ordenado = None
            
            for libro in self.inventario_general:
                if libro.isbn == isbn:
                    libro_general = libro
                    break
            
            for libro in self.inventario_ordenado:
                if libro.isbn == isbn:
                    libro_ordenado = libro
                    break
            
            if not libro_general or not libro_ordenado:
                print(f"Book with ISBN {isbn} not found")
                return False
            
            # Update both references (they point to same objects initially)
            for campo, valor in datos_actualizados.items():
                if hasattr(libro_general, campo) and campo != 'isbn':  # Don't change ISBN
                    setattr(libro_general, campo, valor)
                    setattr(libro_ordenado, campo, valor)
            
            # Save changes
            self.guardar_inventario()
            
            print(f"✓ Book updated: {isbn}")
            return True
            
        except Exception as e:
            print(f"Error updating book: {e}")
            return False
    
    def eliminar_libro(self, isbn):
        """
        Remove a book from both inventories.
        
        Args:
            isbn (str): ISBN of the book to remove
            
        Returns:
            bool: True if removed successfully, False otherwise
        """
        try:
            # Remove from General Inventory
            self.inventario_general = [libro for libro in self.inventario_general 
                                      if libro.isbn != isbn]
            
            # Remove from Sorted Inventory
            self.inventario_ordenado = [libro for libro in self.inventario_ordenado 
                                       if libro.isbn != isbn]
            
            # Save changes
            self.guardar_inventario()
            
            print(f"✓ Book removed: {isbn}")
            return True
            
        except Exception as e:
            print(f"Error removing book: {e}")
            return False
    
    def buscar_por_titulo(self, titulo):
        """
        Search for books by title in the General Inventory.
        
        PROJECT REQUIREMENT: Use Linear Search on unsorted General Inventory.
        
        Args:
            titulo (str): Title or partial title to search for
            
        Returns:
            list: List of matching books
        """
        return buscar_por_titulo(self.inventario_general, titulo)
    
    def buscar_por_autor(self, autor):
        """
        Search for books by author in the General Inventory.
        
        PROJECT REQUIREMENT: Use Linear Search on unsorted General Inventory.
        
        Args:
            autor (str): Author name or partial name to search for
            
        Returns:
            list: List of matching books
        """
        return buscar_por_autor(self.inventario_general, autor)
    
    def buscar_por_isbn(self, isbn):
        """
        Search for a book by ISBN in the Sorted Inventory.
        
        PROJECT REQUIREMENT: Use Binary Search on Sorted Inventory.
        
        Args:
            isbn (str): ISBN to search for
            
        Returns:
            Libro or None: Book object if found, None otherwise
        """
        return buscar_libro_por_isbn(self.inventario_ordenado, isbn)
    
    def buscar_disponibles(self, filtro_autor=None):
        """
        Find all available books (stock > 0).
        
        Args:
            filtro_autor (str, optional): Filter by author. Defaults to None.
            
        Returns:
            list: List of available books
        """
        if filtro_autor:
            return buscar_libros_disponibles(self.inventario_general, 'autor', filtro_autor)
        else:
            return buscar_libros_disponibles(self.inventario_general)
    
    def generar_reporte_por_valor(self, reverso=True):
        """
        Generate inventory report sorted by value (COP).
        
        PROJECT REQUIREMENT: Use Merge Sort to generate global report by value.
        
        Args:
            reverso (bool, optional): Sort descending. Defaults to True.
            
        Returns:
            list: List of books sorted by value
        """
        return generar_reporte_ordenado(
            self.inventario_general,
            clave='valor',
            reverso=reverso,
            formato='dict',
            incluir_indices=True
        )
    
    def obtener_estadisticas(self):
        """
        Get comprehensive inventory statistics.
        
        Returns:
            dict: Dictionary with various statistics
        """
        if not self.inventario_general:
            return {
                'total_libros': 0,
                'total_stock': 0,
                'valor_total': 0,
                'peso_total': 0,
                'disponibles': 0
            }
        
        total_stock = sum(libro.stock for libro in self.inventario_general)
        valor_total = sum(libro.valor * libro.stock for libro in self.inventario_general)
        peso_total = sum(libro.peso * libro.stock for libro in self.inventario_general)
        disponibles = sum(1 for libro in self.inventario_general if libro.stock > 0)
        
        return {
            'total_libros': len(self.inventario_general),
            'total_stock': total_stock,
            'valor_total': round(valor_total, 2),
            'peso_total': round(peso_total, 2),
            'disponibles': disponibles,
            'agotados': len(self.inventario_general) - disponibles
        }
    
    def listar_todos(self, ordenado=False):
        """
        List all books in inventory.
        
        Args:
            ordenado (bool, optional): Use sorted inventory. Defaults to False.
            
        Returns:
            list: List of all books
        """
        if ordenado:
            return self.inventario_ordenado.copy()
        else:
            return self.inventario_general.copy()
    
    def guardar_inventario(self):
        """
        Save inventory to JSON file.
        
        Saves the General Inventory (unsorted) to maintain load order.
        """
        try:
            datos = [libro.to_dict() for libro in self.inventario_general]
            self.archivo_handler.guardar_json(self.ruta_datos, datos)
            return True
        except Exception as e:
            print(f"Error saving inventory: {e}")
            return False
        
    def actualizar_libro(self, isbn_original, libro_actualizado):
  
    # Eliminar el libro anterior
        if self.eliminar_libro(isbn_original):
        # Agregar el libro actualizado
           return self.agregar_libro(libro_actualizado)
        return False

    def verificar_consistencia(self):
        """
        Verify that both inventories are consistent.
        
        Checks that:
        1. Both inventories have the same number of books
        2. Both contain the same ISBNs
        3. Sorted inventory is actually sorted by ISBN
        
        Returns:
            dict: Verification results
        """
        from algoritmos_ordenamiento.insercion import verificar_ordenamiento
        
        general_isbns = set(libro.isbn for libro in self.inventario_general)
        ordenado_isbns = set(libro.isbn for libro in self.inventario_ordenado)
        
        mismo_tamanio = len(self.inventario_general) == len(self.inventario_ordenado)
        mismos_libros = general_isbns == ordenado_isbns
        esta_ordenado = verificar_ordenamiento(self.inventario_ordenado, clave='isbn')
        
        return {
            'consistente': mismo_tamanio and mismos_libros and esta_ordenado,
            'mismo_tamanio': mismo_tamanio,
            'mismos_libros': mismos_libros,
            'ordenado_correcto': esta_ordenado,
            'total_general': len(self.inventario_general),
            'total_ordenado': len(self.inventario_ordenado)
        }