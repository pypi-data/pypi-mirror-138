## Read parse channel files

# key could be  (justweigthing keys):

# string:511145.b0001:511145.b3766

# value could be string:
#  '0 0 0 125 0 0 292 354'



# Inserting mapper uniprot from
#511145	P37637|MDTF_ECOLI	511145.b3514	100.0	2105.0
# key P37637
# value 511145.b3514
from ..api.schemas import UniprotAC, StringAC, MapperList

class MappingRules():
    def __init__(self):
        self.data = []
    
    def push(self, uniprotID:UniprotAC, stringID: StringAC):
        self.data.append( (uniprotID, stringID) )

    def __iter__(self):
        for _ in self.data:
            yield _
    
    def __str__(self) -> str:
        return "\n".join( [f"{_[0]} -- {_[1]}" for _ in self ] )
    
    def __len__(self):
        return len(self.data)

    def pull(self, chunckSize=1000)->MapperList:
        uList = []
        sList = []
        for i in self:
            uList.append(i[0])
            sList.append(i[1])
            if len(uList) % chunckSize == 0:
                yield( MapperList.construct( uniprotIDs=uList, 
                                             stringIDs = sList)
                )
                uList = []
                sList = []
        if uList:
            yield( MapperList.construct( uniprotIDs=uList, 
                                         stringIDs = sList)
            )

def parseMappingRulesFile(path):
    print ("Parsing mapping rules data, this may take a while...")
    mappingRules = MappingRules()
    with open(path, 'r') as f:
        for l in f.readlines():
            if l.startswith("#"):
                continue

            _ = l.split()
            uID = _[1].split('|')[0]
            sID = _[2]
            mappingRules.push(uID, sID)
    return mappingRules