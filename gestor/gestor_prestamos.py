"""
Loan Manager - Library Management System

This module implements the GestorPrestamos class which manages all loan
operations in the library system. This is a CRITICAL component as it
integrates the binary search algorithm with the reservation queue.

PROJECT CRITICAL REQUIREMENT:
    When a book is returned, the result of binary search (position or not found)
    MUST be used to verify if the returned book has pending reservations in the
    queue. If reservations exist, the book must be assigned to the first person
    in the waiting list according to FIFO priority.

Classes:
    GestorPrestamos: Main manager class for loan operations

Author: [Your Name]
Date: December 2025
"""

from datetime import datetime
from estructuras_datos.pila import Pila
from algoritmos_busqueda.busqueda_binaria import verificar_y_asignar_reserva


class GestorPrestamos:
    """
    Manager class for book loan operations.
    
    This class handles all loan-related functionality including:
    - Loan creation and validation
    - Return processing with reservation checking (CRITICAL)
    - Loan history per user (using Stack/Pila)
    - Integration with inventory and user managers
    
    Attributes:
        archivo_handler: Utility for file operations
        gestor_inventario: Reference to inventory manager
        gestor_usuarios: Reference to user manager
        gestor_reservas: Reference to reservation manager
        ruta_datos (str): Path to loan data file
        historial_prestamos (dict): Dictionary mapping user IDs to Pila (Stack)
    """
    
    def __init__(self, archivo_handler, gestor_inventario, gestor_usuarios, 
                 gestor_reservas, ruta_datos="data/prestamos/prestamos.json"):
        """
        Initialize the loan manager.
        
        Args:
            archivo_handler: ArchivoHandler instance
            gestor_inventario: GestorInventario instance
            gestor_usuarios: GestorUsuarios instance
            gestor_reservas: GestorReservas instance
            ruta_datos (str, optional): Path to data file
        """
        self.archivo_handler = archivo_handler
        self.gestor_inventario = gestor_inventario
        self.gestor_usuarios = gestor_usuarios
        self.gestor_reservas = gestor_reservas
        self.ruta_datos = ruta_datos
        
        # PROJECT REQUIREMENT: Loan history per user using Stack (Pila)
        self.historial_prestamos = {}  # Maps user_id -> Pila
        
        # Load existing loan history
        self.cargar_historial()
    
    def cargar_historial(self):
        """
        Load loan history from JSON file.
        
        PROJECT REQUIREMENT: Loan history is stored as Stack (Pila) per user.
        """
        try:
            datos = self.archivo_handler.cargar_json(self.ruta_datos)
            
            if datos:
                # Reconstruct Pila for each user
                for user_id, historial_data in datos.items():
                    pila = Pila.from_dict(historial_data)
                    self.historial_prestamos[user_id] = pila
                
                print(f"✓ Loaded loan history for {len(self.historial_prestamos)} users")
            else:
                print("No loan history found. Starting fresh.")
                
        except Exception as e:
            print(f"Error loading loan history: {e}")
            self.historial_prestamos = {}
    
    def crear_prestamo(self, id_usuario, isbn):
        """
        Create a new loan for a user.
        
        This function:
        1. Validates user can borrow
        2. Validates book is available
        3. Decrements book stock
        4. Increments user's loan count
        5. Adds to user's loan history (Stack/Pila)
        
        Args:
            id_usuario (str): User ID
            isbn (str): ISBN of book to borrow
            
        Returns:
            dict: Result with 'exito' (bool), 'mensaje' (str), and details
        """
        try:
            # Step 1: Validate user exists and can borrow
            usuario = self.gestor_usuarios.obtener_usuario(id_usuario)
            if not usuario:
                return {
                    'exito': False,
                    'mensaje': f"User {id_usuario} not found"
                }
            
            validacion = self.gestor_usuarios.validar_puede_prestar(id_usuario)
            if not validacion['puede_prestar']:
                return {
                    'exito': False,
                    'mensaje': validacion['razon']
                }
            
            # Step 2: Validate book exists and is available
            libro = self.gestor_inventario.buscar_por_isbn(isbn)
            if not libro:
                return {
                    'exito': False,
                    'mensaje': f"Book with ISBN {isbn} not found"
                }
            
            if not libro.esta_disponible():
                return {
                    'exito': False,
                    'mensaje': f"Book '{libro.titulo}' is not available (stock: {libro.stock})"
                }
            
            # Step 3: Process the loan
            fecha_prestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Decrement book stock
            libro.decrementar_stock()
            
            # Increment user's loan count
            usuario.incrementar_prestamos()
            
            # Add to user's loan history (Stack/Pila)
            if id_usuario not in self.historial_prestamos:
                self.historial_prestamos[id_usuario] = Pila()
            
            self.historial_prestamos[id_usuario].apilar(isbn, fecha_prestamo)
            
            # Save all changes
            self.gestor_inventario.guardar_inventario()
            self.gestor_usuarios.guardar_usuarios()
            self.guardar_historial()
            
            return {
                'exito': True,
                'mensaje': f"Loan created successfully",
                'detalles': {
                    'usuario': usuario.nombre,
                    'libro': libro.titulo,
                    'isbn': isbn,
                    'fecha': fecha_prestamo,
                    'prestamos_actuales': usuario.libros_prestados,
                    'stock_restante': libro.stock
                }
            }
            
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f"Error creating loan: {str(e)}"
            }
    
    def devolver_libro(self, id_usuario, isbn):
        """
        Process a book return.
        
        CRITICAL PROJECT REQUIREMENT:
        This function MUST use binary search to find the book in the sorted
        inventory and then verify if there are pending reservations. If
        reservations exist, assign the book to the first person in the queue.
        
        Steps:
        1. Validate loan exists in user's history
        2. Increment book stock
        3. Decrement user's loan count
        4. USE BINARY SEARCH to find book and CHECK RESERVATIONS
        5. If reservations exist, assign to first user in queue (FIFO)
        
        Args:
            id_usuario (str): User ID returning the book
            isbn (str): ISBN of book being returned
            
        Returns:
            dict: Result with 'exito' (bool), 'mensaje' (str), and details
        """
        try:
            # Step 1: Validate user and book exist
            usuario = self.gestor_usuarios.obtener_usuario(id_usuario)
            if not usuario:
                return {
                    'exito': False,
                    'mensaje': f"User {id_usuario} not found"
                }
            
            libro = self.gestor_inventario.buscar_por_isbn(isbn)
            if not libro:
                return {
                    'exito': False,
                    'mensaje': f"Book with ISBN {isbn} not found"
                }
            
            # Step 2: Validate user has this loan
            if id_usuario not in self.historial_prestamos or \
               self.historial_prestamos[id_usuario].esta_vacia():
                return {
                    'exito': False,
                    'mensaje': f"User has no loan history"
                }
            
            # Check if this book is in user's loan history
            historial_usuario = self.historial_prestamos[id_usuario]
            libros_prestados = [prestamo['isbn'] for prestamo in historial_usuario.obtener_todos()]
            
            if isbn not in libros_prestados:
                return {
                    'exito': False,
                    'mensaje': f"User {id_usuario} does not have this book on loan"
                }
            
            # Step 3: Process the return
            fecha_devolucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Increment book stock (book is now available)
            libro.incrementar_stock()
            
            # Decrement user's loan count
            usuario.decrementar_prestamos()
            
            # Save changes to inventory and users
            self.gestor_inventario.guardar_inventario()
            self.gestor_usuarios.guardar_usuarios()
            
            # Step 4: CRITICAL - Use binary search to verify reservations
            # PROJECT REQUIREMENT: Binary search result must be used to check reservations
            resultado_verificacion = verificar_y_asignar_reserva(
                isbn,
                self.gestor_inventario.inventario_ordenado,
                self.gestor_reservas.cola_reservas,
                self  # Pass self as gestor_prestamos for automatic loan processing
            )
            
            resultado = {
                'exito': True,
                'mensaje': f"Book returned successfully",
                'detalles': {
                    'usuario': usuario.nombre,
                    'libro': libro.titulo,
                    'isbn': isbn,
                    'fecha_devolucion': fecha_devolucion,
                    'stock_actual': libro.stock,
                    'prestamos_actuales_usuario': usuario.libros_prestados
                }
            }
            
            # Step 5: If there were reservations, add info to result
            if resultado_verificacion['tiene_reservas']:
                resultado['reserva_asignada'] = True
                resultado['detalles']['usuario_asignado'] = resultado_verificacion['usuario_asignado']
                resultado['mensaje'] += f" - Assigned to reserved user: {resultado_verificacion['usuario_asignado']}"
            else:
                resultado['reserva_asignada'] = False
                resultado['mensaje'] += " - Book is now available for general loan"
            
            return resultado
            
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f"Error processing return: {str(e)}"
            }
    
    def procesar_prestamo_automatico(self, id_usuario, isbn):
        """
        Process an automatic loan when a reserved book becomes available.
        
        This method is called by verificar_y_asignar_reserva when processing
        reservations. It creates a loan without the usual validations since
        the book was reserved.
        
        Args:
            id_usuario (str): User ID who reserved the book
            isbn (str): ISBN of the reserved book
            
        Returns:
            bool: True if loan was processed successfully
        """
        try:
            usuario = self.gestor_usuarios.obtener_usuario(id_usuario)
            libro = self.gestor_inventario.buscar_por_isbn(isbn)
            
            if not usuario or not libro:
                return False
            
            # Check if user can still borrow
            if not usuario.puede_prestar():
                # User reached max loans, put book back in stock
                libro.incrementar_stock()
                self.gestor_inventario.guardar_inventario()
                return False
            
            fecha_prestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Book stock was already decremented by verificar_y_asignar_reserva
            # Just update user and history
            usuario.incrementar_prestamos()
            
            # Add to user's loan history
            if id_usuario not in self.historial_prestamos:
                self.historial_prestamos[id_usuario] = Pila()
            
            self.historial_prestamos[id_usuario].apilar(isbn, fecha_prestamo)
            
            # Save changes
            self.gestor_usuarios.guardar_usuarios()
            self.guardar_historial()
            
            print(f"✓ Automatic loan created for reserved book: {usuario.nombre} - {libro.titulo}")
            return True
            
        except Exception as e:
            print(f"Error processing automatic loan: {e}")
            return False
    
    def obtener_historial_usuario(self, id_usuario):
        """
        Get a user's complete loan history.
        
        PROJECT REQUIREMENT: History is stored as Stack (Pila) - LIFO.
        
        Args:
            id_usuario (str): User ID
            
        Returns:
            list: List of loans (most recent first)
        """
        if id_usuario not in self.historial_prestamos:
            return []
        
        pila = self.historial_prestamos[id_usuario]
        return pila.obtener_todos()[::-1]  # Reverse to show most recent first
    
    def obtener_prestamo_mas_reciente(self, id_usuario):
        """
        Get the most recent loan for a user.
        
        Uses the Stack (Pila) tope() method to get the top element.
        
        Args:
            id_usuario (str): User ID
            
        Returns:
            dict or None: Most recent loan record
        """
        if id_usuario not in self.historial_prestamos:
            return None
        
        return self.historial_prestamos[id_usuario].tope()
    
    def contar_prestamos_libro(self, isbn):
        """
        Count how many times a book has been loaned.
        
        Args:
            isbn (str): ISBN of the book
            
        Returns:
            int: Total number of times the book was loaned
        """
        total = 0
        
        for pila in self.historial_prestamos.values():
            total += pila.contar_prestamos_libro(isbn)
        
        return total
    
    def obtener_libros_mas_prestados(self, limite=10):
        """
        Get the most frequently loaned books.
        
        Args:
            limite (int, optional): Number of books to return. Defaults to 10.
            
        Returns:
            list: List of tuples (isbn, count) sorted by count
        """
        conteo = {}
        
        for pila in self.historial_prestamos.values():
            for prestamo in pila.obtener_todos():
                isbn = prestamo['isbn']
                conteo[isbn] = conteo.get(isbn, 0) + 1
        
        # Sort by count descending
        libros_ordenados = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
        
        return libros_ordenados[:limite]
    
    def obtener_estadisticas(self):
        """
        Get comprehensive loan statistics.
        
        Returns:
            dict: Dictionary with various statistics
        """
        total_usuarios_con_historial = len(self.historial_prestamos)
        total_prestamos_historicos = sum(
            pila.tamanio() for pila in self.historial_prestamos.values()
        )
        
        # Current active loans (from user objects)
        prestamos_activos = sum(
            usuario.libros_prestados 
            for usuario in self.gestor_usuarios.listar_todos()
        )
        
        return {
            'total_usuarios_con_historial': total_usuarios_con_historial,
            'total_prestamos_historicos': total_prestamos_historicos,
            'prestamos_activos': prestamos_activos,
            'prestamos_completados': total_prestamos_historicos - prestamos_activos
        }
    
    def guardar_historial(self):
        """
        Save loan history to JSON file.
        
        Converts all Pila (Stack) objects to dictionaries for serialization.
        """
        try:
            datos = {}
            
            for user_id, pila in self.historial_prestamos.items():
                datos[user_id] = pila.to_dict()
            
            self.archivo_handler.guardar_json(self.ruta_datos, datos)
            return True
            
        except Exception as e:
            print(f"Error saving loan history: {e}")
            return False
    
    def validar_prestamo_posible(self, id_usuario, isbn):
        """
        Validate if a loan is possible without actually creating it.
        
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
                'valido': False,
                'razon': "User not found"
            }
        
        validacion_usuario = self.gestor_usuarios.validar_puede_prestar(id_usuario)
        if not validacion_usuario['puede_prestar']:
            return {
                'valido': False,
                'razon': validacion_usuario['razon']
            }
        
        # Check book
        libro = self.gestor_inventario.buscar_por_isbn(isbn)
        if not libro:
            return {
                'valido': False,
                'razon': "Book not found"
            }
        
        if not libro.esta_disponible():
            return {
                'valido': False,
                'razon': f"Book not available (stock: {libro.stock})"
            }
        
        return {
            'valido': True,
            'razon': "Loan is possible",
            'detalles': {
                'usuario': usuario.nombre,
                'libro': libro.titulo,
                'cupo_restante': usuario.obtener_cupo_disponible(),
                'stock_libro': libro.stock
            }
        }