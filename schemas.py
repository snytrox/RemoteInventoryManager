from pydantic import BaseModel, EmailStr
from typing import Optional, List


# ItemBase: Bir eşya için ortak olan temel alanlar.
class ItemBase(BaseModel):
    name: str
    serial_number: str
    category: str

class ItemCreate(ItemBase):
    owner_id: Optional[int] = None # Eşyayı eklerken birine atamak zorunda değiliz.

# Item: API'den dışarıya (kullanıcıya) gönderilen eşya verisi.
class Item(ItemBase):
    id: int
    status: str 
    
    class Config:
        # SQLAlchemy nesnelerini otomatik olarak Pydantic'e çevirmek için şarttır.
        from_attributes = True


# UserBase: Kullanıcının temel bilgileri.
class UserBase(BaseModel):
    username: str
    email: EmailStr # Email formatında olup olmadığını otomatik kontrol eder.

# UserCreate: Kayıt olurken (Register) kullanılan şema.
class UserCreate(UserBase):
    password: str # Kullanıcıdan şifreyi alırız ama dışarıya asla geri göndermeyiz.

# User: API'den dışarıya gönderilen kullanıcı verisi (Profil bilgisi gibi).
class User(UserBase):
    id: int
    is_admin: bool
    items: List[Item] = [] # Kullanıcının üzerine zimmetli eşyaları da liste olarak döneriz.
    
    class Config:
        from_attributes = True

