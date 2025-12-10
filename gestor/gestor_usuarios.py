"""
User Manager - Library Management System

This module implements the GestorUsuarios class which manages all user
operations in the library system including registration, authentication,
and user status management.

Classes:
    GestorUsuarios: Main manager class for user operations

Author: [Your Name]
Date: December 2025
"""

from models.usuario import Usuario


class GestorUsuarios:
    """
    Manager class for user operations.
    
    This class handles all user-related functionality including:
    - User registration and CRUD operations
    - User authentication and validation
    - Active/inactive status management
    - Loan capacity tracking
    
    Attributes:
        archivo_handler: Utility for file operations
        ruta_datos (str): Path to user data file
        usuarios (dict): Dictionary mapping user IDs to User objects
    """
    
    def __init__(self, archivo_handler, ruta_datos="data/usuarios/usuarios.json"):
        """
        Initialize the user manager.
        
        Args:
            archivo_handler: ArchivoHandler instance for file operations
            ruta_datos (str, optional): Path to data file. Defaults to "data/usuarios/usuarios.json".
        """
        self.archivo_handler = archivo_handler
        self.ruta_datos = ruta_datos
        self.usuarios = {}  # Dictionary for O(1) lookup by ID
        
        # Load existing users
        self.cargar_usuarios()
    
    def cargar_usuarios(self):
        """
        Load users from JSON file.
        """
        try:
            datos = self.archivo_handler.cargar_json(self.ruta_datos)
            
            if datos:
                for usuario_dict in datos:
                    usuario = Usuario.from_dict(usuario_dict)
                    self.usuarios[usuario.id_usuario] = usuario
                
                print(f"✓ Loaded {len(self.usuarios)} users from {self.ruta_datos}")
            else:
                print(f"No users found in {self.ruta_datos}. Starting with empty user database.")
                
        except Exception as e:
            print(f"Error loading users: {e}")
            self.usuarios = {}
    
    def registrar_usuario(self, id_usuario, nombre, email, telefono="", direccion="", max_prestamos=3):
        """
        Register a new user in the system.
        
        Args:
            id_usuario (str): Unique user identifier
            nombre (str): Full name
            email (str): Email address
            telefono (str, optional): Phone number. Defaults to "".
            direccion (str, optional): Address. Defaults to "".
            max_prestamos (int, optional): Max simultaneous loans. Defaults to 3.
            
        Returns:
            dict: Result with 'exito' (bool) and 'mensaje' (str)
        """
        try:
            # Check if user ID already exists
            if id_usuario in self.usuarios:
                return {
                    'exito': False,
                    'mensaje': f"User ID {id_usuario} already exists"
                }
            
            # Check if email already exists
            if self.buscar_por_email(email):
                return {
                    'exito': False,
                    'mensaje': f"Email {email} is already registered"
                }
            
            # Create new user
            usuario = Usuario(
                id_usuario=id_usuario,
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion,
                max_prestamos=max_prestamos
            )
            
            # Add to dictionary
            self.usuarios[id_usuario] = usuario
            
            # Save to file
            self.guardar_usuarios()
            
            return {
                'exito': True,
                'mensaje': f"User {nombre} registered successfully",
                'usuario': usuario
            }
            
        except ValueError as e:
            return {
                'exito': False,
                'mensaje': f"Validation error: {str(e)}"
            }
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f"Error registering user: {str(e)}"
            }
    
    def obtener_usuario(self, id_usuario):
        """
        Get a user by their ID.
        
        Args:
            id_usuario (str): User ID to search for
            
        Returns:
            Usuario or None: User object if found, None otherwise
        """
        return self.usuarios.get(id_usuario)
    
    def buscar_por_email(self, email):
        """
        Search for a user by email address.
        
        Args:
            email (str): Email to search for
            
        Returns:
            Usuario or None: User object if found, None otherwise
        """
        email_normalizado = email.strip().lower()
        
        for usuario in self.usuarios.values():
            if usuario.email.strip().lower() == email_normalizado:
                return usuario
        
        return None
    
    def buscar_por_nombre(self, nombre):
        """
        Search for users by name (partial match).
        
        Args:
            nombre (str): Name or partial name to search for
            
        Returns:
            list: List of matching users
        """
        nombre_busqueda = nombre.strip().lower()
        resultados = []
        
        for usuario in self.usuarios.values():
            if nombre_busqueda in usuario.nombre.strip().lower():
                resultados.append(usuario)
        
        return resultados
    
    def actualizar_usuario(self, id_usuario, datos_actualizados):
        """
        Update a user's information.
        
        Args:
            id_usuario (str): User ID to update
            datos_actualizados (dict): Dictionary with fields to update
            
        Returns:
            dict: Result with 'exito' (bool) and 'mensaje' (str)
        """
        try:
            usuario = self.usuarios.get(id_usuario)
            
            if not usuario:
                return {
                    'exito': False,
                    'mensaje': f"User {id_usuario} not found"
                }
            
            # Update allowed fields (not id_usuario)
            campos_permitidos = ['nombre', 'email', 'telefono', 'direccion', 'max_prestamos']
            
            for campo, valor in datos_actualizados.items():
                if campo in campos_permitidos and hasattr(usuario, campo):
                    # Check email uniqueness if updating email
                    if campo == 'email':
                        usuario_email = self.buscar_por_email(valor)
                        if usuario_email and usuario_email.id_usuario != id_usuario:
                            return {
                                'exito': False,
                                'mensaje': f"Email {valor} is already registered"
                            }
                    
                    setattr(usuario, campo, valor)
            
            # Save changes
            self.guardar_usuarios()
            
            return {
                'exito': True,
                'mensaje': f"User {id_usuario} updated successfully"
            }
            
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f"Error updating user: {str(e)}"
            }
    
    def eliminar_usuario(self, id_usuario):
        """
        Remove a user from the system.
        
        Args:
            id_usuario (str): User ID to remove
            
        Returns:
            dict: Result with 'exito' (bool) and 'mensaje' (str)
        """
        try:
            usuario = self.usuarios.get(id_usuario)
            
            if not usuario:
                return {
                    'exito': False,
                    'mensaje': f"User {id_usuario} not found"
                }
            
            # Check if user has pending loans
            if usuario.tiene_prestamos_pendientes():
                return {
                    'exito': False,
                    'mensaje': f"User has {usuario.libros_prestados} pending loans. Cannot delete."
                }
            
            # Remove user
            del self.usuarios[id_usuario]
            
            # Save changes
            self.guardar_usuarios()
            
            return {
                'exito': True,
                'mensaje': f"User {id_usuario} deleted successfully"
            }
            
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f"Error deleting user: {str(e)}"
            }
    
    def activar_usuario(self, id_usuario):
        """
        Activate a user account.
        
        Args:
            id_usuario (str): User ID to activate
            
        Returns:
            dict: Result with 'exito' (bool) and 'mensaje' (str)
        """
        try:
            usuario = self.usuarios.get(id_usuario)
            
            if not usuario:
                return {
                    'exito': False,
                    'mensaje': f"User {id_usuario} not found"
                }
            
            usuario.activar()
            self.guardar_usuarios()
            
            return {
                'exito': True,
                'mensaje': f"User {id_usuario} activated"
            }
            
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f"Error activating user: {str(e)}"
            }
    
    def desactivar_usuario(self, id_usuario):
        """
        Deactivate a user account.
        
        Args:
            id_usuario (str): User ID to deactivate
            
        Returns:
            dict: Result with 'exito' (bool) and 'mensaje' (str)
        """
        try:
            usuario = self.usuarios.get(id_usuario)
            
            if not usuario:
                return {
                    'exito': False,
                    'mensaje': f"User {id_usuario} not found"
                }
            
            usuario.desactivar()
            self.guardar_usuarios()
            
            return {
                'exito': True,
                'mensaje': f"User {id_usuario} deactivated"
            }
            
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f"Error deactivating user: {str(e)}"
            }
    
    def listar_todos(self, solo_activos=False):
        """
        List all users in the system.
        
        Args:
            solo_activos (bool, optional): Only return active users. Defaults to False.
            
        Returns:
            list: List of users
        """
        if solo_activos:
            return [u for u in self.usuarios.values() if u.activo]
        else:
            return list(self.usuarios.values())
    
    def obtener_estadisticas(self):
        """
        Get comprehensive user statistics.
        
        Returns:
            dict: Dictionary with various statistics
        """
        total_usuarios = len(self.usuarios)
        
        if total_usuarios == 0:
            return {
                'total_usuarios': 0,
                'usuarios_activos': 0,
                'usuarios_inactivos': 0,
                'usuarios_con_prestamos': 0,
                'total_prestamos_activos': 0
            }
        
        activos = sum(1 for u in self.usuarios.values() if u.activo)
        con_prestamos = sum(1 for u in self.usuarios.values() if u.libros_prestados > 0)
        total_prestamos = sum(u.libros_prestados for u in self.usuarios.values())
        
        return {
            'total_usuarios': total_usuarios,
            'usuarios_activos': activos,
            'usuarios_inactivos': total_usuarios - activos,
            'usuarios_con_prestamos': con_prestamos,
            'total_prestamos_activos': total_prestamos
        }
    
    def validar_puede_prestar(self, id_usuario):
        """
        Validate if a user can borrow more books.
        
        Args:
            id_usuario (str): User ID to validate
            
        Returns:
            dict: Result with 'puede_prestar' (bool) and 'razon' (str)
        """
        usuario = self.usuarios.get(id_usuario)
        
        if not usuario:
            return {
                'puede_prestar': False,
                'razon': "User not found"
            }
        
        if not usuario.activo:
            return {
                'puede_prestar': False,
                'razon': "User account is inactive"
            }
        
        if not usuario.puede_prestar():
            return {
                'puede_prestar': False,
                'razon': f"User has reached maximum loans ({usuario.max_prestamos})"
            }
        
        return {
            'puede_prestar': True,
            'razon': f"User can borrow {usuario.obtener_cupo_disponible()} more book(s)"
        }
    
    def guardar_usuarios(self):
        """
        Save users to JSON file.
        """
        try:
            datos = [usuario.to_dict() for usuario in self.usuarios.values()]
            self.archivo_handler.guardar_json(self.ruta_datos, datos)
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    def actualizar_usuario(self, id_original, id_usuario, nombre, email, telefono=None, direccion=None, max_prestamos=3):
   
    # Obtener usuario existente
      usuario = self.obtener_usuario(id_original)
    
      if not usuario:
          return {'exito': False, 'mensaje': 'User not found'}
    
    # Eliminar el usuario anterior
      resultado_eliminar = self.eliminar_usuario(id_original)
    
      if resultado_eliminar['exito']:
        # Registrar el usuario actualizado manteniendo los préstamos
          resultado = self.registrar_usuario(
             id_usuario=id_usuario,
             nombre=nombre,
             email=email,
             telefono=telefono,
             direccion=direccion,
             max_prestamos=max_prestamos
         )
        
       
          if resultado['exito']:
            # Restaurar número de préstamos activos
              usuario_actualizado = self.obtener_usuario(id_usuario)
              usuario_actualizado.libros_prestados = usuario.libros_prestados
              usuario_actualizado.activo = usuario.activo
            
              return {'exito': True, 'mensaje': f'User {nombre} updated successfully'}
          else:
              return resultado
       
    
      return {'exito': False, 'mensaje': 'Could not update user'}

    def generar_id_unico(self):
        """
        Generate a unique user ID.
        
        Returns:
            str: New unique ID in format "USR####"
        """
        if not self.usuarios:
            return "USR0001"
        
        # Extract numeric parts from existing IDs
        numeros = []
        for id_usuario in self.usuarios.keys():
            try:
                if id_usuario.startswith("USR"):
                    numero = int(id_usuario[3:])
                    numeros.append(numero)
            except:
                continue
        
        if numeros:
            siguiente = max(numeros) + 1
        else:
            siguiente = 1
        
        return f"USR{siguiente:04d}"