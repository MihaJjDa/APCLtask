# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.DerivateWord import DerivateWord
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.DerivateGroup import DerivateGroup
from pullenti.morph.internal.MorphSerializeHelper import MorphSerializeHelper
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.internal.ByteArrayWrapper import ByteArrayWrapper
from pullenti.morph.internal.ExplanTreeNode import ExplanTreeNode

class DeserializeHelper:
    
    @staticmethod
    def deserializeDD(str0_ : io.IOBase, dic : 'DerivateDictionary', lazy_load : bool) -> 'ByteArrayWrapper':
        wr = None
        with io.BytesIO() as tmp: 
            MorphSerializeHelper.deflateGzip(str0_, tmp)
            wr = ByteArrayWrapper(bytearray(tmp.getvalue()))
            cou = wr.deserializeInt()
            while cou > 0: 
                p1 = wr.deserializeInt()
                ew = DerivateGroup()
                if (lazy_load): 
                    ew._lazy_pos = wr.position
                    wr.seek(p1)
                else: 
                    DeserializeHelper.deserializeDerivateGroup(wr, ew)
                dic._m_all_groups.append(ew)
                cou -= 1
            dic._m_root = ExplanTreeNode()
            DeserializeHelper.deserializeTreeNode(wr, dic, dic._m_root, lazy_load)
        return wr
    
    @staticmethod
    def deserializeDerivateGroup(str0_ : 'ByteArrayWrapper', dg : 'DerivateGroup') -> None:
        attr = str0_.deserializeShort()
        if (((attr & 1)) != 0): 
            dg.is_dummy = True
        if (((attr & 2)) != 0): 
            dg.not_generate = True
        if (((attr & 4)) != 0): 
            dg.m_transitive = 0
        if (((attr & 8)) != 0): 
            dg.m_transitive = 1
        dg.prefix = str0_.deserializeString()
        cou = str0_.deserializeShort()
        while cou > 0: 
            w = DerivateWord(dg)
            w.spelling = str0_.deserializeString()
            w.class0_ = MorphClass()
            w.class0_.value = (str0_.deserializeShort())
            w.lang = MorphLang._new5(str0_.deserializeShort())
            w.attrs.value = (str0_.deserializeShort())
            dg.words.append(w)
            cou -= 1
        cou = str0_.deserializeShort()
        while cou > 0: 
            pref = Utils.ifNotNull(str0_.deserializeString(), "")
            cas = MorphCase()
            cas.value = (str0_.deserializeShort())
            if (dg.nexts is None): 
                dg.nexts = dict()
            dg.nexts[pref] = cas
            cou -= 1
    
    @staticmethod
    def deserializeTreeNode(str0_ : 'ByteArrayWrapper', dic : 'DerivateDictionary', tn : 'ExplanTreeNode', lazy_load : bool) -> None:
        cou = str0_.deserializeShort()
        li = (list() if cou > 1 else None)
        while cou > 0: 
            id0_ = str0_.deserializeInt()
            if (id0_ > 0 and id0_ <= len(dic._m_all_groups)): 
                gr = dic._m_all_groups[id0_ - 1]
                if (gr._lazy_pos > 0): 
                    p0 = str0_.position
                    str0_.seek(gr._lazy_pos)
                    DeserializeHelper.deserializeDerivateGroup(str0_, gr)
                    gr._lazy_pos = 0
                    str0_.seek(p0)
                if (li is not None): 
                    li.append(gr)
                else: 
                    tn.groups = (gr)
            cou -= 1
        if (li is not None): 
            tn.groups = (li)
        cou = str0_.deserializeShort()
        if (cou == 0): 
            return
        while cou > 0: 
            ke = str0_.deserializeShort()
            p1 = str0_.deserializeInt()
            tn1 = ExplanTreeNode()
            if (tn.nodes is None): 
                tn.nodes = dict()
            if (not ke in tn.nodes): 
                tn.nodes[ke] = tn1
            if (lazy_load): 
                tn1.lazy_pos = str0_.position
                str0_.seek(p1)
            else: 
                DeserializeHelper.deserializeTreeNode(str0_, dic, tn1, False)
            cou -= 1