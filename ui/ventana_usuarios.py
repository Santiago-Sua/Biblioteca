"""
Users Management Window - Library Management System

This module implements the UsuariosWindow class which provides a complete
interface for managing library users including registration, activation/
deactivation, and loan tracking.

Classes:
    UsuariosWindow: Main window for users management

Author: [Your Name]
Date: December 2025
"""

import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from gestor.gestor_usuarios import GestorUsuarios
from utils.validaciones import validar_email, validar_telefono, validar_texto_no_vacio


class UsuariosWindow:
    """
    Users management window.
    
    Provides complete CRUD functionality for users including:
    - View all users
    - Register new users
    - Update user information
    - Activate/deactivate users
    - Delete users
    - View user statistics
    
    Attributes:
        parent: Parent container widget
        archivo_handler: File operations handler
        gestor_usuarios: Users manager instance
    """
    
    def __init__(self, parent, archivo_handler):
        """
        Initialize the users management window.
        
        Args:
            parent: Parent container widget
            archivo_handler: ArchivoHandler instance
        """
        self.parent = parent
        self.archivo_handler = archivo_handler
        
        # Initialize users manager
        self.gestor_usuarios = GestorUsuarios(archivo_handler)
        
        # Create main container
        self.main_frame = tk.Frame(parent, bg="white")
        self.main_frame.pack(fill="both", expand=True)
        
        # Create UI
        self.create_widgets()
        self.cargar_usuarios()
    
    def create_widgets(self):
        """Create all widgets for the users window."""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Users Management",
            font=("Helvetica", 18, "bold"),
            bg="white",
            fg="#004080"
        )
        title_label.pack(pady=10)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: List/View users
        self.tab_lista = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_lista, text="👥 User List")
        self.crear_tab_lista()
        
        # Tab 2: Register/Edit user
        self.tab_formulario = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_formulario, text="➕ Register User")
        self.crear_tab_formulario()
        
        # Tab 3: Statistics
        self.tab_estadisticas = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_estadisticas, text="📊 Statistics")
        self.crear_tab_estadisticas()
    
    def crear_tab_lista(self):
        """Create the user list tab."""
        # Control buttons
        btn_frame = tk.Frame(self.tab_lista, bg="white")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tb.Button(
            btn_frame,
            text="🔄 Refresh",
            bootstyle="info",
            command=self.cargar_usuarios
        ).pack(side="left", padx=5)
        
        tb.Button(
            btn_frame,
            text="✏️ Edit Selected",
            bootstyle="warning",
            command=self.editar_usuario_seleccionado
        ).pack(side="left", padx=5)
        
        tb.Button(
            btn_frame,
            text="✅ Activate",
            bootstyle="success",
            command=self.activar_usuario_seleccionado
        ).pack(side="left", padx=5)
        
        tb.Button(
            btn_frame,
            text="❌ Deactivate",
            bootstyle="warning",
            command=self.desactivar_usuario_seleccionado
        ).pack(side="left", padx=5)
        
        tb.Button(
            btn_frame,
            text="🗑️ Delete Selected",
            bootstyle="danger",
            command=self.eliminar_usuario_seleccionado
        ).pack(side="left", padx=5)
        
        # Filter
        tk.Label(
            btn_frame,
            text="Filter:",
            bg="white",
            font=("Helvetica", 10)
        ).pack(side="left", padx=(20, 5))
        
        self.filter_var = tk.StringVar(value="all")
        tk.Radiobutton(
            btn_frame,
            text="All",
            variable=self.filter_var,
            value="all",
            bg="white",
            command=self.cargar_usuarios
        ).pack(side="left", padx=5)
        
        tk.Radiobutton(
            btn_frame,
            text="Active Only",
            variable=self.filter_var,
            value="active",
            bg="white",
            command=self.cargar_usuarios
        ).pack(side="left", padx=5)
        
        # Treeview with scrollbar
        tree_frame = tk.Frame(self.tab_lista)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Email", "Phone", "Status", "Loans", "MaxLoans"),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("ID", text="User ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Loans", text="Current Loans")
        self.tree.heading("MaxLoans", text="Max Loans")
        
        self.tree.column("ID", width=100)
        self.tree.column("Name", width=180)
        self.tree.column("Email", width=200)
        self.tree.column("Phone", width=120)
        self.tree.column("Status", width=80)
        self.tree.column("Loans", width=100)
        self.tree.column("MaxLoans", width=100)
        
        # Pack
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Statistics label
        self.stats_label = tk.Label(
            self.tab_lista,
            text="",
            bg="white",
            font=("Helvetica", 10)
        )
        self.stats_label.pack(pady=5)
    
    def crear_tab_formulario(self):
        """Create the register/edit user form tab."""
        # Form container
        form_frame = tk.Frame(self.tab_formulario, bg="white")
        form_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        # User ID
        tk.Label(form_frame, text="User ID:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.id_usuario_var = tk.StringVar()
        id_entry = tk.Entry(form_frame, textvariable=self.id_usuario_var, font=("Helvetica", 10), width=30)
        id_entry.grid(row=0, column=1, pady=5, padx=10, sticky="w")
        
        tb.Button(
            form_frame,
            text="🔢 Generate ID",
            bootstyle="secondary-outline",
            command=self.generar_id_usuario
        ).grid(row=0, column=2, padx=5)
        
        # Name
        tk.Label(form_frame, text="Full Name *:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.nombre_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.nombre_var, font=("Helvetica", 10), width=30).grid(
            row=1, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Email
        tk.Label(form_frame, text="Email *:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.email_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.email_var, font=("Helvetica", 10), width=30).grid(
            row=2, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Phone
        tk.Label(form_frame, text="Phone:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=3, column=0, sticky="w", pady=5
        )
        self.telefono_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.telefono_var, font=("Helvetica", 10), width=30).grid(
            row=3, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Address
        tk.Label(form_frame, text="Address:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=4, column=0, sticky="w", pady=5
        )
        self.direccion_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.direccion_var, font=("Helvetica", 10), width=30).grid(
            row=4, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Max Loans
        tk.Label(form_frame, text="Max Loans:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=5, column=0, sticky="w", pady=5
        )
        self.max_prestamos_var = tk.StringVar(value="3")
        tk.Spinbox(
            form_frame,
            from_=1,
            to=10,
            textvariable=self.max_prestamos_var,
            font=("Helvetica", 10),
            width=28
        ).grid(row=5, column=1, pady=5, padx=10, sticky="w")
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        tb.Button(
            btn_frame,
            text="💾 Register User",
            bootstyle="success",
            command=self.registrar_usuario
        ).pack(side="left", padx=10)
        
        tb.Button(
            btn_frame,
            text="🔄 Clear Form",
            bootstyle="secondary",
            command=self.limpiar_formulario
        ).pack(side="left", padx=10)
        
        # Note
        tk.Label(
            form_frame,
            text="* Required fields",
            bg="white",
            font=("Helvetica", 9, "italic"),
            fg="gray"
        ).grid(row=7, column=0, columnspan=3, pady=5)
    
    def crear_tab_estadisticas(self):
        """Create the statistics tab."""
        stats_frame = tk.Frame(self.tab_estadisticas, bg="white")
        stats_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        tk.Label(
            stats_frame,
            text="User Statistics",
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
    
    def cargar_usuarios(self):
        """Load users into the treeview."""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get users
        solo_activos = self.filter_var.get() == "active"
        usuarios = self.gestor_usuarios.listar_todos(solo_activos=solo_activos)
        
        # Populate treeview
        for usuario in usuarios:
            status = "✓ Active" if usuario.activo else "✗ Inactive"
            
            # Color code by status
            tag = "active" if usuario.activo else "inactive"
            
            self.tree.insert("", "end", values=(
                usuario.id_usuario,
                usuario.nombre,
                usuario.email,
                usuario.telefono if usuario.telefono else "N/A",
                status,
                f"{usuario.libros_prestados}",
                f"{usuario.max_prestamos}"
            ), tags=(tag,))
        
        # Configure tags
        self.tree.tag_configure("active", foreground="green")
        self.tree.tag_configure("inactive", foreground="red")
        
        # Update statistics
        stats = self.gestor_usuarios.obtener_estadisticas()
        self.stats_label.config(
            text=f"Total: {stats['total_usuarios']} users | "
                 f"Active: {stats['usuarios_activos']} | "
                 f"Inactive: {stats['usuarios_inactivos']} | "
                 f"With Loans: {stats['usuarios_con_prestamos']}"
        )
    
    def generar_id_usuario(self):
        """Generate a unique user ID."""
        nuevo_id = self.gestor_usuarios.generar_id_unico()
        self.id_usuario_var.set(nuevo_id)
        messagebox.showinfo("ID Generated", f"New User ID: {nuevo_id}")
    
    def registrar_usuario(self):
        """Register a new user."""
        # Get values
        id_usuario = self.id_usuario_var.get().strip()
        nombre = self.nombre_var.get().strip()
        email = self.email_var.get().strip()
        telefono = self.telefono_var.get().strip()
        direccion = self.direccion_var.get().strip()
        max_prestamos_str = self.max_prestamos_var.get().strip()
        
        # Validate required fields
        val_id = validar_texto_no_vacio(id_usuario, "User ID", 3)
        val_nombre = validar_texto_no_vacio(nombre, "Name", 3)
        val_email = validar_email(email)
        
        # Validate phone if provided
        if telefono:
            val_telefono = validar_telefono(telefono)
            if not val_telefono['valido']:
                messagebox.showwarning("Validation Warning", val_telefono['mensaje'])
        
        if not all([val_id['valido'], val_nombre['valido'], val_email['valido']]):
            errores = []
            for val in [val_id, val_nombre, val_email]:
                if not val['valido']:
                    errores.append(val['mensaje'])
            messagebox.showerror("Validation Error", "\n".join(errores))
            return
        
        try:
            max_prestamos = int(max_prestamos_str) if max_prestamos_str else 3
            
            # Register user
            resultado = self.gestor_usuarios.registrar_usuario(
                id_usuario=id_usuario,
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion,
                max_prestamos=max_prestamos
            )
            
            if resultado['exito']:
                messagebox.showinfo("Success", resultado['mensaje'])
                self.limpiar_formulario()
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", resultado['mensaje'])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error registering user: {str(e)}")
    
    def limpiar_formulario(self):
        """Clear all form fields."""
        self.id_usuario_var.set("")
        self.nombre_var.set("")
        self.email_var.set("")
        self.telefono_var.set("")
        self.direccion_var.set("")
        self.max_prestamos_var.set("3")
    
    def editar_usuario_seleccionado(self):
        """Load selected user into form for editing."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a user to edit")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        # Get full user data
        usuario = self.gestor_usuarios.obtener_usuario(values[0])
        
        if not usuario:
            messagebox.showerror("Error", "User not found")
            return
        
        # Load into form
        self.id_usuario_var.set(usuario.id_usuario)
        self.nombre_var.set(usuario.nombre)
        self.email_var.set(usuario.email)
        self.telefono_var.set(usuario.telefono)
        self.direccion_var.set(usuario.direccion)
        self.max_prestamos_var.set(str(usuario.max_prestamos))
        
        # Switch to form tab
        self.notebook.select(self.tab_formulario)
        
        messagebox.showinfo("Edit Mode", "User loaded. Modify fields and click Register to update.")
    
    def activar_usuario_seleccionado(self):
        """Activate selected user."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a user to activate")
            return
        
        item = self.tree.item(selection[0])
        id_usuario = item['values'][0]
        
        resultado = self.gestor_usuarios.activar_usuario(id_usuario)
        
        if resultado['exito']:
            messagebox.showinfo("Success", resultado['mensaje'])
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", resultado['mensaje'])
    
    def desactivar_usuario_seleccionado(self):
        """Deactivate selected user."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a user to deactivate")
            return
        
        item = self.tree.item(selection[0])
        id_usuario = item['values'][0]
        nombre = item['values'][1]
        
        confirm = messagebox.askyesno(
            "Confirm Deactivation",
            f"Are you sure you want to deactivate user:\n\n{nombre} ({id_usuario})?"
        )
        
        if confirm:
            resultado = self.gestor_usuarios.desactivar_usuario(id_usuario)
            
            if resultado['exito']:
                messagebox.showinfo("Success", resultado['mensaje'])
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", resultado['mensaje'])
    
    def eliminar_usuario_seleccionado(self):
        """Delete selected user."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a user to delete")
            return
        
        item = self.tree.item(selection[0])
        id_usuario = item['values'][0]
        nombre = item['values'][1]
        prestamos = item['values'][5]
        
        if int(prestamos) > 0:
            messagebox.showerror(
                "Cannot Delete",
                f"User {nombre} has {prestamos} active loan(s).\n"
                "Users with pending loans cannot be deleted."
            )
            return
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete user:\n\n{nombre} ({id_usuario})?\n\n"
            "This action cannot be undone."
        )
        
        if confirm:
            resultado = self.gestor_usuarios.eliminar_usuario(id_usuario)
            
            if resultado['exito']:
                messagebox.showinfo("Success", resultado['mensaje'])
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", resultado['mensaje'])
    
    def actualizar_estadisticas(self):
        """Update and display statistics."""
        stats = self.gestor_usuarios.obtener_estadisticas()
        
        self.stats_text.delete(1.0, tk.END)
        
        self.stats_text.insert(tk.END, "=" * 70 + "\n")
        self.stats_text.insert(tk.END, "USER STATISTICS\n")
        self.stats_text.insert(tk.END, "=" * 70 + "\n\n")
        
        self.stats_text.insert(tk.END, f"Total Users:              {stats['total_usuarios']}\n")
        self.stats_text.insert(tk.END, f"Active Users:             {stats['usuarios_activos']}\n")
        self.stats_text.insert(tk.END, f"Inactive Users:           {stats['usuarios_inactivos']}\n")
        self.stats_text.insert(tk.END, f"Users with Active Loans:  {stats['usuarios_con_prestamos']}\n")
        self.stats_text.insert(tk.END, f"Total Active Loans:       {stats['total_prestamos_activos']}\n\n")
        
        if stats['total_usuarios'] > 0:
            porcentaje_activos = (stats['usuarios_activos'] / stats['total_usuarios']) * 100
            porcentaje_con_prestamos = (stats['usuarios_con_prestamos'] / stats['total_usuarios']) * 100
            
            self.stats_text.insert(tk.END, "Percentages:\n")
            self.stats_text.insert(tk.END, f"  Active Users:           {porcentaje_activos:.1f}%\n")
            self.stats_text.insert(tk.END, f"  Users with Loans:       {porcentaje_con_prestamos:.1f}%\n\n")
        
        self.stats_text.insert(tk.END, "=" * 70 + "\n")