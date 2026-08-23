# -*- coding: utf-8 -*-
"""Business class per covered stock, set explicitly rather than inferred from the lens.

An earlier pass derived this from the section-1.1 title and mis-read every operating
company that carries a dividend-discount CROSS-CHECK as a bank - DEWA, SALIK, STC,
BURJEEL, EAND, ADNOCGAS among them. The class decides which peer set and which lens a
batch shares, so getting it wrong destroys the reason for batching at all.

Classes follow the protocol's own LENS BY CLASS list.
"""
BANK = ['ADCB','ADIB','ADIBUAE','ALINMA','ALRAJHI','BTFH','COMI','DIB','ENBD','FAB',
        'HRHO','QNB','RIBL','SNB']
DEVELOPER = ['ALDAR','EMAAR','EMAARDEV','EMFD','HELI','MODON','OCDI','ORHD','PHDC','PRDC','TMGH']
HOLDCO = ['2POINTZERO','ALPHADHABI','CCAP','IHC','IQCD','KAKAO','OIH','RAYA','RELIANCE','TMPV']
CONTRACTOR = ['ORAS']

def classify(tk):
    if tk in BANK:       return 'Bank or financial'
    if tk in DEVELOPER:  return 'Real-estate developer'
    if tk in HOLDCO:     return 'Holding company'
    if tk in CONTRACTOR: return 'Contractor'
    return 'Operating company'

ORDER = ['Operating company','Contractor','Real-estate developer','Holding company','Bank or financial']
