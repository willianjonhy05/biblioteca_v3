from database.db import conectar
from models.livro import LivroFisico


class LivroFisicoDAO:

    # =========================
    # BUSCAR ID DA EDITORA PELO CNPJ
    # =========================
    def get_editora_id(self, cnpj):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM editora WHERE cnpj = ?
        """, (cnpj,))

        row = cursor.fetchone()
        conn.close()

        return row[0] if row else None

    # =========================
    # BUSCAR CODIGO CATEGORIA
    # =========================
    def get_categoria_id(self, codigo):
        return codigo  # já é correto no seu banco

    # =========================
    # SALVAR
    # =========================
    def salvar(self, livro: LivroFisico):
        conn = conectar()
        cursor = conn.cursor()

        editora_id = self.get_editora_id(livro.editora.cnpj)

        if not editora_id:
            raise Exception("Editora não encontrada no banco")

        # ================= LIVRO BASE =================
        cursor.execute("""
            INSERT INTO livro (
                isbn, titulo, ano,
                editora_id, categoria_codigo,
                quantidade_exemplares, preco, tipo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 'FISICO')
        """, (
            livro.isbn,
            livro.titulo,
            livro.ano,
            editora_id,              # 🔥 CORRETO AGORA
            livro.categoria.codigo,
            livro.quantidade_exemplares,
            livro.preco
        ))

        # ================= DETALHE FÍSICO =================
        cursor.execute("""
            INSERT INTO livro_fisico (
                isbn, paginas, peso,
                altura, largura, profundidade,
                localizacao_estante
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

        # ================= AUTORES =================
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
                l.isbn, l.titulo,
                l.quantidade_exemplares, l.preco,
                lf.paginas, lf.peso,
                lf.altura, lf.largura, lf.profundidade,
                lf.localizacao_estante,
                c.codigo, c.descricao,
                e.id, e.razao_social
            FROM livro l
            LEFT JOIN livro_fisico lf ON lf.isbn = l.isbn
            LEFT JOIN categoria c ON c.codigo = l.categoria_codigo
            LEFT JOIN editora e ON e.id = l.editora_id
            WHERE l.tipo = 'FISICO'
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows

    # =========================
    # DELETE
    # =========================
    def excluir(self, isbn):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM livro WHERE isbn = ?", (isbn,))

        conn.commit()
        conn.close()

    # =========================
    # UPDATE
    # =========================
    def atualizar(self, isbn, titulo):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE livro
            SET titulo = ?
            WHERE isbn = ?
        """, (titulo, isbn))

        conn.commit()
        conn.close()