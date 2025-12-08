"""
Usuario Model - Library Management System

This module defines the Usuario (User) class which represents a user entity
in the library management system. Each user can borrow books, have a loan
history, and be placed in reservation queues.

Classes:
    Usuario: Main class representing a library user

Author: [Your Name]
Date: December 2025
"""

from datetime import datetime


class Usuario:
    """
    Represents a user in the library system.
    
    This class encapsulates all the information related to a library user
    including personal information, loan history, and reservation status.
    
    Attributes:
        id_usuario (str): Unique identifier for the user
        nombre (str): Full name of the user
        email (str): Email address for contact
        telefono (str): Phone number
        direccion (str): Physical address
        fecha_registro (str): Date when user registered (ISO format)
        activo (bool): Whether the user account is active
        libros_prestados (int): Number of books currently on loan
        max_prestamos (int): Maximum number of simultaneous loans allowed
    """
    
    def __init__(self, id_usuario, nombre, email, telefono="", direccion="",
                 fecha_registro=None, activo=True, libros_prestados=0, max_prestamos=3):
        """
        Initialize a new Usuario instance.
        
        Args:
            id_usuario (str): Unique user identifier
            nombre (str): User's full name
            email (str): User's email address
            telefono (str, optional): Phone number. Defaults to "".
            direccion (str, optional): Physical address. Defaults to "".
            fecha_registro (str, optional): Registration date. Defaults to current date.
            activo (bool, optional): Account status. Defaults to True.
            libros_prestados (int, optional): Current loans. Defaults to 0.
            max_prestamos (int, optional): Max simultaneous loans. Defaults to 3.
            
        Raises:
            ValueError: If required fields are empty or invalid
        """
        if not id_usuario or id_usuario.strip() == "":
            raise ValueError("User ID cannot be empty")
        if not nombre or nombre.strip() == "":
            raise ValueError("Name cannot be empty")
        if not email or email.strip() == "":
            raise ValueError("Email cannot be empty")
        if max_prestamos < 1:
            raise ValueError("Maximum loans must be at least 1")
        if libros_prestados < 0:
            raise ValueError("Number of loaned books cannot be negative")
            
        self.id_usuario = id_usuario.strip()
        self.nombre = nombre.strip()
        self.email = email.strip()
        self.telefono = telefono.strip()
        self.direccion = direccion.strip()
        self.fecha_registro = fecha_registro or datetime.now().strftime("%Y-%m-%d")
        self.activo = bool(activo)
        self.libros_prestados = int(libros_prestados)
        self.max_prestamos = int(max_prestamos)
        
    def to_dict(self):
        """
        Convert the Usuario instance to a dictionary.
        
        This method is useful for JSON serialization and data storage.
        
        Returns:
            dict: Dictionary containing all user attributes
        """
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "fecha_registro": self.fecha_registro,
            "activo": self.activo,
            "libros_prestados": self.libros_prestados,
            "max_prestamos": self.max_prestamos
        }
        
    @classmethod
    def from_dict(cls, data):
        """
        Create a Usuario instance from a dictionary.
        
        This class method allows creating a user object from stored data.
        
        Args:
            data (dict): Dictionary containing user attributes
            
        Returns:
            Usuario: New Usuario instance with the provided data
        """
        return cls(
            id_usuario=data.get("id_usuario", ""),
            nombre=data.get("nombre", ""),
            email=data.get("email", ""),
            telefono=data.get("telefono", ""),
            direccion=data.get("direccion", ""),
            fecha_registro=data.get("fecha_registro"),
            activo=data.get("activo", True),
            libros_prestados=data.get("libros_prestados", 0),
            max_prestamos=data.get("max_prestamos", 3)
        )
        
    def puede_prestar(self):
        """
        Check if the user can borrow more books.
        
        A user can borrow books if their account is active and they haven't
        reached the maximum number of simultaneous loans.
        
        Returns:
            bool: True if user can borrow, False otherwise
        """
        return self.activo and self.libros_prestados < self.max_prestamos
        
    def incrementar_prestamos(self):
        """
        Increment the count of borrowed books by one.
        
        This method is called when a user borrows a new book.
        
        Returns:
            bool: True if increment was successful, False if max reached
        """
        if self.puede_prestar():
            self.libros_prestados += 1
            return True
        return False
        
    def decrementar_prestamos(self):
        """
        Decrement the count of borrowed books by one.
        
        This method is called when a user returns a book.
        
        Returns:
            bool: True if decrement was successful, False if count was already 0
        """
        if self.libros_prestados > 0:
            self.libros_prestados -= 1
            return True
        return False
        
    def desactivar(self):
        """
        Deactivate the user account.
        
        A deactivated user cannot borrow new books.
        """
        self.activo = False
        
    def activar(self):
        """
        Activate the user account.
        
        Allows a previously deactivated user to borrow books again.
        """
        self.activo = True
        
    def tiene_prestamos_pendientes(self):
        """
        Check if the user has pending loans.
        
        Returns:
            bool: True if user has books currently on loan, False otherwise
        """
        return self.libros_prestados > 0
        
    def obtener_cupo_disponible(self):
        """
        Get the number of additional books the user can borrow.
        
        Returns:
            int: Number of books that can still be borrowed
        """
        return self.max_prestamos - self.libros_prestados
        
    def __str__(self):
        """
        Return a string representation of the user.
        
        Returns:
            str: Formatted string with user information
        """
        status = "Active" if self.activo else "Inactive"
        return (f"ID: {self.id_usuario} | Name: {self.nombre} | "
                f"Email: {self.email} | Status: {status} | "
                f"Loans: {self.libros_prestados}/{self.max_prestamos}")
                
    def __repr__(self):
        """
        Return a detailed representation of the user.
        
        Returns:
            str: Technical representation showing all attributes
        """
        return (f"Usuario(id_usuario='{self.id_usuario}', nombre='{self.nombre}', "
                f"email='{self.email}', activo={self.activo}, "
                f"libros_prestados={self.libros_prestados})")
                
    def __eq__(self, other):
        """
        Compare two users for equality based on user ID.
        
        Args:
            other (Usuario): Another user to compare with
            
        Returns:
            bool: True if both users have the same ID
        """
        if not isinstance(other, Usuario):
            return False
        return self.id_usuario == other.id_usuario
        
    def __hash__(self):
        """
        Return hash value based on user ID.
        
        This allows users to be used in sets and as dictionary keys.
        
        Returns:
            int: Hash value of the user ID
        """
        return hash(self.id_usuario)