from pyrediscore import connect, store, get, delete, listKey, setDatabaseParameters, storeMany, mget
from decorator import decorator
from .customError import UniprotKeyMissing, PpiKeyMissing
from typing import List, Tuple, Iterator, Union
from ..api.schemas import MapperList, InteractionDatum, StringAC, UniprotAC
PREFIX="string:"

def MaybePpiKey(stringID1:StringAC, stringID2:UniprotAC):
    return f"ppi:{_setKeyPair(stringID1, stringID2)}"

def _setKeyPair(p1, p2):
    if p1 > p2:
        return f"{p1}:{p2}"
    return f"{p2}:{p1}"

@connect
@storeMany
def storeInteractions(interactionListData:List[InteractionDatum], *args, **kwargs):
    data = {}
    for iDatum in interactionListData:
        _ = iDatum.asRedisArray()
        #print(_)
        data[f"{ MaybePpiKey(iDatum.protein1, iDatum.protein2) }"] = _
        #data[f"ppi:{iDatum.protein2}:{iDatum.protein1}"] = _

    return data

@connect
@delete
def deleteInteractions(*args,**kwargs):
    toDel =  [ _ for _ in listInteractions(*args, **kwargs) ]
    return toDel
    

@connect
@get
def _getInteraction(maybekeyPairExpr, *args, **kwargs):
    return (f"{maybekeyPairExpr}", None)#f"u2s:")

def getSingleInteraction(p1:StringAC, p2:StringAC, *args, slim=False, **kwargs)->Union[\
                    InteractionDatum, List[int]]:
    query = MaybePpiKey(p1, p2)
    #query = _setKeyPair(p1, p2)
    #print(f"KEY is {query} from {p1} {p2}")
    try : 
        _ = _getInteraction(query)
    except KeyError:
        raise PpiKeyMissing(query)
    if slim:
        return _
    #print(_)
    return InteractionDatum(
        protein1       = p1,
        protein2       = p2, 
        neighborhood   = _[0],
        fusion         = _[1],
        cooccurence    = _[2],
        coexpression   = _[3],
        experimental   = _[4],
        database       = _[5],
        textmining     = _[6],
        combined_score = _[7]
    )

def getManyInteractions(targetKeys:Iterator[str], 
                        *args, raw=True, **kwargs)->List[InteractionDatum]:

    _targetKeys = [ _ for _ in targetKeys ]
    ppiIter = _getManyInteractions(_targetKeys, 
                        *args, raw=False, **kwargs)

    data = []
    iPPi = 0
    for ppiScore in ppiIter:
        (p1, p2) = _targetKeys[iPPi].split(':')[1:]
        data.append( 
            InteractionDatum(
                protein1       = p1,
                protein2       = p2, 
                neighborhood   = ppiScore[0],
                fusion         = ppiScore[1],
                cooccurence    = ppiScore[2],
                coexpression   = ppiScore[3],
                experimental   = ppiScore[4],
                database       = ppiScore[5],
                textmining     = ppiScore[6],
                combined_score = ppiScore[7]
            )
        )
        iPPi += 1

    if len(data) != len(_targetKeys):
        raise IndexError(f"Ppi Iterator exhausted before PPi target keys {len(data)} < {len(_targetKeys)}")
    
    return data

@connect
@mget
def _getManyInteractions(targetKeys:List[str], 
                        *args, raw=True, **kwargs):
    _ = [ ppiKey for ppiKey in targetKeys ]
    return (_, None)

@connect
@listKey
def listInteractions(*args, sf1=None, sf2=None, prefix=False, **kwargs):
    if sf1 and sf2:
        return (f"{MaybePpiKey(sf1, sf2)}", '')
    if sf1:
        return (f"ppi:*{sf1}*", '')
    if sf2:
        raise KeyError("Second protein can't be the only one specified")

    return (f"ppi:*", '')#f"u2s:")
