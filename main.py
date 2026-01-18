from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import engine, Base, get_db
from typing import List # List'i buraya eklemeyi unutma, yoksa hata alırsın!
import models
import schemas

# FastAPI uygulamasını başlatıyoruz
app = FastAPI(title="Remote Inventory Manager")

# Uygulama ayağa kalkarken (startup) çalışacak olan sihirli fonksiyon
@app.on_event("startup")
async def startup():
    # Veritabanı motoru üzerinden bir bağlantı açıyoruz
    async with engine.begin() as conn:
        # Modellerdeki tablolar Postgres'te yoksa onları otomatik oluşturur
        await conn.run_sync(models.Base.metadata.create_all)

# Giriş sayfamız (Sistemin çalışıp çalışmadığını anlamak için)
@app.get("/")
async def root():
    return {"status": "Sistem aktif", "hedef": "Polonya"}

# 1. KULLANICI OLUŞTURMA (POST)
@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    # SORGULAMA: Aynı kullanıcı adıyla başka biri var mı?
    # select(models.User) -> "User tablosundan seç" demek
    query = select(models.User).filter(models.User.username == user.username)
    result = await db.execute(query) # Sorguyu çalıştır
    db_user_check = result.scalar_one_or_none() # Sonuç varsa al, yoksa None dön
    
    if db_user_check:
        # Eğer varsa hata fırlat (400 Bad Request)
        raise HTTPException(status_code=400, detail="Bu kullanici adi zaten alinmis kocum!")

    # Yeni kullanıcı nesnesini schemas'tan gelen verilerle oluşturalım
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=user.password  # NOT: Gerçek projede şifre mutlaka 'bcrypt' ile hashlenmeli!
    )
    
    db.add(new_user) # Hafızaya ekle
    await db.commit() # Veritabanına kalıcı olarak yaz (Mühürle)
    await db.refresh(new_user) # Veritabanından gelen ID gibi bilgileri nesneye geri yükle
    return new_user

# 2. TÜM KULLANICILARI LİSTELE (GET)
@app.get("/users", response_model=List[schemas.User])
async def read_users(db: AsyncSession = Depends(get_db)):
    query = select(models.User) # Tüm kullanıcıları seç
    result = await db.execute(query) # Çalıştır
    users = result.scalars().all() # Tüm sonuçları bir liste olarak al
    return users

# 3. TEK BİR KULLANICIYI GETİR (GET)
@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    # Kullanıcıyı ID üzerinden bulmaya çalışan sorgu
    query = select(models.User).filter(models.User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        # Eğer kullanıcı bulunamazsa 404 dön
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi kocum!")
    
    return user
