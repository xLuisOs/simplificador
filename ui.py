import customtkinter as ctk
from tkinter import ttk, messagebox
from parser import parse
from simplifier import simplify_total, optimize_tree
from tree import to_string
from tkinter import font
import re

def validate_expression(expr):
    if not expr.strip():
        raise ValueError("El campo está vacío.")
    
    if re.search(r"[^A-Za-z01\+\*\(\)'\s]", expr):
        raise ValueError("Caracteres inválidos detectados. Solo se permiten letras, 0, 1, '+', '*', paréntesis y apóstrofe (').")
    
    bal = 0
    for c in expr:
        if c == '(':
            bal += 1
        elif c == ')':
            bal -= 1
        if bal < 0:
            raise ValueError("Paréntesis cerrados de forma incorrecta.")
    if bal != 0:
        raise ValueError("Número de paréntesis abiertos y cerrados no coincide.")
    
    if re.search(r"[A-Za-z][A-Za-z]", expr):
        raise ValueError("Se detectaron letras consecutivas sin operador. Usa '+' o '*' entre ellas.")
    
    return True

def execute_ui(entry, table, result_var):
    expr = entry.get()
    steps = []
    try:
        validate_expression(expr)
        tree = parse(expr)
        tree = simplify_total(tree, steps)
        tree = optimize_tree(tree)

        for row in table.get_children():
            table.delete(row)

        if not steps:
            messagebox.showinfo("Simplificación", "No se aplicaron simplificaciones.")
        else:
            for step in steps:
                if "→" not in step or ":" not in step:
                    table.insert("", "end", values=(step, "", ""))
                    continue
                law, rest = step.split(":", 1)
                before, after = rest.split("→",1)
                table.insert("", "end", values=(
                    before.strip(),
                    law.strip(),
                    after.strip()
                ))

        result_var.set(to_string(tree))
    except ValueError as ve:
        messagebox.showerror("Error de validación", str(ve))
    except RecursionError:
        messagebox.showerror("Error", "Error de recursión.")
    except Exception as e:
        messagebox.showerror("Error inesperado", str(e))

def show_result_only(entry, result_var):
    expr = entry.get()
    try:
        tree = parse(expr)
        tree = simplify_total(tree, [])
        tree = optimize_tree(tree)
        result_var.set(to_string(tree))
    except RecursionError:
        messagebox.showerror("Error", "Expresión demasiado compleja o paréntesis mal colocados.")

def clear_all(entry, table, result_var):
    entry.delete(0, "end")
    result_var.set("")
    for row in table.get_children():
        table.delete(row)

def show_help():
    rules = (
        "Signos válidos:\n"
        " - '\n"
        " - +\n"
        " - *\n"
        " - 0, 1\n"
        " - Letras (A, B, C...)\n\n"
        "Propiedades usadas en simplificación:\n"
        "1. Doble negación\n"
        "2. Ley de De Morgan\n"
        "3. Identidad / Anulación\n"
        "4. Idempotencia\n"
        "5. Complemento\n"
        "6. Absorción\n"
        "7. Distributiva\n"
        "8. Factor común"
    )
    messagebox.showinfo("Ayuda - Reglas de Simplificación", rules)

def save_to_file(entry, table, result_var):
    from tkinter import filedialog

    expr = entry.get().strip()
    if not expr:
        messagebox.showwarning("Atención", "El campo de expresión está vacío. No se puede guardar.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt")],
        title="Guardar simplificación"
    )
    if not file_path:
        return

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("REPORTE DE SIMPLIFICACIÓN BOOLEANA\n")
            f.write("_"*60 + "\n\n")
            f.write("Expresión original:\n")
            f.write(expr + "\n\n")

            f.write("Pasos de simplificación:\n")
            f.write("_"*60 + "\n")
            if not table.get_children():
                f.write("No se aplicaron simplificaciones.\n")
            else:
                f.write(f"{'ANTES':<25} {'LEY':<20} {'DESPUÉS':<25}\n")
                f.write("_"*60 + "\n")
                for row_id in table.get_children():
                    row = table.item(row_id)["values"]
                    f.write(f"{str(row[0]):<25} {str(row[1]):<20} {str(row[2]):<25}\n")
            f.write("\n")

            f.write("RESULTADO FINAL:\n")
            f.write(result_var.get() + "\n")

        messagebox.showinfo("Éxito", f"Archivo guardado en:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error al guardar", str(e))


