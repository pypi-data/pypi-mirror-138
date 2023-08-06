from .mapper import *
from .interactions import *
from ..api.schemas import UniprotInteractionDatum, SeededUniprotInteractionDict
from typing import Union, List, Tuple

from pystringbio.api import schemas

def ij2k(i, j ,n):
    return i * (n - 2) + j

def getVectorizedSparsePpiMatrix(interactorList:MaybeTranslatedList, slim=False)->Union[ \
                                                                List[ Tuple[int, InteractionDatum] ],\
                                                                List[ Tuple[int, List[int] ]]\
                                                                ]:
    vector = []
    tot = len(interactorList)
    print(interactorList)
    for i, (uniprotID1, stringID1) in enumerate(interactorList):
        if stringID1 is None:
            continue
        for j in range(i, tot):
            (uniprotID2, stringID2) = interactorList[j]
            if stringID2 is None:
                continue
            try:
                _:InteractionDatum = getSingleInteraction(stringID1, stringID2, slim=slim)
                vector.append( ( ij2k(i, j, tot), _ ) )
            except PpiKeyMissing as e:                
                continue
    return vector

def getPairwiseUniprotInteraction(uniprotID1, uniprotID2,
    *args, **kwargs)->Union[UniprotInteractionDatum, None]:    
    try :
        stringID1 = mapper.translateToStringID(uniprotID1)
        stringID2 = mapper.translateToStringID(uniprotID2)
        #print("==>", stringID1,stringID2)
    except StringKeyMissing as e:
        print(e)
        return None
    
    try:
        datum:InteractionDatum = getSingleInteraction(stringID1, stringID2)
        return UniprotInteractionDatum(
                protein1   = uniprotID1,
                protein1Tr = stringID1,
                protein2   = uniprotID2,
                protein2Tr = stringID2,    
                ppiStringID = MaybePpiKey(stringID1, stringID2),
                datum = datum
            )

    except PpiKeyMissing as e:
        print(e)
        return None
    
def getPartners(uniprotID, *args,  **kwargs)->Union[schemas.SeededUniprotInteractionDict, None]:
    stringID = mapper.translateToStringID(uniprotID)
    targetKeys = listInteractions(sf1=stringID)
    _:List[InteractionDatum]= getManyInteractions(targetKeys)
    data = {}
    for datum in _:
        p1, p2 = [
            mapper.translateToUniprotID(datum.protein1), 
            mapper.translateToUniprotID(datum.protein2) ]
        k = p2 if p1 == uniprotID else p1
        data[k] = datum 
    
    return SeededUniprotInteractionDict(
        query=uniprotID,
        data=data
    )
