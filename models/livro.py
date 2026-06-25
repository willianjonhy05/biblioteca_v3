from models.editora import Editora
from models.categoria import Categoria
from models.autor import Autor

class Livro:
    def __init__(
        self,
        isbn,
        titulo,
        ano,
        editora: Editora,
        quantidade_exemplares,
        preco,
        categoria: Categoria,
        autores: list
    ):
        self.isbn = isbn
        self.titulo = titulo
        self.ano = ano
        self.editora = editora
        self.quantidade_exemplares = quantidade_exemplares
        self.preco = preco
        self.categoria = categoria

        # validação forte de autores
        if not isinstance(autores, list):
            raise TypeError("autores deve ser uma lista de objetos Autor")

        for a in autores:
            if not isinstance(a, Autor):
                raise TypeError("Todos os autores devem ser objetos Autor")

        self.autores = autores

        # associações
        self.categoria.adicionar_livro(self)

        for autor in self.autores:
            autor.adicionar_livro(self)

    def calcular_total(self):
        """
        método base (polimorfismo)
        """
        return self.preco * self.quantidade_exemplares

    def __str__(self):
        return self.titulo    


class LivroDigital(Livro):
    def __init__(
        self,
        isbn,
        titulo,
        ano,
        editora,
        quantidade_exemplares,
        preco,
        categoria,
        autores,
        formato,
        tamanho_mb
    ):
        super().__init__(
            isbn, titulo, ano, editora,
            quantidade_exemplares, preco,
            categoria, autores
        )

        self.formato = formato
        self.tamanho_mb = tamanho_mb

    # 🔥 POLIMORFISMO
    def calcular_total(self):
        valor_base = super().calcular_total()
        return valor_base * 0.80  # 20% desconto digital        
        
class LivroFisico(Livro):
    def __init__(
        self,
        isbn,
        titulo,
        ano,
        editora,
        quantidade_exemplares,
        preco,
        categoria,
        autores,
        paginas,
        peso,
        altura,
        largura,
        profundidade,
        localizacao_estante
    ):

        if quantidade_exemplares <= 0:
            raise ValueError("Livro físico precisa ter pelo menos 1 exemplar")

        super().__init__(
            isbn, titulo, ano, editora,
            quantidade_exemplares, preco,
            categoria, autores
        )

        self.paginas = paginas
        self.peso = peso
        self.altura = altura
        self.largura = largura
        self.profundidade = profundidade
        self.localizacao_estante = localizacao_estante

    # 🔥 POLIMORFISMO
    def calcular_total(self):
        valor_base = super().calcular_total()
        return valor_base * 1.05  # taxa física 5%