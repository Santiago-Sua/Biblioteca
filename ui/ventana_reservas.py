"""
Reservations Management Window - Library Management System

This module implements the ReservasWindow class which provides a complete
interface for managing book reservations using a Queue (FIFO) structure.

PROJECT REQUIREMENT:
    Reservations can only be made for books with stock = 0 (out of stock).
    The waiting list follows FIFO (First In, First Out) priority.

Classes:
    ReservasWindow: Main window for reservations management

Author: [Your Name]
Date: December 2025
"""

import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from gestor.gestor_inventario import GestorInventario
from gestor.gestor_usuarios import GestorUsuarios
from gestor.gestor_reservas import GestorReservas


class ReservasWindow:
    """
    Reservations management window.
    
    Provides complete functionality for reservations including:
    - Create reservations (only for out-of-stock books)
    - Cancel reservations
    - View reservation queue (FIFO order)
    - View user's reservations
    - Reservation statistics
    
    Attributes:
        parent: Parent container widget
        archivo_handler: File operations handler
        gestor_inventario: Inventory manager instance
        gestor_usuarios: Users manager instance
        gestor_reservas: Reservations manager instance
    """
    
    def __init__(self, parent, archivo_handler):
        """
        Initialize the reservations management window.
        
        Args:
            parent: Parent container widget
            archivo_handler: ArchivoHandler instance
        """
        self.parent = parent
        self.archivo_handler = archivo_handler
        
        # Initialize managers
        self.gestor_inventario = GestorInventario(archivo_handler)
        self.gestor_usuarios = GestorUsuarios(archivo_handler)
        self.gestor_reservas = GestorReservas(
            archivo_handler, 
            self.gestor_inventario, 
            self.gestor_usuarios
        )
        
        # Create main container
        self.main_frame = tk.Frame(parent, bg="white")
        self.main_frame.pack(fill="both", expand=True)
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets for the reservations window."""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Reservations Management",
            font=("Helvetica", 18, "bold"),
            bg="white",
            fg="#004080"
        )
        title_label.pack(pady=10)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Create reservation
        self.tab_crear = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_crear, text="➕ Create Reservation")
        self.crear_tab_crear()
        
        # Tab 2: View queue
        self.tab_cola = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_cola, text="📋 Reservation Queue")
        self.crear_tab_cola()
        
        # Tab 3: My reservations
        self.tab_usuario = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_usuario, text="👤 User Reservations")
        self.crear_tab_usuario()
        
        # Tab 4: Statistics
        self.tab_estadisticas = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_estadisticas, text="📊 Statistics")
        self.crear_tab_estadisticas()
    
    def crear_tab_crear(self):
        """Create the reservation creation tab."""
        form_frame = tk.Frame(self.tab_crear, bg="white")
        form_frame.pack(pady=30, padx=50, fill="both", expand=True)
        
        # Title with requirement note
        tk.Label(
            form_frame,
            text="Create New Reservation",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#004080"
        ).grid(row=0, column=0, columnspan=3, pady=10)
        
        tk.Label(
            form_frame,
            text="⚠️ Note: Reservations only allowed for out-of-stock books (stock = 0)",
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
        
        self.res_user_var = tk.StringVar()
        tk.Entry(
            form_frame,
            textvariable=self.res_user_var,
            font=("Helvetica", 11),
            width=25
        ).grid(row=2, column=1, pady=15, padx=10, sticky="w")
        
        tb.Button(
            form_frame,
            text="🔍 Verify User",
            bootstyle="info-outline",
            command=self.verificar_usuario_reserva
        ).grid(row=2, column=2, padx=5)
        
        # ISBN
        tk.Label(
            form_frame,
            text="Book ISBN *:",
            bg="white",
            font=("Helvetica", 11, "bold")
        ).grid(row=3, column=0, sticky="w", pady=15)
        
        self.res_isbn_var = tk.StringVar()
        tk.Entry(
            form_frame,
            textvariable=self.res_isbn_var,
            font=("Helvetica", 11),
            width=25
        ).grid(row=3, column=1, pady=15, padx=10, sticky="w")
        
        tb.Button(
            form_frame,
            text="🔍 Verify Book",
            bootstyle="info-outline",
            command=self.verificar_libro_reserva
        ).grid(row=3, column=2, padx=5)
        
        # Status display
        self.res_status_label = tk.Label(
            form_frame,
            text="",
            bg="white",
            font=("Helvetica", 10),
            fg="blue",
            wraplength=500,
            justify="left"
        )
        self.res_status_label.grid(row=4, column=0, columnspan=3, pady=15)
        
        # Create button
        tb.Button(
            form_frame,
            text="✅ Create Reservation",
            bootstyle="success",
            command=self.crear_reserva
        ).grid(row=5, column=0, columnspan=3, pady=20)
        
        # Clear button
        tb.Button(
            form_frame,
            text="🔄 Clear",
            bootstyle="secondary",
            command=self.limpiar_formulario_reserva
        ).grid(row=6, column=0, columnspan=3, pady=5)
    
    def crear_tab_cola(self):
        """Create the reservation queue tab."""
        queue_frame = tk.Frame(self.tab_cola, bg="white")
        queue_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Control buttons
        btn_frame = tk.Frame(queue_frame, bg="white")
        btn_frame.pack(fill="x", pady=10)
        
        tb.Button(
            btn_frame,
            text="🔄 Refresh Queue",
            bootstyle="info",
            command=self.cargar_cola_reservas
        ).pack(side="left", padx=5)
        
        tb.Button(
            btn_frame,
            text="🗑️ Cancel Selected",
            bootstyle="danger",
            command=self.cancelar_reserva_seleccionada
        ).pack(side="left", padx=5)
        
        # Queue info
        self.queue_info_label = tk.Label(
            queue_frame,
            text="",
            bg="white",
            font=("Helvetica", 10, "bold"),
            fg="#004080"
        )
        self.queue_info_label.pack(pady=5)
        
        # Treeview
        tree_frame = tk.Frame(queue_frame)
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.queue_tree = ttk.Treeview(
            tree_frame,
            columns=("Position", "UserID", "UserName", "ISBN", "BookTitle", "Date"),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        scrollbar_y.config(command=self.queue_tree.yview)
        scrollbar_x.config(command=self.queue_tree.xview)
        
        # Configure columns
        self.queue_tree.heading("Position", text="Position")
        self.queue_tree.heading("UserID", text="User ID")
        self.queue_tree.heading("UserName", text="User Name")
        self.queue_tree.heading("ISBN", text="ISBN")
        self.queue_tree.heading("BookTitle", text="Book Title")
        self.queue_tree.heading("Date", text="Reservation Date")
        
        self.queue_tree.column("Position", width=80)
        self.queue_tree.column("UserID", width=100)
        self.queue_tree.column("UserName", width=150)
        self.queue_tree.column("ISBN", width=130)
        self.queue_tree.column("BookTitle", width=200)
        self.queue_tree.column("Date", width=150)
        
        # Pack
        self.queue_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Load initial data
        self.cargar_cola_reservas()
    
    def crear_tab_usuario(self):
        """Create the user reservations tab."""
        user_frame = tk.Frame(self.tab_usuario, bg="white")
        user_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Search frame
        search_frame = tk.Frame(user_frame, bg="white")
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(
            search_frame,
            text="User ID:",
            bg="white",
            font=("Helvetica", 11)
        ).pack(side="left", padx=5)
        
        self.user_res_var = tk.StringVar()
        tk.Entry(
            search_frame,
            textvariable=self.user_res_var,
            font=("Helvetica", 11),
            width=20
        ).pack(side="left", padx=5)
        
        tb.Button(
            search_frame,
            text="🔍 View My Reservations",
            bootstyle="info",
            command=self.ver_reservas_usuario
        ).pack(side="left", padx=5)
        
        # Results display
        result_frame = tk.Frame(user_frame)
        result_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical")
        
        self.user_res_text = tk.Text(
            result_frame,
            font=("Courier", 10),
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.user_res_text.yview)
        
        self.user_res_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_tab_estadisticas(self):
        """Create the statistics tab."""
        stats_frame = tk.Frame(self.tab_estadisticas, bg="white")
        stats_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        tk.Label(
            stats_frame,
            text="Reservation Statistics",
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
    
    def verificar_usuario_reserva(self):
        """Verify user exists."""
        user_id = self.res_user_var.get().strip()
        
        if not user_id:
            messagebox.showwarning("Empty Field", "Please enter a User ID")
            return
        
        usuario = self.gestor_usuarios.obtener_usuario(user_id)
        
        if usuario:
            self.res_status_label.config(
                text=f"✓ User: {usuario.nombre} ({usuario.email})",
                fg="green"
            )
        else:
            self.res_status_label.config(
                text=f"✗ User not found",
                fg="red"
            )
    
    def verificar_libro_reserva(self):
        """Verify book exists and is out of stock."""
        isbn = self.res_isbn_var.get().strip()
        
        if not isbn:
            messagebox.showwarning("Empty Field", "Please enter an ISBN")
            return
        
        validacion = self.gestor_reservas.validar_puede_reservar(
            self.res_user_var.get().strip(),
            isbn
        )
        
        if validacion['puede_reservar']:
            detalles = validacion['detalles']
            reservas_actuales = detalles['reservas_actuales']
            
            self.res_status_label.config(
                text=f"✓ Book: {detalles['libro']}\n"
                     f"Status: Out of stock (available for reservation)\n"
                     f"Current reservations: {reservas_actuales}\n"
                     f"Your position would be: {reservas_actuales + 1}",
                fg="green"
            )
        else:
            self.res_status_label.config(
                text=f"✗ {validacion['razon']}",
                fg="red"
            )
    
    def crear_reserva(self):
        """Create a new reservation."""
        user_id = self.res_user_var.get().strip()
        isbn = self.res_isbn_var.get().strip()
        
        if not user_id or not isbn:
            messagebox.showerror("Missing Data", "Please enter both User ID and ISBN")
            return
        
        # Create reservation
        resultado = self.gestor_reservas.crear_reserva(user_id, isbn)
        
        if resultado['exito']:
            detalles = resultado['detalles']
            messagebox.showinfo(
                "Success",
                f"Reservation created successfully!\n\n"
                f"User: {detalles['usuario']}\n"
                f"Book: {detalles['libro']}\n"
                f"ISBN: {detalles['isbn']}\n"
                f"Date: {detalles['fecha_reserva']}\n\n"
                f"Your position in queue: {detalles['posicion_en_cola']}\n"
                f"Total reservations for this book: {detalles['total_reservas_libro']}\n\n"
                f"You will be notified when the book becomes available."
            )
            self.limpiar_formulario_reserva()
            self.cargar_cola_reservas()
        else:
            messagebox.showerror("Error", resultado['mensaje'])
    
    def limpiar_formulario_reserva(self):
        """Clear reservation form."""
        self.res_user_var.set("")
        self.res_isbn_var.set("")
        self.res_status_label.config(text="")
    
    def cargar_cola_reservas(self):
        """Load reservation queue."""
        # Clear current items
        for item in self.queue_tree.get_children():
            self.queue_tree.delete(item)
        
        # Get all reservations
        reservas = self.gestor_reservas.listar_todas_reservas()
        
        # Update info label
        self.queue_info_label.config(
            text=f"Total Reservations in Queue: {len(reservas)} (FIFO Order - First In, First Out)"
        )
        
        # Populate treeview
        for i, reserva in enumerate(reservas, 1):
            user_id = reserva['id_usuario']
            isbn = reserva['isbn']
            fecha = reserva['fecha']
            
            # Get user info
            usuario = self.gestor_usuarios.obtener_usuario(user_id)
            nombre_usuario = usuario.nombre if usuario else "Unknown"
            
            # Get book info
            libro = self.gestor_inventario.buscar_por_isbn(isbn)
            titulo_libro = libro.titulo if libro else "Unknown"
            
            self.queue_tree.insert("", "end", values=(
                i,
                user_id,
                nombre_usuario,
                isbn,
                titulo_libro,
                fecha
            ))
    
    def cancelar_reserva_seleccionada(self):
        """Cancel selected reservation."""
        selection = self.queue_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a reservation to cancel")
            return
        
        item = self.queue_tree.item(selection[0])
        values = item['values']
        
        user_id = values[1]
        isbn = values[3]
        nombre_usuario = values[2]
        titulo_libro = values[4]
        
        confirm = messagebox.askyesno(
            "Confirm Cancellation",
            f"Cancel reservation?\n\n"
            f"User: {nombre_usuario} ({user_id})\n"
            f"Book: {titulo_libro}\n"
            f"ISBN: {isbn}"
        )
        
        if confirm:
            resultado = self.gestor_reservas.cancelar_reserva(user_id, isbn)
            
            if resultado['exito']:
                messagebox.showinfo("Success", resultado['mensaje'])
                self.cargar_cola_reservas()
            else:
                messagebox.showerror("Error", resultado['mensaje'])
    
    def ver_reservas_usuario(self):
        """View reservations for a specific user."""
        user_id = self.user_res_var.get().strip()
        
        if not user_id:
            messagebox.showwarning("Empty Field", "Please enter a User ID")
            return
        
        usuario = self.gestor_usuarios.obtener_usuario(user_id)
        if not usuario:
            messagebox.showerror("Error", "User not found")
            return
        
        reservas = self.gestor_reservas.obtener_reservas_usuario(user_id)
        
        self.user_res_text.delete(1.0, tk.END)
        
        self.user_res_text.insert(tk.END, "=" * 80 + "\n")
        self.user_res_text.insert(tk.END, f"RESERVATIONS - {usuario.nombre} ({user_id})\n")
        self.user_res_text.insert(tk.END, "=" * 80 + "\n\n")
        
        if not reservas:
            self.user_res_text.insert(tk.END, "No reservations found.\n")
        else:
            self.user_res_text.insert(tk.END, f"Total reservations: {len(reservas)}\n\n")
            
            for i, reserva in enumerate(reservas, 1):
                isbn = reserva['isbn']
                fecha = reserva['fecha']
                
                libro = self.gestor_inventario.buscar_por_isbn(isbn)
                titulo = libro.titulo if libro else "Unknown"
                
                # Get position in queue
                posicion = self.gestor_reservas.obtener_posicion_en_cola(user_id, isbn)
                
                # Get estimated wait time
                tiempo = self.gestor_reservas.obtener_tiempo_espera_estimado(user_id, isbn)
                
                self.user_res_text.insert(tk.END, f"{i}. {titulo}\n")
                self.user_res_text.insert(tk.END, f"   ISBN: {isbn}\n")
                self.user_res_text.insert(tk.END, f"   Reserved on: {fecha}\n")
                self.user_res_text.insert(tk.END, f"   Position in queue: {posicion}\n")
                self.user_res_text.insert(tk.END, f"   Estimated wait: ~{tiempo['dias_estimados']} days\n\n")
    
    def actualizar_estadisticas(self):
        """Update and display reservation statistics."""
        stats = self.gestor_reservas.obtener_estadisticas()
        
        self.stats_text.delete(1.0, tk.END)
        
        self.stats_text.insert(tk.END, "=" * 70 + "\n")
        self.stats_text.insert(tk.END, "RESERVATION STATISTICS\n")
        self.stats_text.insert(tk.END, "=" * 70 + "\n\n")
        
        self.stats_text.insert(tk.END, f"Total Active Reservations:     {stats['total_reservas']}\n")
        self.stats_text.insert(tk.END, f"Unique Users:                  {stats['usuarios_unicos']}\n")
        self.stats_text.insert(tk.END, f"Unique Books:                  {stats['libros_unicos']}\n")
        self.stats_text.insert(tk.END, f"Avg Reservations per Book:     {stats['promedio_reservas_por_libro']:.2f}\n\n")
        
        # Most reserved books
        self.stats_text.insert(tk.END, "Top 5 Most Reserved Books:\n")
        self.stats_text.insert(tk.END, "-" * 70 + "\n")
        
        top_books = self.gestor_reservas.obtener_libros_mas_reservados(5)
        
        if top_books:
            for i, (isbn, count) in enumerate(top_books, 1):
                libro = self.gestor_inventario.buscar_por_isbn(isbn)
                titulo = libro.titulo if libro else isbn
                self.stats_text.insert(tk.END, f"{i}. {titulo[:45]}\n")
                self.stats_text.insert(tk.END, f"   Reservations: {count}\n\n")
        else:
            self.stats_text.insert(tk.END, "No reservations yet.\n\n")
        
        self.stats_text.insert(tk.END, "=" * 70 + "\n")