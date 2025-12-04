from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .product_serializers import ProductSerializer
from .es_client import get_es_client
from .permissions import IsAuthenticatedFromJWT
from datetime import datetime
import uuid
import math

PRODUCT_INDEX = "products"

PRODUCT_MAPPING = {
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

class ProductIndexCreateView(APIView):
    permission_classes = [IsAuthenticatedFromJWT]

    def post(self, request):
        es = get_es_client()
        if es.indices.exists(index=PRODUCT_INDEX):
            return Response({"detail": "index already exists"}, status=status.HTTP_400_BAD_REQUEST)
        es.indices.create(index=PRODUCT_INDEX, body=PRODUCT_MAPPING)
        return Response({"detail": "index created"}, status=status.HTTP_201_CREATED)

class ProductIndexDeleteView(APIView):
    permission_classes = [IsAuthenticatedFromJWT]

    def delete(self, request):
        es = get_es_client()
        if not es.indices.exists(index=PRODUCT_INDEX):
            return Response({"detail": "index not found"}, status=status.HTTP_404_NOT_FOUND)
        es.indices.delete(index=PRODUCT_INDEX)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductListCreateView(APIView):
    permission_classes = [IsAuthenticatedFromJWT]

    def get(self, request):
        es = get_es_client()
        params = request.query_params
        try:
            page = int(params.get("page", 1))
        except Exception:
            page = 1
        try:
            size = int(params.get("size", 10))
        except Exception:
            size = 10
        if page < 1:
            page = 1
        if size < 1:
            size = 10

        q_text = params.get("q")
        category = params.get("category")
        in_stock = params.get("in_stock")

        must_clauses = []
        if q_text:
            must_clauses.append({
                "multi_match": {
                    "query": q_text,
                    "fields": ["name^2", "description"]
                }
            })
        if category:
            must_clauses.append({"term": {"category": category}})
        if in_stock is not None:
            val = str(in_stock).lower() in ("1", "true", "yes")
            must_clauses.append({"term": {"in_stock": val}})

        if must_clauses:
            body = {"query": {"bool": {"must": must_clauses}}}
        else:
            body = {"query": {"match_all": {}}}

        from_ = (page - 1) * size
        res = es.search(index=PRODUCT_INDEX, body=body, from_=from_, size=size, ignore_unavailable=True)
        hits = res.get("hits", {}).get("hits", [])
        total_hits = res.get("hits", {}).get("total", {}).get("value", 0)
        items = []
        for h in hits:
            src = h.get("_source", {}).copy()
            src["id"] = h.get("_id")
            items.append(src)
        total_pages = math.ceil(total_hits / size) if size > 0 else 0

        return Response({
            "items": items,
            "total": total_hits,
            "page": page,
            "size": size,
            "total_pages": total_pages
        })

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        es = get_es_client()
        new_id = str(uuid.uuid4())
        data["id"] = new_id
        data["created_at"] = datetime.utcnow().isoformat()
        es.index(index=PRODUCT_INDEX, id=new_id, document=data)
        return Response({**data, "id": new_id}, status=status.HTTP_201_CREATED)

class ProductDetailView(APIView):
    permission_classes = [IsAuthenticatedFromJWT]

    def get(self, request, pk):
        es = get_es_client()
        try:
            res = es.get(index=PRODUCT_INDEX, id=pk)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        doc = res["_source"]
        doc["id"] = pk
        return Response(doc)

    def put(self, request, pk):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        es = get_es_client()
        try:
            _ = es.get(index=PRODUCT_INDEX, id=pk)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        doc = serializer.validated_data
        doc["updated_at"] = datetime.utcnow().isoformat()
        doc["id"] = pk
        es.index(index=PRODUCT_INDEX, id=pk, document=doc)
        return Response(doc)

    def delete(self, request, pk):
        es = get_es_client()
        try:
            es.delete(index=PRODUCT_INDEX, id=pk)
        except Exception:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
