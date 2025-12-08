"""
Libro Model - Library Management System

This module defines the Libro (Book) class which represents a book entity
in the library inventory system. Each book has essential attributes like
ISBN, title, author, weight, and value.

Classes:
    Libro: Main class representing a book in the library

Author: [Your Name]
Date: December 2025
"""


class Libro:
    """
    Represents a book in the library inventory.
    
    This class encapsulates all the information related to a book including
    its identification (ISBN), bibliographic data (title, author), physical
    properties (weight), economic value, and availability status.
    
    Attributes:
        isbn (str): International Standard Book Number - unique identifier
        titulo (str): Title of the book
        autor (str): Author of the book
        peso (float): Weight of the book in kilograms
        valor (float): Economic value in Colombian pesos (COP)
        stock (int): Number of copies available
        genero (str): Literary genre of the book
        editorial (str): Publisher of the book
        anio_publicacion (int): Year of publication
    """
    
    def __init__(self, isbn, titulo, autor, peso, valor, stock=1, 
                 genero="General", editorial="Unknown", anio_publicacion=2024):
        """
        Initialize a new Libro instance.
        
        Args:
            isbn (str): Unique ISBN identifier
            titulo (str): Book title
            autor (str): Book author
            peso (float): Weight in kilograms
            valor (float): Value in Colombian pesos
            stock (int, optional): Available copies. Defaults to 1.
            genero (str, optional): Book genre. Defaults to "General".
            editorial (str, optional): Publisher. Defaults to "Unknown".
            anio_publicacion (int, optional): Publication year. Defaults to 2024.
            
        Raises:
            ValueError: If peso or valor are negative, or if ISBN is empty
        """
        if not isbn or isbn.strip() == "":
            raise ValueError("ISBN cannot be empty")
        if peso < 0:
            raise ValueError("Weight cannot be negative")
        if valor < 0:
            raise ValueError("Value cannot be negative")
        if stock < 0:
            raise ValueError("Stock cannot be negative")
            
        self.isbn = isbn.strip()
        self.titulo = titulo.strip()
        self.autor = autor.strip()
        self.peso = float(peso)
        self.valor = float(valor)
        self.stock = int(stock)
        self.genero = genero.strip()
        self.editorial = editorial.strip()
        self.anio_publicacion = int(anio_publicacion)
        
    def to_dict(self):
        """
        Convert the Libro instance to a dictionary.
        
        This method is useful for JSON serialization and data storage.
        
        Returns:
            dict: Dictionary containing all book attributes
        """
        return {
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "peso": self.peso,
            "valor": self.valor,
            "stock": self.stock,
            "genero": self.genero,
            "editorial": self.editorial,
            "anio_publicacion": self.anio_publicacion
        }
        
    @classmethod
    def from_dict(cls, data):
        """
        Create a Libro instance from a dictionary.
        
        This class method allows creating a book object from stored data.
        
        Args:
            data (dict): Dictionary containing book attributes
            
        Returns:
            Libro: New Libro instance with the provided data
        """
        return cls(
            isbn=data.get("isbn", ""),
            titulo=data.get("titulo", ""),
            autor=data.get("autor", ""),
            peso=data.get("peso", 0.0),
            valor=data.get("valor", 0.0),
            stock=data.get("stock", 1),
            genero=data.get("genero", "General"),
            editorial=data.get("editorial", "Unknown"),
            anio_publicacion=data.get("anio_publicacion", 2024)
        )
        
    def decrementar_stock(self):
        """
        Decrease the stock by one unit.
        
        This method is called when a book is loaned out.
        
        Returns:
            bool: True if stock was decremented, False if stock was already 0
        """
        if self.stock > 0:
            self.stock -= 1
            return True
        return False
        
    def incrementar_stock(self):
        """
        Increase the stock by one unit.
        
        This method is called when a book is returned to the library.
        """
        self.stock += 1
        
    def esta_disponible(self):
        """
        Check if the book is available for loan.
        
        Returns:
            bool: True if stock > 0, False otherwise
        """
        return self.stock > 0
        
    def __str__(self):
        """
        Return a string representation of the book.
        
        Returns:
            str: Formatted string with book information
        """
        return (f"ISBN: {self.isbn} | Title: {self.titulo} | "
                f"Author: {self.autor} | Stock: {self.stock}")
                
    def __repr__(self):
        """
        Return a detailed representation of the book.
        
        Returns:
            str: Technical representation showing all attributes
        """
        return (f"Libro(isbn='{self.isbn}', titulo='{self.titulo}', "
                f"autor='{self.autor}', peso={self.peso}, valor={self.valor}, "
                f"stock={self.stock})")
                
    def __eq__(self, other):
        """
        Compare two books for equality based on ISBN.
        
        Args:
            other (Libro): Another book to compare with
            
        Returns:
            bool: True if both books have the same ISBN
        """
        if not isinstance(other, Libro):
            return False
        return self.isbn == other.isbn
        
    def __lt__(self, other):
        """
        Compare two books for ordering based on ISBN.
        
        This method enables sorting books by ISBN.
        
        Args:
            other (Libro): Another book to compare with
            
        Returns:
            bool: True if this book's ISBN is less than the other's
        """
        if not isinstance(other, Libro):
            return NotImplemented
        return self.isbn < other.isbn
        
    def __hash__(self):
        """
        Return hash value based on ISBN.
        
        This allows books to be used in sets and as dictionary keys.
        
        Returns:
            int: Hash value of the ISBN
        """
        return hash(self.isbn)