from sqlalchemy import select
from .models import ConversationMessage
async def history(db,tenant,session,limit=12):
    q=(select(ConversationMessage).where(
      ConversationMessage.tenant_id==tenant,ConversationMessage.session_id==session)
      .order_by(ConversationMessage.id.desc()).limit(limit))
    rows=list(reversed((await db.scalars(q)).all()))
    return [{"role":x.role,"content":x.content} for x in rows]
async def save(db,tenant,session,role,content):
    db.add(ConversationMessage(tenant_id=tenant,session_id=session,role=role,content=content))
    await db.commit()
