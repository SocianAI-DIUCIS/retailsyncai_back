from django.core.management.base import BaseCommand
from api.es_client import get_es_client
from api.utils import hash_password
import uuid
from datetime import datetime

class Command(BaseCommand):
    help = "Seed Elasticsearch with sample data"

    def handle(self, *args, **options):
        es = get_es_client()
        # seed admin user
        user_id = str(uuid.uuid4())
        es.index(index="users", id=user_id, document={
            "id": user_id,
            "username": "admin",
            "email": "admin@example.com",
            "password": hash_password("password123"),
            "created_at": datetime.utcnow().isoformat()
        })
        self.stdout.write(self.style.SUCCESS("Seeded user admin/password123"))

        # sample article
        article_id = str(uuid.uuid4())
        es.index(index="articles", id=article_id, document={
            "title": "Welcome",
            "content": "This is the first seeded article.",
            "author": "admin",
            "created_at": datetime.utcnow().isoformat()
        })
        self.stdout.write(self.style.SUCCESS("Seeded sample article"))

        # sample product
        product_id = str(uuid.uuid4())
        es.index(index="products", id=product_id, document={
            "id": product_id,
            "sku": "PRD-001",
            "name": "Sample Product",
            "description": "A sample product for testing.",
            "price": 19.99,
            "category": "samples",
            "in_stock": True,
            "tags": ["sample", "demo"],
            "created_at": datetime.utcnow().isoformat()
        })
        self.stdout.write(self.style.SUCCESS("Seeded sample product PRD-001"))
