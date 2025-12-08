"""
Cola (Queue) Data Structure - Library Management System

This module implements a Queue (FIFO - First In, First Out) data structure
using Object-Oriented Programming principles. The queue is used to manage
the waiting list for books that are out of stock.

When a book has zero stock, users can be enqueued to reserve it. When the
book is returned, the first user in the queue is dequeued and gets priority.

Classes:
    Cola: Queue implementation with enqueue, dequeue, peek, and utility methods

Author: [Your Name]
Date: December 2025
"""

from datetime import datetime


class Cola:
    """
    Queue (FIFO) implementation for managing reservation waiting list.
    
    This class implements a queue data structure where elements are added
    at the rear and removed from the front following First In, First Out principle.
    Used specifically for managing book reservations when stock is zero.
    
    Attributes:
        elementos (list): Internal list storing queue elements
        capacidad_max (int): Maximum number of elements allowed (None for unlimited)
    """
    
    def __init__(self, capacidad_max=None):
        """
        Initialize an empty queue.
        
        Args:
            capacidad_max (int, optional): Maximum queue size. Defaults to None (unlimited).
        """
        self.elementos = []
        self.capacidad_max = capacidad_max
        
    def encolar(self, id_usuario, isbn, fecha=None):
        """
        Enqueue a reservation request.
        
        Adds a new reservation to the rear of the queue. Each reservation contains
        the user ID, book ISBN, and reservation date.
        
        Args:
            id_usuario (str): ID of the user requesting the reservation
            isbn (str): ISBN of the book to reserve
            fecha (str, optional): Reservation date in ISO format. Defaults to current date.
            
        Returns:
            bool: True if element was enqueued successfully, False if queue is full
            
        Raises:
            ValueError: If id_usuario or ISBN is empty
        """
        if not id_usuario or id_usuario.strip() == "":
            raise ValueError("User ID cannot be empty")
        if not isbn or isbn.strip() == "":
            raise ValueError("ISBN cannot be empty")
            
        if self.esta_llena():
            return False
            
        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        registro = {
            "id_usuario": id_usuario.strip(),
            "isbn": isbn.strip(),
            "fecha": fecha
        }
        
        self.elementos.append(registro)
        return True
        
    def desencolar(self):
        """
        Dequeue the first reservation from the queue.
        
        Removes and returns the element at the front of the queue (oldest reservation).
        
        Returns:
            dict: Dictionary with 'id_usuario', 'isbn', and 'fecha', or None if queue is empty
        """
        if self.esta_vacia():
            return None
        return self.elementos.pop(0)
        
    def frente(self):
        """
        Get the front element without removing it (peek operation).
        
        Returns the first reservation in line without modifying the queue.
        
        Returns:
            dict: Dictionary with 'id_usuario', 'isbn', and 'fecha', or None if queue is empty
        """
        if self.esta_vacia():
            return None
        return self.elementos[0]
        
    def esta_vacia(self):
        """
        Check if the queue is empty.
        
        Returns:
            bool: True if queue has no elements, False otherwise
        """
        return len(self.elementos) == 0
        
    def esta_llena(self):
        """
        Check if the queue has reached maximum capacity.
        
        Returns:
            bool: True if queue is full, False otherwise (or if unlimited)
        """
        if self.capacidad_max is None:
            return False
        return len(self.elementos) >= self.capacidad_max
        
    def tamanio(self):
        """
        Get the current number of elements in the queue.
        
        Returns:
            int: Number of elements currently in the queue
        """
        return len(self.elementos)
        
    def vaciar(self):
        """
        Remove all elements from the queue.
        
        Clears the entire queue, resetting it to empty state.
        """
        self.elementos.clear()
        
    def obtener_todos(self):
        """
        Get all elements in the queue without modifying it.
        
        Returns a copy of all elements from front to rear (oldest first).
        
        Returns:
            list: List of all reservation records in the queue (copy)
        """
        return self.elementos.copy()
        
    def buscar_usuario(self, id_usuario):
        """
        Search for all reservations by a specific user.
        
        Args:
            id_usuario (str): User ID to search for
            
        Returns:
            list: List of all reservation records for the user
        """
        resultados = []
        for registro in self.elementos:
            if registro["id_usuario"] == id_usuario:
                resultados.append(registro)
        return resultados
        
    def buscar_libro(self, isbn):
        """
        Search for all reservations for a specific book.
        
        Args:
            isbn (str): ISBN of the book to search for
            
        Returns:
            list: List of all reservation records for the book
        """
        resultados = []
        for registro in self.elementos:
            if registro["isbn"] == isbn:
                resultados.append(registro)
        return resultados
        
    def tiene_reserva(self, id_usuario, isbn):
        """
        Check if a user already has a reservation for a specific book.
        
        Args:
            id_usuario (str): User ID to check
            isbn (str): ISBN of the book
            
        Returns:
            bool: True if user has a reservation for this book, False otherwise
        """
        for registro in self.elementos:
            if registro["id_usuario"] == id_usuario and registro["isbn"] == isbn:
                return True
        return False
        
    def posicion_usuario(self, id_usuario, isbn):
        """
        Get the position of a user in the queue for a specific book.
        
        Args:
            id_usuario (str): User ID to find
            isbn (str): ISBN of the book
            
        Returns:
            int: Position in queue (1-based), or -1 if not found
        """
        for index, registro in enumerate(self.elementos):
            if registro["id_usuario"] == id_usuario and registro["isbn"] == isbn:
                return index + 1  # 1-based position
        return -1
        
    def contar_reservas_libro(self, isbn):
        """
        Count how many reservations exist for a specific book.
        
        Args:
            isbn (str): ISBN of the book to count
            
        Returns:
            int: Number of reservations for this book
        """
        return sum(1 for registro in self.elementos if registro["isbn"] == isbn)
        
    def remover_reserva(self, id_usuario, isbn):
        """
        Remove a specific reservation from the queue.
        
        Allows canceling a reservation before it's processed.
        
        Args:
            id_usuario (str): User ID
            isbn (str): ISBN of the book
            
        Returns:
            bool: True if reservation was found and removed, False otherwise
        """
        for i, registro in enumerate(self.elementos):
            if registro["id_usuario"] == id_usuario and registro["isbn"] == isbn:
                self.elementos.pop(i)
                return True
        return False
        
    def obtener_siguiente_usuario(self, isbn):
        """
        Get the next user in line for a specific book.
        
        Useful for checking who will get the book when it becomes available.
        
        Args:
            isbn (str): ISBN of the book
            
        Returns:
            dict: Reservation record of the next user, or None if no reservations
        """
        for registro in self.elementos:
            if registro["isbn"] == isbn:
                return registro
        return None
        
    def to_dict(self):
        """
        Convert the queue to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the queue
        """
        return {
            "elementos": self.elementos.copy(),
            "capacidad_max": self.capacidad_max
        }
        
    @classmethod
    def from_dict(cls, data):
        """
        Create a Cola instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing queue data
            
        Returns:
            Cola: New queue instance with the provided data
        """
        cola = cls(capacidad_max=data.get("capacidad_max"))
        cola.elementos = data.get("elementos", [])
        return cola
        
    def __len__(self):
        """
        Get the size of the queue using len() function.
        
        Returns:
            int: Number of elements in the queue
        """
        return len(self.elementos)
        
    def __str__(self):
        """
        Return a string representation of the queue.
        
        Returns:
            str: String showing queue size and front element
        """
        if self.esta_vacia():
            return "Cola(empty)"
        return f"Cola(size={self.tamanio()}, front={self.frente()})"
        
    def __repr__(self):
        """
        Return a detailed representation of the queue.
        
        Returns:
            str: Technical representation of the queue
        """
        return f"Cola(elementos={self.tamanio()}, capacidad_max={self.capacidad_max})"
        
    def __iter__(self):
        """
        Make the queue iterable (from front to rear).
        
        Yields:
            dict: Each reservation record from oldest to newest
        """
        for registro in self.elementos:
            yield registro