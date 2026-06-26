from database.db import conectar
from models.livro import LivroDigital


class LivroDigitalDAO:

    # =========================
    # SALVAR
    # =========================
    def salvar(self, livro: LivroDigital):
        conn = conectar()
        cursor = conn.cursor()

        # ================= LIVRO BASE =================
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
            livro.editora.cnpj if livro.editora else None,
            livro.categoria.codigo if livro.categoria else None,
            livro.quantidade_exemplares,
            livro.preco
        ))

        # ================= DETALHE DIGITAL =================
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

        # ================= AUTORES (N:N) =================
        for autor in livro.autores:
            cursor.execute("""
                INSERT INTO livro_autor (isbn, passaporte)
                VALUES (?, ?)
            """, (
                livro.isbn,
                autor.passaporte
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
                l.isbn,
                l.titulo,
                ld.formato,
                ld.tamanho_mb,
                l.preco,
                c.descricao,
                e.razao_social
            FROM livro l
            LEFT JOIN livro_digital ld ON ld.isbn = l.isbn
            LEFT JOIN categoria c ON c.codigo = l.categoria_codigo
            LEFT JOIN editora e ON e.cnpj = l.editora_id
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