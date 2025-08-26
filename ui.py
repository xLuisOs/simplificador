import customtkinter as ctk
from tkinter import ttk, messagebox
from parser import parse
from simplifier import simplify_total, optimize_tree
from tree import to_string

def execute_ui(entry, table, result_var):
    expr = entry.get()
    steps = []
    try:
        tree = parse(expr)
        tree = simplify_total(tree, steps)
        tree = optimize_tree(tree)

        for row in table.get_children():
            table.delete(row)

        if not steps:
            messagebox.showinfo("Simplificación", "No se aplicaron simplificaciones.")
        else:
            for step in steps:
                if "→" in step:
                    before, after = step.split("→")
                    law = before.split(":")[0]
                    table.insert("", "end", values=(
                        before.split(":")[1].strip(),
                        law.strip(),
                        after.strip()
                    ))

        result_var.set(to_string(tree))
    except RecursionError:
        messagebox.showerror("Error", "Expresión demasiado compleja o paréntesis mal colocados.")

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

def create_ui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Simplificador Booleano Definitivo")
    root.update()
    root.state("zoomed") 
    root.configure(fg_color="#1B1F2B")
    frame = ctk.CTkFrame(root, corner_radius=25, fg_color="#1B1F2B")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(frame,
                 text="Ingresa expresión booleana (ej: (A'+B)*(A+B'))",
                 fg_color=None,
                 text_color="#E0E0E0",
                 font=("Arial", 14)).pack(anchor="w")
    entry = ctk.CTkEntry(frame, width=500,
                         fg_color="#2A2E3E",
                         text_color="#E0E0E0",
                         placeholder_text_color="#888888")
    entry.pack(pady=10)

    buttons_frame = ctk.CTkFrame(frame, fg_color="#1B1F2B")
    buttons_frame.pack(pady=10)

    simplify_button = ctk.CTkButton(
        buttons_frame,
        text="Simplificar",
        width=180,
        height=45,
        corner_radius=25,
        font=("Arial", 14, "bold"),
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
        font=("Arial", 14, "bold"),
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
        font=("Arial", 14, "bold"),
        fg_color=("#1e3c72", "#9d50bb"),
        hover_color=("#3A7CA5", "#8A2BE2"),
        text_color="#FFFFFF",
        command=lambda: clear_all(entry, table, result_var)
    )
    clear_button.pack(side="left", padx=5)

    tree_frame = ctk.CTkFrame(frame, corner_radius=25, fg_color="#2A2E3E")
    tree_frame.pack(pady=10, fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#2A2E3E",
                    foreground="#E0E0E0",
                    fieldbackground="#2A2E3E",
                    rowheight=25)
    style.map("Treeview",
              background=[("selected", "#3A7CA5")],
              foreground=[("selected", "#FFFFFF")])

    table = ttk.Treeview(tree_frame, columns=("Before", "Law", "After"), show="headings", height=15)
    table.heading("Before", text="Antes")
    table.heading("Law", text="Ley aplicada")
    table.heading("After", text="Después")
    table.column("Before", width=250)
    table.column("Law", width=150)
    table.column("After", width=250)
    table.pack(fill="both", expand=True, padx=5, pady=5)

    result_var = ctk.StringVar()
    ctk.CTkLabel(frame, text="Resultado final:", text_color="#E0E0E0", font=("Arial", 14)).pack(anchor="w", pady=(10, 0))
    ctk.CTkLabel(frame, textvariable=result_var, wraplength=1200, text_color="#FFFFFF").pack(anchor="w")

    return root