from core.models.category import Category
from core.models.node import Node


categories = (
    Category(color="#4F8EF7", name="Banco de Dados", id="58c17ac2-e23a-4757-b99a-89bab9b31576"),
    Category(color="#F59E0B", name="Processamento", id="82a48b06-4aea-4e15-bffe-c5f9863e6dfb"),
    Category(color="#06B6D4", name="Rede e comunicação", id="a1952bb3-807e-4354-b72a-a3f96dd01853"),
    Category(color="#8B5CF6", name="Mensageria", id="52bdddbc-2c4c-44fc-82e6-04d3cc8f219d"),
    Category(color="#10B981", name="Armazenamento", id="4b819ca2-9157-4a4c-ab31-37d2b70ede81"),
    Category(color="#EF4444", name="Segurança", id="516d4e75-dbb8-4483-a8a3-b462187b4999"),
    Category(color="#EC4899", name="Observabilidade", id="5e9cd8a6-e6fb-4e44-9913-90797a49c37f"),
    Category(color="#A3A3A3", name="Clientes", id="f83e0f1e-cb44-4032-8142-76af0fb42ef5"),
)

CATEGORY_IDS = {
    "database": "58c17ac2-e23a-4757-b99a-89bab9b31576",
    "compute": "82a48b06-4aea-4e15-bffe-c5f9863e6dfb",
    "network": "a1952bb3-807e-4354-b72a-a3f96dd01853",
    "messaging": "52bdddbc-2c4c-44fc-82e6-04d3cc8f219d",
    "storage": "4b819ca2-9157-4a4c-ab31-37d2b70ede81",
    "security": "516d4e75-dbb8-4483-a8a3-b462187b4999",
    "observability": "5e9cd8a6-e6fb-4e44-9913-90797a49c37f",
    "client": "f83e0f1e-cb44-4032-8142-76af0fb42ef5",
}

nodes = (
        Node(category=CATEGORY_IDS["database"], name="SQL", price=100),
        Node(category=CATEGORY_IDS["database"], name="NoSQL", price=120),
        Node(category=CATEGORY_IDS["database"], name="Redis", price=150),
        Node(category=CATEGORY_IDS["database"], name="PostgreSQL", price=180),
        Node(category=CATEGORY_IDS["database"], name="MongoDB", price=180),
        Node(category=CATEGORY_IDS["compute"], name="Servidor", price=100),
        Node(category=CATEGORY_IDS["compute"], name="Servidor de Aplicação", price=150),
        Node(category=CATEGORY_IDS["compute"], name="Worker", price=120),
        Node(category=CATEGORY_IDS["compute"], name="Lambda", price=180),
        Node(category=CATEGORY_IDS["compute"], name="Container", price=160),
        Node(category=CATEGORY_IDS["network"], name="Balanceador de Carga", price=200),
        Node(category=CATEGORY_IDS["network"], name="API Gateway", price=180),
        Node(category=CATEGORY_IDS["network"], name="Proxy Reverso", price=120),
        Node(category=CATEGORY_IDS["network"], name="DNS", price=80),
        Node(category=CATEGORY_IDS["network"], name="CDN", price=250),
        Node(category=CATEGORY_IDS["messaging"], name="Fila de Mensagens", price=150),
        Node(category=CATEGORY_IDS["messaging"], name="RabbitMQ", price=200),
        Node(category=CATEGORY_IDS["messaging"], name="Kafka", price=300),
        Node(category=CATEGORY_IDS["messaging"], name="Barramento de Eventos", price=220),
        Node(category=CATEGORY_IDS["storage"], name="Armazenamento de Objetos", price=150),
        Node(category=CATEGORY_IDS["storage"], name="Armazenamento de Arquivos", price=100),
        Node(category=CATEGORY_IDS["storage"], name="Armazenamento em Bloco", price=180),
        Node(category=CATEGORY_IDS["storage"], name="Data Lake", price=300),
        Node(category=CATEGORY_IDS["security"], name="Firewall", price=150),
        Node(category=CATEGORY_IDS["security"], name="Serviço de Autenticação", price=180),
        Node(category=CATEGORY_IDS["security"], name="Serviço de Autorização", price=180),
        Node(category=CATEGORY_IDS["security"], name="WAF", price=220),
        Node(category=CATEGORY_IDS["observability"], name="Logger", price=80),
        Node(category=CATEGORY_IDS["observability"], name="Coletor de Métricas", price=120),
        Node(category=CATEGORY_IDS["observability"], name="Rastreamento Distribuído", price=180),
        Node(category=CATEGORY_IDS["observability"], name="Monitoramento", price=150),
        Node(category=CATEGORY_IDS["client"], name="Cliente Web", price=0),
        Node(category=CATEGORY_IDS["client"], name="Cliente Mobile", price=0),
        Node(category=CATEGORY_IDS["client"], name="Cliente Desktop", price=0),
        Node(category=CATEGORY_IDS["client"], name="Dispositivo IoT", price=50),
)

