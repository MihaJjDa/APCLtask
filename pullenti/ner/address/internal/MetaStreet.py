﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.


from pullenti.ner.ReferentClass import ReferentClass

class MetaStreet(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.address.StreetReferent import StreetReferent
        MetaStreet._global_meta = MetaStreet()
        MetaStreet._global_meta.addFeature(StreetReferent.ATTR_TYP, "Тип", 0, 0)
        MetaStreet._global_meta.addFeature(StreetReferent.ATTR_NAME, "Наименование", 1, 0)
        MetaStreet._global_meta.addFeature(StreetReferent.ATTR_NUMBER, "Номер", 0, 1)
        MetaStreet._global_meta.addFeature(StreetReferent.ATTR_SECNUMBER, "Доп.номер", 0, 1)
        MetaStreet._global_meta.addFeature(StreetReferent.ATTR_GEO, "Географический объект", 0, 1)
        MetaStreet._global_meta.addFeature(StreetReferent.ATTR_FIAS, "Объект ФИАС", 0, 1)
        MetaStreet._global_meta.addFeature(StreetReferent.ATTR_BTI, "Объект БТИ", 0, 1)
        MetaStreet._global_meta.addFeature(StreetReferent.ATTR_OKM, "Код ОКМ УМ", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.address.StreetReferent import StreetReferent
        return StreetReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Улица"
    
    IMAGE_ID = "street"
    
    def getImageId(self, obj : 'Referent'=None) -> str:
        return MetaStreet.IMAGE_ID
    
    _global_meta = None