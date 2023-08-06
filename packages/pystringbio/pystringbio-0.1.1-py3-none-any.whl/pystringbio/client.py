from typing import List
import requests
from .io.mapping import MappingRules
from .io.interactions import InteractionDatum
import progressbar

def loadMappingRules(mappingRules:MappingRules, chunckSize=1000):
    acc = 0
    with progressbar.ProgressBar(max_value=len(mappingRules)) as bar:
        for mapperList in mappingRules.pull(chunckSize=chunckSize):
            #print(mapperList.json())
            res = requests.put("http://localhost:8000/api/load/mappers", data = mapperList.json())
            acc = acc  + chunckSize if acc  + chunckSize < len(mappingRules) else len(mappingRules)
            bar.update(acc)
        #bar.update(len(mappingRules) - 1)

def loadInteractionData(interactionData:List[InteractionDatum], chunckSize=1000):
    acc = 0
    with progressbar.ProgressBar(max_value=len(interactionData)) as bar:
        for interactionQuantum in interactionData.pull(chunckSize=chunckSize):
            asJson = ' { "interactionList" : [' +\
                 ','.join(\
                 [_.json() for _ in interactionQuantum ]\
                 )  + ']}'
        #print(asJson)
            res = requests.put("http://localhost:8000/api/load/interactions", data = asJson)
            acc = acc  + chunckSize if acc  + chunckSize < len(interactionData) else len(interactionData)
            bar.update(acc)
        #bar.update(len(interactionData) - 1)