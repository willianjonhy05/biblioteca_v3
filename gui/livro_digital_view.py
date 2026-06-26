import tkinter as tk
from tkinter import ttk, messagebox

from dao.livro_digital_dao import LivroDigitalDAO
from dao.categoria_dao import CategoriaDAO
from dao.editora_dao import EditoraDAO
from dao.autor_dao import AutorDAO
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
        self.autores = AutorDAO().listar()

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
            columns=("isbn", "titulo", "categoria", "editora", "formato", "tamanho", "preco"),
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
                    l[5] or "",  # categoria
                    l[6] or "",  # editora
                    l[2],  # formato
                    l[3],  # tamanho
                    f"R$ {l[4]:.2f}" if l[4] else "R$ 0.00"
                )
            )

    # =========================
    # ADICIONAR
    # =========================
    def adicionar(self):
        self.carregar_dados()

        win = tk.Toplevel(self.root)
        win.title("Novo Livro Digital")

        tk.Label(win, text="ISBN").grid(row=0, column=0)
        isbn = tk.Entry(win)
        isbn.grid(row=0, column=1)

        tk.Label(win, text="Título").grid(row=1, column=0)
        titulo = tk.Entry(win)
        titulo.grid(row=1, column=1)

        tk.Label(win, text="Categoria").grid(row=2, column=0)
        categoria = ttk.Combobox(win, values=[c.descricao for c in self.categorias], state="readonly")
        categoria.grid(row=2, column=1)

        tk.Label(win, text="Editora").grid(row=3, column=0)
        editora = ttk.Combobox(win, values=[e.razao_social for e in self.editoras], state="readonly")
        editora.grid(row=3, column=1)

        # =========================
        # AUTORES (AGORA CORRETO)
        # =========================
        tk.Label(win, text="Autores").grid(row=4, column=0)

        listbox = tk.Listbox(win, selectmode="multiple")
        listbox.grid(row=4, column=1)

        for a in self.autores:
            listbox.insert(tk.END, a.nome)

        tk.Label(win, text="Formato").grid(row=5, column=0)
        formato = tk.Entry(win)
        formato.grid(row=5, column=1)

        tk.Label(win, text="Tamanho MB").grid(row=6, column=0)
        tamanho = tk.Entry(win)
        tamanho.grid(row=6, column=1)

        tk.Label(win, text="Preço").grid(row=7, column=0)
        preco = tk.Entry(win)
        preco.grid(row=7, column=1)

        def salvar():

            cat_obj = next((c for c in self.categorias if c.descricao == categoria.get()), None)
            edi_obj = next((e for e in self.editoras if e.razao_social == editora.get()), None)

            autores_obj = [self.autores[i] for i in listbox.curselection()]

            if not cat_obj or not edi_obj:
                messagebox.showerror("Erro", "Selecione categoria e editora")
                return

            if not autores_obj:
                messagebox.showerror("Erro", "Selecione pelo menos um autor")
                return

            livro = LivroDigital(
                isbn.get(),
                titulo.get(),
                2024,
                edi_obj,
                1,
                float(preco.get() or 0),
                cat_obj,
                autores_obj,   # ✅ AQUI ESTÁ O CAMPO CORRETO
                formato.get(),
                float(tamanho.get() or 0)
            )

            self.dao.salvar(livro)
            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=8, column=0, columnspan=2)

    # =========================
    # EDITAR
    # =========================
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

        tk.Label(win, text="Formato").grid(row=1, column=0)
        formato = tk.Entry(win)
        formato.grid(row=1, column=1)

        tk.Label(win, text="Tamanho MB").grid(row=2, column=0)
        tamanho = tk.Entry(win)
        tamanho.grid(row=2, column=1)

        def salvar():
            self.dao.atualizar(
                isbn,
                titulo.get(),
                formato.get(),
                float(tamanho.get() or 0)
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
            return

        isbn = self.tree.item(item, "values")[0]

        if messagebox.askyesno("Confirmação", "Excluir?"):
            self.dao.excluir(isbn)
            self.carregar()

    # =========================
    # LIMPAR
    # =========================
    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()