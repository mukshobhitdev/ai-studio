import os
from azure.search.documents import SearchClient, SearchApiKeyCredential
from azure.ai.embeddings import OpenAIEmbeddings

class SearchIndexer:
    def __init__(self):
        endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        key = os.getenv("AZURE_SEARCH_KEY")
        self.index_client = SearchClient(endpoint, index_name="pdf-index", credential=SearchApiKeyCredential(key))
        self.embedder = OpenAIEmbeddings(deployment=os.getenv("AZURE_OPENAI_EMBED_MODEL"))

    def index_doc(self, doc_id: str, text: str):
        embedding = self.embedder.embed_query(text)
        return self.index_client.upload_documents(documents=[{"id": doc_id, "text": text, "embedding": embedding}])
