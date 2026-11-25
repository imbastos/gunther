from core.models import Post

posts = [
    Post(
        name="O que é Arquitetura de Sistemas?",
        text=(
            "A Arquitetura de Sistemas define a organização dos componentes "
            "de um sistema, suas responsabilidades e a maneira como "
            "interagem. Ela envolve decisões sobre tecnologias, comunicação, "
            "armazenamento de dados e estrutura da aplicação. Uma boa "
            "arquitetura busca atender aos requisitos do sistema, considerando "
            "aspectos como desempenho, segurança, escalabilidade e manutenção."
        ),
        image="assets/articles/system-architecture.png",
        is_highlighted=True,
    ),
    Post(
        name="Monólitos e Microsserviços",
        text=(
            "Uma arquitetura monolítica concentra as funcionalidades de uma "
            "aplicação em uma única unidade de implantação. Já a arquitetura "
            "de microsserviços divide o sistema em serviços menores e "
            "independentes, organizados em torno de responsabilidades "
            "específicas. Cada abordagem possui vantagens e limitações: "
            "monólitos tendem a ser mais simples de desenvolver inicialmente, "
            "enquanto microsserviços podem facilitar a evolução independente "
            "de partes do sistema, embora aumentem a complexidade operacional."
        ),
        image="assets/articles/monolith-microservices.png",
        is_highlighted=True,
    ),
    Post(
        name="Escalabilidade em Sistemas",
        text=(
            "Escalabilidade é a capacidade de um sistema lidar com o aumento "
            "da demanda. Na escalabilidade vertical, são ampliados os recursos "
            "de uma máquina, como memória e processamento. Na horizontal, "
            "são adicionadas novas instâncias da aplicação para distribuir "
            "a carga. A escolha depende dos requisitos, dos custos e das "
            "características da aplicação."
        ),
        image="assets/articles/scalability.png",
    ),
    Post(
        name="A importância dos Bancos de Dados",
        text=(
            "Bancos de dados são componentes fundamentais na maioria dos "
            "sistemas, responsáveis pelo armazenamento e pela recuperação "
            "de informações. Bancos relacionais organizam os dados em tabelas "
            "e utilizam relacionamentos para representar suas conexões. "
            "Bancos não relacionais oferecem diferentes modelos de organização, "
            "como documentos e chave-valor. A escolha deve considerar o "
            "formato dos dados e as necessidades da aplicação."
        ),
        image="assets/articles/databases.png",
    ),
    Post(
        name="Balanceamento de Carga",
        text=(
            "O balanceamento de carga distribui as requisições recebidas "
            "entre diferentes servidores ou instâncias de uma aplicação. "
            "Essa estratégia ajuda a evitar a sobrecarga de um único servidor "
            "e pode melhorar a disponibilidade e o desempenho do sistema. "
            "Existem diferentes algoritmos de distribuição, como Round Robin "
            "e Least Connections."
        ),
        image="assets/articles/load-balancing.png",
    ),
    Post(
        name="Tolerância a Falhas",
        text=(
            "Tolerância a falhas é a capacidade de um sistema continuar "
            "oferecendo seus serviços mesmo quando determinados componentes "
            "apresentam problemas. Estratégias como replicação, redundância, "
            "recuperação automática e monitoramento ajudam a reduzir o "
            "impacto de falhas. Essas decisões são especialmente importantes "
            "em sistemas que precisam manter alta disponibilidade."
        ),
        image="assets/articles/fault-tolerance.png",
    ),
]