def create_ui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Simplificador Booleano")
    root.update()
    root.state("zoomed") 
    root.configure(fg_color="#1B1F2B")
    frame = ctk.CTkFrame(root, corner_radius=25, fg_color="#1B1F2B")
    frame.pack(padx=20, pady=50, fill="both", expand=True)

    ctk.CTkLabel(frame,
                 text="Ingresa una expresión booleana:",
                 fg_color=None,
                 text_color="#E0E0E0",
                 font=("Arial", 30, "bold"),
                anchor="center").pack(pady=10, fill="x")
    entry = ctk.CTkEntry(frame, width=550, height=45,
                         fg_color="#2A2E3E",
                         text_color="#E0E0E0",
                         font=("Arial", 20),
                         placeholder_text_color="#888888")
    entry.pack(pady=20)

    buttons_frame = ctk.CTkFrame(frame, fg_color="#1B1F2B")
    buttons_frame.pack(pady=10)

    simplify_button = ctk.CTkButton(
        buttons_frame,
        text="Simplificar",
        width=180,
        height=45,
        corner_radius=25,
        font=("Arial", 16, "bold"),
        fg_color=("#1e3c72", "#9d50bb"),
        hover_color=("#3A7CA5", "#8A2BE2"),
        text_color="#FFFFFF",
        command=lambda: execute_ui(entry, table, result_var)
    )
    simplify_button.pack(side="left", padx=5)

    result_button = ctk.CTkButton(
        buttons_frame,
        text="Resultado final",
        width=180,
        height=45,
        corner_radius=25,
        font=("Arial", 16, "bold"),
        fg_color=("#1e3c72", "#9d50bb"),
        hover_color=("#3A7CA5", "#8A2BE2"),
        text_color="#FFFFFF",
        command=lambda: show_result_only(entry, result_var)
    )
    result_button.pack(side="left", padx=5)

    clear_button = ctk.CTkButton(
        buttons_frame,
        text="Limpiar todo",
        width=180,
        height=45,
        corner_radius=25,
        font=("Arial", 16, "bold"),
        fg_color=("#1e3c72", "#9d50bb"),
        hover_color=("#3A7CA5", "#8A2BE2"),
        text_color="#FFFFFF",
        command=lambda: clear_all(entry, table, result_var)
    )
    clear_button.pack(side="left", padx=5)

    tree_frame = ctk.CTkFrame(frame, corner_radius=25, fg_color="#2A2E3E")
    tree_frame.pack(pady=20, fill="x")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#2A2E3E",
                    foreground="#E0E0E0",
                    fieldbackground="#2A2E3E",
                    rowheight=35)
    style.map("Treeview",
              background=[("selected", "#8A2BE2")],
              foreground=[("selected", "#FFFFFF")])
    style.configure("Treeview", font=font.Font(family="Arial", size=14))
    style.configure("Treeview.Heading", font=font.Font(family="Arial", size=16, weight="bold"))

    table = ttk.Treeview(tree_frame, columns=("Before", "Law", "After"), show="headings", height=12)
    table.heading("Before", text="Antes")
    table.heading("Law", text="Ley aplicada")
    table.heading("After", text="Después")
    table.column("Before", width=250)
    table.column("Law", width=150)
    table.column("After", width=250)
    table.pack(fill="x", padx=5, pady=5)

    result_var = ctk.StringVar()
    ctk.CTkLabel(frame, text="Resultado final:", text_color="#E0E0E0", font=("Arial", 25, "bold")).pack(anchor="w", pady=(10, 0))
    ctk.CTkLabel(frame, textvariable=result_var, wraplength=1200, font=("Arial", 25,"bold"), text_color="#FFFFFF").pack(anchor="w")

    help = ctk.CTkButton(
        master=frame,
        text="Ayuda",
        width=120,
        height=40,
        corner_radius=20,
        fg_color=("#1e3c72", "#393ff1"),
        font=("Arial", 15, "bold"),
        hover_color=("#3A7CA5", "#0008ff"),
        command=show_help
        )
    help.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

    save_button = ctk.CTkButton(
        buttons_frame,
        text="Guardar archivo",
        width=180,
        height=45,
        corner_radius=25,
        font=("Arial", 16, "bold"),
        fg_color=("#1e3c72", "#9d50bb"),
        hover_color=("#3A7CA5", "#8A2BE2"),
        text_color="#FFFFFF",
        command=lambda: save_to_file(entry, table, result_var)
        )
    save_button.pack(side="left", padx=5)

    return root