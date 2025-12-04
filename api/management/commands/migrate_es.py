from django.core.management.base import BaseCommand
from api.es_client import get_es_client

USER_INDEX = "users"
ARTICLE_INDEX = "articles"
PRODUCT_INDEX = "products"

user_mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "username": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "email": {"type": "keyword"},
            "password": {"type": "keyword"},
            "created_at": {"type": "date"}
        }
    }
}

article_mapping = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "content": {"type": "text"},
            "author": {"type": "keyword"},
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"}
        }
    }
}

product_mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "sku": {"type": "keyword"},
            "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "description": {"type": "text"},
            "price": {"type": "double"},
            "category": {"type": "keyword"},
            "in_stock": {"type": "boolean"},
            "tags": {"type": "keyword"},
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"}
        }
    }
}

class Command(BaseCommand):
    help = "Create indices with mappings in Elasticsearch (users, articles, products)"

    def handle(self, *args, **options):
        es = get_es_client()
        if not es.indices.exists(index=USER_INDEX):
            es.indices.create(index=USER_INDEX, body=user_mapping)
            self.stdout.write(self.style.SUCCESS(f"Created index {USER_INDEX}"))
        else:
            self.stdout.write(f"{USER_INDEX} already exists")
        if not es.indices.exists(index=ARTICLE_INDEX):
            es.indices.create(index=ARTICLE_INDEX, body=article_mapping)
            self.stdout.write(self.style.SUCCESS(f"Created index {ARTICLE_INDEX}"))
        else:
            self.stdout.write(f"{ARTICLE_INDEX} already exists")
        if not es.indices.exists(index=PRODUCT_INDEX):
            es.indices.create(index=PRODUCT_INDEX, body=product_mapping)
            self.stdout.write(self.style.SUCCESS(f"Created index {PRODUCT_INDEX}"))
        else:
            self.stdout.write(f"{PRODUCT_INDEX} already exists")
