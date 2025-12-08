"""
File Handler Utility - Library Management System

This module provides the ArchivoHandler class which centralizes all file
operations in the library system. It handles JSON and CSV file operations
with consistent error handling and validation.

Classes:
    ArchivoHandler: Main class for file I/O operations

Author: [Your Name]
Date: December 2025
"""

import json
import csv
import os
from datetime import datetime


class ArchivoHandler:
    """
    Handler class for all file operations.
    
    This class provides methods to read and write JSON and CSV files,
    ensuring consistent error handling and data validation across the system.
    
    Methods:
        - cargar_json: Load data from JSON file
        - guardar_json: Save data to JSON file
        - cargar_csv: Load data from CSV file
        - guardar_csv: Save data to CSV file
        - verificar_archivo_existe: Check if file exists
        - crear_directorio: Create directory if it doesn't exist
        - obtener_backup_path: Generate backup file path
        - crear_backup: Create backup of existing file
    """
    
    def __init__(self, encoding='utf-8'):
        """
        Initialize the file handler.
        
        Args:
            encoding (str, optional): File encoding. Defaults to 'utf-8'.
        """
        self.encoding = encoding
    
    def cargar_json(self, ruta_archivo):
        """
        Load data from a JSON file.
        
        Args:
            ruta_archivo (str): Path to JSON file
            
        Returns:
            dict or list or None: Loaded data, or None if error/file not found
            
        Example:
            >>> handler = ArchivoHandler()
            >>> datos = handler.cargar_json("data/libros/libros.json")
        """
        try:
            if not self.verificar_archivo_existe(ruta_archivo):
                print(f"File not found: {ruta_archivo}")
                return None
            
            with open(ruta_archivo, 'r', encoding=self.encoding) as file:
                datos = json.load(file)
                return datos
                
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from {ruta_archivo}: {e}")
            return None
        except Exception as e:
            print(f"Error loading file {ruta_archivo}: {e}")
            return None
    
    def guardar_json(self, ruta_archivo, datos, crear_backup=False):
        """
        Save data to a JSON file.
        
        Args:
            ruta_archivo (str): Path to JSON file
            datos: Data to save (must be JSON serializable)
            crear_backup (bool, optional): Create backup before saving. Defaults to False.
            
        Returns:
            bool: True if saved successfully, False otherwise
            
        Example:
            >>> handler = ArchivoHandler()
            >>> datos = [{"isbn": "123", "titulo": "Book"}]
            >>> handler.guardar_json("data/libros/libros.json", datos)
        """
        try:
            # Create directory if it doesn't exist
            directorio = os.path.dirname(ruta_archivo)
            if directorio:
                self.crear_directorio(directorio)
            
            # Create backup if requested and file exists
            if crear_backup and self.verificar_archivo_existe(ruta_archivo):
                self.crear_backup(ruta_archivo)
            
            # Save data
            with open(ruta_archivo, 'w', encoding=self.encoding) as file:
                json.dump(datos, file, indent=2, ensure_ascii=False)
            
            return True
            
        except TypeError as e:
            print(f"Error: Data is not JSON serializable: {e}")
            return False
        except Exception as e:
            print(f"Error saving file {ruta_archivo}: {e}")
            return False
    
    def cargar_csv(self, ruta_archivo, delimitador=',', tiene_encabezado=True):
        """
        Load data from a CSV file.
        
        Args:
            ruta_archivo (str): Path to CSV file
            delimitador (str, optional): CSV delimiter. Defaults to ','.
            tiene_encabezado (bool, optional): If CSV has header row. Defaults to True.
            
        Returns:
            list: List of dictionaries (if tiene_encabezado=True) or list of lists
            
        Example:
            >>> handler = ArchivoHandler()
            >>> datos = handler.cargar_csv("initial_data/libros_inicial.csv")
        """
        try:
            if not self.verificar_archivo_existe(ruta_archivo):
                print(f"File not found: {ruta_archivo}")
                return []
            
            datos = []
            
            with open(ruta_archivo, 'r', encoding=self.encoding) as file:
                if tiene_encabezado:
                    reader = csv.DictReader(file, delimiter=delimitador)
                    for row in reader:
                        datos.append(dict(row))
                else:
                    reader = csv.reader(file, delimiter=delimitador)
                    for row in reader:
                        datos.append(row)
            
            return datos
            
        except Exception as e:
            print(f"Error loading CSV {ruta_archivo}: {e}")
            return []
    
    def guardar_csv(self, ruta_archivo, datos, encabezados=None, delimitador=','):
        """
        Save data to a CSV file.
        
        Args:
            ruta_archivo (str): Path to CSV file
            datos (list): List of dictionaries or list of lists
            encabezados (list, optional): Column headers. Defaults to None.
            delimitador (str, optional): CSV delimiter. Defaults to ','.
            
        Returns:
            bool: True if saved successfully, False otherwise
            
        Example:
            >>> handler = ArchivoHandler()
            >>> datos = [{"isbn": "123", "titulo": "Book"}]
            >>> handler.guardar_csv("reports/libros.csv", datos)
        """
        try:
            # Create directory if it doesn't exist
            directorio = os.path.dirname(ruta_archivo)
            if directorio:
                self.crear_directorio(directorio)
            
            with open(ruta_archivo, 'w', encoding=self.encoding, newline='') as file:
                if not datos:
                    return True  # Empty data, nothing to write
                
                # Determine if data is list of dicts or list of lists
                if isinstance(datos[0], dict):
                    # List of dictionaries
                    if encabezados is None:
                        encabezados = list(datos[0].keys())
                    
                    writer = csv.DictWriter(file, fieldnames=encabezados, delimiter=delimitador)
                    writer.writeheader()
                    writer.writerows(datos)
                else:
                    # List of lists
                    writer = csv.writer(file, delimiter=delimitador)
                    if encabezados:
                        writer.writerow(encabezados)
                    writer.writerows(datos)
            
            return True
            
        except Exception as e:
            print(f"Error saving CSV {ruta_archivo}: {e}")
            return False
    
    def verificar_archivo_existe(self, ruta_archivo):
        """
        Check if a file exists.
        
        Args:
            ruta_archivo (str): Path to file
            
        Returns:
            bool: True if file exists, False otherwise
        """
        return os.path.isfile(ruta_archivo)
    
    def crear_directorio(self, ruta_directorio):
        """
        Create a directory if it doesn't exist.
        
        Args:
            ruta_directorio (str): Path to directory
            
        Returns:
            bool: True if created or already exists, False on error
        """
        try:
            os.makedirs(ruta_directorio, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory {ruta_directorio}: {e}")
            return False
    
    def obtener_backup_path(self, ruta_archivo):
        """
        Generate a backup file path with timestamp.
        
        Args:
            ruta_archivo (str): Original file path
            
        Returns:
            str: Backup file path
            
        Example:
            >>> handler = ArchivoHandler()
            >>> backup = handler.obtener_backup_path("data/libros.json")
            >>> # Returns: "data/libros_backup_20251207_143022.json"
        """
        directorio = os.path.dirname(ruta_archivo)
        nombre_archivo = os.path.basename(ruta_archivo)
        nombre_sin_ext, extension = os.path.splitext(nombre_archivo)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_nombre = f"{nombre_sin_ext}_backup_{timestamp}{extension}"
        
        return os.path.join(directorio, backup_nombre)
    
    def crear_backup(self, ruta_archivo):
        """
        Create a backup of an existing file.
        
        Args:
            ruta_archivo (str): Path to file to backup
            
        Returns:
            str or None: Path to backup file if successful, None otherwise
        """
        try:
            if not self.verificar_archivo_existe(ruta_archivo):
                print(f"Cannot backup: file {ruta_archivo} does not exist")
                return None
            
            backup_path = self.obtener_backup_path(ruta_archivo)
            
            # Copy file content
            with open(ruta_archivo, 'r', encoding=self.encoding) as original:
                contenido = original.read()
            
            with open(backup_path, 'w', encoding=self.encoding) as backup:
                backup.write(contenido)
            
            print(f"✓ Backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None
    
    def limpiar_backups_antiguos(self, ruta_directorio, dias=7):
        """
        Remove backup files older than specified days.
        
        Args:
            ruta_directorio (str): Directory containing backups
            dias (int, optional): Age threshold in days. Defaults to 7.
            
        Returns:
            int: Number of backups removed
        """
        try:
            if not os.path.isdir(ruta_directorio):
                return 0
            
            contador = 0
            ahora = datetime.now()
            
            for archivo in os.listdir(ruta_directorio):
                if "_backup_" not in archivo:
                    continue
                
                ruta_completa = os.path.join(ruta_directorio, archivo)
                
                # Get file modification time
                tiempo_modificacion = os.path.getmtime(ruta_completa)
                fecha_modificacion = datetime.fromtimestamp(tiempo_modificacion)
                
                # Calculate age
                edad = (ahora - fecha_modificacion).days
                
                if edad > dias:
                    os.remove(ruta_completa)
                    contador += 1
                    print(f"Removed old backup: {archivo}")
            
            return contador
            
        except Exception as e:
            print(f"Error cleaning backups: {e}")
            return 0
    
    def exportar_datos(self, datos, ruta_salida, formato='json'):
        """
        Export data to file in specified format.
        
        Args:
            datos: Data to export
            ruta_salida (str): Output file path
            formato (str, optional): Export format ('json' or 'csv'). Defaults to 'json'.
            
        Returns:
            bool: True if exported successfully, False otherwise
        """
        try:
            if formato.lower() == 'json':
                return self.guardar_json(ruta_salida, datos)
            elif formato.lower() == 'csv':
                return self.guardar_csv(ruta_salida, datos)
            else:
                print(f"Unsupported format: {formato}")
                return False
                
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def listar_archivos(self, ruta_directorio, extension=None):
        """
        List files in a directory with optional extension filter.
        
        Args:
            ruta_directorio (str): Directory to list
            extension (str, optional): Filter by extension (e.g., '.json'). Defaults to None.
            
        Returns:
            list: List of file names
        """
        try:
            if not os.path.isdir(ruta_directorio):
                return []
            
            archivos = os.listdir(ruta_directorio)
            
            if extension:
                if not extension.startswith('.'):
                    extension = '.' + extension
                archivos = [f for f in archivos if f.endswith(extension)]
            
            return sorted(archivos)
            
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def obtener_info_archivo(self, ruta_archivo):
        """
        Get information about a file.
        
        Args:
            ruta_archivo (str): Path to file
            
        Returns:
            dict: File information (size, dates, etc.) or None if error
        """
        try:
            if not self.verificar_archivo_existe(ruta_archivo):
                return None
            
            stats = os.stat(ruta_archivo)
            
            return {
                'ruta': ruta_archivo,
                'nombre': os.path.basename(ruta_archivo),
                'tamanio_bytes': stats.st_size,
                'tamanio_kb': round(stats.st_size / 1024, 2),
                'fecha_creacion': datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                'fecha_modificacion': datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                'existe': True
            }
            
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None