"""
Reservation Manager - Library Management System

This module implements the GestorReservas class which manages book reservations
using a Queue (Cola) data structure. Reservations follow FIFO (First In, First Out)
priority when books become available.

PROJECT REQUIREMENT:
    Implement reservation waiting list as a Queue (FIFO). Users can only be
    enqueued for a reservation if the book has stock = 0 (out of stock).

Classes:
    GestorReservas: Main manager class for reservation operations

Author: [Your Name]
Date: December 2025
"""

from datetime import datetime
from estructuras_datos.cola import Cola


class GestorReservas:
    """
    Manager class for book reservation operations.
    
    This class handles all reservation-related functionality including:
    - Reservation queue management (FIFO)
    - Reservation creation and cancellation
    - Integration with loan processing
    - Validation that reservations only occur for out-of-stock books
    
    Attributes:
        archivo_handler: Utility for file operations
        gestor_inventario: Reference to inventory manager
        gestor_usuarios: Reference to user manager
        ruta_datos (str): Path to reservation data file
        cola_reservas (Cola): Queue for managing reservations (FIFO)
    """
    
    def __init__(self, archivo_handler, gestor_inventario, gestor_usuarios,
                 ruta_datos="data/reservas/reservas.json"):
        """
        Initialize the reservation manager.
        
        Args:
            archivo_handler: ArchivoHandler instance
            gestor_inventario: GestorInventario instance
            gestor_usuarios: GestorUsuarios instance
            ruta_datos (str, optional): Path to data file
        """
        self.archivo_handler = archivo_handler
        self.gestor_inventario = gestor_inventario
        self.gestor_usuarios = gestor_usuarios
        self.ruta_datos = ruta_datos
        
        # PROJECT REQUIREMENT: Waiting list as Queue (FIFO)
        self.cola_reservas = Cola()
        
        # Load existing reservations
        self.cargar_reservas()
    
    def cargar_reservas(self):
        """
        Load reservations from JSON file.
        
        PROJECT REQUIREMENT: Reservations stored in Queue structure.
        """
        try:
            datos = self.archivo_handler.cargar_json(self.ruta_datos)
            
            if datos:
                self.cola_reservas = Cola.from_dict(datos)
                print(f"✓ Loaded {self.cola_reservas.tamanio()} reservations")
            else:
                print("No reservations found. Starting with empty queue.")
                
        except Exception as e:
            print(f"Error loading reservations: {e}")
            self.cola_reservas = Cola()
    
    def crear_reserva(self, id_usuario, isbn):
        """
        Create a reservation for a book.
        
        PROJECT REQUIREMENT: Can only reserve if book stock = 0.
        
        Steps:
        1. Validate user exists
        2. Validate book exists
        3. Validate book is OUT OF STOCK (stock = 0)
        4. Validate user doesn't already have a reservation for this book
        5. Enqueue the reservation (FIFO)
        
        Args:
            id_usuario (str): User ID making the reservation
            isbn (str): ISBN of book to reserve
            
        Returns:
            dict: Result with 'exito' (bool), 'mensaje' (str), and details
        """
        try:
            # Step 1: Validate user exists
            usuario = self.gestor_usuarios.obtener_usuario(id_usuario)
            if not usuario:
                return {
                    'exito': False,
                    'mensaje': f"User {id_usuario} not found"
                }
            
            # Step 2: Validate book exists
            libro = self.gestor_inventario.buscar_por_isbn(isbn)
            if not libro:
                return {
                    'exito': False,
                    'mensaje': f"Book with ISBN {isbn} not found"
                }
            
            # Step 3: PROJECT REQUIREMENT - Only reserve if stock = 0
            if libro.stock > 0:
                return {
                    'exito': False,
                    'mensaje': f"Book '{libro.titulo}' is available (stock: {libro.stock}). Cannot reserve available books."
                }
            
            # Step 4: Validate user doesn't already have a reservation
            if self.cola_reservas.tiene_reserva(id_usuario, isbn):
                posicion = self.cola_reservas.posicion_usuario(id_usuario, isbn)
                return {
                    'exito': False,
                    'mensaje': f"User already has a reservation for this book (position {posicion} in queue)"
                }
            
            # Step 5: Enqueue the reservation (FIFO)
            fecha_reserva = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            exito = self.cola_reservas.encolar(id_usuario, isbn, fecha_reserva)
            
            if not exito:
                return {
                    'exito': False,
                    'mensaje': "Queue is full. Cannot add more reservations."
                }
            
            # Save changes
            self.guardar_reservas()
            
            # Get position in queue
            posicion = self.cola_reservas.posicion_usuario(id_usuario, isbn)
            total_en_cola = self.cola_reservas.contar_reservas_libro(isbn)
            
            return {
                'exito': True,
                'mensaje': f"Reservation created successfully",
                'detalles': {
                    'usuario': usuario.nombre,
                    'libro': libro.titulo,
                    'isbn': isbn,
                    'fecha_reserva': fecha_reserva,
                    'posicion_en_cola': posicion,
                    'total_reservas_libro': total_en_cola
                }
            }
            
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f"Error creating reservation: {str(e)}"
            }
    
    def cancelar_reserva(self, id_usuario, isbn):
        """
        Cancel a user's reservation for a book.
        
        Args:
            id_usuario (str): User ID
            isbn (str): ISBN of reserved book
            
        Returns:
            dict: Result with 'exito' (bool) and 'mensaje' (str)
        """
        try:
            # Validate reservation exists
            if not self.cola_reservas.tiene_reserva(id_usuario, isbn):
                return {
                    'exito': False,
                    'mensaje': f"User {id_usuario} does not have a reservation for ISBN {isbn}"
                }
            
            # Remove the reservation
            exito = self.cola_reservas.remover_reserva(id_usuario, isbn)
            
            if exito:
                self.guardar_reservas()
                return {
                    'exito': True,
                    'mensaje': "Reservation cancelled successfully"
                }
            else:
                return {
                    'exito': False,
                    'mensaje': "Error removing reservation from queue"
                }
                
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f"Error cancelling reservation: {str(e)}"
            }
    
    def obtener_reservas_usuario(self, id_usuario):
        """
        Get all reservations for a specific user.
        
        Args:
            id_usuario (str): User ID
            
        Returns:
            list: List of reservation records for the user
        """
        return self.cola_reservas.buscar_usuario(id_usuario)
    
    def obtener_reservas_libro(self, isbn):
        """
        Get all reservations for a specific book.
        
        Args:
            isbn (str): ISBN of the book
            
        Returns:
            list: List of reservation records for the book (in FIFO order)
        """
        return self.cola_reservas.buscar_libro(isbn)
    
    def obtener_siguiente_usuario(self, isbn):
        """
        Get the next user in line for a book.
        
        This shows who will get the book when it becomes available,
        following FIFO priority.
        
        Args:
            isbn (str): ISBN of the book
            
        Returns:
            dict or None: Next user's reservation record
        """
        return self.cola_reservas.obtener_siguiente_usuario(isbn)
    
    def obtener_posicion_en_cola(self, id_usuario, isbn):
        """
        Get a user's position in the queue for a specific book.
        
        Args:
            id_usuario (str): User ID
            isbn (str): ISBN of the book
            
        Returns:
            int: Position in queue (1-based), or -1 if not found
        """
        return self.cola_reservas.posicion_usuario(id_usuario, isbn)
    
    def listar_todas_reservas(self):
        """
        List all reservations in the queue.
        
        Returns:
            list: All reservation records in FIFO order
        """
        return self.cola_reservas.obtener_todos()
    
    def contar_reservas_libro(self, isbn):
        """
        Count how many reservations exist for a book.
        
        Args:
            isbn (str): ISBN of the book
            
        Returns:
            int: Number of reservations for this book
        """
        return self.cola_reservas.contar_reservas_libro(isbn)
    
    def obtener_libros_mas_reservados(self, limite=10):
        """
        Get books with most reservations.
        
        Args:
            limite (int, optional): Number of books to return. Defaults to 10.
            
        Returns:
            list: List of tuples (isbn, count) sorted by count descending
        """
        conteo = {}
        
        for reserva in self.cola_reservas.obtener_todos():
            isbn = reserva['isbn']
            conteo[isbn] = conteo.get(isbn, 0) + 1
        
        # Sort by count descending
        libros_ordenados = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
        
        return libros_ordenados[:limite]
    
    def obtener_estadisticas(self):
        """
        Get comprehensive reservation statistics.
        
        Returns:
            dict: Dictionary with various statistics
        """
        total_reservas = self.cola_reservas.tamanio()
        
        if total_reservas == 0:
            return {
                'total_reservas': 0,
                'usuarios_unicos': 0,
                'libros_unicos': 0,
                'promedio_reservas_por_libro': 0
            }
        
        # Count unique users and books
        usuarios = set()
        libros = set()
        
        for reserva in self.cola_reservas.obtener_todos():
            usuarios.add(reserva['id_usuario'])
            libros.add(reserva['isbn'])
        
        return {
            'total_reservas': total_reservas,
            'usuarios_unicos': len(usuarios),
            'libros_unicos': len(libros),
            'promedio_reservas_por_libro': round(total_reservas / len(libros), 2) if libros else 0
        }
    
    def validar_puede_reservar(self, id_usuario, isbn):
        """
        Validate if a user can make a reservation.
        
        Args:
            id_usuario (str): User ID
            isbn (str): ISBN of book
            
        Returns:
            dict: Validation result with details
        """
        # Check user
        usuario = self.gestor_usuarios.obtener_usuario(id_usuario)
        if not usuario:
            return {
                'puede_reservar': False,
                'razon': "User not found"
            }
        
        # Check book
        libro = self.gestor_inventario.buscar_por_isbn(isbn)
        if not libro:
            return {
                'puede_reservar': False,
                'razon': "Book not found"
            }
        
        # Check stock (PROJECT REQUIREMENT: Only reserve if stock = 0)
        if libro.stock > 0:
            return {
                'puede_reservar': False,
                'razon': f"Book is available (stock: {libro.stock}). Cannot reserve available books."
            }
        
        # Check if already reserved
        if self.cola_reservas.tiene_reserva(id_usuario, isbn):
            posicion = self.cola_reservas.posicion_usuario(id_usuario, isbn)
            return {
                'puede_reservar': False,
                'razon': f"Already reserved (position {posicion} in queue)"
            }
        
        return {
            'puede_reservar': True,
            'razon': "Reservation is possible",
            'detalles': {
                'usuario': usuario.nombre,
                'libro': libro.titulo,
                'reservas_actuales': self.cola_reservas.contar_reservas_libro(isbn)
            }
        }
    
    def limpiar_reservas_libro(self, isbn):
        """
        Remove all reservations for a specific book.
        
        This might be used if a book is permanently removed from inventory.
        
        Args:
            isbn (str): ISBN of the book
            
        Returns:
            int: Number of reservations removed
        """
        reservas_libro = self.cola_reservas.buscar_libro(isbn)
        contador = 0
        
        for reserva in reservas_libro:
            if self.cola_reservas.remover_reserva(reserva['id_usuario'], isbn):
                contador += 1
        
        if contador > 0:
            self.guardar_reservas()
        
        return contador
    
    def obtener_tiempo_espera_estimado(self, id_usuario, isbn):
        """
        Estimate waiting time for a reservation.
        
        This is a simple estimate based on position in queue.
        Assumes average loan duration.
        
        Args:
            id_usuario (str): User ID
            isbn (str): ISBN of book
            
        Returns:
            dict: Estimated waiting time information
        """
        if not self.cola_reservas.tiene_reserva(id_usuario, isbn):
            return {
                'tiene_reserva': False,
                'mensaje': "User does not have a reservation for this book"
            }
        
        posicion = self.cola_reservas.posicion_usuario(id_usuario, isbn)
        
        # Simple estimate: assume 14 days average loan duration
        dias_promedio_prestamo = 14
        dias_estimados = (posicion - 1) * dias_promedio_prestamo
        
        return {
            'tiene_reserva': True,
            'posicion': posicion,
            'dias_estimados': dias_estimados,
            'mensaje': f"Estimated wait: ~{dias_estimados} days (position {posicion})"
        }
    
    def guardar_reservas(self):
        """
        Save reservations to JSON file.
        
        Converts Cola (Queue) object to dictionary for serialization.
        """
        try:
            datos = self.cola_reservas.to_dict()
            self.archivo_handler.guardar_json(self.ruta_datos, datos)
            return True
            
        except Exception as e:
            print(f"Error saving reservations: {e}")
            return False