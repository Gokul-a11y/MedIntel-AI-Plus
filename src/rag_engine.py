import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="medical_reports"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_rag_index(report_text):

    try:
        existing = collection.get()

        if existing["ids"]:
            collection.delete(
                ids=existing["ids"]
            )
    except:
        pass

    chunks = []

    chunk_size = 500
    overlap = 100

    for i in range(
        0,
        len(report_text),
        chunk_size - overlap
    ):

        chunk = report_text[
            i:i + chunk_size
        ]

        chunks.append(chunk)

    embeddings = model.encode(
        chunks
    ).tolist()

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[
            f"chunk_{i}"
            for i in range(len(chunks))
        ]
    )

    return len(chunks)


def retrieve_context(query):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    return context