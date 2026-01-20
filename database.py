from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# 1. Veritabanı Bağlantı Adresi (Connection String)
# postgresql+asyncpg: Postgres kullanacağımızı ve asenkron (asyncpg) sürücüsünü kullanacağımızı belirtir.
# postgres:123456: Kullanıcı adı ve şifre.
# @localhost/postgres: Kendi bilgisayarındaki 'postgres' isimli veritabanına bağlanır.
DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost/postgres"

# 2. Asenkron Motorun (Engine) Oluşturulması
# create_async_engine: Veritabanı ile Python arasındaki ana boru hattını döşer.
# echo=True: Arka planda çalışan tüm SQL sorgularını terminale yazar.
engine = create_async_engine(DATABASE_URL, echo=True)

# 3. Oturum Fabrikası (SessionMaker)
# async_sessionmaker: Veritabanında işlem yapacağımız her seferinde bize yeni bir 'oturum' (session) verir.
# bind=engine: Bu fabrikaya hangi motoru kullanacağını söyler.
# expire_on_commit=False: Veri kaydedildikten sonra nesnelerin 'bayatlamasını' önler (Asenkron yapıda şarttır).
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# 4. Temel Sınıf (Base Class)
# Modellerimizin (User, Item) veritabanı tablosu olduğunu SQLAlchemy'ye bu sınıf üzerinden anlatacağız.
class Base(DeclarativeBase):
    pass

# 5. Veritabanı Bağımlılığı (Dependency Injection)
# get_db: FastAPI'de her API isteği geldiğinde bu fonksiyon çalışır.
# async with: Oturumu güvenli bir şekilde açar.
# yield: Oturumu API fonksiyonuna ödünç verir, işlem bitince otomatik olarak kapatır (Bellek temizliği için kritik).
async def get_db():
    async with SessionLocal() as session:
        yield session

