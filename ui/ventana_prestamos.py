"""
Loans Management Window - Library Management System

This module implements the PrestamosWindow class which provides a complete
interface for managing book loans including creation, returns, and history.

CRITICAL FEATURE:
    When processing a return, this window triggers the binary search + 
    reservation verification process, which is a critical requirement of the project.

Classes:
    PrestamosWindow: Main window for loans management

Author: [Your Name]
Date: December 2025
"""

import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from gestor.gestor_inventario import GestorInventario
from gestor.gestor_usuarios import GestorUsuarios
from gestor.gestor_prestamos import GestorPrestamos
from gestor.gestor_reservas import GestorReservas


class PrestamosWindow:
    """
    Loans management window.
    
    Provides complete functionality for loans including:
    - Create new loans
    - Process book returns (CRITICAL: triggers binary search + reservation check)
    - View loan history per user
    - View all active loans
    - Loan statistics
    
    Attributes:
        parent: Parent container widget
        archivo_handler: File operations handler
        gestor_inventario: Inventory manager instance
        gestor_usuarios: Users manager instance
        gestor_reservas: Reservations manager instance
        gestor_prestamos: Loans manager instance
    """
    
    def __init__(self, parent, archivo_handler):
        """
        Initialize the loans management window.
        
        Args:
            parent: Parent container widget
            archivo_handler: ArchivoHandler instance
        """
        self.parent = parent
        self.archivo_handler = archivo_handler
        
        # Initialize managers in correct order
        self.gestor_inventario = GestorInventario(archivo_handler)
        self.gestor_usuarios = GestorUsuarios(archivo_handler)
        self.gestor_reservas = GestorReservas(
            archivo_handler, 
            self.gestor_inventario, 
            self.gestor_usuarios
        )
        self.gestor_prestamos = GestorPrestamos(
            archivo_handler,
            self.gestor_inventario,
            self.gestor_usuarios,
            self.gestor_reservas
        )
        
        # Create main container
        self.main_frame = tk.Frame(parent, bg="white")
        self.main_frame.pack(fill="both", expand=True)
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets for the loans window."""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Loans Management",
            font=("Helvetica", 18, "bold"),
            bg="white",
            fg="#004080"
        )
        title_label.pack(pady=10)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Create loan
        self.tab_crear = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_crear, text="➕ Create Loan")
        self.crear_tab_crear()
        
        # Tab 2: Return book
        self.tab_devolver = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_devolver, text="↩️ Return Book")
        self.crear_tab_devolver()
        
        # Tab 3: Loan history
        self.tab_historial = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_historial, text="📋 Loan History")
        self.crear_tab_historial()
        
        # Tab 4: Statistics
        self.tab_estadisticas = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_estadisticas, text="📊 Statistics")
        self.crear_tab_estadisticas()
    
    def crear_tab_crear(self):
        """Create the loan creation tab."""
        form_frame = tk.Frame(self.tab_crear, bg="white")
        form_frame.pack(pady=30, padx=50, fill="both", expand=True)
        
        # Title
        tk.Label(
            form_frame,
            text="Create New Loan",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#004080"
        ).grid(row=0, column=0, columnspan=3, pady=20)
        
        # User ID
        tk.Label(
            form_frame,
            text="User ID *:",
            bg="white",
            font=("Helvetica", 11, "bold")
        ).grid(row=1, column=0, sticky="w", pady=10)
        
        self.loan_user_var = tk.StringVar()
        tk.Entry(
            form_frame,
            textvariable=self.loan_user_var,
            font=("Helvetica", 11),
            width=25
        ).grid(row=1, column=1, pady=10, padx=10, sticky="w")
        
        tb.Button(
            form_frame,
            text="🔍 Verify User",
            bootstyle="info-outline",
            command=self.verificar_usuario_prestamo
        ).grid(row=1, column=2, padx=5)
        
        # ISBN
        tk.Label(
            form_frame,
            text="Book ISBN *:",
            bg="white",
            font=("Helvetica", 11, "bold")
        ).grid(row=2, column=0, sticky="w", pady=10)
        
        self.loan_isbn_var = tk.StringVar()
        tk.Entry(
            form_frame,
            textvariable=self.loan_isbn_var,
            font=("Helvetica", 11),
            width=25
        ).grid(row=2, column=1, pady=10, padx=10, sticky="w")
        
        tb.Button(
            form_frame,
            text="🔍 Verify Book",
            bootstyle="info-outline",
            command=self.verificar_libro_prestamo
        ).grid(row=2, column=2, padx=5)
        
        # Status display
        self.loan_status_label = tk.Label(
            form_frame,
            text="",
            bg="white",
            font=("Helvetica", 10),
            fg="blue",
            wraplength=400,
            justify="left"
        )
        self.loan_status_label.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Create button
        tb.Button(
            form_frame,
            text="✅ Create Loan",
            bootstyle="success",
            command=self.crear_prestamo
        ).grid(row=4, column=0, columnspan=3, pady=20)
        
        # Clear button
        tb.Button(
            form_frame,
            text="🔄 Clear",
            bootstyle="secondary",
            command=self.limpiar_formulario_prestamo
        ).grid(row=5, column=0, columnspan=3, pady=5)
    
    def crear_tab_devolver(self):
        """Create the book return tab."""
        form_frame = tk.Frame(self.tab_devolver, bg="white")
        form_frame.pack(pady=30, padx=50, fill="both", expand=True)
        
        # Title with CRITICAL note
        tk.Label(
            form_frame,
            text="Return Book",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#004080"
        ).grid(row=0, column=0, columnspan=3, pady=10)
        
        tk.Label(
            form_frame,
            text="⚠️ CRITICAL: Uses Binary Search + Reservation Check",
            font=("Helvetica", 9, "italic"),
            bg="white",
            fg="red"
        ).grid(row=1, column=0, columnspan=3, pady=5)
        
        # User ID
        tk.Label(
            form_frame,
            text="User ID *:",
            bg="white",
            font=("Helvetica", 11, "bold")
        ).grid(row=2, column=0, sticky="w", pady=15)
        
        self.return_user_var = tk.StringVar()
        tk.Entry(
            form_frame,
            textvariable=self.return_user_var,
            font=("Helvetica", 11),
            width=25
        ).grid(row=2, column=1, pady=15, padx=10, sticky="w")
        
        tb.Button(
            form_frame,
            text="📋 View User Loans",
            bootstyle="info-outline",
            command=self.ver_prestamos_usuario
        ).grid(row=2, column=2, padx=5)
        
        # ISBN
        tk.Label(
            form_frame,
            text="Book ISBN *:",
            bg="white",
            font=("Helvetica", 11, "bold")
        ).grid(row=3, column=0, sticky="w", pady=15)
        
        self.return_isbn_var = tk.StringVar()
        tk.Entry(
            form_frame,
            textvariable=self.return_isbn_var,
            font=("Helvetica", 11),
            width=25
        ).grid(row=3, column=1, pady=15, padx=10, sticky="w")
        
        # Status display
        self.return_status_label = tk.Label(
            form_frame,
            text="",
            bg="white",
            font=("Helvetica", 10),
            fg="blue",
            wraplength=400,
            justify="left"
        )
        self.return_status_label.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Return button
        tb.Button(
            form_frame,
            text="↩️ Process Return",
            bootstyle="success",
            command=self.devolver_libro
        ).grid(row=5, column=0, columnspan=3, pady=20)
        
        # Result display (for reservation info)
        self.return_result_text = tk.Text(
            form_frame,
            height=8,
            width=60,
            font=("Helvetica", 10)
        )
        self.return_result_text.grid(row=6, column=0, columnspan=3, pady=10)
    
    def crear_tab_historial(self):
        """Create the loan history tab."""
        history_frame = tk.Frame(self.tab_historial, bg="white")
        history_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Search frame
        search_frame = tk.Frame(history_frame, bg="white")
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(
            search_frame,
            text="User ID:",
            bg="white",
            font=("Helvetica", 11)
        ).pack(side="left", padx=5)
        
        self.history_user_var = tk.StringVar()
        tk.Entry(
            search_frame,
            textvariable=self.history_user_var,
            font=("Helvetica", 11),
            width=20
        ).pack(side="left", padx=5)
        
        tb.Button(
            search_frame,
            text="🔍 View History",
            bootstyle="info",
            command=self.cargar_historial
        ).pack(side="left", padx=5)
        
        # History display
        history_text_frame = tk.Frame(history_frame)
        history_text_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(history_text_frame, orient="vertical")
        
        self.history_text = tk.Text(
            history_text_frame,
            font=("Courier", 10),
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.history_text.yview)
        
        self.history_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_tab_estadisticas(self):
        """Create the statistics tab."""
        stats_frame = tk.Frame(self.tab_estadisticas, bg="white")
        stats_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        tk.Label(
            stats_frame,
            text="Loan Statistics",
            bg="white",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        tb.Button(
            stats_frame,
            text="🔄 Refresh Statistics",
            bootstyle="info",
            command=self.actualizar_estadisticas
        ).pack(pady=10)
        
        # Statistics display
        self.stats_text = tk.Text(
            stats_frame,
            height=20,
            width=80,
            font=("Courier", 11)
        )
        self.stats_text.pack(fill="both", expand=True, pady=10)
        
        # Initial load
        self.actualizar_estadisticas()
    
    def verificar_usuario_prestamo(self):
        """Verify user can borrow books."""
        user_id = self.loan_user_var.get().strip()
        
        if not user_id:
            messagebox.showwarning("Empty Field", "Please enter a User ID")
            return
        
        validacion = self.gestor_usuarios.validar_puede_prestar(user_id)
        
        if validacion['puede_prestar']:
            usuario = self.gestor_usuarios.obtener_usuario(user_id)
            self.loan_status_label.config(
                text=f"✓ User: {usuario.nombre}\n{validacion['razon']}",
                fg="green"
            )
        else:
            self.loan_status_label.config(
                text=f"✗ {validacion['razon']}",
                fg="red"
            )
    
    def verificar_libro_prestamo(self):
        """Verify book is available for loan."""
        isbn = self.loan_isbn_var.get().strip()
        
        if not isbn:
            messagebox.showwarning("Empty Field", "Please enter an ISBN")
            return
        
        libro = self.gestor_inventario.buscar_por_isbn(isbn)
        
        if not libro:
            self.loan_status_label.config(
                text=f"✗ Book not found",
                fg="red"
            )
        elif not libro.esta_disponible():
            self.loan_status_label.config(
                text=f"✗ Book '{libro.titulo}' is not available (stock: {libro.stock})",
                fg="red"
            )
        else:
            self.loan_status_label.config(
                text=f"✓ Book: {libro.titulo}\nAuthor: {libro.autor}\nAvailable: {libro.stock} copies",
                fg="green"
            )
    
    def crear_prestamo(self):
        """Create a new loan."""
        user_id = self.loan_user_var.get().strip()
        isbn = self.loan_isbn_var.get().strip()
        
        if not user_id or not isbn:
            messagebox.showerror("Missing Data", "Please enter both User ID and ISBN")
            return
        
        # Create loan
        resultado = self.gestor_prestamos.crear_prestamo(user_id, isbn)
        
        if resultado['exito']:
            detalles = resultado['detalles']
            messagebox.showinfo(
                "Success",
                f"Loan created successfully!\n\n"
                f"User: {detalles['usuario']}\n"
                f"Book: {detalles['libro']}\n"
                f"Date: {detalles['fecha']}\n\n"
                f"User now has {detalles['prestamos_actuales']} active loan(s)\n"
                f"Book stock: {detalles['stock_restante']}"
            )
            self.limpiar_formulario_prestamo()
        else:
            messagebox.showerror("Error", resultado['mensaje'])
    
    def limpiar_formulario_prestamo(self):
        """Clear loan form."""
        self.loan_user_var.set("")
        self.loan_isbn_var.set("")
        self.loan_status_label.config(text="")
    
    def ver_prestamos_usuario(self):
        """View user's current loans."""
        user_id = self.return_user_var.get().strip()
        
        if not user_id:
            messagebox.showwarning("Empty Field", "Please enter a User ID")
            return
        
        usuario = self.gestor_usuarios.obtener_usuario(user_id)
        if not usuario:
            messagebox.showerror("Error", "User not found")
            return
        
        historial = self.gestor_prestamos.obtener_historial_usuario(user_id)
        
        if not historial:
            messagebox.showinfo("No Loans", f"User {usuario.nombre} has no loan history")
            return
        
        # Show loans
        mensaje = f"Loans for {usuario.nombre}:\n\n"
        for i, prestamo in enumerate(historial[:5], 1):  # Show last 5
            libro = self.gestor_inventario.buscar_por_isbn(prestamo['isbn'])
            titulo = libro.titulo if libro else prestamo['isbn']
            mensaje += f"{i}. {titulo}\n   ISBN: {prestamo['isbn']}\n   Date: {prestamo['fecha']}\n\n"
        
        messagebox.showinfo("User Loans", mensaje)
    
    def devolver_libro(self):
        """
        Process a book return.
        
        CRITICAL FUNCTION: This triggers the binary search + reservation check.
        """
        user_id = self.return_user_var.get().strip()
        isbn = self.return_isbn_var.get().strip()
        
        if not user_id or not isbn:
            messagebox.showerror("Missing Data", "Please enter both User ID and ISBN")
            return
        
        # Process return - CRITICAL: This uses binary search + reservation verification
        resultado = self.gestor_prestamos.devolver_libro(user_id, isbn)
        
        # Display result
        self.return_result_text.delete(1.0, tk.END)
        
        if resultado['exito']:
            detalles = resultado['detalles']
            
            # Success message
            mensaje = "=" * 60 + "\n"
            mensaje += "BOOK RETURN PROCESSED SUCCESSFULLY\n"
            mensaje += "=" * 60 + "\n\n"
            mensaje += f"User: {detalles['usuario']}\n"
            mensaje += f"Book: {detalles['libro']}\n"
            mensaje += f"ISBN: {detalles['isbn']}\n"
            mensaje += f"Return Date: {detalles['fecha_devolucion']}\n"
            mensaje += f"Current Stock: {detalles['stock_actual']}\n"
            mensaje += f"User's Active Loans: {detalles['prestamos_actuales_usuario']}\n\n"
            
            # CRITICAL: Show reservation info
            if resultado.get('reserva_asignada'):
                mensaje += "🎯 RESERVATION ASSIGNED!\n"
                mensaje += "-" * 60 + "\n"
                mensaje += "Binary Search Result: Book found in sorted inventory\n"
                mensaje += "Reservation Queue Check: Pending reservations found\n"
                mensaje += f"Book assigned to: {detalles['usuario_asignado']}\n"
                mensaje += "Priority: FIFO (First in queue)\n"
                mensaje += "Status: Automatic loan created\n"
            else:
                mensaje += "ℹ️ No Reservations\n"
                mensaje += "-" * 60 + "\n"
                mensaje += "Binary Search Result: Book found in sorted inventory\n"
                mensaje += "Reservation Queue Check: No pending reservations\n"
                mensaje += "Status: Book available for general loan\n"
            
            self.return_result_text.insert(tk.END, mensaje)
            
            messagebox.showinfo("Success", resultado['mensaje'])
            
            # Clear form
            self.return_user_var.set("")
            self.return_isbn_var.set("")
            self.return_status_label.config(text="")
        else:
            messagebox.showerror("Error", resultado['mensaje'])
    
    def cargar_historial(self):
        """Load loan history for a user."""
        user_id = self.history_user_var.get().strip()
        
        if not user_id:
            messagebox.showwarning("Empty Field", "Please enter a User ID")
            return
        
        usuario = self.gestor_usuarios.obtener_usuario(user_id)
        if not usuario:
            messagebox.showerror("Error", "User not found")
            return
        
        historial = self.gestor_prestamos.obtener_historial_usuario(user_id)
        
        self.history_text.delete(1.0, tk.END)
        
        self.history_text.insert(tk.END, "=" * 80 + "\n")
        self.history_text.insert(tk.END, f"LOAN HISTORY - {usuario.nombre} ({user_id})\n")
        self.history_text.insert(tk.END, "=" * 80 + "\n\n")
        
        if not historial:
            self.history_text.insert(tk.END, "No loan history found.\n")
        else:
            self.history_text.insert(tk.END, f"Total loans in history: {len(historial)}\n\n")
            
            for i, prestamo in enumerate(historial, 1):
                libro = self.gestor_inventario.buscar_por_isbn(prestamo['isbn'])
                titulo = libro.titulo if libro else "Unknown"
                
                self.history_text.insert(tk.END, f"{i}. {titulo}\n")
                self.history_text.insert(tk.END, f"   ISBN: {prestamo['isbn']}\n")
                self.history_text.insert(tk.END, f"   Date: {prestamo['fecha']}\n\n")
    
    def actualizar_estadisticas(self):
        """Update and display loan statistics."""
        stats = self.gestor_prestamos.obtener_estadisticas()
        
        self.stats_text.delete(1.0, tk.END)
        
        self.stats_text.insert(tk.END, "=" * 70 + "\n")
        self.stats_text.insert(tk.END, "LOAN STATISTICS\n")
        self.stats_text.insert(tk.END, "=" * 70 + "\n\n")
        
        self.stats_text.insert(tk.END, f"Users with Loan History:      {stats['total_usuarios_con_historial']}\n")
        self.stats_text.insert(tk.END, f"Total Historical Loans:        {stats['total_prestamos_historicos']}\n")
        self.stats_text.insert(tk.END, f"Currently Active Loans:        {stats['prestamos_activos']}\n")
        self.stats_text.insert(tk.END, f"Completed Loans:               {stats['prestamos_completados']}\n\n")
        
        # Most loaned books
        self.stats_text.insert(tk.END, "Top 5 Most Loaned Books:\n")
        self.stats_text.insert(tk.END, "-" * 70 + "\n")
        
        top_books = self.gestor_prestamos.obtener_libros_mas_prestados(5)
        
        for i, (isbn, count) in enumerate(top_books, 1):
            libro = self.gestor_inventario.buscar_por_isbn(isbn)
            titulo = libro.titulo if libro else isbn
            self.stats_text.insert(tk.END, f"{i}. {titulo[:40]}\n")
            self.stats_text.insert(tk.END, f"   Times loaned: {count}\n\n")
        
        self.stats_text.insert(tk.END, "=" * 70 + "\n")