import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import sympy as sp
from sympy import symbols, lambdify, integrate, sympify, latex
from PIL import Image, ImageTk
import webbrowser
import re

class IntegralMasterPro:
    def __init__(self, root):
        self.root = root
        self.root.title("El Yamiyecto")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg="#2c3e50")
        
        # Variables para la integral
        self.integral_parts = {
            'function': '',
            'variable': 'x',
            'lower_limit': '',
            'upper_limit': ''
        }
        
        # Elementos disponibles para arrastrar
        self.available_elements = {
            'funciones': ['x', 'x^2', 'x^3', '√x', 'sin(x)', 'cos(x)', 'tan(x)', 'e^x', 'ln(x)', '1/x', '|x|'],
            'operaciones': ['+', '-', '×', '÷', '(', ')', '^'],
            'constantes': ['0', '1', '2', '3', 'π', 'e', '-1', '-2', '-π'],
            'limites': ['0', '1', '2', '3', 'π', '2π', 'e', '-1', '-π']
        }
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.setup_ui()
        
        # Variables de tema
        self.dark_mode = True
        self.graph_style = "default"
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar colores para modo oscuro
        self.style.configure('.', background="#2c3e50", foreground="#ecf0f1")
        self.style.configure('TFrame', background="#2c3e50")
        self.style.configure('TLabel', background="#2c3e50", foreground="#ecf0f1")
        self.style.configure('TButton', background="#3498db", foreground="#2c3e50", 
                            font=('Arial', 10, 'bold'), borderwidth=1)
        self.style.map('TButton', background=[('active', '#2980b9')])
        self.style.configure('TLabelframe', background="#34495e", foreground="#ecf0f1")
        self.style.configure('TLabelframe.Label', background="#34495e", foreground="#ecf0f1")
        self.style.configure('TEntry', fieldbackground="#ecf0f1", foreground="#2c3e50")
        self.style.configure('TCombobox', fieldbackground="#ecf0f1", foreground="#2c3e50")
        
        # Estilo para botones de funciones
        self.style.configure('Func.TButton', background="#9b59b6", font=('Arial', 9, 'bold'))
        self.style.map('Func.TButton', background=[('active', '#8e44ad')])
        
        # Estilo para botones de operaciones
        self.style.configure('Op.TButton', background="#2ecc71", font=('Arial', 10, 'bold'))
        self.style.map('Op.TButton', background=[('active', '#27ae60')])
        
        # Estilo para botones de constantes
        self.style.configure('Const.TButton', background="#e67e22", font=('Arial', 9, 'bold'))
        self.style.map('Const.TButton', background=[('active', '#d35400')])
        
        # Estilo para botones de límites
        self.style.configure('Limit.TButton', background="#e74c3c", font=('Arial', 8, 'bold'))
        self.style.map('Limit.TButton', background=[('active', '#c0392b')])
        
        # Estilo para botones especiales
        self.style.configure('Special.TButton', background="#1abc9c", font=('Arial', 9, 'bold'))
        self.style.map('Special.TButton', background=[('active', '#16a085')])
        
    def setup_ui(self):
        # Crear paneles principales
        main_panel = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo (controles)
        control_frame = ttk.Frame(main_panel, padding=10)
        main_panel.add(control_frame, weight=1)
        
        # Panel derecho (gráfico y resultados)
        result_frame = ttk.Frame(main_panel, padding=10)
        main_panel.add(result_frame, weight=2)
        
        # ========== PANEL DE CONTROL ==========
        # Logo y título
        logo_frame = ttk.Frame(control_frame)
        logo_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Logo simulado (en lugar de cargar una imagen)
        logo_label = ttk.Label(logo_frame, text="∫", font=('Arial', 36, 'bold'), 
                              foreground="#3498db", background="#2c3e50")
        logo_label.pack(side=tk.LEFT, padx=5)
        
        title_frame = ttk.Frame(logo_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(title_frame, text="IntegralMaster Pro 3000 UPV ", font=('Arial', 16, 'bold')).pack(anchor=tk.W)
        ttk.Label(title_frame, text="Constructor y Visualizador de Integrales", 
                 font=('Arial', 10)).pack(anchor=tk.W)
        
        # Barra de herramientas
        toolbar = ttk.Frame(control_frame)
        toolbar.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(toolbar, text="📚 Ejemplos", command=self.show_examples, 
                  style='Special.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📋 Historial", command=self.show_history, 
                  style='Special.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🌙 Tema", command=self.toggle_theme, 
                  style='Special.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="❓ Ayuda", command=self.show_help, 
                  style='Special.TButton').pack(side=tk.LEFT, padx=2)
        
        # Constructor de integrales
        integral_frame = ttk.LabelFrame(control_frame, text="Constructor de Integrales", padding=10)
        integral_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Display de la integral
        self.integral_display = ttk.Label(integral_frame, text="∫ dx", 
                                         font=('Cambria Math', 24), background="#34495e")
        self.integral_display.pack(pady=(5, 15))
        
        # Entradas para la integral
        input_frame = ttk.Frame(integral_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Límite superior
        ttk.Label(input_frame, text="Límite Superior:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.upper_limit_var = tk.StringVar()
        self.upper_limit_entry = ttk.Entry(input_frame, textvariable=self.upper_limit_var, width=10)
        self.upper_limit_entry.grid(row=0, column=1, padx=(0, 15))
        
        # Límite inferior
        ttk.Label(input_frame, text="Límite Inferior:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.lower_limit_var = tk.StringVar()
        self.lower_limit_entry = ttk.Entry(input_frame, textvariable=self.lower_limit_var, width=10)
        self.lower_limit_entry.grid(row=0, column=3)
        
        # Función
        ttk.Label(integral_frame, text="Función f(x):").pack(anchor=tk.W, pady=(10, 5))
        self.function_var = tk.StringVar()
        self.function_var.trace_add('write', self.update_integral_display)
        self.function_entry = ttk.Entry(integral_frame, textvariable=self.function_var, width=30)
        self.function_entry.pack(fill=tk.X)
        
        # Botones de límites rápidos
        limits_frame = ttk.Frame(integral_frame)
        limits_frame.pack(fill=tk.X, pady=(10, 5))
        
        ttk.Label(limits_frame, text="Límites rápidos:").pack(side=tk.LEFT)
        for limit in self.available_elements['limites']:
            btn = ttk.Button(limits_frame, text=limit, width=4, style='Limit.TButton',
                           command=lambda l=limit: self.set_limit(l))
            btn.pack(side=tk.LEFT, padx=2)
        
        # Elementos disponibles
        elements_frame = ttk.LabelFrame(control_frame, text="Elementos Disponibles", padding=10)
        elements_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Funciones
        ttk.Label(elements_frame, text="Funciones:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        functions_frame = ttk.Frame(elements_frame)
        functions_frame.pack(fill=tk.X, pady=(0, 10))
        
        for func in self.available_elements['funciones']:
            btn = ttk.Button(functions_frame, text=func, style='Func.TButton',
                           command=lambda f=func: self.add_to_function(f))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Operaciones
        ttk.Label(elements_frame, text="Operaciones:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        operations_frame = ttk.Frame(elements_frame)
        operations_frame.pack(fill=tk.X, pady=(0, 10))
        
        for op in self.available_elements['operaciones']:
            btn = ttk.Button(operations_frame, text=op, width=3, style='Op.TButton',
                           command=lambda o=op: self.add_to_function(o))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Constantes
        ttk.Label(elements_frame, text="Constantes:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        constants_frame = ttk.Frame(elements_frame)
        constants_frame.pack(fill=tk.X)
        
        for const in self.available_elements['constantes']:
            btn = ttk.Button(constants_frame, text=const, style='Const.TButton',
                           command=lambda c=const: self.add_to_function(c))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Botones de control
        control_buttons = ttk.Frame(control_frame)
        control_buttons.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(control_buttons, text="🧹 Limpiar Todo", 
                  command=self.clear_all, style='Special.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_buttons, text="🔢 Calcular", 
                  command=self.calculate_and_plot, style='TButton').pack(side=tk.RIGHT, padx=5)
        
        # ========== PANEL DE RESULTADOS ==========
        # Pestañas para gráfico e información
        self.notebook = ttk.Notebook(result_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de Gráfico
        graph_tab = ttk.Frame(self.notebook)
        self.notebook.add(graph_tab, text="Gráfico")
        
        # Frame para el gráfico
        graph_container = ttk.Frame(graph_tab)
        graph_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear figura de matplotlib
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(8, 5), facecolor="#2c3e50")
        self.fig.set_facecolor("#2c3e50")
        self.ax.set_facecolor("#34495e")
        self.canvas = FigureCanvasTkAgg(self.fig, graph_container)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Barra de herramientas de matplotlib
        self.toolbar = NavigationToolbar2Tk(self.canvas, graph_container)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Pestaña de Resultados
        results_tab = ttk.Frame(self.notebook)
        self.notebook.add(results_tab, text="Resultados")
        
        # Área de texto para resultados
        self.result_text = scrolledtext.ScrolledText(results_tab, wrap=tk.WORD, 
                                                   font=('Consolas', 11), 
                                                   bg="#34495e", fg="#ecf0f1")
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.result_text.insert(tk.END, "Aquí se mostrarán los resultados detallados...")
        self.result_text.config(state=tk.DISABLED)
        
        # Pestaña de Historial
        self.history_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text="Historial", state=tk.HIDDEN)
        
        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_var.set("Listo")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Historial de cálculos
        self.history = []
        
        # Configurar eventos
        self.function_entry.bind("<Return>", lambda e: self.calculate_and_plot())
        self.upper_limit_entry.bind("<Return>", lambda e: self.calculate_and_plot())
        self.lower_limit_entry.bind("<Return>", lambda e: self.calculate_and_plot())
        
    def add_to_function(self, element):
        current = self.function_var.get()
        # Convertir símbolos matemáticos a formato Python
        element = element.replace('^', '**').replace('×', '*').replace('÷', '/').replace('√', 'sqrt')
        self.function_var.set(current + element)
        
    def update_integral_display(self, *args):
        """Actualiza la visualización de la integral con formato matemático"""
        func = self.function_var.get()
        lower = self.lower_limit_var.get() or "a"
        upper = self.upper_limit_var.get() or "b"
        
        # Formatear la función para visualización
        func_display = func.replace('**', '^').replace('*', '')
        display_text = f"∫  {func_display}  dx\n{lower} → {upper}"
        self.integral_display.config(text=display_text)
        
    def set_limit(self, limit):
        # Simple logic: if upper is empty, set upper; otherwise set lower
        if not self.upper_limit_var.get():
            self.upper_limit_var.set(limit)
        else:
            self.lower_limit_var.set(limit)
        self.update_integral_display()
    
    def clear_function(self):
        self.function_var.set("")
    
    def clear_all(self):
        self.function_var.set("")
        self.upper_limit_var.set("")
        self.lower_limit_var.set("")
        self.update_integral_display()
        self.ax.clear()
        self.canvas.draw()
        self.update_result_text("Campos limpiados. Listo para nueva integral.")
        self.status_var.set("Campos limpiados")
    
    def format_math_expression(self, expr_str):
        """Formatea la expresión para mejor visualización"""
        replacements = {
            '**': '^',
            '*': '',
            'sqrt': '√',
            'exp': 'e^',
            'log': 'ln',
            'pi': 'π',
            'sin': 'sen'
        }
        
        for key, value in replacements.items():
            expr_str = expr_str.replace(key, value)
            
        # Mejorar exponentes
        expr_str = re.sub(r'\^\((\d+)\)', r'^\1', expr_str)
        expr_str = re.sub(r'\^\((\w+)\)', r'^\1', expr_str)
        
        return expr_str
    
    def update_result_text(self, content):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, content)
        self.result_text.config(state=tk.DISABLED)
    
    def calculate_and_plot(self):
        self.status_var.set("Calculando...")
        self.root.update()
        
        try:
            # Obtener valores
            function_str = self.function_var.get()
            upper_limit_str = self.upper_limit_var.get()
            lower_limit_str = self.lower_limit_var.get()
            
            if not all([function_str, upper_limit_str, lower_limit_str]):
                messagebox.showerror("Error", "Por favor completa todos los campos")
                self.status_var.set("Error: Campos incompletos")
                return
            
            # Crear símbolo
            x = symbols('x')
            
            # Convertir strings a expresiones de sympy
            function_expr = sympify(function_str.replace('^', '**'))
            upper_limit = float(sympify(upper_limit_str).evalf())
            lower_limit = float(sympify(lower_limit_str).evalf())
            
            if lower_limit >= upper_limit:
                messagebox.showerror("Error", "El límite inferior debe ser menor que el superior")
                self.status_var.set("Error: Límites incorrectos")
                return
            
            # Calcular la integral
            integral_result = integrate(function_expr, (x, lower_limit, upper_limit))
            integral_value = float(integral_result.evalf())
            
            # Crear función para graficar
            func_lambdified = lambdify(x, function_expr, 'numpy')
            
            # Limpiar el gráfico anterior
            self.ax.clear()
            
            # Crear puntos para la gráfica
            range_extension = (upper_limit - lower_limit) * 0.2
            x_min = min(lower_limit, upper_limit) - range_extension
            x_max = max(lower_limit, upper_limit) + range_extension
            
            x_vals = np.linspace(x_min, x_max, 1000)
            y_vals = func_lambdified(x_vals)
            
            # Graficar la función
            self.ax.plot(x_vals, y_vals, 'cyan', linewidth=2.5, 
                        label=f'f(x) = {self.format_math_expression(function_str)}')
            
            # Rellenar el área bajo la curva
            x_fill = np.linspace(lower_limit, upper_limit, 500)
            y_fill = func_lambdified(x_fill)
            self.ax.fill_between(x_fill, y_fill, alpha=0.4, color='#3498db', 
                               label=f'Área = {integral_value:.4f}')
            
            # Líneas verticales en los límites
            self.ax.axvline(x=lower_limit, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.9)
            self.ax.axvline(x=upper_limit, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.9)
            
            # Punto de intersección con el eje x (si existe)
            x_intersect = np.linspace(lower_limit, upper_limit, 100)
            y_intersect = func_lambdified(x_intersect)
            self.ax.plot(x_intersect, np.zeros_like(x_intersect), 'white', alpha=0.3)
            
            # Configurar el gráfico
            self.ax.set_xlabel('x', fontsize=10)
            self.ax.set_ylabel('f(x)', fontsize=10)
            
            # Título con expresión matemática formateada
            func_display = self.format_math_expression(function_str)
            title = f"∫  {func_display}  dx = {integral_value:.4f}\nLímites: [{lower_limit:.2f} → {upper_limit:.2f}]"
            self.ax.set_title(title, fontsize=12, pad=15)
            
            self.ax.grid(True, alpha=0.2, linestyle='--')
            self.ax.legend(loc='upper right', framealpha=0.3)
            
            # Actualizar el canvas
            self.canvas.draw()
            
            # Mostrar resultados en la pestaña de texto
            result_content = f"=== RESULTADOS DE LA INTEGRAL ===\n\n"
            result_content += f"Función: f(x) = {self.format_math_expression(function_str)}\n"
            result_content += f"Límite inferior: {lower_limit}\n"
            result_content += f"Límite superior: {upper_limit}\n\n"
            result_content += f"Resultado simbólico: {integral_result}\n"
            result_content += f"Resultado numérico: {integral_value:.6f}\n\n"
            result_content += f"=== ANÁLISIS ===\n\n"
            
            # Añadir interpretación del resultado
            if integral_value > 0:
                result_content += "El área bajo la curva es positiva, lo que indica que la función "
                result_content += "está por encima del eje x en el intervalo dado.\n"
            elif integral_value < 0:
                result_content += "El área bajo la curva es negativa, lo que indica que la función "
                result_content += "está por debajo del eje x en el intervalo dado.\n"
            else:
                result_content += "El área neta es cero, lo que indica que las áreas positiva y negativa "
                result_content += "se cancelan exactamente en este intervalo.\n"
                
            # Añadir al historial
            history_entry = {
                'function': function_str,
                'lower': lower_limit,
                'upper': upper_limit,
                'result': integral_value,
                'symbolic': str(integral_result)
            }
            self.history.append(history_entry)
            
            self.update_result_text(result_content)
            self.notebook.select(1)  # Mostrar pestaña de resultados
            
            self.status_var.set(f"Cálculo completado. Resultado: {integral_value:.4f}")
            
        except Exception as e:
            error_msg = f"Error al calcular la integral: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.status_var.set(f"Error: {str(e)[:50]}...")
    
    def show_examples(self):
        examples = """
        Ejemplos de integrales para probar:
        
        1. Integral de una constante:
           Función: 2
           Límite inferior: 0
           Límite superior: 5
           
        2. Integral lineal:
           Función: 3*x
           Límite inferior: 1
           Límite superior: 4
           
        3. Integral cuadrática:
           Función: x^2
           Límite inferior: 0
           Límite superior: 3
           
        4. Integral trigonométrica:
           Función: sin(x)
           Límite inferior: 0
           Límite superior: π
           (Usar 'pi' para π)
           
        5. Integral exponencial:
           Función: e^x
           Límite inferior: 0
           Límite superior: 1
        """
        self.update_result_text(examples)
        self.notebook.select(1)  # Mostrar pestaña de resultados
        self.status_var.set("Ejemplos mostrados")
    
    def show_history(self):
        if not self.history:
            self.update_result_text("El historial está vacío.")
            self.notebook.select(1)
            return
            
        # Crear contenido del historial
        hist_content = "=== HISTORIAL DE CÁLCULOS ===\n\n"
        for i, entry in enumerate(self.history, 1):
            hist_content += f"{i}. ∫ {self.format_math_expression(entry['function'])} dx "
            hist_content += f"de {entry['lower']} a {entry['upper']}\n"
            hist_content += f"   Resultado: {entry['result']:.4f}\n"
            hist_content += f"   Expresión simbólica: {entry['symbolic']}\n\n"
        
        self.update_result_text(hist_content)
        self.notebook.select(1)  # Mostrar pestaña de resultados
        self.status_var.set(f"Mostrando {len(self.history)} cálculos históricos")
    
    def toggle_theme(self):
        if self.dark_mode:
            # Cambiar a modo claro
            self.style.configure('.', background="#ecf0f1", foreground="#2c3e50")
            self.style.configure('TFrame', background="#ecf0f1")
            self.style.configure('TLabel', background="#ecf0f1", foreground="#2c3e50")
            self.style.configure('TLabelframe', background="#d6dbdf", foreground="#2c3e50")
            self.style.configure('TLabelframe.Label', background="#d6dbdf", foreground="#2c3e50")
            self.root.configure(bg="#ecf0f1")
            self.integral_display.config(background="#d6dbdf")
            self.result_text.config(bg="#ffffff", fg="#2c3e50")
            plt.style.use('default')
            self.fig.set_facecolor("#ffffff")
            self.ax.set_facecolor("#f0f3f7")
            self.dark_mode = False
            self.status_var.set("Tema cambiado a claro")
        else:
            # Cambiar a modo oscuro
            self.style.configure('.', background="#2c3e50", foreground="#ecf0f1")
            self.style.configure('TFrame', background="#2c3e50")
            self.style.configure('TLabel', background="#2c3e50", foreground="#ecf0f1")
            self.style.configure('TLabelframe', background="#34495e", foreground="#ecf0f1")
            self.style.configure('TLabelframe.Label', background="#34495e", foreground="#ecf0f1")
            self.root.configure(bg="#2c3e50")
            self.integral_display.config(background="#34495e")
            self.result_text.config(bg="#34495e", fg="#ecf0f1")
            plt.style.use('dark_background')
            self.fig.set_facecolor("#2c3e50")
            self.ax.set_facecolor("#34495e")
            self.dark_mode = True
            self.status_var.set("Tema cambiado a oscuro")
        
        self.canvas.draw()
    
    def show_help(self):
        help_text = """
        IntegralMaster Pro - Ayuda
        
        CÓMO USAR:
        1. Construye tu función usando los botones de funciones, operaciones y constantes
        2. Establece los límites de integración (inferior y superior)
        3. Haz clic en 'Calcular' para ver el resultado y la gráfica
        
        CARACTERÍSTICAS:
        - Visualización del área bajo la curva
        - Resultados numéricos y simbólicos
        - Historial de cálculos
        - Temas claro/oscuro
        - Ejemplos predefinidos
        
        TIPS:
        - Usa '^' para exponentes (ej: x^2)
        - Usa 'sqrt' para raíz cuadrada
        - Usa 'pi' para el número π
        - Usa 'e' para la constante de Euler
        - Puedes teclear directamente en los campos de función y límites
        - Presiona Enter en cualquier campo para calcular automáticamente
        
        Para más información sobre cálculo integral, visita:
        https://es.wikipedia.org/wiki/Integral
        """
        self.update_result_text(help_text)
        self.notebook.select(1)
        self.status_var.set("Ayuda mostrada")

def main():
    root = tk.Tk()
    app = IntegralMasterPro(root)
    root.mainloop()

if __name__ == "__main__":
    main()