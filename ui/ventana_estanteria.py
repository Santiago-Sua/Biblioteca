"""
Shelf Management Window - Library Management System

This module implements the EstanteriaWindow class which provides interfaces
for the shelf optimization module using Brute Force and Backtracking algorithms.

PROJECT REQUIREMENTS:
    - Brute Force: Find ALL combinations of 4 books that exceed 8 kg
    - Backtracking: Find optimal combination that maximizes value without exceeding 8 kg

Classes:
    EstanteriaWindow: Main window for shelf optimization

Author: [Your Name]
Date: December 2025
"""

import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from gestor.gestor_inventario import GestorInventario
from algoritmos_resolucion.fuerza_bruta import (
    encontrar_combinaciones_riesgosas,
    analizar_seguridad_estantes,
    demostrar_fuerza_bruta
)
from algoritmos_resolucion.backtracking import (
    optimizar_estante,
    backtracking_con_demostracion
)


class EstanteriaWindow:
    """
    Shelf management and optimization window.
    
    Provides functionality for:
    - Brute Force: Find risky combinations (4 books > 8 kg)
    - Backtracking: Optimize shelf value (max value, ≤ 8 kg)
    - Safety analysis
    - Optimization reports
    
    Attributes:
        parent: Parent container widget
        archivo_handler: File operations handler
        gestor_inventario: Inventory manager instance
    """
    
    def __init__(self, parent, archivo_handler):
        """
        Initialize the shelf management window.
        
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
    
    def create_widgets(self):
        """Create all widgets for the shelf window."""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Shelf Management & Optimization",
            font=("Helvetica", 18, "bold"),
            bg="white",
            fg="#004080"
        )
        title_label.pack(pady=10)
        
        # Info label
        info_label = tk.Label(
            self.main_frame,
            text="Maximum shelf capacity: 8.0 kg",
            font=("Helvetica", 10, "italic"),
            bg="white",
            fg="red"
        )
        info_label.pack(pady=5)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Brute Force (Risky combinations)
        self.tab_brute_force = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_brute_force, text="⚠️ Brute Force (Risky)")
        self.crear_tab_brute_force()
        
        # Tab 2: Backtracking (Optimization)
        self.tab_backtracking = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_backtracking, text="✨ Backtracking (Optimal)")
        self.crear_tab_backtracking()
        
        # Tab 3: Safety Analysis
        self.tab_analisis = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_analisis, text="📊 Safety Analysis")
        self.crear_tab_analisis()
    
    def crear_tab_brute_force(self):
        """Create the brute force analysis tab."""
        bf_frame = tk.Frame(self.tab_brute_force, bg="white")
        bf_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        tk.Label(
            bf_frame,
            text="Brute Force - Find Risky Combinations",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#004080"
        ).pack(pady=10)
        
        # Description
        desc_text = (
            "This algorithm exhaustively searches ALL possible combinations of 4 books\n"
            "to identify those that exceed the 8 kg safety threshold.\n\n"
            "⚠️ These combinations are DANGEROUS and should be avoided!"
        )
        tk.Label(
            bf_frame,
            text=desc_text,
            font=("Helvetica", 10),
            bg="white",
            justify="center"
        ).pack(pady=10)
        
        # Settings
        settings_frame = tk.Frame(bf_frame, bg="white")
        settings_frame.pack(pady=15)
        
        tk.Label(
            settings_frame,
            text="Risk Threshold (kg):",
            bg="white",
            font=("Helvetica", 10)
        ).grid(row=0, column=0, padx=5, pady=5)
        
        self.bf_threshold_var = tk.StringVar(value="8.0")
        tk.Spinbox(
            settings_frame,
            from_=5.0,
            to=15.0,
            increment=0.5,
            textvariable=self.bf_threshold_var,
            font=("Helvetica", 10),
            width=10
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # Run button
        tb.Button(
            bf_frame,
            text="⚡ Run Brute Force Analysis",
            bootstyle="danger",
            command=self.ejecutar_fuerza_bruta
        ).pack(pady=15)
        
        # Results display
        results_frame = tk.Frame(bf_frame)
        results_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical")
        
        self.bf_results_text = tk.Text(
            results_frame,
            font=("Courier", 9),
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.bf_results_text.yview)
        
        self.bf_results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_tab_backtracking(self):
        """Create the backtracking optimization tab."""
        bt_frame = tk.Frame(self.tab_backtracking, bg="white")
        bt_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        tk.Label(
            bt_frame,
            text="Backtracking - Optimize Shelf Value",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#004080"
        ).pack(pady=10)
        
        # Description
        desc_text = (
            "This algorithm finds the OPTIMAL combination of books that\n"
            "maximizes total value while respecting the 8 kg weight constraint.\n\n"
            "✨ Uses pruning to efficiently explore the solution space!"
        )
        tk.Label(
            bt_frame,
            text=desc_text,
            font=("Helvetica", 10),
            bg="white",
            justify="center"
        ).pack(pady=10)
        
        # Settings
        settings_frame = tk.Frame(bt_frame, bg="white")
        settings_frame.pack(pady=15)
        
        tk.Label(
            settings_frame,
            text="Max Capacity (kg):",
            bg="white",
            font=("Helvetica", 10)
        ).grid(row=0, column=0, padx=5, pady=5)
        
        self.bt_capacity_var = tk.StringVar(value="8.0")
        tk.Spinbox(
            settings_frame,
            from_=5.0,
            to=15.0,
            increment=0.5,
            textvariable=self.bt_capacity_var,
            font=("Helvetica", 10),
            width=10
        ).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(
            settings_frame,
            text="Show Exploration:",
            bg="white",
            font=("Helvetica", 10)
        ).grid(row=1, column=0, padx=5, pady=5)
        
        self.bt_show_exploration = tk.BooleanVar(value=False)
        tk.Checkbutton(
            settings_frame,
            text="Display step-by-step exploration",
            variable=self.bt_show_exploration,
            bg="white"
        ).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Run button
        tb.Button(
            bt_frame,
            text="🚀 Run Backtracking Optimization",
            bootstyle="success",
            command=self.ejecutar_backtracking
        ).pack(pady=15)
        
        # Results display
        results_frame = tk.Frame(bt_frame)
        results_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical")
        
        self.bt_results_text = tk.Text(
            results_frame,
            font=("Courier", 9),
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.bt_results_text.yview)
        
        self.bt_results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_tab_analisis(self):
        """Create the safety analysis tab."""
        analysis_frame = tk.Frame(self.tab_analisis, bg="white")
        analysis_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        tk.Label(
            analysis_frame,
            text="Comprehensive Safety Analysis",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#004080"
        ).pack(pady=10)
        
        # Description
        desc_text = (
            "Complete analysis of shelf safety including:\n"
            "• Total risky vs safe combinations\n"
            "• Risk percentage\n"
            "• Most dangerous combination\n"
            "• Heavy books analysis"
        )
        tk.Label(
            analysis_frame,
            text=desc_text,
            font=("Helvetica", 10),
            bg="white",
            justify="center"
        ).pack(pady=10)
        
        # Run button
        tb.Button(
            analysis_frame,
            text="📊 Generate Safety Report",
            bootstyle="info",
            command=self.generar_analisis_seguridad
        ).pack(pady=15)
        
        # Results display
        results_frame = tk.Frame(analysis_frame)
        results_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical")
        
        self.analysis_text = tk.Text(
            results_frame,
            font=("Courier", 10),
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.analysis_text.yview)
        
        self.analysis_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def ejecutar_fuerza_bruta(self):
        """Execute brute force algorithm."""
        try:
            umbral = float(self.bf_threshold_var.get())
            
            # Get books
            libros = self.gestor_inventario.listar_todos()
            
            if len(libros) < 4:
                messagebox.showerror(
                    "Insufficient Books",
                    "Need at least 4 books to analyze combinations"
                )
                return
            
            self.bf_results_text.delete(1.0, tk.END)
            self.bf_results_text.insert(tk.END, "Running Brute Force Analysis...\n\n")
            self.bf_results_text.update()
            
            # Run algorithm
            resultado = encontrar_combinaciones_riesgosas(
                libros,
                umbral=umbral,
                num_libros=4,
                incluir_detalles=True
            )
            
            # Display results
            self.bf_results_text.delete(1.0, tk.END)
            
            self.bf_results_text.insert(tk.END, "=" * 90 + "\n")
            self.bf_results_text.insert(tk.END, "BRUTE FORCE ANALYSIS - RISKY COMBINATIONS\n")
            self.bf_results_text.insert(tk.END, "=" * 90 + "\n\n")
            
            self.bf_results_text.insert(tk.END, f"Risk Threshold: {umbral} kg\n")
            self.bf_results_text.insert(tk.END, f"Books Analyzed: {len(libros)}\n")
            self.bf_results_text.insert(tk.END, f"Total Combinations Explored: {resultado['total_exploradas']:,}\n")
            self.bf_results_text.insert(tk.END, f"Risky Combinations Found: {resultado['total_encontradas']}\n\n")
            
            if resultado['total_encontradas'] == 0:
                self.bf_results_text.insert(tk.END, "✓ No risky combinations found!\n")
                self.bf_results_text.insert(tk.END, "All 4-book combinations are within safe limits.\n")
            else:
                self.bf_results_text.insert(tk.END, "⚠️ WARNING: Risky combinations detected!\n\n")
                
                # Show first 20 combinations
                max_mostrar = min(20, len(resultado['combinaciones_riesgosas']))
                
                for i, combo in enumerate(resultado['combinaciones_riesgosas'][:max_mostrar], 1):
                    self.bf_results_text.insert(tk.END, f"Combination {i}:\n")
                    self.bf_results_text.insert(tk.END, f"  Total Weight: {combo['peso_total']} kg (exceeds by {combo['exceso']} kg)\n")
                    
                    for j, (titulo, isbn) in enumerate(zip(combo['titulos'], combo['isbns']), 1):
                        titulo_short = titulo[:40] + "..." if len(titulo) > 40 else titulo
                        self.bf_results_text.insert(tk.END, f"  {j}. {titulo_short}\n")
                        self.bf_results_text.insert(tk.END, f"     ISBN: {isbn}\n")
                    
                    self.bf_results_text.insert(tk.END, "\n")
                
                if resultado['total_encontradas'] > max_mostrar:
                    restantes = resultado['total_encontradas'] - max_mostrar
                    self.bf_results_text.insert(tk.END, f"... and {restantes} more risky combinations\n")
            
            self.bf_results_text.insert(tk.END, "\n" + "=" * 90 + "\n")
            
            messagebox.showinfo(
                "Analysis Complete",
                f"Brute Force Analysis Complete!\n\n"
                f"Explored: {resultado['total_exploradas']:,} combinations\n"
                f"Found: {resultado['total_encontradas']} risky combinations"
            )
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid threshold value")
        except Exception as e:
            messagebox.showerror("Error", f"Error running analysis: {str(e)}")
    
    def ejecutar_backtracking(self):
        """Execute backtracking optimization."""
        try:
            capacidad = float(self.bt_capacity_var.get())
            mostrar_exploracion = self.bt_show_exploration.get()
            
            # Get books
            libros = self.gestor_inventario.listar_todos()
            
            if len(libros) < 1:
                messagebox.showerror("No Books", "Need at least 1 book to optimize")
                return
            
            self.bt_results_text.delete(1.0, tk.END)
            self.bt_results_text.insert(tk.END, "Running Backtracking Optimization...\n\n")
            self.bt_results_text.update()
            
            # Run algorithm
            resultado = optimizar_estante(
                libros,
                capacidad_maxima=capacidad,
                incluir_exploracion=True
            )
            
            # Display results
            self.bt_results_text.delete(1.0, tk.END)
            
            self.bt_results_text.insert(tk.END, "=" * 90 + "\n")
            self.bt_results_text.insert(tk.END, "BACKTRACKING OPTIMIZATION - MAXIMUM VALUE\n")
            self.bt_results_text.insert(tk.END, "=" * 90 + "\n\n")
            
            self.bt_results_text.insert(tk.END, f"Max Capacity: {capacidad} kg\n")
            self.bt_results_text.insert(tk.END, f"Books Available: {len(libros)}\n\n")
            
            if 'exploracion' in resultado:
                exp = resultado['exploracion']
                self.bt_results_text.insert(tk.END, "Algorithm Performance:\n")
                self.bt_results_text.insert(tk.END, f"  Nodes Explored: {exp['nodos_explorados']}\n")
                self.bt_results_text.insert(tk.END, f"  Nodes Pruned: {exp['nodos_podados']}\n")
                self.bt_results_text.insert(tk.END, f"  Pruning Efficiency: {(exp['nodos_podados']/exp['nodos_explorados']*100):.1f}%\n")
                self.bt_results_text.insert(tk.END, f"  Max Depth Reached: {exp['max_profundidad']}\n")
                self.bt_results_text.insert(tk.END, f"  Solutions Found: {exp['soluciones_encontradas']}\n\n")
            
            self.bt_results_text.insert(tk.END, "OPTIMAL SOLUTION:\n")
            self.bt_results_text.insert(tk.END, "-" * 90 + "\n")
            self.bt_results_text.insert(tk.END, f"Books in Combination: {resultado['num_libros']}\n")
            self.bt_results_text.insert(tk.END, f"Total Value: ${resultado['valor_total']:,.0f} COP ✨\n")
            self.bt_results_text.insert(tk.END, f"Total Weight: {resultado['peso_total']:.2f} kg\n")
            self.bt_results_text.insert(tk.END, f"Space Remaining: {resultado['espacio_restante']:.2f} kg\n\n")
            
            self.bt_results_text.insert(tk.END, "Books in Optimal Combination:\n")
            self.bt_results_text.insert(tk.END, "-" * 90 + "\n")
            
            for i, (titulo, isbn) in enumerate(zip(resultado['titulos'], resultado['isbns']), 1):
                libro = self.gestor_inventario.buscar_por_isbn(isbn)
                titulo_short = titulo[:50] + "..." if len(titulo) > 50 else titulo
                
                self.bt_results_text.insert(tk.END, f"{i}. {titulo_short}\n")
                self.bt_results_text.insert(tk.END, f"   ISBN: {isbn}\n")
                
                if libro:
                    self.bt_results_text.insert(tk.END, f"   Weight: {libro.peso:.2f} kg | Value: ${libro.valor:,.0f} COP\n")
                
                self.bt_results_text.insert(tk.END, "\n")
            
            self.bt_results_text.insert(tk.END, "=" * 90 + "\n")
            
            messagebox.showinfo(
                "Optimization Complete",
                f"Backtracking Optimization Complete!\n\n"
                f"Optimal Value: ${resultado['valor_total']:,.0f} COP\n"
                f"Books: {resultado['num_libros']}\n"
                f"Weight: {resultado['peso_total']:.2f} / {capacidad} kg"
            )
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid capacity value")
        except Exception as e:
            messagebox.showerror("Error", f"Error running optimization: {str(e)}")
    
    def generar_analisis_seguridad(self):
        """Generate comprehensive safety analysis."""
        try:
            libros = self.gestor_inventario.listar_todos()
            
            if len(libros) < 4:
                messagebox.showerror(
                    "Insufficient Books",
                    "Need at least 4 books for analysis"
                )
                return
            
            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.insert(tk.END, "Generating Safety Analysis...\n\n")
            self.analysis_text.update()
            
            # Run comprehensive analysis
            analisis = analizar_seguridad_estantes(libros, umbral=8.0)
            
            # Display results
            self.analysis_text.delete(1.0, tk.END)
            
            self.analysis_text.insert(tk.END, "=" * 80 + "\n")
            self.analysis_text.insert(tk.END, "COMPREHENSIVE SAFETY ANALYSIS\n")
            self.analysis_text.insert(tk.END, "=" * 80 + "\n\n")
            
            self.analysis_text.insert(tk.END, "OVERVIEW:\n")
            self.analysis_text.insert(tk.END, f"  Books Analyzed: {analisis['total_libros']}\n")
            self.analysis_text.insert(tk.END, f"  Total Combinations: {analisis['total_combinaciones']:,}\n")
            self.analysis_text.insert(tk.END, f"  Risk Threshold: {analisis['umbral_riesgo']} kg\n\n")
            
            self.analysis_text.insert(tk.END, "RESULTS:\n")
            self.analysis_text.insert(tk.END, f"  Risky Combinations: {analisis['num_riesgosas']:,}\n")
            self.analysis_text.insert(tk.END, f"  Safe Combinations: {analisis['combinaciones_seguras']:,}\n")
            self.analysis_text.insert(tk.END, f"  Risk Percentage: {analisis['porcentaje_riesgo']:.2f}%\n\n")
            
            if analisis['num_riesgosas'] > 0:
                self.analysis_text.insert(tk.END, "RISK STATISTICS:\n")
                self.analysis_text.insert(tk.END, f"  Average Weight (Risky): {analisis['peso_promedio_riesgosas']:.2f} kg\n")
                self.analysis_text.insert(tk.END, f"  Maximum Weight Found: {analisis['peso_maximo_encontrado']:.2f} kg\n")
                self.analysis_text.insert(tk.END, f"  Minimum Risky Weight: {analisis['peso_minimo_riesgoso']:.2f} kg\n\n")
                
                if analisis['combinacion_mas_riesgosa']:
                    combo = analisis['combinacion_mas_riesgosa']
                    self.analysis_text.insert(tk.END, "MOST DANGEROUS COMBINATION:\n")
                    self.analysis_text.insert(tk.END, f"  Total Weight: {combo['peso_total']:.2f} kg\n")
                    self.analysis_text.insert(tk.END, f"  Exceeds Threshold By: {combo['exceso']:.2f} kg\n")
                    self.analysis_text.insert(tk.END, "  Books:\n")
                    
                    for titulo in combo['titulos']:
                        titulo_short = titulo[:60] + "..." if len(titulo) > 60 else titulo
                        self.analysis_text.insert(tk.END, f"    • {titulo_short}\n")
            
            self.analysis_text.insert(tk.END, "\n" + "=" * 80 + "\n")
            
            # Safety recommendation
            if analisis['porcentaje_riesgo'] > 50:
                nivel = "🔴 HIGH RISK"
            elif analisis['porcentaje_riesgo'] > 20:
                nivel = "🟡 MODERATE RISK"
            else:
                nivel = "🟢 LOW RISK"
            
            self.analysis_text.insert(tk.END, f"\nSAFETY LEVEL: {nivel}\n")
            
            messagebox.showinfo(
                "Analysis Complete",
                f"Safety Analysis Complete!\n\n"
                f"Risk Level: {nivel}\n"
                f"Risky: {analisis['num_riesgosas']:,} / {analisis['total_combinaciones']:,}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating analysis: {str(e)}")