import io
from pypdf import PdfReader
ALLOWED={"application/pdf","text/plain","text/markdown"}
def extract(data:bytes,content_type:str)->str:
    if content_type not in ALLOWED:raise ValueError("unsupported document type")
    if content_type=="application/pdf":
        reader=PdfReader(io.BytesIO(data))
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    return data.decode("utf-8",errors="replace")
def chunks(text:str,size=1200,overlap=180):
    text=" ".join(text.split())
    if not text:return []
    out=[];i=0
    while i<len(text):
        out.append(text[i:i+size]);i+=max(1,size-overlap)
    return out
