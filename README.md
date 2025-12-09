# 📚 Library Management System

**Sistema de Gestión de Bibliotecas**

Proyecto Final - Técnicas de Programación 2025-2

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características Principales](#-características-principales)
- [Requisitos del Proyecto](#-requisitos-del-proyecto)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Algoritmos Implementados](#-algoritmos-implementados)
- [Estructuras de Datos](#-estructuras-de-datos)
- [Interfaces de Usuario](#-interfaces-de-usuario)
- [Documentación Técnica](#-documentación-técnica)
- [Autores](#-autores)

---

## 🎯 Descripción General

Sistema completo de gestión de bibliotecas implementado en Python que integra algoritmos de ordenamiento, búsqueda y resolución de problemas, junto con estructuras de datos avanzadas (Pila y Cola) y una interfaz gráfica moderna.

### Objetivo del Proyecto

Diseñar e implementar un Sistema de Gestión de Bibliotecas (SGB) que:
- Maneje diversas estructuras de datos
- Aplique algoritmos para clasificar, buscar y resolver problemas de asignación de recursos
- Demuestre comprensión profunda de todos los temas de "Técnicas de Programación"

---

## ✨ Características Principales

### 📖 Gestión de Libros
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Dos inventarios: General (orden de carga) y Ordenado (por ISBN)
- ✅ Búsqueda por título, autor e ISBN
- ✅ Reportes ordenados por valor (COP)
- ✅ Importación desde CSV

### 👥 Gestión de Usuarios
- ✅ Registro y autenticación
- ✅ Activación/desactivación de cuentas
- ✅ Control de límite de préstamos
- ✅ Historial por usuario

### 📋 Gestión de Préstamos
- ✅ Crear préstamos con validaciones
- ✅ **Devoluciones con verificación automática de reservas** (CRÍTICO)
- ✅ Historial usando Pila (LIFO)
- ✅ Estadísticas de préstamos

### ⏳ Gestión de Reservas
- ✅ Solo para libros agotados (stock = 0)
- ✅ Cola FIFO (First In, First Out)
- ✅ Asignación automática al devolver libro
- ✅ Posición y tiempo estimado de espera

### 📚 Optimización de Estanterías
- ✅ Fuerza Bruta: Encuentra combinaciones riesgosas (4 libros > 8 kg)
- ✅ Backtracking: Maximiza valor sin exceder 8 kg
- ✅ Análisis de seguridad completo

### 📊 Reportes y Analytics
- ✅ Recursión de Pila: Valor total por autor
- ✅ Recursión de Cola: Peso promedio por autor
- ✅ Reportes con Merge Sort
- ✅ Exportación a CSV

---

## 📝 Requisitos del Proyecto

### Estructuras de Datos
- [x] **Adquisición de Datos**: Carga desde CSV/JSON (30 libros iniciales)
- [x] **Listas Maestras**: Inventario General e Inventario Ordenado
- [x] **Pilas (Historial)**: Gestión de historial de préstamos (LIFO)
- [x] **Colas (Reservas)**: Lista de espera para libros agotados (FIFO)

### Algoritmos de Ordenamiento
- [x] **Insertion Sort**: Mantiene inventario ordenado por ISBN
- [x] **Merge Sort**: Genera reportes globales ordenados por valor

### Algoritmos de Búsqueda
- [x] **Búsqueda Lineal**: Por título/autor en Inventario General
- [x] **Búsqueda Binaria**: Por ISBN en Inventario Ordenado
- [x] **CRÍTICO**: Resultado de búsqueda binaria usado para verificar reservas

### Algoritmos de Resolución
- [x] **Fuerza Bruta**: Todas las combinaciones de 4 libros > 8 kg
- [x] **Backtracking**: Maximiza valor con restricción de peso ≤ 8 kg

### Recursión
- [x] **Recursión de Pila**: Valor total de libros por autor
- [x] **Recursión de Cola**: Peso promedio por autor (con demostración)

### Arquitectura
- [x] **POO**: Todo el sistema estructurado en clases
- [x] **Modularidad**: Código separado en módulos lógicos
- [x] **Documentación**: Código completamente documentado en inglés

---

## 📁 Estructura del Proyecto

```
biblioteca_system/
├── main.py                          # Punto de entrada
├── requirements.txt                 # Dependencias
├── README.md                       # Este archivo
│
├── data/                           # Datos persistentes (JSON)
│   ├── libros/
│   ├── usuarios/
│   ├── prestamos/
│   ├── reservas/
│   └── estantes/
│
├── initial_data/                   # Datos iniciales
│   └── libros_inicial.csv         # 30 libros base
│
├── reports/                        # Reportes exportados
│   └── .gitkeep
│
├── models/                         # Modelos de datos
│   ├── libro.py
│   ├── usuario.py
│   └── estante.py
│
├── estructuras_datos/              # Estructuras de datos
│   ├── pila.py                    # Stack (LIFO)
│   └── cola.py                    # Queue (FIFO)
│
├── algoritmos_ordenamiento/        # Algoritmos de ordenamiento
│   ├── insercion.py
│   └── merge_sort.py
│
├── algoritmos_busqueda/            # Algoritmos de búsqueda
│   ├── busqueda_lineal.py
│   └── busqueda_binaria.py
│
├── algoritmos_resolucion/          # Resolución de problemas
│   ├── fuerza_bruta.py
│   └── backtracking.py
│
├── recursion/                      # Funciones recursivas
│   ├── recursion_pila.py
│   └── recursion_cola.py
│
├── gestor/                         # Capa de negocio
│   ├── gestor_inventario.py
│   ├── gestor_usuarios.py
│   ├── gestor_prestamos.py
│   └── gestor_reservas.py
│
├── utils/                          # Utilidades
│   ├── archivo_handler.py
│   └── validaciones.py
│
└── ui/                             # Interfaz gráfica
    ├── ventana_principal.py
    ├── ventana_libros.py
    ├── ventana_usuarios.py
    ├── ventana_prestamos.py
    ├── ventana_reservas.py
    ├── ventana_estanteria.py
    └── ventana_reportes.py
```

---

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
```bash
cd biblioteca_system
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Verificar instalación de tkinter**
```bash
python -m tkinter
# Debería abrir una ventana de prueba
```

---

## 💻 Uso

### Iniciar la Aplicación

```bash
python main.py
```

### Cargar Datos Iniciales

La aplicación crea automáticamente la estructura de carpetas. Para cargar los 30 libros iniciales:

**Opción 1: Desde código**
```python
from gestor.gestor_inventario import GestorInventario
from utils.archivo_handler import ArchivoHandler

handler = ArchivoHandler()
gestor = GestorInventario(handler)
gestor.cargar_desde_csv("initial_data/libros_inicial.csv")
```

**Opción 2: Manualmente**
- Usar la interfaz de "Books Management"
- Agregar libros uno por uno
- O implementar botón de importación CSV

### Navegación

La aplicación tiene 6 módulos principales:

1. **📚 BOOKS** - Gestión de libros
2. **👤 USERS** - Gestión de usuarios
3. **📋 LOANS** - Préstamos y devoluciones
4. **⏳ RESERVATIONS** - Cola de reservas
5. **📚 SHELVES** - Optimización de estanterías
6. **📊 REPORTS** - Reportes y recursión

---

## 🔧 Algoritmos Implementados

### Ordenamiento

#### Insertion Sort
- **Ubicación**: `algoritmos_ordenamiento/insercion.py`
- **Uso**: Mantener inventario ordenado por ISBN
- **Complejidad**: O(n²) peor caso, O(n) mejor caso
- **Función principal**: `insertar_ordenado()`

#### Merge Sort
- **Ubicación**: `algoritmos_ordenamiento/merge_sort.py`
- **Uso**: Generar reportes ordenados por valor
- **Complejidad**: O(n log n)
- **Función principal**: `generar_reporte_ordenado()`

### Búsqueda

#### Linear Search
- **Ubicación**: `algoritmos_busqueda/busqueda_lineal.py`
- **Uso**: Búsqueda por título/autor
- **Complejidad**: O(n)
- **Funciones**: `buscar_por_titulo()`, `buscar_por_autor()`

#### Binary Search ⭐ CRÍTICO
- **Ubicación**: `algoritmos_busqueda/busqueda_binaria.py`
- **Uso**: Búsqueda por ISBN + verificación de reservas
- **Complejidad**: O(log n)
- **Función crítica**: `verificar_y_asignar_reserva()`

### Resolución de Problemas

#### Brute Force
- **Ubicación**: `algoritmos_resolucion/fuerza_bruta.py`
- **Uso**: Encontrar combinaciones de 4 libros > 8 kg
- **Complejidad**: O(n⁴)
- **Función**: `encontrar_combinaciones_riesgosas()`

#### Backtracking
- **Ubicación**: `algoritmos_resolucion/backtracking.py`
- **Uso**: Maximizar valor sin exceder 8 kg
- **Complejidad**: O(2ⁿ) con poda
- **Función**: `optimizar_estante()`

### Recursión

#### Stack Recursion
- **Ubicación**: `recursion/recursion_pila.py`
- **Uso**: Calcular valor total por autor
- **Función**: `calcular_valor_total_por_autor()`

#### Tail Recursion
- **Ubicación**: `recursion/recursion_cola.py`
- **Uso**: Calcular peso promedio por autor
- **Función**: `calcular_peso_promedio_por_autor()`

---

## 📊 Estructuras de Datos

### Pila (Stack - LIFO)
- **Implementación**: `estructuras_datos/pila.py`
- **Uso**: Historial de préstamos por usuario
- **Operaciones**: `apilar()`, `desapilar()`, `tope()`

### Cola (Queue - FIFO)
- **Implementación**: `estructuras_datos/cola.py`
- **Uso**: Lista de espera para reservas
- **Operaciones**: `encolar()`, `desencolar()`, `frente()`

---

## 🖥️ Interfaces de Usuario

### Ventana de Libros
- Vista de inventarios (general y ordenado)
- CRUD de libros con validaciones
- Búsquedas por título, autor, ISBN
- Generación de reportes

### Ventana de Usuarios
- Registro de usuarios
- Activación/desactivación
- Gestión de límites de préstamo
- Estadísticas

### Ventana de Préstamos ⭐ CRÍTICA
- Crear préstamos con validaciones
- **Procesar devoluciones con verificación automática de reservas**
- Historial por usuario (Stack)
- Estadísticas

### Ventana de Reservas
- Crear reservas (solo para stock = 0)
- Ver cola FIFO
- Cancelar reservas
- Tiempo de espera estimado

### Ventana de Estanterías
- Análisis de fuerza bruta
- Optimización con backtracking
- Reporte de seguridad

### Ventana de Reportes
- Cálculos recursivos por autor
- Reportes con Merge Sort
- Estadísticas del sistema
- Exportación a CSV

---

## 📚 Documentación Técnica

### Flujo Crítico: Devolución con Reservas

```
1. Usuario devuelve libro
   ↓
2. Stock del libro se incrementa
   ↓
3. BÚSQUEDA BINARIA encuentra libro en inventario ordenado
   ↓
4. Se verifica COLA de reservas para ese ISBN
   ↓
5a. Si HAY reservas:
    - Se DESENCOLA primer usuario (FIFO)
    - Se crea préstamo automático
    - Stock vuelve a 0
    
5b. Si NO hay reservas:
    - Libro queda disponible para préstamo general
```

### Validaciones Implementadas

- **ISBN**: Formato y checksum (ISBN-10/ISBN-13)
- **Email**: Formato válido
- **Teléfono**: Formato colombiano
- **Números positivos**: Peso, valor, stock
- **Stock = 0**: Para crear reservas

### Persistencia de Datos

Todos los datos se guardan en formato JSON:
- `data/libros/libros.json`
- `data/usuarios/usuarios.json`
- `data/prestamos/prestamos.json`
- `data/reservas/reservas.json`

---

## 🧪 Casos de Prueba Sugeridos

### Test 1: Búsqueda Binaria + Reservas
1. Agotar stock de un libro (prestar todas las copias)
2. Crear 2-3 reservas para ese libro
3. Devolver el libro
4. Verificar que se asigna automáticamente al primero de la cola

### Test 2: Fuerza Bruta
1. Verificar que encuentra combinaciones de 4 libros > 8 kg
2. Ejemplo: Guerra y Paz (2.8) + Don Quijote (2.5) + Los Miserables (3.0) + Canción de Hielo (2.4) = 10.7 kg

### Test 3: Backtracking
1. Ejecutar optimización con capacidad de 8 kg
2. Verificar que maximiza valor sin exceder peso
3. Observar estadísticas de nodos explorados y podados

### Test 4: Recursión
1. Buscar "García Márquez" (tiene 3 libros)
2. Calcular valor total (Stack Recursion)
3. Calcular peso promedio (Tail Recursion)
4. Activar demostración paso a paso

---

## 🎓 Autores

**[juan david nuñez]**
**[ Compañero]**

Universidad: [Universidad de caldas]
Curso: Técnicas de Programación 2025-2
Fecha: Diciembre 2025

---

## 📄 Licencia

Este proyecto es parte de un trabajo académico para el curso de Técnicas de Programación.

---

## 🙏 Agradecimientos

- Profesor del curso de Técnicas de Programación


---

## 📞 Contacto

Para preguntas sobre el proyecto:
- Email: [juan.nunez37550@ucaldas.edu.com]
- GitHub: [juandavidnunez]

---

**🎉 ¡Gracias por revisar nuestro proyecto!**