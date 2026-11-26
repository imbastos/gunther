from uuid import uuid4

from core.models.game import Game

katas = [
    Game(
        id=str(uuid4()),
        name="Monólito vs. Microsserviços",
        description="Projete uma arquitetura para uma aplicação de comércio eletrônico considerando os requisitos de escalabilidade e manutenibilidade.",
        difficulty=1,
    ),
    Game(
        id=str(uuid4()),
        name="Escalabilidade de uma API",
        description="Projete uma arquitetura capaz de suportar um aumento significativo no número de requisições simultâneas.",
        difficulty=2,
    ),
    Game(
        id=str(uuid4()),
        name="Processamento Assíncrono",
        description="Projete uma solução para processar grandes volumes de tarefas em segundo plano utilizando mensageria.",
        difficulty=3,
    ),
    Game(
        id=str(uuid4()),
        name="Alta Disponibilidade",
        description="Projete uma arquitetura resiliente capaz de continuar operando mesmo diante da falha de componentes.",
        difficulty=3,
    ),
    Game(
        id=str(uuid4()),
        name="Sistema de Streaming",
        description="Projete uma plataforma de distribuição de conteúdo multimídia considerando disponibilidade, latência e escalabilidade.",
        difficulty=4,
        is_weekly=True,
    ),
]
