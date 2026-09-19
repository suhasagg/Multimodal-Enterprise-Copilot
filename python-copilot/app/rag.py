import uuid
from sqlalchemy import select
from openai import AsyncOpenAI
from .config import settings
from .models import KnowledgeChunk
client=AsyncOpenAI(api_key=settings.openai_api_key)
async def embed(texts):
    r=await client.embeddings.create(model=settings.embedding_model,input=texts)
    return [x.embedding for x in r.data]
async def ingest(db,tenant,doc_id,name,parts):
    vectors=await embed(parts)
    for i,(text,vec) in enumerate(zip(parts,vectors)):
        db.add(KnowledgeChunk(id=f"{doc_id}:{i}",tenant_id=tenant,document_id=doc_id,
          source_name=name,chunk_index=i,content=text,embedding=vec))
    await db.commit()
async def search(db,tenant,query,k=5):
    qvec=(await embed([query]))[0]
    stmt=(select(KnowledgeChunk)
      .where(KnowledgeChunk.tenant_id==tenant)
      .order_by(KnowledgeChunk.embedding.cosine_distance(qvec)).limit(k))
    rows=(await db.scalars(stmt)).all()
    return [{"citation":f"{r.source_name}#chunk-{r.chunk_index}","content":r.content} for r in rows]
