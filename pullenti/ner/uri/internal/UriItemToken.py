﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.Termin import Termin

class UriItemToken(MetaToken):
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.value = None;
    
    @staticmethod
    def attachUriContent(t0 : 'Token', after_http : bool) -> 'UriItemToken':
        res = UriItemToken.__AttachUriContent(t0, ".;:-_=+&%#@/\\?[]()!~", after_http)
        if (res is None): 
            return None
        if (res.end_token.isCharOf(".;-:") and res.end_char > 3): 
            res.end_token = res.end_token.previous
            res.value = res.value[0:0+len(res.value) - 1]
        if (res.value.endswith("/")): 
            res.value = res.value[0:0+len(res.value) - 1]
        if (res.value.endswith("\\")): 
            res.value = res.value[0:0+len(res.value) - 1]
        return res
    
    @staticmethod
    def attachISOContent(t0 : 'Token', spec_chars : str) -> 'UriItemToken':
        t = t0
        while True:
            if (t is None): 
                return None
            if (t.isCharOf(":/\\") or t.is_hiphen or t.isValue("IEC", None)): 
                t = t.next0_
                continue
            break
        if (not ((isinstance(t, NumberToken)))): 
            return None
        t1 = t
        delim = chr(0)
        txt = io.StringIO()
        first_pass3140 = True
        while True:
            if first_pass3140: first_pass3140 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_whitespace_before and t != t1): 
                break
            if (isinstance(t, NumberToken)): 
                if (delim != (chr(0))): 
                    print(delim, end="", file=txt)
                delim = (chr(0))
                t1 = t
                print(t.getSourceText(), end="", file=txt)
                continue
            if (not ((isinstance(t, TextToken)))): 
                break
            if (not t.isCharOf(spec_chars)): 
                break
            delim = t.getSourceText()[0]
        if (txt.tell() == 0): 
            return None
        return UriItemToken._new2550(t0, t1, Utils.toStringStringIO(txt))
    
    @staticmethod
    def __AttachUriContent(t0 : 'Token', chars_ : str, can_be_whitespaces : bool=False) -> 'UriItemToken':
        txt = io.StringIO()
        t1 = t0
        dom = UriItemToken.attachDomainName(t0, True, can_be_whitespaces)
        if (dom is not None): 
            if (len(dom.value) < 3): 
                return None
        open_char = chr(0)
        t = t0
        if (dom is not None): 
            t = dom.end_token.next0_
        first_pass3141 = True
        while True:
            if first_pass3141: first_pass3141 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t != t0 and t.is_whitespace_before): 
                if (t.is_newline_before or not can_be_whitespaces): 
                    break
                if (dom is None): 
                    break
                if (t.previous.is_hiphen): 
                    pass
                elif (t.previous.isCharOf(",;")): 
                    break
                elif (t.previous.isChar('.') and t.chars.is_letter and t.length_char == 2): 
                    pass
                else: 
                    ok = False
                    tt1 = t
                    if (t.isCharOf("\\/")): 
                        tt1 = t.next0_
                    tt0 = tt1
                    first_pass3142 = True
                    while True:
                        if first_pass3142: first_pass3142 = False
                        else: tt1 = tt1.next0_
                        if (not (tt1 is not None)): break
                        if (tt1 != tt0 and tt1.is_whitespace_before): 
                            break
                        if (isinstance(tt1, NumberToken)): 
                            continue
                        if (not ((isinstance(tt1, TextToken)))): 
                            break
                        term1 = (tt1).term
                        if (((term1 == "HTM" or term1 == "HTML" or term1 == "SHTML") or term1 == "ASP" or term1 == "ASPX") or term1 == "JSP"): 
                            ok = True
                            break
                        if (not tt1.chars.is_letter): 
                            if (tt1.isCharOf("\\/")): 
                                ok = True
                                break
                            if (not tt1.isCharOf(chars_)): 
                                break
                        elif (not tt1.chars.is_latin_letter): 
                            break
                    if (not ok): 
                        break
            if (isinstance(t, NumberToken)): 
                nt = Utils.asObjectOrNull(t, NumberToken)
                print(nt.getSourceText(), end="", file=txt)
                t1 = t
                continue
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is None): 
                rt = Utils.asObjectOrNull(t, ReferentToken)
                if (rt is not None and rt.begin_token.isValue("РФ", None)): 
                    if (txt.tell() > 0 and Utils.getCharAtStringIO(txt, txt.tell() - 1) == '.'): 
                        print(rt.begin_token.getSourceText(), end="", file=txt)
                        t1 = t
                        continue
                if (rt is not None and rt.chars.is_latin_letter and rt.begin_token == rt.end_token): 
                    print(rt.begin_token.getSourceText(), end="", file=txt)
                    t1 = t
                    continue
                break
            src = tt.getSourceText()
            ch = src[0]
            if (not str.isalpha(ch)): 
                if (chars_.find(ch) < 0): 
                    break
                if (ch == '(' or ch == '['): 
                    open_char = ch
                elif (ch == ')'): 
                    if (open_char != '('): 
                        break
                    open_char = (chr(0))
                elif (ch == ']'): 
                    if (open_char != '['): 
                        break
                    open_char = (chr(0))
            print(src, end="", file=txt)
            t1 = t
        if (txt.tell() == 0): 
            return dom
        i = 0
        while i < txt.tell(): 
            if (str.isalnum(Utils.getCharAtStringIO(txt, i))): 
                break
            i += 1
        if (i >= txt.tell()): 
            return dom
        if (Utils.getCharAtStringIO(txt, txt.tell() - 1) == '.' or Utils.getCharAtStringIO(txt, txt.tell() - 1) == '/'): 
            Utils.setLengthStringIO(txt, txt.tell() - 1)
            t1 = t1.previous
        if (dom is not None): 
            Utils.insertStringIO(txt, 0, dom.value)
        tmp = Utils.toStringStringIO(txt)
        if (tmp.startswith("\\\\")): 
            Utils.replaceStringIO(txt, "\\\\", "//")
            tmp = Utils.toStringStringIO(txt)
        if (tmp.startswith("//")): 
            tmp = tmp[2:]
        if (Utils.compareStrings(tmp, "WWW", True) == 0): 
            return None
        res = UriItemToken._new2550(t0, t1, Utils.toStringStringIO(txt))
        return res
    
    @staticmethod
    def attachDomainName(t0 : 'Token', check_ : bool, can_be_whitspaces : bool) -> 'UriItemToken':
        txt = io.StringIO()
        t1 = t0
        ip_count = 0
        is_ip = True
        t = t0
        first_pass3143 = True
        while True:
            if first_pass3143: first_pass3143 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_whitespace_before and t != t0): 
                ok = False
                if (not t.is_newline_before and can_be_whitspaces): 
                    tt1 = t
                    first_pass3144 = True
                    while True:
                        if first_pass3144: first_pass3144 = False
                        else: tt1 = tt1.next0_
                        if (not (tt1 is not None)): break
                        if (tt1.isChar('.') or tt1.is_hiphen): 
                            continue
                        if (tt1.is_whitespace_before): 
                            if (tt1.is_newline_before): 
                                break
                            if (tt1.previous is not None and ((tt1.previous.isChar('.') or tt1.previous.is_hiphen))): 
                                pass
                            else: 
                                break
                        if (not ((isinstance(tt1, TextToken)))): 
                            break
                        if (UriItemToken.__m_std_groups.tryParse(tt1, TerminParseAttr.NO) is not None): 
                            ok = True
                            break
                        if (not tt1.chars.is_latin_letter): 
                            break
                if (not ok): 
                    break
            if (isinstance(t, NumberToken)): 
                nt = Utils.asObjectOrNull(t, NumberToken)
                if (nt.int_value is None): 
                    break
                print(nt.getSourceText(), end="", file=txt)
                t1 = t
                if (nt.typ == NumberSpellingType.DIGIT and nt.int_value >= 0 and (nt.int_value < 256)): 
                    ip_count += 1
                else: 
                    is_ip = False
                continue
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is None): 
                break
            src = (tt).term
            ch = src[0]
            if (not str.isalpha(ch)): 
                if (".-_".find(ch) < 0): 
                    break
                if (ch != '.'): 
                    is_ip = False
            else: 
                is_ip = False
            print(src.lower(), end="", file=txt)
            t1 = t
        if (txt.tell() == 0): 
            return None
        if (ip_count != 4): 
            is_ip = False
        points = 0
        i = 0
        while i < txt.tell(): 
            if (Utils.getCharAtStringIO(txt, i) == '.'): 
                if (i == 0): 
                    return None
                if (i >= (txt.tell() - 1)): 
                    Utils.setLengthStringIO(txt, txt.tell() - 1)
                    t1 = t1.previous
                    break
                if (Utils.getCharAtStringIO(txt, i - 1) == '.' or Utils.getCharAtStringIO(txt, i + 1) == '.'): 
                    return None
                points += 1
            i += 1
        if (points == 0): 
            return None
        if (check_): 
            ok = is_ip
            if (not is_ip): 
                if (Utils.toStringStringIO(txt) == "localhost"): 
                    ok = True
            if (not ok and t1.previous is not None and t1.previous.isChar('.')): 
                if (UriItemToken.__m_std_groups.tryParse(t1, TerminParseAttr.NO) is not None): 
                    ok = True
            if (not ok): 
                return None
        return UriItemToken._new2550(t0, t1, Utils.toStringStringIO(txt).lower())
    
    @staticmethod
    def attachMailUsers(t1 : 'Token') -> typing.List['UriItemToken']:
        if (t1 is None): 
            return None
        if (t1.isChar('}')): 
            res0 = UriItemToken.attachMailUsers(t1.previous)
            if (res0 is None): 
                return None
            t1 = res0[0].begin_token.previous
            first_pass3145 = True
            while True:
                if first_pass3145: first_pass3145 = False
                else: t1 = t1.previous
                if (not (t1 is not None)): break
                if (t1.isChar('{')): 
                    res0[0].begin_token = t1
                    return res0
                if (t1.isCharOf(";,")): 
                    continue
                res1 = UriItemToken.attachMailUsers(t1)
                if (res1 is None): 
                    return None
                res0.insert(0, res1[0])
                t1 = res1[0].begin_token
            return None
        txt = io.StringIO()
        t0 = t1
        t = t1
        first_pass3146 = True
        while True:
            if first_pass3146: first_pass3146 = False
            else: t = t.previous
            if (not (t is not None)): break
            if (t.is_whitespace_after): 
                break
            if (isinstance(t, NumberToken)): 
                nt = Utils.asObjectOrNull(t, NumberToken)
                Utils.insertStringIO(txt, 0, nt.getSourceText())
                t0 = t
                continue
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is None): 
                break
            src = tt.getSourceText()
            ch = src[0]
            if (not str.isalpha(ch)): 
                if (".-_".find(ch) < 0): 
                    break
            Utils.insertStringIO(txt, 0, src)
            t0 = t
        if (txt.tell() == 0): 
            return None
        res = list()
        res.append(UriItemToken._new2550(t0, t1, Utils.toStringStringIO(txt).lower()))
        return res
    
    @staticmethod
    def attachUrl(t0 : 'Token') -> 'UriItemToken':
        srv = UriItemToken.attachDomainName(t0, True, False)
        if (srv is None): 
            return None
        txt = Utils.newStringIO(srv.value)
        t1 = srv.end_token
        if (t1.next0_ is not None and t1.next0_.isChar(':') and (isinstance(t1.next0_.next0_, NumberToken))): 
            t1 = t1.next0_.next0_
            print(":{0}".format((t1).value), end="", file=txt, flush=True)
        t = t1.next0_
        while t is not None: 
            if (t.is_whitespace_before): 
                break
            if (not t.isChar('/')): 
                break
            if (t.is_whitespace_after): 
                t1 = t
                break
            dat = UriItemToken.__AttachUriContent(t.next0_, ".-_+%", False)
            if (dat is None): 
                t1 = t
                break
            t1 = dat.end_token
            t = t1
            print("/{0}".format(dat.value), end="", file=txt, flush=True)
            t = t.next0_
        if ((t1.next0_ is not None and t1.next0_.isChar('?') and not t1.next0_.is_whitespace_after) and not t1.is_whitespace_after): 
            dat = UriItemToken.__AttachUriContent(t1.next0_.next0_, ".-_+%=&", False)
            if (dat is not None): 
                t1 = dat.end_token
                print("?{0}".format(dat.value), end="", file=txt, flush=True)
        if ((t1.next0_ is not None and t1.next0_.isChar('#') and not t1.next0_.is_whitespace_after) and not t1.is_whitespace_after): 
            dat = UriItemToken.__AttachUriContent(t1.next0_.next0_, ".-_+%", False)
            if (dat is not None): 
                t1 = dat.end_token
                print("#{0}".format(dat.value), end="", file=txt, flush=True)
        i = 0
        while i < txt.tell(): 
            if (str.isalpha(Utils.getCharAtStringIO(txt, i))): 
                break
            i += 1
        if (i >= txt.tell()): 
            return None
        return UriItemToken._new2550(t0, t1, Utils.toStringStringIO(txt))
    
    @staticmethod
    def attachISBN(t0 : 'Token') -> 'UriItemToken':
        txt = io.StringIO()
        t1 = t0
        digs = 0
        t = t0
        first_pass3147 = True
        while True:
            if first_pass3147: first_pass3147 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                break
            if (t.is_newline_before and t != t0): 
                if (t.previous is not None and t.previous.is_hiphen): 
                    pass
                else: 
                    break
            if (isinstance(t, NumberToken)): 
                nt = Utils.asObjectOrNull(t, NumberToken)
                if (nt.typ != NumberSpellingType.DIGIT or not nt.morph.class0_.is_undefined): 
                    break
                d = nt.getSourceText()
                print(d, end="", file=txt)
                digs += len(d)
                t1 = t
                if (digs > 13): 
                    break
                continue
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is None): 
                break
            s = tt.term
            if (s != "-" and s != "Х" and s != "X"): 
                break
            if (s == "Х"): 
                s = "X"
            print(s, end="", file=txt)
            t1 = t
            if (s != "-"): 
                break
        dig = 0
        i = 0
        while i < txt.tell(): 
            if (str.isdigit(Utils.getCharAtStringIO(txt, i))): 
                dig += 1
            i += 1
        if (dig < 7): 
            return None
        return UriItemToken._new2550(t0, t1, Utils.toStringStringIO(txt))
    
    @staticmethod
    def attachBBK(t0 : 'Token') -> 'UriItemToken':
        txt = io.StringIO()
        t1 = t0
        digs = 0
        t = t0
        first_pass3148 = True
        while True:
            if first_pass3148: first_pass3148 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_before and t != t0): 
                break
            if (t.is_table_control_char): 
                break
            if (isinstance(t, NumberToken)): 
                nt = Utils.asObjectOrNull(t, NumberToken)
                if (nt.typ != NumberSpellingType.DIGIT or not nt.morph.class0_.is_undefined): 
                    break
                d = nt.getSourceText()
                print(d, end="", file=txt)
                digs += len(d)
                t1 = t
                continue
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt is None): 
                break
            if (tt.isChar(',')): 
                break
            if (tt.isChar('(')): 
                if (not ((isinstance(tt.next0_, NumberToken)))): 
                    break
            s = tt.getSourceText()
            if (str.isalpha(s[0])): 
                if (tt.is_whitespace_before): 
                    break
            print(s, end="", file=txt)
            t1 = t
        if ((txt.tell() < 3) or (digs < 2)): 
            return None
        if (Utils.getCharAtStringIO(txt, txt.tell() - 1) == '.'): 
            Utils.setLengthStringIO(txt, txt.tell() - 1)
            t1 = t1.previous
        return UriItemToken._new2550(t0, t1, Utils.toStringStringIO(txt))
    
    @staticmethod
    def attachSkype(t0 : 'Token') -> 'UriItemToken':
        if (t0.chars.is_cyrillic_letter): 
            return None
        res = UriItemToken.__AttachUriContent(t0, "._", False)
        if (res is None): 
            return None
        if (len(res.value) < 5): 
            return None
        return res
    
    @staticmethod
    def attachIcqContent(t0 : 'Token') -> 'UriItemToken':
        if (not ((isinstance(t0, NumberToken)))): 
            return None
        res = UriItemToken.attachISBN(t0)
        if (res is None): 
            return None
        if ("-" in res.value): 
            res.value = res.value.replace("-", "")
        for ch in res.value: 
            if (not str.isdigit(ch)): 
                return None
        if ((len(res.value) < 6) or len(res.value) > 10): 
            return None
        return res
    
    __m_std_groups = None
    
    @staticmethod
    def initialize() -> None:
        if (UriItemToken.__m_std_groups is not None): 
            return
        UriItemToken.__m_std_groups = TerminCollection()
        domain_groups = ["com;net;org;inf;biz;name;aero;arpa;edu;int;gov;mil;coop;museum;mobi;travel", "ac;ad;ae;af;ag;ai;al;am;an;ao;aq;ar;as;at;au;aw;az", "ba;bb;bd;be;bf;bg;bh;bi;bj;bm;bn;bo;br;bs;bt;bv;bw;by;bz", "ca;cc;cd;cf;cg;ch;ci;ck;cl;cm;cn;co;cr;cu;cv;cx;cy;cz", "de;dj;dk;dm;do;dz", "ec;ee;eg;eh;er;es;et;eu", "fi;fj;fk;fm;fo;fr", "ga;gd;ge;gf;gg;gh;gi;gl;gm;gn;gp;gq;gr;gs;gt;gu;gw;gy", "hk;hm;hn;hr;ht;hu", "id;ie;il;im;in;io;iq;ir;is;it", "je;jm;jo;jp", "ke;kg;kh;ki;km;kn;kp;kr;kw;ky;kz", "la;lb;lc;li;lk;lr;ls;lt;lu;lv;ly", "ma;mc;md;mg;mh;mk;ml;mm;mn;mo;mp;mq;mr;ms;mt;mu;mv;mw;mx;my;mz", "na;nc;ne;nf;ng;ni;nl;no;np;nr;nu;nz", "om", "pa;pe;pf;pg;ph;pk;pl;pm;pn;pr;ps;pt;pw;py", "qa", "re;ro;ru;rw", "sa;sb;sc;sd;se;sg;sh;si;sj;sk;sl;sm;sn;so;sr;st;su;sv;sy;sz", "tc;td;tf;tg;th;tj;tk;tm;tn;to;tp;tr;tt;tv;tw;tz", "ua;ug;uk;um;us;uy;uz", "va;vc;ve;vg;vi;vn;vu", "wf;ws", "ye;yt;yu", "za;zm;zw"]
        separator = [';']
        for domain_group in domain_groups: 
            for domain in Utils.splitString(domain_group.upper(), separator, True): 
                UriItemToken.__m_std_groups.add(Termin(domain, MorphLang.UNKNOWN, True))
    
    @staticmethod
    def _new2550(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'UriItemToken':
        res = UriItemToken(_arg1, _arg2)
        res.value = _arg3
        return res