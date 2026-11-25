from enum import StrEnum


class ArticleArea(StrEnum):
    """Áreas de conhecimento em arquitetura de sistemas."""

    REQUISITOS = "requisitos"
    PROJETO_DE_SOFTWARE = "projeto_de_software"
    ARQUITETURA_DE_SISTEMAS = "arquitetura_de_sistemas"
    PADROES_ARQUITETURAIS = "padroes_arquiteturais"
    PADROES_DE_PROJETO = "padroes_de_projeto"
    MICROSSERVICOS = "microsservicos"
    PROJETO_DE_APIS = "projeto_de_apis"
    BANCOS_DE_DADOS = "bancos_de_dados"
    ARQUITETURA_DE_DADOS = "arquitetura_de_dados"
    INTEGRACAO_DE_SISTEMAS = "integracao_de_sistemas"
    SEGURANCA = "seguranca"
    DESEMPENHO = "desempenho"
    ESCALABILIDADE = "escalabilidade"
    COMPUTACAO_EM_NUVEM = "computacao_em_nuvem"
    DEVOPS = "devops"
    TESTES = "testes"
    INFRAESTRUTURA = "infraestrutura"
    MANUTENCAO = "manutencao"
    DOCUMENTACAO = "documentacao"
    OUTROS = "outros"
