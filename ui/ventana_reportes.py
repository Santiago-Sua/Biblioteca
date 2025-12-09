"""
Reports and Analytics Window - Library Management System

This module implements the ReportesWindow class which provides comprehensive
reporting functionality including recursive calculations, inventory reports,
and system analytics.

PROJECT REQUIREMENTS:
    - Stack Recursion: Calculate total value of books by author
    - Tail Recursion: Calculate average weight of books by author

Classes:
    ReportesWindow: Main window for reports and analytics

Author: [Your Name]
Date: December 2025
"""

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from datetime import datetime

from gestor.gestor_inventario import GestorInventario
from gestor.gestor_usuarios import GestorUsuarios
from gestor.gestor_prestamos import GestorPrestamos
from gestor.gestor_reservas import GestorReservas
from recursion.recursion_pila import calcular_valor_total_por_autor, demostrar_recursion_pila
from recursion.recursion_cola import calcular_peso_promedio_por_autor, demostrar_recursion_cola


class ReportesWindow:
    """
    Reports and analytics window.
    
    Provides comprehensive reporting including:
    - Recursive calculations (stack and tail recursion)
    - Inventory reports (Merge Sort)
    - System statistics
    - Export functionality
    
    Attributes:
        parent: Parent container widget
        archivo_handler: File operations handler
        gestor_inventario: Inventory manager instance
        gestor_usuarios: Users manager instance
        gestor_prestamos: Loans manager instance
        gestor_reservas: Reservations manager instance
    """
    
    def __init__(self, parent, archivo_handler):
        """
        Initialize the reports window.
        
        Args:
            parent: Parent container widget
            archivo_handler: ArchivoHandler instance
        """
        self.parent = parent
        self.archivo_handler = archivo_handler
        
        # Initialize all managers
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
        """Create all widgets for the reports window."""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Reports & Analytics",
            font=("Helvetica", 18, "bold"),
            bg="white",
            fg="#004080"
        )
        title_label.pack(pady=10)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Recursive calculations
        self.tab_recursion = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_recursion, text="🔄 Recursion")
        self.crear_tab_recursion()
        
        # Tab 2: Inventory reports
        self.tab_inventario = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_inventario, text="📚 Inventory Reports")
        self.crear_tab_inventario()
        
        # Tab 3: System statistics
        self.tab_estadisticas = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_estadisticas, text="📊 System Statistics")
        self.crear_tab_estadisticas()
    
    def crear_tab_recursion(self):
        """Create the recursion calculations tab."""
        recursion_frame = tk.Frame(self.tab_recursion, bg="white")
        recursion_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        tk.Label(
            recursion_frame,
            text="Recursive Calculations by Author",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#004080"
        ).pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(recursion_frame, bg="white")
        input_frame.pack(pady=15)
        
        tk.Label(
            input_frame,
            text="Author Name:",
            bg="white",
            font=("Helvetica", 11)
        ).grid(row=0, column=0, padx=5, pady=10)
        
        self.autor_var = tk.StringVar()
        tk.Entry(
            input_frame,
            textvariable=self.autor_var,
            font=("Helvetica", 11),
            width=30
        ).grid(row=0, column=1, padx=5, pady=10)
        
        # Calculation type
        tk.Label(
            input_frame,
            text="Calculation Type:",
            bg="white",
            font=("Helvetica", 11)
        ).grid(row=1, column=0, padx=5, pady=10)
        
        self.recursion_type_var = tk.StringVar(value="both")
        
        type_frame = tk.Frame(input_frame, bg="white")
        type_frame.grid(row=1, column=1, sticky="w", padx=5)
        
        tk.Radiobutton(
            type_frame,
            text="Stack Recursion (Total Value)",
            variable=self.recursion_type_var,
            value="stack",
            bg="white"
        ).pack(anchor="w")
        
        tk.Radiobutton(
            type_frame,
            text="Tail Recursion (Avg Weight)",
            variable=self.recursion_type_var,
            value="tail",
            bg="white"
        ).pack(anchor="w")
        
        tk.Radiobutton(
            type_frame,
            text="Both (with demonstration)",
            variable=self.recursion_type_var,
            value="both",
            bg="white"
        ).pack(anchor="w")
        
        # Run button
        tb.Button(
            recursion_frame,
            text="🔄 Calculate",
            bootstyle="success",
            command=self.calcular_recursion
        ).pack(pady=15)
        
        # Results display
        results_frame = tk.Frame(recursion_frame)
        results_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical")
        
        self.recursion_text = tk.Text(
            results_frame,
            font=("Courier", 9),
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.recursion_text.yview)
        
        self.recursion_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_tab_inventario(self):
        """Create the inventory reports tab."""
        inv_frame = tk.Frame(self.tab_inventario, bg="white")
        inv_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        tk.Label(
            inv_frame,
            text="Inventory Reports (Merge Sort)",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#004080"
        ).pack(pady=10)
        
        # Options
        options_frame = tk.Frame(inv_frame, bg="white")
        options_frame.pack(pady=15)
        
        tk.Label(
            options_frame,
            text="Sort by:",
            bg="white",
            font=("Helvetica", 11)
        ).grid(row=0, column=0, padx=5, pady=5)
        
        self.sort_by_var = tk.StringVar(value="value")
        
        sort_frame = tk.Frame(options_frame, bg="white")
        sort_frame.grid(row=0, column=1, sticky="w", padx=5)
        
        tk.Radiobutton(
            sort_frame,
            text="Value (COP)",
            variable=self.sort_by_var,
            value="value",
            bg="white"
        ).pack(side="left", padx=5)
        
        tk.Radiobutton(
            sort_frame,
            text="Weight (kg)",
            variable=self.sort_by_var,
            value="weight",
            bg="white"
        ).pack(side="left", padx=5)
        
        tk.Label(
            options_frame,
            text="Order:",
            bg="white",
            font=("Helvetica", 11)
        ).grid(row=1, column=0, padx=5, pady=5)
        
        self.order_var = tk.StringVar(value="desc")
        
        order_frame = tk.Frame(options_frame, bg="white")
        order_frame.grid(row=1, column=1, sticky="w", padx=5)
        
        tk.Radiobutton(
            order_frame,
            text="Descending (High to Low)",
            variable=self.order_var,
            value="desc",
            bg="white"
        ).pack(anchor="w")
        
        tk.Radiobutton(
            order_frame,
            text="Ascending (Low to High)",
            variable=self.order_var,
            value="asc",
            bg="white"
        ).pack(anchor="w")
        
        # Buttons
        btn_frame = tk.Frame(inv_frame, bg="white")
        btn_frame.pack(pady=15)
        
        tb.Button(
            btn_frame,
            text="📊 Generate Report",
            bootstyle="success",
            command=self.generar_reporte_inventario
        ).pack(side="left", padx=5)
        
        tb.Button(
            btn_frame,
            text="💾 Export to CSV",
            bootstyle="info",
            command=self.exportar_reporte_csv
        ).pack(side="left", padx=5)
        
        # Results display
        results_frame = tk.Frame(inv_frame)
        results_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical")
        
        self.inventory_text = tk.Text(
            results_frame,
            font=("Courier", 9),
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.inventory_text.yview)
        
        self.inventory_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_tab_estadisticas(self):
        """Create the system statistics tab."""
        stats_frame = tk.Frame(self.tab_estadisticas, bg="white")
        stats_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        tk.Label(
            stats_frame,
            text="System Statistics",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#004080"
        ).pack(pady=10)
        
        # Refresh button
        tb.Button(
            stats_frame,
            text="🔄 Refresh All Statistics",
            bootstyle="info",
            command=self.actualizar_estadisticas_sistema
        ).pack(pady=15)
        
        # Results display
        results_frame = tk.Frame(stats_frame)
        results_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical")
        
        self.system_stats_text = tk.Text(
            results_frame,
            font=("Courier", 10),
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.system_stats_text.yview)
        
        self.system_stats_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initial load
        self.actualizar_estadisticas_sistema()
    
    def calcular_recursion(self):
        """Calculate recursive functions for an author."""
        autor = self.autor_var.get().strip()
        
        if not autor:
            messagebox.showwarning("Empty Field", "Please enter an author name")
            return
        
        tipo = self.recursion_type_var.get()
        libros = self.gestor_inventario.listar_todos()
        
        if not libros:
            messagebox.showerror("No Books", "No books in inventory")
            return
        
        self.recursion_text.delete(1.0, tk.END)
        
        self.recursion_text.insert(tk.END, "=" * 90 + "\n")
        self.recursion_text.insert(tk.END, "RECURSIVE CALCULATIONS BY AUTHOR\n")
        self.recursion_text.insert(tk.END, "=" * 90 + "\n\n")
        self.recursion_text.insert(tk.END, f"Author: {autor}\n")
        self.recursion_text.insert(tk.END, f"Total books in inventory: {len(libros)}\n\n")
        
        try:
            if tipo in ["stack", "both"]:
                self.recursion_text.insert(tk.END, "-" * 90 + "\n")
                self.recursion_text.insert(tk.END, "STACK RECURSION - Total Value Calculation\n")
                self.recursion_text.insert(tk.END, "-" * 90 + "\n\n")
                
                valor_total = calcular_valor_total_por_autor(libros, autor)
                
                self.recursion_text.insert(tk.END, f"Total Value of books by {autor}:\n")
                self.recursion_text.insert(tk.END, f"${valor_total:,.0f} COP\n\n")
                
                if tipo == "both":
                    self.recursion_text.insert(tk.END, "Demonstration (showing recursion process):\n\n")
                    self.recursion_text.update()
                    
                    # Redirect stdout temporarily
                    import io
                    import sys
                    old_stdout = sys.stdout
                    sys.stdout = buffer = io.StringIO()
                    
                    demostrar_recursion_pila(libros[:8], autor, max_profundidad=5)
                    
                    sys.stdout = old_stdout
                    demo_output = buffer.getvalue()
                    self.recursion_text.insert(tk.END, demo_output)
                    self.recursion_text.insert(tk.END, "\n")
            
            if tipo in ["tail", "both"]:
                self.recursion_text.insert(tk.END, "-" * 90 + "\n")
                self.recursion_text.insert(tk.END, "TAIL RECURSION - Average Weight Calculation\n")
                self.recursion_text.insert(tk.END, "-" * 90 + "\n\n")
                
                peso_promedio = calcular_peso_promedio_por_autor(libros, autor, mostrar_proceso=False)
                
                self.recursion_text.insert(tk.END, f"Average Weight of books by {autor}:\n")
                self.recursion_text.insert(tk.END, f"{peso_promedio:.2f} kg\n\n")
                
                if tipo == "both":
                    self.recursion_text.insert(tk.END, "Demonstration (showing tail recursion with accumulators):\n\n")
                    self.recursion_text.update()
                    
                    # Redirect stdout
                    import io
                    import sys
                    old_stdout = sys.stdout
                    sys.stdout = buffer = io.StringIO()
                    
                    calcular_peso_promedio_por_autor(libros[:8], autor, mostrar_proceso=True)
                    
                    sys.stdout = old_stdout
                    demo_output = buffer.getvalue()
                    self.recursion_text.insert(tk.END, demo_output)
            
            self.recursion_text.insert(tk.END, "\n" + "=" * 90 + "\n")
            
            messagebox.showinfo("Success", "Recursive calculations completed!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating: {str(e)}")
    
    def generar_reporte_inventario(self):
        """Generate inventory report using Merge Sort."""
        try:
            sort_by = self.sort_by_var.get()
            order_desc = self.order_var.get() == "desc"
            
            # Generate report
            if sort_by == "value":
                reporte = self.gestor_inventario.generar_reporte_por_valor(reverso=order_desc)
                columna_sort = "Value"
            else:
                from algoritmos_ordenamiento.merge_sort import generar_reporte_ordenado
                reporte = generar_reporte_ordenado(
                    self.gestor_inventario.listar_todos(),
                    clave='peso',
                    reverso=order_desc,
                    formato='dict',
                    incluir_indices=True
                )
                columna_sort = "Weight"
            
            # Display report
            self.inventory_text.delete(1.0, tk.END)
            
            self.inventory_text.insert(tk.END, "=" * 100 + "\n")
            self.inventory_text.insert(tk.END, f"INVENTORY REPORT - SORTED BY {columna_sort.upper()} (MERGE SORT)\n")
            self.inventory_text.insert(tk.END, "=" * 100 + "\n\n")
            
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.inventory_text.insert(tk.END, f"Generated: {fecha}\n")
            self.inventory_text.insert(tk.END, f"Sort Order: {'Descending' if order_desc else 'Ascending'}\n")
            self.inventory_text.insert(tk.END, f"Total Books: {len(reporte)}\n\n")
            
            # Header
            header = f"{'#':<5} {'Title':<35} {'Author':<25} {'Value (COP)':<15} {'Weight (kg)':<12} {'Stock':<6}\n"
            self.inventory_text.insert(tk.END, header)
            self.inventory_text.insert(tk.END, "-" * 100 + "\n")
            
            # Data
            for libro in reporte:
                pos = libro.get('posicion', '-')
                titulo = libro['titulo'][:33] + ".." if len(libro['titulo']) > 35 else libro['titulo']
                autor = libro['autor'][:23] + ".." if len(libro['autor']) > 25 else libro['autor']
                valor = f"${libro['valor']:,.0f}"
                peso = f"{libro['peso']:.2f}"
                stock = libro['stock']
                
                linea = f"{pos:<5} {titulo:<35} {autor:<25} {valor:<15} {peso:<12} {stock:<6}\n"
                self.inventory_text.insert(tk.END, linea)
            
            # Summary
            total_valor = sum(l['valor'] * l['stock'] for l in reporte)
            total_peso = sum(l['peso'] * l['stock'] for l in reporte)
            
            self.inventory_text.insert(tk.END, "\n" + "=" * 100 + "\n")
            self.inventory_text.insert(tk.END, "SUMMARY:\n")
            self.inventory_text.insert(tk.END, f"Total Inventory Value: ${total_valor:,.0f} COP\n")
            self.inventory_text.insert(tk.END, f"Total Inventory Weight: {total_peso:.2f} kg\n")
            self.inventory_text.insert(tk.END, "=" * 100 + "\n")
            
            messagebox.showinfo("Success", f"Report generated with {len(reporte)} books")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")
    
    def exportar_reporte_csv(self):
        """Export current report to CSV file."""
        try:
            # Ask for file location
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"inventory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if not filename:
                return
            
            sort_by = self.sort_by_var.get()
            order_desc = self.order_var.get() == "desc"
            
            # Generate report
            if sort_by == "value":
                reporte = self.gestor_inventario.generar_reporte_por_valor(reverso=order_desc)
            else:
                from algoritmos_ordenamiento.merge_sort import generar_reporte_ordenado
                reporte = generar_reporte_ordenado(
                    self.gestor_inventario.listar_todos(),
                    clave='peso',
                    reverso=order_desc,
                    formato='dict',
                    incluir_indices=False
                )
            
            # Export to CSV
            success = self.archivo_handler.guardar_csv(filename, reporte)
            
            if success:
                messagebox.showinfo("Success", f"Report exported to:\n{filename}")
            else:
                messagebox.showerror("Error", "Failed to export report")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting: {str(e)}")
    
    def actualizar_estadisticas_sistema(self):
        """Update and display comprehensive system statistics."""
        try:
            # Get statistics from all managers
            stats_inv = self.gestor_inventario.obtener_estadisticas()
            stats_users = self.gestor_usuarios.obtener_estadisticas()
            stats_loans = self.gestor_prestamos.obtener_estadisticas()
            stats_res = self.gestor_reservas.obtener_estadisticas()
            
            self.system_stats_text.delete(1.0, tk.END)
            
            self.system_stats_text.insert(tk.END, "=" * 80 + "\n")
            self.system_stats_text.insert(tk.END, "LIBRARY MANAGEMENT SYSTEM - COMPREHENSIVE STATISTICS\n")
            self.system_stats_text.insert(tk.END, "=" * 80 + "\n\n")
            
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.system_stats_text.insert(tk.END, f"Generated: {fecha}\n\n")
            
            # Inventory
            self.system_stats_text.insert(tk.END, "📚 INVENTORY:\n")
            self.system_stats_text.insert(tk.END, f"  Total Books (Titles):        {stats_inv['total_libros']}\n")
            self.system_stats_text.insert(tk.END, f"  Total Stock (Copies):        {stats_inv['total_stock']}\n")
            self.system_stats_text.insert(tk.END, f"  Available Books:             {stats_inv['disponibles']}\n")
            self.system_stats_text.insert(tk.END, f"  Out of Stock:                {stats_inv['agotados']}\n")
            self.system_stats_text.insert(tk.END, f"  Total Inventory Value:       ${stats_inv['valor_total']:,.0f} COP\n")
            self.system_stats_text.insert(tk.END, f"  Total Inventory Weight:      {stats_inv['peso_total']:.2f} kg\n\n")
            
            # Users
            self.system_stats_text.insert(tk.END, "👥 USERS:\n")
            self.system_stats_text.insert(tk.END, f"  Total Registered Users:      {stats_users['total_usuarios']}\n")
            self.system_stats_text.insert(tk.END, f"  Active Users:                {stats_users['usuarios_activos']}\n")
            self.system_stats_text.insert(tk.END, f"  Inactive Users:              {stats_users['usuarios_inactivos']}\n")
            self.system_stats_text.insert(tk.END, f"  Users with Active Loans:     {stats_users['usuarios_con_prestamos']}\n\n")
            
            # Loans
            self.system_stats_text.insert(tk.END, "📋 LOANS:\n")
            self.system_stats_text.insert(tk.END, f"  Users with Loan History:     {stats_loans['total_usuarios_con_historial']}\n")
            self.system_stats_text.insert(tk.END, f"  Total Historical Loans:      {stats_loans['total_prestamos_historicos']}\n")
            self.system_stats_text.insert(tk.END, f"  Currently Active Loans:      {stats_loans['prestamos_activos']}\n")
            self.system_stats_text.insert(tk.END, f"  Completed Loans:             {stats_loans['prestamos_completados']}\n\n")
            
            # Reservations
            self.system_stats_text.insert(tk.END, "⏳ RESERVATIONS:\n")
            self.system_stats_text.insert(tk.END, f"  Active Reservations:         {stats_res['total_reservas']}\n")
            self.system_stats_text.insert(tk.END, f"  Unique Users:                {stats_res['usuarios_unicos']}\n")
            self.system_stats_text.insert(tk.END, f"  Unique Books Reserved:       {stats_res['libros_unicos']}\n")
            self.system_stats_text.insert(tk.END, f"  Avg Reservations/Book:       {stats_res['promedio_reservas_por_libro']:.2f}\n\n")
            
            # Calculated metrics
            self.system_stats_text.insert(tk.END, "📊 CALCULATED METRICS:\n")
            
            if stats_inv['total_libros'] > 0:
                avg_value = stats_inv['valor_total'] / stats_inv['total_libros']
                avg_weight = stats_inv['peso_total'] / stats_inv['total_stock'] if stats_inv['total_stock'] > 0 else 0
                self.system_stats_text.insert(tk.END, f"  Average Value per Title:     ${avg_value:,.0f} COP\n")
                self.system_stats_text.insert(tk.END, f"  Average Weight per Copy:     {avg_weight:.2f} kg\n")
            
            if stats_users['total_usuarios'] > 0:
                loan_rate = (stats_users['usuarios_con_prestamos'] / stats_users['total_usuarios']) * 100
                self.system_stats_text.insert(tk.END, f"  User Loan Participation:     {loan_rate:.1f}%\n")
            
            if stats_loans['total_prestamos_historicos'] > 0:
                completion_rate = (stats_loans['prestamos_completados'] / stats_loans['total_prestamos_historicos']) * 100
                self.system_stats_text.insert(tk.END, f"  Loan Completion Rate:        {completion_rate:.1f}%\n")
            
            self.system_stats_text.insert(tk.END, "\n" + "=" * 80 + "\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading statistics: {str(e)}")