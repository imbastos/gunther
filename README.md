![Banner do projeto Gunther](README-Banner.png)

<h1 align="center"> Gunther </h1>
<a name="top"></a>

## 👾 Considerações iniciais

Este é um projeto desenvolvido para fins acadêmicos por estudantes da [Universidade Federal Rural de Pernambuco (UFRPE)](https://ufrpe.br), como parte da disciplina de **Projeto Interdisciplinar para Sistemas de Informação**.

O Gunther é um projeto independente e de caráter acadêmico, **não possuindo vínculo institucional, representação ou afiliação oficial com a UFRPE**.

O presente documento tem como objetivo apresentar o escopo, o planejamento pedagógico, a arquitetura e os requisitos envolvidos na construção do sistema.

---

## 🎯 Sobre o projeto

O **Gunther** é uma ferramenta educacional gamificada desenvolvida em terminal (TUI) com o objetivo de integrar o estudo teórico à aplicação prática de conceitos de **Arquitetura de Sistemas**, aproximando estudantes de problemas reais de design e engenharia de software.

### Problema

Estudar Arquitetura de Sistemas exige um nível elevado de abstração, especialmente porque as soluções de software envolvem _trade-offs_ cujos impactos só são compreendidos em cenários reais. Sem essa vivência prática, os conceitos estudados podem parecer distantes e abstratos, dificultando a consolidação do aprendizado.

### Objetivos

Promover uma aprendizagem progressiva que reduza a intangibilidade da área sem os custos financeiros e computacionais de uma implementação real. Para isso, o sistema combina:

- **Exercícios práticos e cronometrados (katas):** estímulo à resolução de problemas em condições semelhantes às reais.
- **Modo livre:** ambiente voltado à experimentação de soluções arquiteturais.
- **Análise de artigos e Wiki:** construção de pensamento crítico a partir da leitura e discussão de casos reais.

### Metodologia Pedagógica

Baseado na **Taxonomia de Objetivos Educacionais**, o conteúdo do Gunther é estruturado em três etapas progressivas de complexidade cognitiva:

1. **Conhecimento:** introdução simples aos conceitos, priorizando o senso de utilidade.
2. **Análise:** perguntas reflexivas que conectam os conceitos estudados à intuição do estudante.
3. **Avaliação:** testes de _System Design_, nos quais o estudante avalia e escolhe as melhores decisões arquiteturais para um cenário específico.

---

## 📋 Requisitos

Abaixo estão listados os requisitos funcionais definidos para o sistema e seus respectivos status de entrega:

| ID        | Requisito funcional                    | Prioridade                                                           | Status | Escopo |
| --------- | -------------------------------------- | -------------------------------------------------------------------- | ------ | ------ |
| **RF001** | Interface Gráfica (TUI)                | <span style="color: oklch(63.7% 0.237 25.331)">P1 - Altíssima</span> | Pronta | 2 VA   |
| **RF002** | Banco de Dados                         | <span style="color: oklch(63.7% 0.237 25.331)">P1 - Altíssima</span> | Pronta | 2 VA   |
| **RF003** | CRUD de Usuário                        | <span style="color: oklch(63.7% 0.237 25.331)">P1 - Altíssima</span> | Pronta | 2 VA   |
| **RF004** | Gerenciamento de artigos               | <span style="color: oklch(79.5% 0.184 86.047)">P2 - Alta</span>      | Pronta | 2 VA   |
| **RF005** | Gerenciamento de conteúdos (Wiki)      | <span style="color: oklch(79.5% 0.184 86.047)">P2 - Alta</span>      | Pronta | 2 VA   |
| **RF006** | Role Based Access (Controle de acesso) | <span style="color: oklch(85.2% 0.199 91.936)">P3 - Regular</span>   | Pronta | 2 VA   |
| **RF007** | Resumo de atividades                   | <span style="color: oklch(69.6% 0.17 162.48)">P4 - Baixa</span>      | Pronta | 2 VA   |
| **RF008** | Gamificação                            | <span style="color: oklch(63.7% 0.237 25.331)">P1 - Altíssima</span> | Pronta | 2 VA   |
| **RF009** | Sistema de busca                       | <span style="color: oklch(85.2% 0.199 91.936)">P3 - Regular</span>   | Pronta | 2 VA   |
| **RF010** | Sistema de upload                      | <span style="color: oklch(63.7% 0.237 25.331)">P1 - Altíssima</span> | Pronta | 2 VA   |

---

## 🛠️ Tecnologias Utilizadas

- **[Python](https://www.python.org/):** Linguagem principal do projeto.
- **[Textual](https://textual.textualize.io/):** Framework para construção da interface gráfica no terminal (TUI).
- **[textual-image](https://github.com/lnqs/textual-image):** Biblioteca para renderização de imagens diretamente no terminal.
- **Domain-Driven Design (DDD):** Padrão arquitetural adotado na organização de pastas e isolamento de domínio.

## 🏗️ Arquitetura e organização do projeto

O Gunther foi desenvolvido em Python, adotando uma organização inspirada nos princípios de Domain-Driven Design (DDD) e separando as responsabilidades da aplicação em diferentes camadas.

A arquitetura utiliza principalmente os padrões Repository, Service e Dependency Injection (Injeção de Dependência), buscando reduzir o acoplamento entre os componentes, facilitar a manutenção e permitir maior reutilização do código.

---

## 🚀 Como executar

> [!NOTE]
> Certifique-se de ter o **Python 3.10+** instalado em seu ambiente antes de prosseguir.

1. Clone o repositório:
   ```bash
   git clone [https://github.com/imbastos/gunther.git](https://github.com/imbastos/gunther.git)
   cd gunther
   ```
2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv

   # Linux/macOS:

   source .venv/bin/activate

   # Windows:
   .venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash

   python -m pip install -r requirements.txt
   ```

4. Execute a aplicação:

   ```bash

   python -m main
   ```

## 🌱 Inicialização do banco de dados

Após instalar as dependências, é necessário executar o processo de seed para popular o banco de dados com os dados iniciais necessários para o funcionamento da aplicação.

Para realizar essa operação, execute o comando na raiz do projeto:

```bash
python -m infra.db.sqlite.seed
```

Esse comando executa o módulo responsável pela inicialização dos dados do banco de dados SQLite, preparando a aplicação para utilização.

## 🤝 Feedbacks e Contribuições

Para feedbacks, sugestões ou dúvidas sobre o projeto, entre em contato:

- 📧 E-mail: [isaac.bastos@ufrpe.br](mailto:isaac.bastos@ufrpe.br)
- 📃 Artigo: [Link do Drive](https://drive.google.com/drive/folders/1C8hhpwnhtxMsR1KtcCoXYwbOPWlXXIxE?usp=drive_link)

## 📃 Licença

Este projeto é distribuído sob os termos da [GNU General Public License v3.0 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.html).

Consulte o arquivo LICENSE para obter mais informações sobre os termos e condições de uso, modificação e distribuição do projeto.

[Voltar ao início](#top)