NODES = {
    "database": {
        "color": "#4F8EF7",
        "category_name": "Banco de dados",
        "nodes": (
            {"label": "SQL", "price": 100},
            {"label": "NoSQL", "price": 120},
            {"label": "Redis", "price": 150},
            {"label": "PostgreSQL", "price": 180},
            {"label": "MongoDB", "price": 180},
        ),
    },
    "compute": {
        "color": "#F59E0B",
        "category_name": "Processamento",
        "nodes": (
            {"label": "Servidor", "price": 100},
            {"label": "Servidor de Aplicação", "price": 150},
            {"label": "Worker", "price": 120},
            {"label": "Lambda", "price": 180},
            {"label": "Container", "price": 160},
        ),
    },
    "network": {
        "color": "#06B6D4",
        "category_name": "Rede e comunicação",
        "nodes": (
            {"label": "Balanceador de Carga", "price": 200},
            {"label": "API Gateway", "price": 180},
            {"label": "Proxy Reverso", "price": 120},
            {"label": "DNS", "price": 80},
            {"label": "CDN", "price": 250},
        ),
    },
    "messaging": {
        "color": "#8B5CF6",
        "category_name": "Mensageria",
        "nodes": (
            {"label": "Fila de Mensagens", "price": 150},
            {"label": "RabbitMQ", "price": 200},
            {"label": "Kafka", "price": 300},
            {"label": "Barramento de Eventos", "price": 220},
        ),
    },
    "storage": {
        "color": "#10B981",
        "category_name": "Armazenamento",
        "nodes": (
            {"label": "Armazenamento de Objetos", "price": 150},
            {"label": "Armazenamento de Arquivos", "price": 100},
            {"label": "Armazenamento em Bloco", "price": 180},
            {"label": "Data Lake", "price": 300},
        ),
    },
    "security": {
        "color": "#EF4444",
        "category_name": "Segurança",
        "nodes": (
            {"label": "Firewall", "price": 150},
            {"label": "Serviço de Autenticação", "price": 180},
            {"label": "Serviço de Autorização", "price": 180},
            {"label": "WAF", "price": 220},
        ),
    },
    "observability": {
        "color": "#EC4899",
        "category_name": "Observabilidade",
        "nodes": (
            {"label": "Logger", "price": 80},
            {"label": "Coletor de Métricas", "price": 120},
            {"label": "Rastreamento Distribuído", "price": 180},
            {"label": "Monitoramento", "price": 150},
        ),
    },
    "client": {
        "color": "#A3A3A3",
        "category_name": "Clientes",
        "nodes": (
            {"label": "Cliente Web", "price": 0},
            {"label": "Cliente Mobile", "price": 0},
            {"label": "Cliente Desktop", "price": 0},
            {"label": "Dispositivo IoT", "price": 50},
        ),
    },
}