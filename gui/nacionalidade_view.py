import tkinter as tk
from tkinter import ttk, messagebox

from dao.nacionalidade_dao import NacionalidadeDAO
from models.nacionalidade import Nacionalidade


class NacionalidadeView:

    def __init__(self, root, voltar):
        self.root = root
        self.dao = NacionalidadeDAO()
        self.voltar = voltar

        self.tela()

    # =========================
    # TELA
    # =========================
    def tela(self):
        self.limpar()

        tk.Label(
            self.root,
            text="🌍 Nacionalidades",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack()

        self.tree = ttk.Treeview(frame, columns=("codigo", "descricao"), show="headings")

        self.tree.heading("codigo", text="Código")
        self.tree.heading("descricao", text="Descrição")

        self.tree.column("codigo", width=100)
        self.tree.column("descricao", width=250)

        self.tree.pack()

        # =========================
        # BOTÕES
        # =========================
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Atualizar", command=self.carregar).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Adicionar", command=self.adicionar).grid(row=0, column=1, padx=5)  # 🔥 NOVO
        tk.Button(btn_frame, text="Editar", command=self.editar).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Excluir", command=self.excluir).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Voltar", command=self.voltar).grid(row=0, column=4, padx=5)

        self.carregar()

    # =========================
    # CARREGAR
    # =========================
    def carregar(self):
        self.tree.delete(*self.tree.get_children())

        for n in self.dao.listar():
            self.tree.insert("", "end", values=(n.codigo, n.descricao))

    # =========================
    # ADICIONAR (NOVO)
    # =========================
    def adicionar(self):
        win = tk.Toplevel(self.root)
        win.title("Nova Nacionalidade")

        tk.Label(win, text="Descrição").grid(row=0, column=0)

        entry = tk.Entry(win)
        entry.grid(row=0, column=1)

        def salvar():
            if not entry.get():
                messagebox.showerror("Erro", "Descrição obrigatória")
                return

            nacionalidade = Nacionalidade(None, entry.get())
            self.dao.salvar(nacionalidade)

            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=1, column=0, columnspan=2)

    # =========================
    # EDITAR
    # =========================
    def editar(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione uma nacionalidade")
            return

        codigo, descricao = self.tree.item(item, "values")

        win = tk.Toplevel(self.root)
        win.title("Editar Nacionalidade")

        tk.Label(win, text="Código").grid(row=0, column=0)
        tk.Label(win, text=codigo).grid(row=0, column=1)

        tk.Label(win, text="Descrição").grid(row=1, column=0)

        entry = tk.Entry(win)
        entry.insert(0, descricao)
        entry.grid(row=1, column=1)

        def salvar():
            if not entry.get():
                messagebox.showerror("Erro", "Campo obrigatório")
                return

            self.dao.atualizar(codigo, entry.get())
            win.destroy()
            self.carregar()

        tk.Button(win, text="Salvar", command=salvar).grid(row=2, column=0, columnspan=2)

    # =========================
    # EXCLUIR
    # =========================
    def excluir(self):
        item = self.tree.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione uma nacionalidade")
            return

        codigo, _ = self.tree.item(item, "values")

        if messagebox.askyesno("Confirmação", "Deseja excluir?"):
            self.dao.excluir(codigo)
            self.carregar()

    # =========================
    # LIMPAR
    # =========================
    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()