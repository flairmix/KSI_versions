import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models import DatasetVersion, OKSRecord, Base
import asyncio
import uuid

DATABASE_URL = "sqlite+aiosqlite:///oks.db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

CSV_PATH = "2025_03_data/03_OKS.csv"

async def load_csv():
    async with AsyncSessionLocal() as session:
        df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8", dtype=str)
        df.dropna(subset=["Наименование"], inplace=True)
        df["Класс"] = df["Класс"].ffill()
        df["Подкласс 1"] = df["Подкласс 1"].ffill()
        df["Подкласс 2"] = df["Подкласс 2"].ffill()
        df.fillna("", inplace=True)

        version = DatasetVersion(name=f"Manual load {uuid.uuid4().hex[:8]}")
        session.add(version)
        await session.flush()

        for _, row in df.iterrows():
            record = OKSRecord(
                version_id=version.id,
                uin=row.get("УИН"),
                klass=row.get("Класс"),
                subclass_1=row.get("Подкласс 1"),
                subclass_2=row.get("Подкласс 2"),
                subclass_3=row.get("Подкласс 3"),
                type_percent=row.get("Тип (%%)"),
                name=row.get("Наименование"),
                definition=row.get("Определение"),
                source=row.get("Источник"),
                subclass_criteria=row.get("Критерии определения подклассов"),
                tech_economic_indicators=row.get("Технико-экономические показатели\n<Prp>"),
                oks_code_gge=row.get("Код соответствующего ОКС (группы ОКС) по классификатору ОКС ГГЭ"),
                oks_code_mssk=row.get("Код соответствующего ОКС по классификатору МССК"),
                oks_code_rzd=row.get("Код соответствующего ОКС по КТИМ ОАО \"РЖД\""),
                notes=row.get("Примечания"),
                synonyms=row.get("Синонимы"),
            )
            session.add(record)

        await session.commit()
        print(f"Uploaded version {version.name} with {len(df)} records")

if __name__ == "__main__":
    asyncio.run(load_csv())
