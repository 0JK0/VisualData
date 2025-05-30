# 📊 Herramienta de Visualización de Datos CSV

Una aplicación de escritorio desarrollada en Python para analizar y visualizar datos de incidencias urbanas mediante gráficos interactivos.

## ✨ Características

- **Interfaz gráfica intuitiva** construida con Tkinter
- **Carga de archivos CSV** con manejo de fechas automático
- **4 tipos de visualizaciones** diferentes:
  - Conteo de incidencias por tipo de problema y estado
  - Tiempo promedio de resolución por tipo de problema
  - Evolución temporal de incidencias reportadas
  - Distribución de incidencias por comuna y tipo

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**
- **Pandas** - Manipulación y análisis de datos
- **Matplotlib** - Generación de gráficos
- **Tkinter** - Interfaz gráfica de usuario

## 📋 Requisitos

```bash
pip install pandas matplotlib
```

## 🚀 Uso

1. Ejecutar la aplicación:
```bash
python main.py
```

2. Hacer clic en "Browse CSV File" para cargar un archivo CSV
3. Seleccionar el tipo de visualización deseada
4. Los gráficos se mostrarán con herramientas de zoom y navegación

## 📊 Formato de Datos Esperado

El archivo CSV debe contener las siguientes columnas:
- `Fecha` - Fecha del reporte (formato YYYY-MM-DD)
- `Problema` - Tipo de problema reportado
- `Estado` - Estado actual de la incidencia
- `TiempoSolucion` - Días para resolver (para incidencias solucionadas)
- `Comuna` - Comuna donde ocurrió la incidencia

## 🎯 Objetivo del Proyecto

Este proyecto fue desarrollado como parte de mi aprendizaje en análisis de datos y desarrollo de interfaces gráficas, demostrando habilidades en:
- Procesamiento de datos con Pandas
- Visualización de datos con Matplotlib
- Desarrollo de aplicaciones GUI con Tkinter
- Manejo de errores y validación de datos

---

💡 *Proyecto desarrollado para análisis de datos urbanos y visualización interactiva*
