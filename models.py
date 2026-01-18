from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from typing import List, Optional

# Tüm tabloların ortak atası. Veritabanı tablolarını bu sınıftan türeteceğiz.
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users" # Veritabanındaki tablonun fiziksel adı
    
    # id: Her kullanıcının benzersiz numarası. index=True aramalarda hız sağlar.
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # unique=True: Aynı kullanıcı adı veya email ile iki kişi kayıt olamaz.
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    
    # Şifreyi asla açık yazmıyoruz, hash'lenmiş (karıştırılmış) halini tutuyoruz.
    hashed_password: Mapped[str] = mapped_column()
    
    # default=False: Yeni her üye önce 'standart kullanıcı' olur, admin yetkisini biz veririz.
    is_admin: Mapped[bool] = mapped_column(default=False)
    
    # İLİŞKİ: Bu kullanıcıya ait olan tüm eşyaların listesi.
    # back_populates: Item tablosundaki 'owner' değişkeniyle bu alanı birbirine bağlar.
    items: Mapped[List["Item"]] = relationship(back_populates="owner")

class Item(Base):
    __tablename__ = "items" # Veritabanındaki eşya tablosu adı
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Eşyanın adı (Örn: MacBook Pro, Samsung Monitör)
    name: Mapped[str] = mapped_column()
    
    # serial_number: Harf içerebileceği için 'str' yaptık. Her cihazın seri nosu tektir.
    serial_number: Mapped[str] = mapped_column(unique=True)
    
    # category: Laptop mu, kulaklık mı, telefon mu?
    category: Mapped[str] = mapped_column()
    
    # default="available": Yeni eklenen cihaz ilk başta 'müsait/boşta' olarak işaretlenir.
    # available: Boşta, assigned: Zimmetli, broken: Arızalı gibi durumlar için.
    status: Mapped[str] = mapped_column(default="available")
    
    # owner_id: Bu cihazın kime ait olduğunu tutan yabancı anahtar (Foreign Key).
    # Optional[int]: Cihaz henüz kimseye verilmemiş olabilir (sahibi null olabilir).
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    
    # İLİŞKİ: Bu eşyadan, sahibinin bilgilerine (User objesine) hızlıca ulaşmamızı sağlar.
    owner: Mapped[Optional["User"]] = relationship(back_populates="items")

