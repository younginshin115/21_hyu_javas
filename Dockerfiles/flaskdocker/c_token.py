# -*- coding: utf-8 -*-

from konlpy.tag import Okt
import re
from jamo import h2j, j2hcj

class c_token:
    def only_korean(self, k_string):
        re_string = re.compile('[^ ㄱ-ㅣ가-힣]+').sub('', k_string)
        return re_string

    def m_tokenize(self, k_string):
        okt = Okt()
        token = okt.morphs(self.only_korean(k_string))
        return token

    def c_tokenize(self, k_string):
        c_token = j2hcj(h2j(self.only_korean(k_string)))
        return list(c_token)

    def cm_tokenize(self, k_string):
        okt = Okt()
        token = okt.morphs(self.only_korean(k_string))
        cm_token = []
        for i in token:
            cm_token.append(self.c_tokenize(i))
        return cm_token

    def noun_tokenize(self, k_string):
        okt = Okt()
        token = okt.nouns(self.only_korean(k_string))
        return token
