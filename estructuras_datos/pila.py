"""
Pila (Stack) Data Structure - Library Management System

This module implements a Stack (LIFO - Last In, First Out) data structure
using Object-Oriented Programming principles. The stack is used to manage
the loan history per user in the library system.

When a user borrows a book, the loan record (ISBN and date) is pushed onto
their personal stack. The most recent loan is always at the top.

Classes:
    Pila: Stack implementation with push, pop, peek, and utility methods

Author: [Your Name]
Date: December 2025
"""

from datetime import datetime


class Pila:
    """
    Stack (LIFO) implementation for managing loan history.
    
    This class implements a stack data structure where elements are added
    and removed from the top following Last In, First Out principle.
    Used specifically for tracking loan history per user.
    
    Attributes:
        elementos (list): Internal list storing stack elements
        capacidad_max (int): Maximum number of elements allowed (None for unlimited)
    """
    
    def __init__(self, capacidad_max=None):
        """
        Initialize an empty stack.
        
        Args:
            capacidad_max (int, optional): Maximum stack size. Defaults to None (unlimited).
        """
        self.elementos = []
        self.capacidad_max = capacidad_max
        
    def apilar(self, isbn, fecha=None):
        """
        Push a loan record onto the stack.
        
        Adds a new loan record to the top of the stack. Each record contains
        the book's ISBN and the loan date.
        
        Args:
            isbn (str): ISBN of the borrowed book
            fecha (str, optional): Loan date in ISO format. Defaults to current date.
            
        Returns:
            bool: True if element was pushed successfully, False if stack is full
            
        Raises:
            ValueError: If ISBN is empty
        """
        if not isbn or isbn.strip() == "":
            raise ValueError("ISBN cannot be empty")
            
        if self.esta_llena():
            return False
            
        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        registro = {
            "isbn": isbn.strip(),
            "fecha": fecha
        }
        
        self.elementos.append(registro)
        return True
        
    def desapilar(self):
        """
        Pop the most recent loan record from the stack.
        
        Removes and returns the element at the top of the stack (most recent loan).
        
        Returns:
            dict: Dictionary with 'isbn' and 'fecha', or None if stack is empty
        """
        if self.esta_vacia():
            return None
        return self.elementos.pop()
        
    def tope(self):
        """
        Get the top element without removing it (peek operation).
        
        Returns the most recent loan without modifying the stack.
        
        Returns:
            dict: Dictionary with 'isbn' and 'fecha', or None if stack is empty
        """
        if self.esta_vacia():
            return None
        return self.elementos[-1]
        
    def esta_vacia(self):
        """
        Check if the stack is empty.
        
        Returns:
            bool: True if stack has no elements, False otherwise
        """
        return len(self.elementos) == 0
        
    def esta_llena(self):
        """
        Check if the stack has reached maximum capacity.
        
        Returns:
            bool: True if stack is full, False otherwise (or if unlimited)
        """
        if self.capacidad_max is None:
            return False
        return len(self.elementos) >= self.capacidad_max
        
    def tamanio(self):
        """
        Get the current number of elements in the stack.
        
        Returns:
            int: Number of elements currently in the stack
        """
        return len(self.elementos)
        
    def vaciar(self):
        """
        Remove all elements from the stack.
        
        Clears the entire stack, resetting it to empty state.
        """
        self.elementos.clear()
        
    def obtener_todos(self):
        """
        Get all elements in the stack without modifying it.
        
        Returns a copy of all elements from top to bottom (most recent first).
        
        Returns:
            list: List of all loan records in the stack (copy)
        """
        return self.elementos.copy()
        
    def buscar(self, isbn):
        """
        Search for a book in the loan history.
        
        Searches the stack for any loan record matching the given ISBN.
        
        Args:
            isbn (str): ISBN to search for
            
        Returns:
            list: List of all matching loan records, empty list if not found
        """
        resultados = []
        for registro in self.elementos:
            if registro["isbn"] == isbn:
                resultados.append(registro)
        return resultados
        
    def contar_prestamos_libro(self, isbn):
        """
        Count how many times a specific book has been borrowed.
        
        Args:
            isbn (str): ISBN of the book to count
            
        Returns:
            int: Number of times the book appears in loan history
        """
        return sum(1 for registro in self.elementos if registro["isbn"] == isbn)
        
    def obtener_ultimo_prestamo(self):
        """
        Get the most recent loan record.
        
        Alias for tope() method with more descriptive name.
        
        Returns:
            dict: Most recent loan record, or None if stack is empty
        """
        return self.tope()
        
    def to_dict(self):
        """
        Convert the stack to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the stack
        """
        return {
            "elementos": self.elementos.copy(),
            "capacidad_max": self.capacidad_max
        }
        
    @classmethod
    def from_dict(cls, data):
        """
        Create a Pila instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing stack data
            
        Returns:
            Pila: New stack instance with the provided data
        """
        pila = cls(capacidad_max=data.get("capacidad_max"))
        pila.elementos = data.get("elementos", [])
        return pila
        
    def __len__(self):
        """
        Get the size of the stack using len() function.
        
        Returns:
            int: Number of elements in the stack
        """
        return len(self.elementos)
        
    def __str__(self):
        """
        Return a string representation of the stack.
        
        Returns:
            str: String showing stack size and top element
        """
        if self.esta_vacia():
            return "Pila(empty)"
        return f"Pila(size={self.tamanio()}, top={self.tope()})"
        
    def __repr__(self):
        """
        Return a detailed representation of the stack.
        
        Returns:
            str: Technical representation of the stack
        """
        return f"Pila(elementos={self.tamanio()}, capacidad_max={self.capacidad_max})"
        
    def __iter__(self):
        """
        Make the stack iterable (from top to bottom).
        
        Yields:
            dict: Each loan record from most recent to oldest
        """
        for registro in reversed(self.elementos):
            yield registro