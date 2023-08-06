from pyrediscore import connect, store, get, delete, listKey, setDatabaseParameters, storeMany
from decorator import decorator
from .customError import UniprotKeyMissing, StringKeyMissing
from typing import Union, List, Tuple

from ..api.schemas import MapperList, StringAC, UniprotAC, MaybeTranslatedList


def maybeTranslateManyToStringID(uniprotIDs:List[UniprotAC]) -> MaybeTranslatedList: 
    res = []
    for _ in uniprotIDs:
        try:
            tr = translateToStringID(_)
            res.append( (_, tr) )
        except UniprotKeyMissing as e:
            res.append( (_, None) )
    return res

def translateToStringID(uniprotID:UniprotAC):   
    key = f"u2s:{uniprotID}"
    try : 
        trKey = _translate(key).strip('"')
        return trKey
    except KeyError:
        raise UniprotKeyMissing(uniprotID)

def translateToUniprotID(stringID:StringAC):
    key = f"s2u:{stringID}"
    try : 
        trKey = _translate(key)
        return trKey.strip('"')
    except KeyError:
        raise StringKeyMissing(stringID)

@connect
@get
def _translate(key ,*args, rawDecode=True, **kwargs):
    return (key, None)

######## SETTER ##########
def storeMappingRules(mapperList:MapperList):
    data = {}
    for uniprotID, stringID  in zip(mapperList.uniprotIDs, mapperList.stringIDs):
        data[f"u2s:{uniprotID}"] = stringID
        data[f"s2u:{stringID}"]  = uniprotID
    print(f"DEEPSTORE:{data}")
    return _storeMappingRules(data)

@connect
@storeMany
def _storeMappingRules(data, *args, **kwargs):
    return data 

@connect
@delete
def deleteMappingRules(*args,**kwargs):
    toDel =  [ _ for _ in listMappingRuleU2S(*args, **kwargs) ]
    toDel += [ _ for _ in listMappingRuleS2U(*args, **kwargs) ]
    
    return toDel

@connect
@listKey
def listMappingRuleU2S(*args, prefix=False, **kwargs):
    return (f"u2s:*", '')#f"u2s:")

@connect
@listKey
def listMappingRuleS2U(*args, prefix=False, **kwargs):
    return (f"s2u:*", '')#f"s2u:")
