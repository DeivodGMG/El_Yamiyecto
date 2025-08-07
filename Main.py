import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy as sp
from sympy import symbols, lambdify, integrate, sympify

class IntegralBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("El Constructor y Visualizador de Integrales Definidas 3000")
        self.root.geometry("1000x700")
        
        # Variables para la integral
        self.integral_parts = {
            'function': '',
            'variable': 'x',
            'lower_limit': '',
            'upper_limit': ''
        }
        
        # Elementos disponibles para arrastrar
        self.available_elements = {
            'functions': ['x', 'x**2', 'x**3', 'sin(x)', 'cos(x)', 'exp(x)', '1/x'],
            'operations': ['+', '-', '*', '/'],
            'constants': ['1', '2', '3', 'pi', 'e'],
            'limits': ['0', '1', '2', '3', '4', '5', 'pi', '2*pi']
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para elementos disponibles
        elements_frame = ttk.LabelFrame(main_frame, text="Elementos Disponibles", padding=10)
        elements_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Funciones
        ttk.Label(elements_frame, text="Funciones:").grid(row=0, column=0, sticky=tk.W)
        functions_frame = ttk.Frame(elements_frame)
        functions_frame.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        for i, func in enumerate(self.available_elements['functions']):
            btn = ttk.Button(functions_frame, text=func, width=8,
                           command=lambda f=func: self.add_to_function(f))
            btn.grid(row=0, column=i, padx=2)
        
        # Operaciones
        ttk.Label(elements_frame, text="Operaciones:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        operations_frame = ttk.Frame(elements_frame)
        operations_frame.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        for i, op in enumerate(self.available_elements['operations']):
            btn = ttk.Button(operations_frame, text=op, width=5,
                           command=lambda o=op: self.add_to_function(o))
            btn.grid(row=0, column=i, padx=2)
        
        # Constantes
        ttk.Label(elements_frame, text="Constantes:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        constants_frame = ttk.Frame(elements_frame)
        constants_frame.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        for i, const in enumerate(self.available_elements['constants']):
            btn = ttk.Button(constants_frame, text=const, width=5,
                           command=lambda c=const: self.add_to_function(c))
            btn.grid(row=0, column=i, padx=2)
        
        # Frame para construir la integral
        integral_frame = ttk.LabelFrame(main_frame, text="Constructor de Integral", padding=10)
        integral_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Display de la integral
        integral_display_frame = ttk.Frame(integral_frame)
        integral_display_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(integral_display_frame, text="∫", font=('Arial', 20)).grid(row=0, column=0)
        
        # Límite superior
        ttk.Label(integral_display_frame, text="Límite superior:").grid(row=0, column=1, padx=(10, 0))
        self.upper_limit_var = tk.StringVar()
        self.upper_limit_entry = ttk.Entry(integral_display_frame, textvariable=self.upper_limit_var, width=10)
        self.upper_limit_entry.grid(row=0, column=2, padx=(5, 0))
        
        # Función
        ttk.Label(integral_display_frame, text="Función:").grid(row=1, column=1, padx=(10, 0), pady=(5, 0))
        self.function_var = tk.StringVar()
        self.function_entry = ttk.Entry(integral_display_frame, textvariable=self.function_var, width=30)
        self.function_entry.grid(row=1, column=2, columnspan=2, padx=(5, 0), pady=(5, 0))
        
        # Límite inferior
        ttk.Label(integral_display_frame, text="Límite inferior:").grid(row=2, column=1, padx=(10, 0), pady=(5, 0))
        self.lower_limit_var = tk.StringVar()
        self.lower_limit_entry = ttk.Entry(integral_display_frame, textvariable=self.lower_limit_var, width=10)
        self.lower_limit_entry.grid(row=2, column=2, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(integral_display_frame, text="dx", font=('Arial', 12)).grid(row=1, column=4, padx=(5, 0))
        
        # Botones de límites rápidos
        limits_frame = ttk.Frame(integral_frame)
        limits_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(limits_frame, text="Límites rápidos:").pack(side=tk.LEFT)
        for limit in self.available_elements['limits']:
            btn = ttk.Button(limits_frame, text=limit, width=6,
                           command=lambda l=limit: self.set_limit(l))
            btn.pack(side=tk.LEFT, padx=2)
        
        # Botones de control
        control_frame = ttk.Frame(integral_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(control_frame, text="Limpiar Función", 
                  command=self.clear_function).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Limpiar Todo", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Calcular y Graficar", 
                  command=self.calculate_and_plot).pack(side=tk.RIGHT)
        
        # Frame para el gráfico
        self.plot_frame = ttk.LabelFrame(main_frame, text="Visualización", padding=10)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def add_to_function(self, element):
        current = self.function_var.get()
        self.function_var.set(current + element)
        
    def set_limit(self, limit):
        # Simple logic: if upper is empty, set upper; otherwise set lower
        if not self.upper_limit_var.get():
            self.upper_limit_var.set(limit)
        else:
            self.lower_limit_var.set(limit)
    
    def clear_function(self):
        self.function_var.set("")
    
    def clear_all(self):
        self.function_var.set("")
        self.upper_limit_var.set("")
        self.lower_limit_var.set("")
    
    def calculate_and_plot(self):
        try:
            # Obtener valores
            function_str = self.function_var.get()
            upper_limit_str = self.upper_limit_var.get()
            lower_limit_str = self.lower_limit_var.get()
            
            if not all([function_str, upper_limit_str, lower_limit_str]):
                messagebox.showerror("Error", "Por favor completa todos los campos")
                return
            
            # Crear símbolo
            x = symbols('x')
            
            # Convertir strings a expresiones de sympy
            function_expr = sympify(function_str)
            upper_limit = float(sympify(upper_limit_str).evalf())
            lower_limit = float(sympify(lower_limit_str).evalf())
            
            if lower_limit >= upper_limit:
                messagebox.showerror("Error", "El límite inferior debe ser menor que el superior")
                return
            
            # Calcular la integral
            integral_result = integrate(function_expr, (x, lower_limit, upper_limit))
            integral_value = float(integral_result.evalf())
            
            # Crear función para graficar
            func_lambdified = lambdify(x, function_expr, 'numpy')
            
            # Limpiar el gráfico anterior
            self.ax.clear()
            
            # Crear puntos para la gráfica
            x_vals = np.linspace(lower_limit - 1, upper_limit + 1, 1000)
            y_vals = func_lambdified(x_vals)
            
            # Graficar la función
            self.ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {function_str}')
            
            # Rellenar el área bajo la curva
            x_fill = np.linspace(lower_limit, upper_limit, 200)
            y_fill = func_lambdified(x_fill)
            self.ax.fill_between(x_fill, y_fill, alpha=0.3, color='lightblue', 
                               label=f'Área = {integral_value:.4f}')
            
            # Líneas verticales en los límites
            self.ax.axvline(x=lower_limit, color='red', linestyle='--', alpha=0.7)
            self.ax.axvline(x=upper_limit, color='red', linestyle='--', alpha=0.7)
            
            # Configurar el gráfico
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('f(x)')
            self.ax.set_title(f'∫[{lower_limit}→{upper_limit}] {function_str} dx = {integral_value:.4f}')
            self.ax.grid(True, alpha=0.3)
            self.ax.legend()
            
            # Actualizar el canvas
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la integral: {str(e)}")

def main():
    root = tk.Tk()
    app = IntegralBuilder(root)
    root.mainloop()

if __name__ == "__main__":
    main()