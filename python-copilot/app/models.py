from datetime import datetime
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Text,DateTime,Integer
from pgvector.sqlalchemy import Vector
from .database import Base
class KnowledgeChunk(Base):
    __tablename__="knowledge_chunks"
    id:Mapped[str]=mapped_column(String(100),primary_key=True)
    tenant_id:Mapped[str]=mapped_column(String(100),index=True)
    document_id:Mapped[str]=mapped_column(String(100),index=True)
    source_name:Mapped[str]=mapped_column(String(300))
    chunk_index:Mapped[int]=mapped_column(Integer)
    content:Mapped[str]=mapped_column(Text)
    embedding:Mapped[list]=mapped_column(Vector(1536))
class ConversationMessage(Base):
    __tablename__="conversation_messages"
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    tenant_id:Mapped[str]=mapped_column(String(100),index=True)
    session_id:Mapped[str]=mapped_column(String(100),index=True)
    role:Mapped[str]=mapped_column(String(20))
    content:Mapped[str]=mapped_column(Text)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
