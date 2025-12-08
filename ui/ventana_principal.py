"""
Main Window - Library Management System

This module defines the main application window that serves as the container
for all other windows. It handles navigation between different modules and
initializes all managers (gestores).

Note: The actual main window is created in main.py (BibliotecaApp class).
This module is kept for consistency but the main logic is in main.py.

Classes:
    VentanaPrincipal: Main application window (optional wrapper)

Author: [Your Name]
Date: December 2025
"""

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb

from gestor.gestor_inventario import GestorInventario
from gestor.gestor_usuarios import GestorUsuarios
from gestor.gestor_prestamos import GestorPrestamos
from gestor.gestor_reservas import GestorReservas
from utils.archivo_handler import ArchivoHandler


class VentanaPrincipal:
    """
    Main application window wrapper.
    
    This class can be used as an alternative to the BibliotecaApp in main.py,
    or as a reference for understanding the window structure.
    
    Attributes:
        root: Root window
        archivo_handler: File operations handler
        gestor_inventario: Inventory manager
        gestor_usuarios: Users manager
        gestor_reservas: Reservations manager
        gestor_prestamos: Loans manager
    """
    
    def __init__(self, root):
        """
        Initialize the main window.
        
        Args:
            root: Tkinter root window or frame
        """
        self.root = root
        
        # Initialize file handler
        self.archivo_handler = ArchivoHandler()
        
        # Initialize managers in correct order
        self.gestor_inventario = GestorInventario(self.archivo_handler)
        self.gestor_usuarios = GestorUsuarios(self.archivo_handler)
        self.gestor_reservas = GestorReservas(
            self.archivo_handler, 
            self.gestor_inventario, 
            self.gestor_usuarios
        )
        self.gestor_prestamos = GestorPrestamos(
            self.archivo_handler,
            self.gestor_inventario,
            self.gestor_usuarios,
            self.gestor_reservas
        )
        
        # Create UI
        self.create_widgets()
        
        # Show welcome message
        self.mostrar_estadisticas_iniciales()
    
    def create_widgets(self):
        """Create all widgets for the main window."""
        # Title frame
        title_frame = tk.Frame(self.root, bg="#004080", height=60)
        title_frame.pack(side="top", fill="x")
        
        title_label = tk.Label(
            title_frame,
            text="📚 Library Management System",
            font=("Helvetica", 22, "bold"),
            bg="#004080",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side="bottom", fill="x")
    
    def mostrar_estadisticas_iniciales(self):
        """Display initial system statistics."""
        try:
            stats_inventario = self.gestor_inventario.obtener_estadisticas()
            stats_usuarios = self.gestor_usuarios.obtener_estadisticas()
            stats_prestamos = self.gestor_prestamos.obtener_estadisticas()
            stats_reservas = self.gestor_reservas.obtener_estadisticas()
            
            mensaje = f"""
System Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Books: {stats_inventario['total_libros']} titles, {stats_inventario['total_stock']} copies
   Available: {stats_inventario['disponibles']} | Out of stock: {stats_inventario['agotados']}
   Total value: ${stats_inventario['valor_total']:,.0f} COP

👤 Users: {stats_usuarios['total_usuarios']} registered
   Active: {stats_usuarios['usuarios_activos']} | Inactive: {stats_usuarios['usuarios_inactivos']}
   With loans: {stats_usuarios['usuarios_con_prestamos']}

📋 Loans: {stats_prestamos['prestamos_activos']} active
   Historical: {stats_prestamos['total_prestamos_historicos']} total

⏳ Reservations: {stats_reservas['total_reservas']} pending
   Unique books: {stats_reservas['libros_unicos']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            print(mensaje)
            self.actualizar_status("System loaded successfully")
            
        except Exception as e:
            print(f"Error loading statistics: {e}")
            self.actualizar_status("Error loading statistics")
    
    def actualizar_status(self, mensaje):
        """
        Update status bar message.
        
        Args:
            mensaje (str): Status message to display
        """
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text=mensaje)
    
    def obtener_gestores(self):
        """
        Get all manager instances.
        
        Returns:
            dict: Dictionary with all managers
        """
        return {
            'inventario': self.gestor_inventario,
            'usuarios': self.gestor_usuarios,
            'prestamos': self.gestor_prestamos,
            'reservas': self.gestor_reservas
        }


def crear_ventana_principal():
    """
    Create and return a standalone main window.
    
    This function can be used for testing or as an alternative entry point.
    
    Returns:
        VentanaPrincipal: Main window instance
    """
    root = tb.Window(themename="superhero")
    root.title("Library Management System")
    root.geometry("1200x700")
    
    ventana = VentanaPrincipal(root)
    
    return ventana, root


if __name__ == "__main__":
    # Test the main window
    ventana, root = crear_ventana_principal()
    
    # Display test message
    messagebox.showinfo(
        "System Ready",
        "Library Management System initialized successfully!\n\n"
        "All managers loaded:\n"
        "✓ Inventory Manager\n"
        "✓ Users Manager\n"
        "✓ Loans Manager\n"
        "✓ Reservations Manager"
    )
    
    root.mainloop()