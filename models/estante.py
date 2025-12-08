"""
Estante Model - Library Management System

This module defines the Estante (Shelf) class which represents a physical
shelf in the library. Each shelf has weight capacity constraints and can
hold multiple books. This is used for the shelf optimization module.

Classes:
    Estante: Main class representing a library shelf

Author: [Your Name]
Date: December 2025
"""


class Estante:
    """
    Represents a shelf in the library.
    
    This class encapsulates information about a physical shelf including
    its capacity constraints, current load, and the books it contains.
    Used for optimization algorithms (brute force and backtracking).
    
    Attributes:
        id_estante (str): Unique identifier for the shelf
        nombre (str): Descriptive name of the shelf
        capacidad_max (float): Maximum weight capacity in kilograms
        peso_actual (float): Current weight of books on the shelf in kg
        libros (list): List of ISBN codes of books on this shelf
        ubicacion (str): Physical location in the library
        seccion (str): Library section (e.g., "Fiction", "Science", etc.)
    """
    
    # Default maximum capacity in kilograms (as per project requirements)
    CAPACIDAD_DEFAULT = 8.0
    
    def __init__(self, id_estante, nombre, capacidad_max=CAPACIDAD_DEFAULT,
                 peso_actual=0.0, libros=None, ubicacion="", seccion="General"):
        """
        Initialize a new Estante instance.
        
        Args:
            id_estante (str): Unique shelf identifier
            nombre (str): Descriptive name for the shelf
            capacidad_max (float, optional): Max weight in kg. Defaults to 8.0.
            peso_actual (float, optional): Current weight. Defaults to 0.0.
            libros (list, optional): List of ISBN codes. Defaults to empty list.
            ubicacion (str, optional): Physical location. Defaults to "".
            seccion (str, optional): Library section. Defaults to "General".
            
        Raises:
            ValueError: If capacity or weight values are invalid
        """
        if not id_estante or id_estante.strip() == "":
            raise ValueError("Shelf ID cannot be empty")
        if not nombre or nombre.strip() == "":
            raise ValueError("Shelf name cannot be empty")
        if capacidad_max <= 0:
            raise ValueError("Maximum capacity must be positive")
        if peso_actual < 0:
            raise ValueError("Current weight cannot be negative")
        if peso_actual > capacidad_max:
            raise ValueError("Current weight cannot exceed maximum capacity")
            
        self.id_estante = id_estante.strip()
        self.nombre = nombre.strip()
        self.capacidad_max = float(capacidad_max)
        self.peso_actual = float(peso_actual)
        self.libros = libros if libros is not None else []
        self.ubicacion = ubicacion.strip()
        self.seccion = seccion.strip()
        
    def to_dict(self):
        """
        Convert the Estante instance to a dictionary.
        
        This method is useful for JSON serialization and data storage.
        
        Returns:
            dict: Dictionary containing all shelf attributes
        """
        return {
            "id_estante": self.id_estante,
            "nombre": self.nombre,
            "capacidad_max": self.capacidad_max,
            "peso_actual": self.peso_actual,
            "libros": self.libros.copy(),
            "ubicacion": self.ubicacion,
            "seccion": self.seccion
        }
        
    @classmethod
    def from_dict(cls, data):
        """
        Create an Estante instance from a dictionary.
        
        This class method allows creating a shelf object from stored data.
        
        Args:
            data (dict): Dictionary containing shelf attributes
            
        Returns:
            Estante: New Estante instance with the provided data
        """
        return cls(
            id_estante=data.get("id_estante", ""),
            nombre=data.get("nombre", ""),
            capacidad_max=data.get("capacidad_max", cls.CAPACIDAD_DEFAULT),
            peso_actual=data.get("peso_actual", 0.0),
            libros=data.get("libros", []),
            ubicacion=data.get("ubicacion", ""),
            seccion=data.get("seccion", "General")
        )
        
    def puede_agregar_libro(self, peso_libro):
        """
        Check if a book with given weight can be added to the shelf.
        
        Args:
            peso_libro (float): Weight of the book in kilograms
            
        Returns:
            bool: True if book can be added without exceeding capacity
        """
        return (self.peso_actual + peso_libro) <= self.capacidad_max
        
    def agregar_libro(self, isbn, peso):
        """
        Add a book to the shelf.
        
        Args:
            isbn (str): ISBN of the book to add
            peso (float): Weight of the book in kilograms
            
        Returns:
            bool: True if book was added successfully, False if capacity exceeded
        """
        if self.puede_agregar_libro(peso):
            self.libros.append(isbn)
            self.peso_actual += peso
            return True
        return False
        
    def remover_libro(self, isbn, peso):
        """
        Remove a book from the shelf.
        
        Args:
            isbn (str): ISBN of the book to remove
            peso (float): Weight of the book in kilograms
            
        Returns:
            bool: True if book was removed successfully, False if not found
        """
        if isbn in self.libros:
            self.libros.remove(isbn)
            self.peso_actual = max(0, self.peso_actual - peso)
            return True
        return False
        
    def vaciar(self):
        """
        Remove all books from the shelf.
        
        Resets the shelf to empty state.
        """
        self.libros.clear()
        self.peso_actual = 0.0
        
    def esta_vacio(self):
        """
        Check if the shelf is empty.
        
        Returns:
            bool: True if shelf has no books, False otherwise
        """
        return len(self.libros) == 0
        
    def esta_lleno(self):
        """
        Check if the shelf is at maximum capacity.
        
        Returns:
            bool: True if shelf cannot hold more weight, False otherwise
        """
        return self.peso_actual >= self.capacidad_max
        
    def obtener_espacio_disponible(self):
        """
        Get the remaining weight capacity of the shelf.
        
        Returns:
            float: Available weight capacity in kilograms
        """
        return self.capacidad_max - self.peso_actual
        
    def obtener_porcentaje_ocupacion(self):
        """
        Calculate the percentage of capacity currently used.
        
        Returns:
            float: Percentage of capacity used (0-100)
        """
        if self.capacidad_max == 0:
            return 0.0
        return (self.peso_actual / self.capacidad_max) * 100
        
    def obtener_numero_libros(self):
        """
        Get the number of books currently on the shelf.
        
        Returns:
            int: Number of books on this shelf
        """
        return len(self.libros)
        
    def es_riesgoso(self):
        """
        Check if the shelf is at risk (exceeding safe weight limit).
        
        According to project requirements, shelves exceeding 8 kg are risky.
        
        Returns:
            bool: True if current weight exceeds or equals capacity, False otherwise
        """
        return self.peso_actual >= self.capacidad_max
        
    def __str__(self):
        """
        Return a string representation of the shelf.
        
        Returns:
            str: Formatted string with shelf information
        """
        return (f"Shelf: {self.nombre} (ID: {self.id_estante}) | "
                f"Weight: {self.peso_actual:.2f}/{self.capacidad_max:.2f} kg | "
                f"Books: {len(self.libros)} | "
                f"Occupancy: {self.obtener_porcentaje_ocupacion():.1f}%")
                
    def __repr__(self):
        """
        Return a detailed representation of the shelf.
        
        Returns:
            str: Technical representation showing all attributes
        """
        return (f"Estante(id_estante='{self.id_estante}', nombre='{self.nombre}', "
                f"capacidad_max={self.capacidad_max}, peso_actual={self.peso_actual}, "
                f"libros={len(self.libros)})")
                
    def __eq__(self, other):
        """
        Compare two shelves for equality based on shelf ID.
        
        Args:
            other (Estante): Another shelf to compare with
            
        Returns:
            bool: True if both shelves have the same ID
        """
        if not isinstance(other, Estante):
            return False
        return self.id_estante == other.id_estante
        
    def __hash__(self):
        """
        Return hash value based on shelf ID.
        
        This allows shelves to be used in sets and as dictionary keys.
        
        Returns:
            int: Hash value of the shelf ID
        """
        return hash(self.id_estante)