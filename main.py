import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(_file_)))

from ui.ventana_libros import LibrosWindow
from ui.ventana_usuarios import UsuariosWindow
from ui.ventana_prestamos import PrestamosWindow
from ui.ventana_reservas import ReservasWindow
from ui.ventana_estanteria import EstanteriaWindow
from ui.ventana_reportes import ReportesWindow
from utils.archivo_handler import ArchivoHandler


class BibliotecaApp(tb.Window):
    """
    Main application class for the Library Management System.
    Manages the main window and navigation between different modules.
    
    Attributes:
        option_display (tk.LabelFrame): Container for displaying different module windows
        archivo_handler (ArchivoHandler): Utility for handling JSON/CSV files
    """
    
    def _init_(self):
        """Initialize the main application window and components."""
        super()._init_(themename="superhero")
        self.title("Library Management System")
        self.geometry("1200x700")
        self.resizable(True, True)
        
        # Initialize file handler
        self.archivo_handler = ArchivoHandler()
        
        # Initialize data structure
        self.ensure_data_structure()
        
        # Create main widgets
        self.create_widgets()
        
    def ensure_data_structure(self):
        """
        Ensure all required data directories and files exist.
        Creates the directory structure if it doesn't exist.
        """
        directories = [
            "data/libros",
            "data/usuarios",
            "data/prestamos",
            "data/reservas",
            "data/estantes",
            "reports",
            "initial_data"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
        # Initialize empty JSON files if they don't exist
        json_files = [
            "data/libros/libros.json",
            "data/usuarios/usuarios.json",
            "data/prestamos/prestamos.json",
            "data/reservas/reservas.json",
            "data/estantes/estantes.json"
        ]
        
        for json_file in json_files:
            if not os.path.exists(json_file):
                self.archivo_handler.guardar_json(json_file, [])
                
    def create_widgets(self):
        """Create and configure all main window widgets."""
        self.configure(bg="white")
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create main display area
        self.option_display = tk.LabelFrame(
            self,
            text="Welcome to Library Management System",
            font=("Helvetica", 18, "bold"),
            fg="#004080",
            bg="white",
            relief="groove",
            bd=3
        )
        self.option_display.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Show welcome message
        self.show_welcome()
        
    def create_menu_bar(self):
        """Create the top menu bar with navigation buttons."""
        menu_bar = tk.Frame(self, bg="#004080", height=70, relief='raised', bd=2)
        menu_bar.pack(side="top", fill="x")
        
        # Title label
        title_label = tk.Label(
            menu_bar,
            text="📚 Library Management System",
            font=("Helvetica", 22, "bold"),
            bg="#004080",
            fg="white"
        )
        title_label.pack(side="left", padx=20, pady=10)
        
        # Navigation buttons
        menu_options = [
            ("BOOKS", self.show_books),
            ("USERS", self.show_users),
            ("LOANS", self.show_loans),
            ("RESERVATIONS", self.show_reservations),
            ("SHELVES", self.show_shelves),
            ("REPORTS", self.show_reports)
        ]
        
        self.buttons = []
        for text, command in menu_options:
            button = tb.Button(
                menu_bar,
                text=text,
                bootstyle="primary-outline",
                width=13,
                command=command
            )
            button.pack(side="left", padx=5, pady=15)
            self.buttons.append(button)
            
    def clear_display(self):
        """Clear all widgets from the main display area."""
        for widget in self.option_display.winfo_children():
            widget.destroy()
            
    def show_welcome(self):
        """Display welcome message on the main screen."""
        self.option_display.config(text="Welcome")
        self.clear_display()
        
        welcome_frame = tk.Frame(self.option_display, bg="white")
        welcome_frame.pack(expand=True)
        
        # Welcome title
        welcome_title = tk.Label(
            welcome_frame,
            text="Welcome to Library Management System",
            font=("Helvetica", 24, "bold"),
            fg="#004080",
            bg="white"
        )
        welcome_title.pack(pady=20)
        
        # Description
        description = tk.Label(
            welcome_frame,
            text="Manage books, users, loans, reservations, and more\n"
                 "Select an option from the menu above to get started",
            font=("Helvetica", 14),
            fg="#333333",
            bg="white",
            justify="center"
        )
        description.pack(pady=10)
        
        # System info
        info_frame = tk.Frame(welcome_frame, bg="white")
        info_frame.pack(pady=30)
        
        features = [
            "📖 Books Management (CRUD)",
            "👤 Users Management",
            "📋 Loans & Returns",
            "⏳ Reservation Queue",
            "📚 Shelf Optimization",
            "📊 Reports & Analytics"
        ]
        
        for i, feature in enumerate(features):
            label = tk.Label(
                info_frame,
                text=feature,
                font=("Helvetica", 12),
                fg="#555555",
                bg="white",
                anchor="w"
            )
            label.grid(row=i//2, column=i%2, padx=30, pady=10, sticky="w")
            
    def show_books(self):
        """Display the Books management window."""
        self.option_display.config(text="Books Management")
        self.clear_display()
        LibrosWindow(self.option_display, self.archivo_handler)
        
    def show_users(self):
        """Display the Users management window."""
        self.option_display.config(text="Users Management")
        self.clear_display()
        UsuariosWindow(self.option_display, self.archivo_handler)
        
    def show_loans(self):
        """Display the Loans management window."""
        self.option_display.config(text="Loans Management")
        self.clear_display()
        PrestamosWindow(self.option_display, self.archivo_handler)
        
    def show_reservations(self):
        """Display the Reservations management window."""
        self.option_display.config(text="Reservations Management")
        self.clear_display()
        ReservasWindow(self.option_display, self.archivo_handler)
        
    def show_shelves(self):
        """Display the Shelves optimization window."""
        self.option_display.config(text="Shelf Management & Optimization")
        self.clear_display()
        EstanteriaWindow(self.option_display, self.archivo_handler)
        
    def show_reports(self):
        """Display the Reports generation window."""
        self.option_display.config(text="Reports & Analytics")
        self.clear_display()
        ReportesWindow(self.option_display, self.archivo_handler)


def main():
    """
    Main entry point of the application.
    Creates and runs the main application window.
    """
    try:
        app = BibliotecaApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Critical Error", f"Failed to start application:\n{str(e)}")
        raise


if _name_ == "_main_":
    main()