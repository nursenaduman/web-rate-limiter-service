import logging
import sys
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from app.rate_limiter import rate_limit_dependency

# --- LOGGING AYARLARI  ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("server.log"), # Dosyaya yaz
        logging.StreamHandler(sys.stdout)  # Ekrana yaz
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Rate Limiter Service",
    description="Simple IP-based rate limiting service for web applications",
    version="1.0.0"
)

# Hata Yönetimi 
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Beklenmeyen Hata: {exc} - IP: {request.client.host}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "details": str(exc)},
    )

@app.get("/")
def root(request: Request):
    # Log örneği
    logger.info(f"Root erişimi - IP: {request.client.host}")
    return {"message": "Rate Limiter Service is running"}

@app.get("/limited-endpoint", dependencies=[Depends(rate_limit_dependency)])
def limited_endpoint(request: Request):
    logger.info(f"✅ Başarılı Erişim - IP: {request.client.host}")
    return {
        "status": "success",
        "message": "You have access to this endpoint"
    }