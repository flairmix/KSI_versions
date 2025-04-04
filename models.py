from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DatasetVersion(Base):
    __tablename__ = "dataset_versions"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now())
    description = Column(Text, nullable=True)

    oks_records = relationship("OKSRecord", back_populates="version", cascade="all, delete")

class OKSRecord(Base):
    __tablename__ = "oks_records"

    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, ForeignKey("dataset_versions.id"))
    uin = Column("УИН", String)
    klass = Column("Класс", String)
    subclass_1 = Column("Подкласс 1", String)
    subclass_2 = Column("Подкласс 2", String)
    subclass_3 = Column("Подкласс 3", String)
    type_percent = Column("Тип (%%)", String)
    name = Column("Наименование", String)
    definition = Column("Определение", Text)
    source = Column("Источник", Text)
    subclass_criteria = Column("Критерии определения подклассов", Text)
    tech_economic_indicators = Column("Технико-экономические показатели\n<Prp>", Text)
    oks_code_gge = Column("Код соответствующего ОКС (группы ОКС) по классификатору ОКС ГГЭ", String)
    oks_code_mssk = Column("Код соответствующего ОКС по классификатору МССК", String)
    oks_code_rzd = Column("Код соответствующего ОКС по КТИМ ОАО \"РЖД\"", String)
    notes = Column("Примечания", Text)
    synonyms = Column("Синонимы", Text)

    version = relationship("DatasetVersion", back_populates="oks_records")
