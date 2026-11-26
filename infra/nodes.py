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