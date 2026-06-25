import tkinter as tk
from tkinter import ttk, messagebox

from dao.livro_digital_dao import LivroDigitalDAO
from dao.categoria_dao import CategoriaDAO
from dao.editora_dao import EditoraDAO
from models.livro import LivroDigital


class LivroDigitalView:

    def __init__(self, root, voltar):
        self.root = root
        self.dao = LivroDigitalDAO()
        self.voltar = voltar

        self.tela()

    # =========================
    # CARREGAR DADOS
    # =========================
    def carregar_dados(self):
        self.categorias = CategoriaDAO().listar()
        self.editoras = EditoraDAO().listar()

    # =========================
    # TELA
    # =========================
    def tela(self):
        self.limpar()
        self.carregar_dados()

        tk.Label(self.root, text="💻 Livros Digitais", font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack()

        self.tree = ttk.Treeview(
            frame,
            columns=("isbn", "titulo", "formato", "tamanho", "preco"),
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

    # =========================
    # CARREGAR
    # =========================
    def carregar(self):
        self.carregar_dados()
        self.tree.delete(*self.tree.get_children())

        for l in self.dao.listar():
            self.tree.insert(
                "",
                "end",
                values=(
                    l[0],  # isbn
                    l[1],  # titulo
                    l[2],  # formato
                    l[3],  # tamanho
                    f"R$ {l[4]:.2f}"
                )
            )

    # =========================
    # ADICIONAR
    # =========================
    def adicionar(self):
        win = tk.Toplevel(self.root)
        win.title("Novo Livro Digital")

        tk.Label(win, text="ISBN").grid(row=0, column=0)
        isbn = tk.Entry(win)
        isbn.grid(row=0, column=1)

        tk.Label(win, text="Título").grid(row=1, column=0)
        titulo = tk.Entry(win)
        titulo.grid(row=1, column=1)

        tk.Label(win, text="Formato").grid(row=2, column=0)
        formato = tk.Entry(win)
        formato.grid(row=2, column=1)

        tk.Label(win, text="Tamanho MB").grid(row=3, column=0)
        tamanho = tk.Entry(win)
        tamanho.grid(row=3, column=1)

        tk.Label(win, text="Preço").grid(row=4, column=0)
        preco = tk.Entry(win)
        preco.grid(row=4, column=1)

        def salvar():
            if not isbn.get() or not titulo.get():
                messagebox.showerror("Erro", "Campos obrigatórios")
                return

            livro = LivroDigital(
                isbn.get(),
                titulo.get(),
                2024,
                None,
                1,
                float(preco.get() or 0),
                None,
                [],
                formato.get(),
                float(tamanho.get() or 0)
            )

            self.dao.salvar(livro)
            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=5, column=0, columnspan=2)

    # =========================
    # EDITAR
    # =========================
    def editar(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro")
            return

        isbn, titulo, formato, tamanho, preco = self.tree.item(item, "values")

        win = tk.Toplevel(self.root)
        win.title("Editar Livro Digital")

        tk.Label(win, text="Título").grid(row=0, column=0)
        titulo_e = tk.Entry(win)
        titulo_e.insert(0, titulo)
        titulo_e.grid(row=0, column=1)

        tk.Label(win, text="Formato").grid(row=1, column=0)
        formato_e = tk.Entry(win)
        formato_e.insert(0, formato)
        formato_e.grid(row=1, column=1)

        tk.Label(win, text="Tamanho MB").grid(row=2, column=0)
        tamanho_e = tk.Entry(win)
        tamanho_e.insert(0, tamanho)
        tamanho_e.grid(row=2, column=1)

        def salvar():
            self.dao.atualizar(
                isbn,
                titulo_e.get(),
                formato_e.get(),
                float(tamanho_e.get() or 0)
            )

            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=3, column=0, columnspan=2)

    # =========================
    # EXCLUIR
    # =========================
    def excluir(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro")
            return

        isbn = self.tree.item(item, "values")[0]

        if messagebox.askyesno("Confirmação", "Deseja excluir?"):
            self.dao.excluir(isbn)
            self.carregar()

    # =========================
    # LIMPAR
    # =========================
    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()