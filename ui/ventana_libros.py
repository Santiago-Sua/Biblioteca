"""
Books Management Window - Library Management System

This module implements the LibrosWindow class which provides a complete
interface for managing the book inventory including CRUD operations,
searches, and report generation.

Classes:
    LibrosWindow: Main window for books management

Author: [Your Name]
Date: December 2025
"""

import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from models.libro import Libro
from gestor.gestor_inventario import GestorInventario
from utils.validaciones import validar_isbn, validar_numero_positivo, validar_texto_no_vacio


class LibrosWindow:
    """
    Books management window.
    
    Provides complete CRUD functionality for books including:
    - View all books (General and Sorted inventories)
    - Create new books
    - Update book information
    - Delete books
    - Search by title, author, or ISBN
    - Generate reports sorted by value
    
    Attributes:
        parent: Parent container widget
        archivo_handler: File operations handler
        gestor_inventario: Inventory manager instance
    """
    
    def __init__(self, parent, archivo_handler):
        """
        Initialize the books management window.
        
        Args:
            parent: Parent container widget
            archivo_handler: ArchivoHandler instance
        """
        self.parent = parent
        self.archivo_handler = archivo_handler
        
        # Initialize inventory manager
        self.gestor_inventario = GestorInventario(archivo_handler)
        
        # Create main container
        self.main_frame = tk.Frame(parent, bg="white")
        self.main_frame.pack(fill="both", expand=True)
        
        # Create UI
        self.create_widgets()
        self.cargar_libros()
    
    def create_widgets(self):
        """Create all widgets for the books window."""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Books Management",
            font=("Helvetica", 18, "bold"),
            bg="white",
            fg="#004080"
        )
        title_label.pack(pady=10)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: List/View books
        self.tab_lista = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_lista, text="📋 Book List")
        self.crear_tab_lista()
        
        # Tab 2: Add/Edit book
        self.tab_formulario = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_formulario, text="➕ Add/Edit Book")
        self.crear_tab_formulario()
        
        # Tab 3: Search
        self.tab_busqueda = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_busqueda, text="🔍 Search")
        self.crear_tab_busqueda()
        
        # Tab 4: Reports
        self.tab_reportes = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_reportes, text="📊 Reports")
        self.crear_tab_reportes()
    
    def crear_tab_lista(self):
        """Create the book list tab."""
        # Control buttons
        btn_frame = tk.Frame(self.tab_lista, bg="white")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tb.Button(
            btn_frame,
            text="🔄 Refresh",
            bootstyle="info",
            command=self.cargar_libros
        ).pack(side="left", padx=5)
        
        tb.Button(
            btn_frame,
            text="✏️ Edit Selected",
            bootstyle="warning",
            command=self.editar_libro_seleccionado
        ).pack(side="left", padx=5)
        
        tb.Button(
            btn_frame,
            text="🗑️ Delete Selected",
            bootstyle="danger",
            command=self.eliminar_libro_seleccionado
        ).pack(side="left", padx=5)
        
        # Inventory selector
        tk.Label(
            btn_frame,
            text="Inventory:",
            bg="white",
            font=("Helvetica", 10)
        ).pack(side="left", padx=(20, 5))
        
        self.inventory_var = tk.StringVar(value="general")
        tk.Radiobutton(
            btn_frame,
            text="General (Load Order)",
            variable=self.inventory_var,
            value="general",
            bg="white",
            command=self.cargar_libros
        ).pack(side="left", padx=5)
        
        tk.Radiobutton(
            btn_frame,
            text="Sorted (by ISBN)",
            variable=self.inventory_var,
            value="ordenado",
            bg="white",
            command=self.cargar_libros
        ).pack(side="left", padx=5)
        
        # Treeview with scrollbar
        tree_frame = tk.Frame(self.tab_lista)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ISBN", "Title", "Author", "Weight", "Value", "Stock", "Genre"),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Weight", text="Weight (kg)")
        self.tree.heading("Value", text="Value (COP)")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Genre", text="Genre")
        
        self.tree.column("ISBN", width=120)
        self.tree.column("Title", width=200)
        self.tree.column("Author", width=150)
        self.tree.column("Weight", width=80)
        self.tree.column("Value", width=100)
        self.tree.column("Stock", width=60)
        self.tree.column("Genre", width=100)
        
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
        """Create the add/edit book form tab."""
        # Form container
        form_frame = tk.Frame(self.tab_formulario, bg="white")
        form_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        # ISBN
        tk.Label(form_frame, text="ISBN *:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.isbn_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.isbn_var, font=("Helvetica", 10), width=30).grid(
            row=0, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Title
        tk.Label(form_frame, text="Title *:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.titulo_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.titulo_var, font=("Helvetica", 10), width=30).grid(
            row=1, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Author
        tk.Label(form_frame, text="Author *:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.autor_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.autor_var, font=("Helvetica", 10), width=30).grid(
            row=2, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Weight
        tk.Label(form_frame, text="Weight (kg) *:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=3, column=0, sticky="w", pady=5
        )
        self.peso_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.peso_var, font=("Helvetica", 10), width=30).grid(
            row=3, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Value
        tk.Label(form_frame, text="Value (COP) *:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=4, column=0, sticky="w", pady=5
        )
        self.valor_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.valor_var, font=("Helvetica", 10), width=30).grid(
            row=4, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Stock
        tk.Label(form_frame, text="Stock:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=5, column=0, sticky="w", pady=5
        )
        self.stock_var = tk.StringVar(value="1")
        tk.Entry(form_frame, textvariable=self.stock_var, font=("Helvetica", 10), width=30).grid(
            row=5, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Genre
        tk.Label(form_frame, text="Genre:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=6, column=0, sticky="w", pady=5
        )
        self.genero_var = tk.StringVar(value="General")
        tk.Entry(form_frame, textvariable=self.genero_var, font=("Helvetica", 10), width=30).grid(
            row=6, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Editorial
        tk.Label(form_frame, text="Publisher:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=7, column=0, sticky="w", pady=5
        )
        self.editorial_var = tk.StringVar(value="Unknown")
        tk.Entry(form_frame, textvariable=self.editorial_var, font=("Helvetica", 10), width=30).grid(
            row=7, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Year
        tk.Label(form_frame, text="Year:", bg="white", font=("Helvetica", 10, "bold")).grid(
            row=8, column=0, sticky="w", pady=5
        )
        self.anio_var = tk.StringVar(value="2024")
        tk.Entry(form_frame, textvariable=self.anio_var, font=("Helvetica", 10), width=30).grid(
            row=8, column=1, pady=5, padx=10, sticky="w"
        )
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        tb.Button(
            btn_frame,
            text="💾 Save Book",
            bootstyle="success",
            command=self.guardar_libro
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
        ).grid(row=10, column=0, columnspan=2, pady=5)
    
    def crear_tab_busqueda(self):
        """Create the search tab."""
        search_frame = tk.Frame(self.tab_busqueda, bg="white")
        search_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Search options
        tk.Label(
            search_frame,
            text="Search by:",
            bg="white",
            font=("Helvetica", 12, "bold")
        ).pack(anchor="w", pady=(0, 10))
        
        self.search_type_var = tk.StringVar(value="title")
        
        tk.Radiobutton(
            search_frame,
            text="Title",
            variable=self.search_type_var,
            value="title",
            bg="white"
        ).pack(anchor="w")
        
        tk.Radiobutton(
            search_frame,
            text="Author",
            variable=self.search_type_var,
            value="author",
            bg="white"
        ).pack(anchor="w")
        
        tk.Radiobutton(
            search_frame,
            text="ISBN (exact)",
            variable=self.search_type_var,
            value="isbn",
            bg="white"
        ).pack(anchor="w")
        
        # Search entry
        tk.Label(
            search_frame,
            text="Search term:",
            bg="white",
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w", pady=(15, 5))
        
        self.search_var = tk.StringVar()
        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Helvetica", 12),
            width=40
        ).pack(anchor="w", pady=5)
        
        tb.Button(
            search_frame,
            text="🔍 Search",
            bootstyle="primary",
            command=self.buscar_libros
        ).pack(anchor="w", pady=10)
        
        # Results
        tk.Label(
            search_frame,
            text="Results:",
            bg="white",
            font=("Helvetica", 12, "bold")
        ).pack(anchor="w", pady=(15, 5))
        
        self.search_results_text = tk.Text(
            search_frame,
            height=15,
            width=80,
            font=("Helvetica", 10)
        )
        self.search_results_text.pack(fill="both", expand=True)
    
    def crear_tab_reportes(self):
        """Create the reports tab."""
        report_frame = tk.Frame(self.tab_reportes, bg="white")
        report_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        tk.Label(
            report_frame,
            text="Generate Inventory Report",
            bg="white",
            font=("Helvetica", 14, "bold")
        ).pack(pady=10)
        
        tk.Label(
            report_frame,
            text="Sort books by value (COP) using Merge Sort algorithm",
            bg="white",
            font=("Helvetica", 10)
        ).pack(pady=5)
        
        # Sort order
        self.sort_order_var = tk.StringVar(value="desc")
        
        order_frame = tk.Frame(report_frame, bg="white")
        order_frame.pack(pady=10)
        
        tk.Radiobutton(
            order_frame,
            text="Highest to Lowest",
            variable=self.sort_order_var,
            value="desc",
            bg="white"
        ).pack(side="left", padx=10)
        
        tk.Radiobutton(
            order_frame,
            text="Lowest to Highest",
            variable=self.sort_order_var,
            value="asc",
            bg="white"
        ).pack(side="left", padx=10)
        
        tb.Button(
            report_frame,
            text="📊 Generate Report",
            bootstyle="success",
            command=self.generar_reporte
        ).pack(pady=10)
        
        # Report display
        self.report_text = tk.Text(
            report_frame,
            height=20,
            width=90,
            font=("Courier", 9)
        )
        self.report_text.pack(fill="both", expand=True, pady=10)
    
    def cargar_libros(self):
        """Load books into the treeview."""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get books from selected inventory
        ordenado = self.inventory_var.get() == "ordenado"
        libros = self.gestor_inventario.listar_todos(ordenado=ordenado)
        
        # Populate treeview
        for libro in libros:
            self.tree.insert("", "end", values=(
                libro.isbn,
                libro.titulo,
                libro.autor,
                f"{libro.peso:.2f}",
                f"${libro.valor:,.0f}",
                libro.stock,
                libro.genero
            ))
        
        # Update statistics
        stats = self.gestor_inventario.obtener_estadisticas()
        self.stats_label.config(
            text=f"Total: {stats['total_libros']} books | "
                 f"Stock: {stats['total_stock']} copies | "
                 f"Available: {stats['disponibles']} | "
                 f"Value: ${stats['valor_total']:,.0f} COP"
        )
    
    def guardar_libro(self):
        """Save a new book or update existing one."""
        # Validate inputs
        isbn = self.isbn_var.get().strip()
        titulo = self.titulo_var.get().strip()
        autor = self.autor_var.get().strip()
        peso_str = self.peso_var.get().strip()
        valor_str = self.valor_var.get().strip()
        stock_str = self.stock_var.get().strip()
        genero = self.genero_var.get().strip()
        editorial = self.editorial_var.get().strip()
        anio_str = self.anio_var.get().strip()
        
        # Validate required fields
        val_isbn = validar_isbn(isbn)
        val_titulo = validar_texto_no_vacio(titulo, "Title", 2)
        val_autor = validar_texto_no_vacio(autor, "Author", 2)
        val_peso = validar_numero_positivo(peso_str, "Weight")
        val_valor = validar_numero_positivo(valor_str, "Value")
        
        if not all([val_isbn['valido'], val_titulo['valido'], val_autor['valido'], 
                   val_peso['valido'], val_valor['valido']]):
            errores = []
            for val in [val_isbn, val_titulo, val_autor, val_peso, val_valor]:
                if not val['valido']:
                    errores.append(val['mensaje'])
            messagebox.showerror("Validation Error", "\n".join(errores))
            return
        
        try:
            # Create book object
            libro = Libro(
                isbn=isbn,
                titulo=titulo,
                autor=autor,
                peso=float(peso_str),
                valor=float(valor_str),
                stock=int(stock_str) if stock_str else 1,
                genero=genero if genero else "General",
                editorial=editorial if editorial else "Unknown",
                anio_publicacion=int(anio_str) if anio_str else 2024
            )
            
            # Add to inventory
            if self.gestor_inventario.agregar_libro(libro):
                messagebox.showinfo("Success", f"Book '{titulo}' added successfully!")
                self.limpiar_formulario()
                self.cargar_libros()
            else:
                messagebox.showerror("Error", "Could not add book. ISBN might already exist.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error saving book: {str(e)}")
    
    def limpiar_formulario(self):
        """Clear all form fields."""
        self.isbn_var.set("")
        self.titulo_var.set("")
        self.autor_var.set("")
        self.peso_var.set("")
        self.valor_var.set("")
        self.stock_var.set("1")
        self.genero_var.set("General")
        self.editorial_var.set("Unknown")
        self.anio_var.set("2024")
    
    def editar_libro_seleccionado(self):
        """Load selected book into form for editing."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a book to edit")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        # Load into form
        self.isbn_var.set(values[0])
        self.titulo_var.set(values[1])
        self.autor_var.set(values[2])
        self.peso_var.set(values[3])
        self.valor_var.set(values[4].replace('$', '').replace(',', ''))
        self.stock_var.set(values[5])
        self.genero_var.set(values[6])
        
        # Switch to form tab
        self.notebook.select(self.tab_formulario)
        
        messagebox.showinfo("Edit Mode", "Book loaded. Modify and save to update.")
    
    def eliminar_libro_seleccionado(self):
        """Delete selected book."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a book to delete")
            return
        
        item = self.tree.item(selection[0])
        isbn = item['values'][0]
        titulo = item['values'][1]
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete:\n\n{titulo}\nISBN: {isbn}?"
        )
        
        if confirm:
            if self.gestor_inventario.eliminar_libro(isbn):
                messagebox.showinfo("Success", "Book deleted successfully")
                self.cargar_libros()
            else:
                messagebox.showerror("Error", "Could not delete book")
    
    def buscar_libros(self):
        """Search for books based on selected criteria."""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            messagebox.showwarning("Empty Search", "Please enter a search term")
            return
        
        search_type = self.search_type_var.get()
        
        if search_type == "title":
            resultados = self.gestor_inventario.buscar_por_titulo(search_term)
        elif search_type == "author":
            resultados = self.gestor_inventario.buscar_por_autor(search_term)
        else:  # isbn
            libro = self.gestor_inventario.buscar_por_isbn(search_term)
            resultados = [libro] if libro else []
        
        # Display results
        self.search_results_text.delete(1.0, tk.END)
        
        if not resultados:
            self.search_results_text.insert(tk.END, "No books found.\n")
        else:
            self.search_results_text.insert(tk.END, f"Found {len(resultados)} book(s):\n\n")
            
            for i, libro in enumerate(resultados, 1):
                self.search_results_text.insert(tk.END, f"{i}. {libro.titulo}\n")
                self.search_results_text.insert(tk.END, f"   ISBN: {libro.isbn}\n")
                self.search_results_text.insert(tk.END, f"   Author: {libro.autor}\n")
                self.search_results_text.insert(tk.END, f"   Value: ${libro.valor:,.0f} COP\n")
                self.search_results_text.insert(tk.END, f"   Stock: {libro.stock}\n\n")
    
    def generar_reporte(self):
        """Generate inventory report sorted by value."""
        reverso = self.sort_order_var.get() == "desc"
        reporte = self.gestor_inventario.generar_reporte_por_valor(reverso=reverso)
        
        # Display report
        self.report_text.delete(1.0, tk.END)
        
        self.report_text.insert(tk.END, "=" * 90 + "\n")
        self.report_text.insert(tk.END, "INVENTORY REPORT - SORTED BY VALUE (MERGE SORT)\n")
        self.report_text.insert(tk.END, "=" * 90 + "\n\n")
        
        orden = "Highest to Lowest" if reverso else "Lowest to Highest"
        self.report_text.insert(tk.END, f"Order: {orden}\n")
        self.report_text.insert(tk.END, f"Total Books: {len(reporte)}\n\n")
        
        self.report_text.insert(tk.END, f"{'#':<5} {'Title':<30} {'Author':<20} {'Value (COP)':<15} {'Stock':<6}\n")
        self.report_text.insert(tk.END, "-" * 90 + "\n")
        
        for libro in reporte:
            pos = libro.get('posicion', '-')
            titulo = libro['titulo'][:28] + ".." if len(libro['titulo']) > 30 else libro['titulo']
            autor = libro['autor'][:18] + ".." if len(libro['autor']) > 20 else libro['autor']
            valor = f"${libro['valor']:,.0f}"
            stock = libro['stock']
            
            self.report_text.insert(tk.END, f"{pos:<5} {titulo:<30} {autor:<20} {valor:<15} {stock:<6}\n")
        
        self.report_text.insert(tk.END, "\n" + "=" * 90 + "\n")
        
        messagebox.showinfo("Success", f"Report generated with {len(reporte)} books")