from database.db import conectar
from models.livro import LivroDigital


class LivroDigitalDAO:

    # =========================
    # SALVAR
    # =========================
    def salvar(self, livro: LivroDigital):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO livro (
                isbn, titulo, ano,
                editora_id, categoria_codigo,
                quantidade_exemplares, preco, tipo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 'DIGITAL')
        """, (
            livro.isbn,
            livro.titulo,
            livro.ano,
            livro.editora.id if livro.editora else None,
            livro.categoria.codigo if livro.categoria else None,
            livro.quantidade_exemplares,
            livro.preco
        ))

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

    # =========================
    # LISTAR
    # =========================
    def listar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                l.isbn, l.titulo,
                ld.formato, ld.tamanho_mb,
                l.preco
            FROM livro l
            INNER JOIN livro_digital ld ON ld.isbn = l.isbn
            WHERE l.tipo = 'DIGITAL'
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows

    # =========================
    # ATUALIZAR
    # =========================
    def atualizar(self, isbn, titulo, formato, tamanho_mb):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE livro
            SET titulo = ?
            WHERE isbn = ?
        """, (titulo, isbn))

        cursor.execute("""
            UPDATE livro_digital
            SET formato = ?, tamanho_mb = ?
            WHERE isbn = ?
        """, (formato, tamanho_mb, isbn))

        conn.commit()
        conn.close()

    # =========================
    # EXCLUIR
    # =========================
    def excluir(self, isbn):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM livro WHERE isbn = ?", (isbn,))

        conn.commit()
        conn.close()