from database.db import conectar
from models.livro import Livro
from models.editora import Editora
from models.categoria import Categoria
from models.autor import Autor


class LivroDAO:

    def salvar(self, livro: Livro):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO livro (
                isbn, titulo, ano,
                editora_id, categoria_codigo,
                quantidade_exemplares, preco, tipo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            livro.isbn,
            livro.titulo,
            livro.ano,
            livro.editora.id if hasattr(livro.editora, "id") else None,
            livro.categoria.codigo,
            livro.quantidade_exemplares,
            livro.preco,
            "BASE"
        ))

        conn.commit()
        conn.close()

    def excluir(self, isbn):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM livro WHERE isbn = ?", (isbn,))

        conn.commit()
        conn.close()
        
    def listar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT isbn, titulo, ano, quantidade_exemplares, preco, tipo
            FROM livro
        """)

        rows = cursor.fetchall()
        conn.close()

        livros = []

        for isbn, titulo, ano, qtd, preco, tipo in rows:
            livros.append({
                "isbn": isbn,
                "titulo": titulo,
                "ano": ano,
                "quantidade": qtd,
                "preco": preco,
                "tipo": tipo
            })

        return livros
    
    def listar_fisicos(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT l.isbn, l.titulo, l.ano, lf.paginas, lf.peso, lf.localizacao_estante
            FROM livro l
            INNER JOIN livro_fisico lf ON l.isbn = lf.isbn
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows    
    
    
    def listar_digitais(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT l.isbn, l.titulo, l.ano, ld.formato, ld.tamanho_mb
            FROM livro l
            INNER JOIN livro_digital ld ON l.isbn = ld.isbn
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows
    
    def contar_por_editora(self, cnpj):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM livro
            WHERE editora_cnpj = ?
        """, (cnpj,))

        resultado = cursor.fetchone()[0]
        conn.close()

        return resultado    
    
    def contar_por_categoria(self, codigo_categoria):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM livro
            WHERE categoria_id = ?
        """, (codigo_categoria,))

        qtd = cursor.fetchone()[0]
        conn.close()

        return qtd