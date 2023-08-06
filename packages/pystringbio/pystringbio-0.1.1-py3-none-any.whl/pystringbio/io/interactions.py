## Read parse channel files

# key could be  (justweigthing keys):

# string:511145.b0001:511145.b3766

# value could be string:
#  '0 0 0 125 0 0 292 354'



# Inserting mapper uniprot from
#511145	P37637|MDTF_ECOLI	511145.b3514	100.0	2105.0
# key P37637
# value 511145.b3514
from ..api.schemas import UniprotAC, StringAC, InteractionDatum
from typing import List

class InteractionData():
    def __init__(self):
        self.data = []
    
    def push(self, data:InteractionDatum):
        self.data.append(data)

    def __iter__(self):
        for _ in self.data:
            yield _

    def __str__(self) -> str:
        return "\n".join( [ str(_) for _ in self ] )

    def __len__(self):
        return len(self.data)

    def pull(self, chunckSize=1000)->List[InteractionDatum]:
        buffer = []
        for ppiDatum in self:
            buffer.append(ppiDatum)
            if len(buffer) % chunckSize == 0:
                yield buffer
                buffer = []
        if buffer:
            yield buffer

def parseInteractionFile(path)->InteractionData:
    data = InteractionData()
    print ("Parsing interaction data, this may take a while...")
    with open(path, 'r') as f:
        for l in f.readlines():
            if l.startswith("#"):
                continue
            _ = l.split()
            data.push(
                InteractionDatum(
                    protein1=_[0],
                    protein2=_[1],
                    neighborhood=_[2],
                    fusion=_[3],
                    cooccurence=_[4],
                    coexpression=_[5],
                    experimental=_[6],
                    database=_[7],
                    textmining=_[8],
                    combined_score=_[9]
                )
            )
          
    return data