from fastapi import FastAPI, File, HTTPException, status, Depends
from PIL import Image, ImageOps
from fastapi.responses import StreamingResponse
import io
from miller import isPrime
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import secrets
from datetime import datetime

app = FastAPI()

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"jakub"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"&AxO96k0%"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return current_username_bytes


@app.get("/current_time")
async def current_time(username: str = Depends(get_current_username)):
    now = datetime.now()
    corrected_date = now.strftime("%A: %H:%M:%S")
    return corrected_date




@app.get("/prime/{number}")
async def Prime(number):
    if number.isnumeric() and len(number) < 20:
        number = int(number)
        if number == 0 or number == 1:
            return False
        elif number == 2:
            return True
        wynik = isPrime(number)
        return wynik
    else:
        return {"Podana wartość nie jest liczbą naturalną"}


@app.post("/picture/invert")
async def InvertPicture(file: bytes = File()):
    picture = Image.open(io.BytesIO(file))
    inverted_image = ImageOps.invert(picture)
    responseimage = io.BytesIO()
    inverted_image.save(responseimage, "JPEG")
    responseimage.seek(0)
    return StreamingResponse(responseimage, media_type="image/jpeg")



