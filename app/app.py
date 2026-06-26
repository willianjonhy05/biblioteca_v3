import tkinter as tk
from tkinter import messagebox

from database.db import criar_tabela

from gui.editora_view import EditoraView
from gui.categoria_view import CategoriaView
from gui.nacionalidade_view import NacionalidadeView
from gui.autor_view import AutorView
from gui.livro_fisico_view import LivroFisicoView
from gui.livro_digital_view import LivroDigitalView

from dao.editora_dao import EditoraDAO
from dao.categoria_dao import CategoriaDAO
from dao.nacionalidade_dao import NacionalidadeDAO
from dao.autor_dao import AutorDAO
from dao.livro_dao import LivroDAO


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("📚 ERP Biblioteca")
        self.root.geometry("1000x650")

        criar_tabela()

        self.editora_dao = EditoraDAO()
        self.categoria_dao = CategoriaDAO()
        self.nacionalidade_dao = NacionalidadeDAO()
        self.autor_dao = AutorDAO()
        self.livro_dao = LivroDAO()

        self.dashboard()

    # =========================
    # DASHBOARD
    # =========================
    def dashboard(self):
        self.limpar()

        tk.Label(
            self.root,
            text="📚 PAINEL ERP BIBLIOTECA",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        # ================= KPIs =================
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        categorias = len(self.categoria_dao.listar())
        autores = len(self.autor_dao.listar())
        editoras = len(self.editora_dao.listar())
        nacionalidades = len(self.nacionalidade_dao.listar())

        livros_fisicos = len(self.livro_dao.listar_fisicos())
        livros_digitais = len(self.livro_dao.listar_digitais())

        # 🔥 CORREÇÃO PRINCIPAL (sem usar calcular_total em dict/tupla)
        valor_total = sum(l.preco * l.quantidade_exemplares for l in self.livro_dao.listar())

        tk.Label(frame, text=f"📚 Categorias: {categorias}").grid(row=0, column=0, padx=10)
        tk.Label(frame, text=f"👤 Autores: {autores}").grid(row=0, column=1, padx=10)
        tk.Label(frame, text=f"🏢 Editoras: {editoras}").grid(row=0, column=2, padx=10)
        tk.Label(frame, text=f"🌍 Nacionalidades: {nacionalidades}").grid(row=0, column=3, padx=10)

        tk.Label(frame, text=f"📖 Físicos: {livros_fisicos}").grid(row=1, column=0, padx=10)
        tk.Label(frame, text=f"💻 Digitais: {livros_digitais}").grid(row=1, column=1, padx=10)
        tk.Label(frame, text=f"💰 Total em Mercadoria: R$ {valor_total:.2f}").grid(row=1, column=2, padx=10)

        # ================= MENU =================
        tk.Label(self.root, text="📂 MÓDULOS", font=("Arial", 16, "bold")).pack(pady=15)

        frame2 = tk.Frame(self.root)
        frame2.pack()

        tk.Button(frame2, text="🏢 Editora", width=18, command=self.tela_editora).grid(row=0, column=0, padx=5)
        tk.Button(frame2, text="📚 Categoria", width=18, command=self.tela_categoria).grid(row=0, column=1, padx=5)
        tk.Button(frame2, text="🌍 Nacionalidade", width=18, command=self.tela_nacionalidade).grid(row=0, column=2, padx=5)
        tk.Button(frame2, text="👤 Autores", width=18, command=self.tela_autor).grid(row=0, column=3, padx=5)

        frame3 = tk.Frame(self.root)
        frame3.pack(pady=10)

        tk.Button(frame3, text="📖 Livros Físicos", width=18, command=self.tela_livro_fisico).grid(row=0, column=0, padx=5)
        tk.Button(frame3, text="💻 Livros Digitais", width=18, command=self.tela_livro_digital).grid(row=0, column=1, padx=5)


        tk.Button(self.root, text="❌ Sair", command=self.root.quit).pack(pady=20)

    # =========================
    # NAVIGATION
    # =========================
    def tela_editora(self):
        EditoraView(self.root, self.dashboard)

    def tela_categoria(self):
        CategoriaView(self.root, self.dashboard)

    def tela_nacionalidade(self):
        NacionalidadeView(self.root, self.dashboard)

    def tela_autor(self):
        AutorView(self.root, self.dashboard)

    def tela_livro_fisico(self):
        LivroFisicoView(self.root, self.dashboard)

    def tela_livro_digital(self):
        LivroDigitalView(self.root, self.dashboard)

    # =========================
    # UTIL
    # =========================
    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()