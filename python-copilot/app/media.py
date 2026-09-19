import base64
from openai import AsyncOpenAI
from .config import settings
client=AsyncOpenAI(api_key=settings.openai_api_key)
IMAGE_TYPES={"image/png","image/jpeg","image/webp","image/gif"}
async def understand_image(data:bytes,mime:str,question:str)->str:
    if mime not in IMAGE_TYPES:raise ValueError("unsupported image type")
    encoded=base64.b64encode(data).decode()
    r=await client.responses.create(model=settings.vision_model,input=[{
      "role":"user","content":[
        {"type":"input_text","text":question or "Describe this image for an enterprise copilot."},
        {"type":"input_image","image_url":f"data:{mime};base64,{encoded}"}
      ]}])
    return r.output_text
async def transcribe_audio(data:bytes,filename:str)->str:
    # Provider adapter isolated here so deployments can substitute their approved speech model/service.
    import tempfile,os
    suffix=os.path.splitext(filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix) as f:
        f.write(data);f.flush()
        with open(f.name,"rb") as audio:
            r=await client.audio.transcriptions.create(model="gpt-4o-transcribe",file=audio)
    return r.text
