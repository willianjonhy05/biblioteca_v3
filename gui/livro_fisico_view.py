import tkinter as tk
from tkinter import ttk, messagebox

from dao.livro_fisico_dao import LivroFisicoDAO
from dao.categoria_dao import CategoriaDAO
from dao.editora_dao import EditoraDAO
from dao.autor_dao import AutorDAO

from models.livro import LivroFisico


class LivroFisicoView:

    def __init__(self, root, voltar):
        self.root = root
        self.dao = LivroFisicoDAO()
        self.voltar = voltar

        self.tela()

    def carregar_dados(self):
        self.categorias = CategoriaDAO().listar()
        self.editoras = EditoraDAO().listar()
        self.autores = AutorDAO().listar()

    def tela(self):
        self.limpar()
        self.carregar_dados()

        tk.Label(self.root, text="📖 Livros Físicos", font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack()

        self.tree = ttk.Treeview(
            frame,
            columns=("isbn", "titulo", "categoria", "editora", "paginas", "peso"),
            show="headings"
        )

        for c in self.tree["columns"]:
            self.tree.heading(c, text=c.upper())

        self.tree.pack()

        btn = tk.Frame(self.root)
        btn.pack(pady=10)

        tk.Button(btn, text="Atualizar", command=self.carregar).grid(row=0, column=0)
        tk.Button(btn, text="Novo", command=self.adicionar).grid(row=0, column=1)
        tk.Button(btn, text="Editar", command=self.editar).grid(row=0, column=2)
        tk.Button(btn, text="Excluir", command=self.excluir).grid(row=0, column=3)
        tk.Button(btn, text="Voltar", command=self.voltar).grid(row=0, column=4)

        self.carregar()

    def carregar(self):
        self.carregar_dados()
        self.tree.delete(*self.tree.get_children())

        for l in self.dao.listar():
            self.tree.insert(
                "",
                "end",
                values=(
                    l[0],
                    l[1],
                    l[11] if len(l) > 11 else "",
                    l[13] if len(l) > 13 else "",
                    l[4],
                    l[5]
                )
            )

    def adicionar(self):
        self.carregar_dados()

        win = tk.Toplevel(self.root)
        win.title("Novo Livro Físico")

        tk.Label(win, text="ISBN").grid(row=0, column=0)
        isbn = tk.Entry(win)
        isbn.grid(row=0, column=1)

        tk.Label(win, text="Título").grid(row=1, column=0)
        titulo = tk.Entry(win)
        titulo.grid(row=1, column=1)

        # ================= CATEGORIA =================
        tk.Label(win, text="Categoria").grid(row=2, column=0)
        cat_map = {c.descricao: c for c in self.categorias}
        cat_combo = ttk.Combobox(win, values=list(cat_map.keys()), state="readonly")
        cat_combo.grid(row=2, column=1)

        # ================= EDITORA (CNPJ) =================
        tk.Label(win, text="Editora (CNPJ)").grid(row=3, column=0)
        edi_map = {e.cnpj: e for e in self.editoras}
        edi_combo = ttk.Combobox(win, values=list(edi_map.keys()), state="readonly")
        edi_combo.grid(row=3, column=1)

        # ================= AUTORES =================
        tk.Label(win, text="Autores").grid(row=4, column=0)
        listbox = tk.Listbox(win, selectmode="multiple")
        listbox.grid(row=4, column=1)

        for a in self.autores:
            listbox.insert(tk.END, a.nome)

        tk.Label(win, text="Páginas").grid(row=5, column=0)
        paginas = tk.Entry(win)
        paginas.grid(row=5, column=1)

        tk.Label(win, text="Peso").grid(row=6, column=0)
        peso = tk.Entry(win)
        peso.grid(row=6, column=1)

        def salvar():

            categoria_obj = cat_map.get(cat_combo.get())
            editora_obj = edi_map.get(edi_combo.get())
            autores_obj = [self.autores[i] for i in listbox.curselection()]

            if not categoria_obj or not editora_obj:
                messagebox.showerror("Erro", "Selecione categoria e editora")
                return

            livro = LivroFisico(
                isbn.get(),
                titulo.get(),
                2024,
                editora_obj,
                1,
                0,
                categoria_obj,
                autores_obj,
                int(paginas.get() or 0),
                float(peso.get() or 0),
                0, 0, 0,
                "A1"
            )

            self.dao.salvar(livro)
            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=7, column=0, columnspan=2)

    def editar(self):
        item = self.tree.focus()
        if not item:
            return

        isbn = self.tree.item(item, "values")[0]

        win = tk.Toplevel(self.root)
        win.title("Editar")

        tk.Label(win, text="Título").grid(row=0, column=0)
        titulo = tk.Entry(win)
        titulo.grid(row=0, column=1)

        def salvar():
            self.dao.atualizar(isbn, titulo.get())
            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=1, column=0, columnspan=2)

    def excluir(self):
        item = self.tree.focus()
        if not item:
            return

        isbn = self.tree.item(item, "values")[0]

        if messagebox.askyesno("Confirmação", "Excluir?"):
            self.dao.excluir(isbn)
            self.carregar()

    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()