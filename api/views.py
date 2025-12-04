from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, ArticleSerializer
from .es_client import get_es_client
from .utils import hash_password, verify_password, create_token_pair_for_user
from .permissions import IsAuthenticatedFromJWT
from datetime import datetime
import uuid

USER_INDEX = "users"
ARTICLE_INDEX = "articles"

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        es = get_es_client()
        username = serializer.validated_data["username"]
        q = {"query": {"term": {"username.keyword": username}}}
        res = es.search(index=USER_INDEX, body=q, size=1, ignore_unavailable=True)
        if res.get("hits", {}).get("total", {}).get("value", 0) > 0:
            return Response({"detail": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user_id = str(uuid.uuid4())
        hashed = hash_password(serializer.validated_data["password"])
        doc = {
            "id": user_id,
            "username": username,
            "email": serializer.validated_data["email"],
            "password": hashed,
            "created_at": datetime.utcnow().isoformat(),
        }
        es.index(index=USER_INDEX, id=user_id, document=doc)
        return Response({"id": user_id, "username": username, "email": doc["email"]}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        es = get_es_client()
        username = serializer.validated_data["username"]
        q = {"query": {"term": {"username.keyword": username}}}
        res = es.search(index=USER_INDEX, body=q, size=1, ignore_unavailable=True)
        hits = res.get("hits", {}).get("hits", [])
        if not hits:
            return Response({"detail": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        user_doc = hits[0]["_source"]
        if not verify_password(user_doc["password"], serializer.validated_data["password"]):
            return Response({"detail": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        tokens = create_token_pair_for_user(user_doc["id"], user_doc["username"])
        return Response(tokens)

class ArticleListCreateView(APIView):
    permission_classes = [IsAuthenticatedFromJWT]

    def get(self, request):
        es = get_es_client()
        q = {"query": {"match_all": {}}}
        res = es.search(index=ARTICLE_INDEX, body=q, size=100, ignore_unavailable=True)
        items = [ {**h["_source"], "id": h["_id"]} for h in res.get("hits", {}).get("hits", []) ]
        return Response(items)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        es = get_es_client()
        doc = serializer.validated_data
        doc["author"] = getattr(request, "user_payload", {}).get("username", "unknown")
        doc["created_at"] = datetime.utcnow().isoformat()
        new_id = str(uuid.uuid4())
        es.index(index=ARTICLE_INDEX, id=new_id, document=doc)
        doc["id"] = new_id
        return Response(doc, status=status.HTTP_201_CREATED)

class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticatedFromJWT]

    def get(self, request, pk):
        es = get_es_client()
        try:
            res = es.get(index=ARTICLE_INDEX, id=pk)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        doc = res["_source"]
        doc["id"] = pk
        return Response(doc)

    def put(self, request, pk):
        serializer = ArticleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        es = get_es_client()
        try:
            doc = serializer.validated_data
            doc["updated_at"] = datetime.utcnow().isoformat()
            es.index(index=ARTICLE_INDEX, id=pk, document=doc)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        doc["id"] = pk
        return Response(doc)

    def delete(self, request, pk):
        es = get_es_client()
        try:
            es.delete(index=ARTICLE_INDEX, id=pk)
        except Exception:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
