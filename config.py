"""
config.py
---------
Global configuration file for the Library Management System.

This module centralizes:
- Directory paths
- File paths
- System constants
- Logging configuration
- Application metadata
"""

import os
from pathlib import Path


# ============================================================
# 📌 BASE PATHS
# ============================================================

# Root directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Data directories
DATA_DIR = BASE_DIR / "data"
LIBROS_DIR = DATA_DIR / "libros"
USUARIOS_DIR = DATA_DIR / "usuarios"
PRESTAMOS_DIR = DATA_DIR / "prestamos"
RESERVAS_DIR = DATA_DIR / "reservas"
ESTANTES_DIR = DATA_DIR / "estantes"

# Initial CSV data
INITIAL_DATA_DIR = BASE_DIR / "initial_data"
INITIAL_CSV_LIBROS = INITIAL_DATA_DIR / "libros_inicial.csv"

# Reports output directory
REPORTS_DIR = BASE_DIR / "reports"


# ============================================================
# 📌 FILE PATHS (JSON persistence)
# ============================================================

LIBROS_JSON = LIBROS_DIR / "libros.json"
USUARIOS_JSON = USUARIOS_DIR / "usuarios.json"
PRESTAMOS_JSON = PRESTAMOS_DIR / "prestamos.json"
RESERVAS_JSON = RESERVAS_DIR / "reservas.json"
ESTANTES_JSON = ESTANTES_DIR / "estantes.json"


# ============================================================
# 📌 SYSTEM CONSTANTS
# ============================================================

# Loan rules
MAX_PRESTAMOS_POR_USUARIO = 3
DIAS_MAX_PRESTAMO = 15

# Shelf optimization (Backtracking)
MAX_PESO_ESTANTE = 8.0  # kg
MAX_LIBROS_FUERZA_BRUTA = 4

# Valid formats
VALID_EXTENSIONS_CSV = (".csv",)
VALID_EXTENSIONS_JSON = (".json",)

# UI settings (tkinter)
APP_TITLE = "📚 Library Management System"
WINDOW_SIZE = "1200x700"


# ============================================================
# 📌 LOGGING CONFIG
# ============================================================

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / "system.log"

import logging

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("LibrarySystem")


# ============================================================
# 📌 DIRECTORY CREATION (first run)
# ============================================================

def ensure_directories_exist():
    """Automatically creates required directories on first run."""

    directories = [
        DATA_DIR,
        LIBROS_DIR,
        USUARIOS_DIR,
        PRESTAMOS_DIR,
        RESERVAS_DIR,
        ESTANTES_DIR,
        REPORTS_DIR,
        LOGS_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


# Create them on import
ensure_directories_exist()


# ============================================================
# 📌 APP INFO
# ============================================================

APP_AUTHOR = "Juan David Nuñez"
APP_VERSION = "1.0"
APP_YEAR = "2025"
APP_UNIVERSITY = "Universidad de Caldas"

