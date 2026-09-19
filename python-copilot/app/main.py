import uuid
from fastapi import FastAPI,Depends,File,Form,Header,HTTPException,UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from prometheus_client import Counter,Histogram,make_asgi_app
from .database import init_db,get_db
from .config import settings
from .documents import extract,chunks
from .rag import ingest,search
from .media import understand_image,transcribe_audio
from .memory import history,save
from .agents import answer
from .telemetry import tracer

app=FastAPI(title="Multimodal Enterprise Copilot",version="1.0.0")
app.mount("/metrics",make_asgi_app())
REQ=Counter("copilot_requests_total","Copilot requests",["mode"])
LAT=Histogram("copilot_request_seconds","Copilot request duration")

@app.on_event("startup")
async def startup():await init_db()

@app.get("/health")
async def health():return {"status":"ok"}

async def read_limited(file:UploadFile):
    data=await file.read(settings.max_upload_mb*1024*1024+1)
    if len(data)>settings.max_upload_mb*1024*1024:raise HTTPException(413,"file too large")
    return data

@app.post("/v1/knowledge")
async def knowledge(file:UploadFile=File(...),x_tenant_id:str=Header(...),
                    db:AsyncSession=Depends(get_db)):
    data=await read_limited(file)
    try:text=extract(data,file.content_type or "application/octet-stream")
    except ValueError as e:raise HTTPException(415,str(e))
    parts=chunks(text)
    if not parts:raise HTTPException(400,"document contains no extractable text")
    doc="doc-"+uuid.uuid4().hex[:12]
    await ingest(db,x_tenant_id,doc,file.filename or "upload",parts)
    return {"document_id":doc,"chunks":len(parts)}

@app.post("/v1/copilot")
async def copilot(message:str=Form(...),session_id:str|None=Form(None),
    image:UploadFile|None=File(None),audio:UploadFile|None=File(None),
    x_tenant_id:str=Header(...),db:AsyncSession=Depends(get_db)):
    sid=session_id or "sess-"+uuid.uuid4().hex[:12]
    media=[]
    if image:
        data=await read_limited(image)
        media.append("IMAGE ANALYSIS:\n"+await understand_image(data,image.content_type or "",message))
    if audio:
        data=await read_limited(audio)
        media.append("AUDIO TRANSCRIPT:\n"+await transcribe_audio(data,audio.filename or "audio.wav"))
    evidence=await search(db,x_tenant_id,message,k=5)
    hist=await history(db,x_tenant_id,sid)
    with tracer.start_as_current_span("copilot.turn") as span:
        span.set_attribute("tenant.id",x_tenant_id)
        span.set_attribute("copilot.has_image",bool(image))
        span.set_attribute("copilot.has_audio",bool(audio))
        result=await answer(message,evidence,"\n\n".join(media),hist,settings.java_mcp_url,x_tenant_id)
    await save(db,x_tenant_id,sid,"user",message)
    await save(db,x_tenant_id,sid,"assistant",result)
    REQ.labels("multimodal" if media else "text").inc()
    return {"session_id":sid,"answer":result,"sources":[x["citation"] for x in evidence]}
