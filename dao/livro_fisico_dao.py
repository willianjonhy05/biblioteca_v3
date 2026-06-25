from database.db import conectar
from models.livro import LivroFisico


class LivroFisicoDAO:

    def salvar(self, livro: LivroFisico):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO livro_fisico (
                isbn, paginas, peso, altura,
                largura, profundidade, localizacao_estante
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            livro.isbn,
            livro.paginas,
            livro.peso,
            livro.altura,
            livro.largura,
            livro.profundidade,
            livro.localizacao_estante
        ))

        conn.commit()
        conn.close()

    def listar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM livro_fisico")
        rows = cursor.fetchall()
        conn.close()

        return rows