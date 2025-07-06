from fastapi import FastAPI, UploadFile, File, HTTPException,Request
from uuid import uuid4
import os
import shutil
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import logging
import asyncio


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger=logging.getLogger(__name__)

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR= "/app/uploads"

os.makedirs(UPLOAD_DIR,exist_ok=True)

@app.get("/status")
def check_status():
    return {"status":"It is running"}


## file upload based on uuid 

MAX_FILE_SIZE=10*1024*1024
RATE_LIMIT_SECONDS=5
ip_last_upload_time={}
FILE_TTL_SECONDS=24*60*60


@app.post("/api/v1/upload")
async def upload_file(request:Request,file: UploadFile = File(...)):
    ## upload a file
    ## return a uuid 
    client_ip=request.client.host
    now=time.time()

    # Rate Limiting
    last_time=ip_last_upload_time.get(client_ip,0)
    if now-last_time < RATE_LIMIT_SECONDS:
        logger.error("Failed to upload file",exc_info=True)
        raise HTTPException(status_code=429,detail="Too many requests.Slow Down.")

    # Sized Limit
    contents=await file.read()
    if len(contents) > MAX_FILE_SIZE:
        logger.error("Failed to upload file",exc_info=True)
        raise HTTPException(status_code=413,detail="File too large (limit 10 MB)")

    try:
        file_uuid=str(uuid4())
        _,ext=os.path.splitext(file.filename)
        filename=f"{file_uuid}{ext}"
        file_path=os.path.join(UPLOAD_DIR,filename)
         
        with open(file_path,"wb") as buffer:
            buffer.write(contents)
        
        logger.info(f"File {filename} uploaded by {client_ip}")
        ip_last_upload_time[client_ip]=now
        return {"file_uuid":file_uuid}    
    
    except Exception as e:
        logger.error("Failed to upload file",exc_info=True)
        raise HTTPException(status_code=500,detail=f"Upload failed: {e}")


@app.get("/api/v1/download/{uuid}")
async def download_file(uuid:str):
    try:
       for filename in os.listdir(UPLOAD_DIR):
         if filename.startswith(uuid):
            file_path=os.path.join(UPLOAD_DIR,filename)
            logger.info(f"File {filename} downloaded")
            return FileResponse(file_path,filename=filename)

    except Exception as e:
        logger.error("Failed to downlaod file",exc_info=True)
        raise HTTPException(status_code=500,detail=f"Download failed: {e}")



async def storage_cleanup():
    while True:
        now=time.time()
        for filename in os.listdir(UPLOAD_DIR):
            path=os.path.join(UPLOAD_DIR,filename)
            if os.path.isfile(path):
                if now-os.path.getmtime(path)>FILE_TTL_SECONDS:
                    os.remove(path)
        await asyncio.sleep(3600)        


@app.on_event("startup")
async def startup_event():
     asyncio.create_task(storage_cleanup())