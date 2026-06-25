from database.db import conectar
from models.livro import LivroDigital


class LivroDigitalDAO:

    def salvar(self, livro: LivroDigital):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO livro_digital (
                isbn, formato, tamanho_mb,
                link_download, possui_drm
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            livro.isbn,
            livro.formato,
            livro.tamanho_mb,
            livro.link_download,
            1 if livro.possui_drm else 0
        ))

        conn.commit()
        conn.close()

    def listar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM livro_digital")
        rows = cursor.fetchall()
        conn.close()

        return rows