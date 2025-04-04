from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OKS(Base):
    __tablename__ = "oks"

    uin = Column("УИН", String, primary_key=True)
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

    def __repr__(self):
        return f"<OKS(name='{self.name}', uin='{self.uin}')>"