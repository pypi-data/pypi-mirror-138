from __future__ import annotations
from typing import List, Optional, Tuple, Union, Dict

from pydantic import BaseModel, Json, validator, root_validator
import re 



uniprot_acc_regex = re.compile(
    r'[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}'
)

class UniprotAC(str):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = uniprot_acc_regex.fullmatch(v.upper())
        if not m:
            raise ValueError(f"invalid uniprot accession at {v}")
        # you could also return a string here which would mean model.post_code
        # would be a string, pydantic won't care but you could end up with some
        # confusion since the value's type won't match the type annotation
        # exactly
        return cls(f'{v.upper()}')

    def __repr__(self):
        return f'{super().__repr__()}'

class UniprotList(BaseModel):
    uniprotIDs:List[UniprotAC]


class StringAC(str):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
       # m = uniprot_acc_regex.fullmatch(v.upper())
       # if not m:
       #     raise ValueError(f"invalid uniprot accession at {v}")
        # you could also return a string here which would mean model.post_code
        # would be a string, pydantic won't care but you could end up with some
        # confusion since the value's type won't match the type annotation
        # exactly
        return cls(f'{v.lower()}')

    def __repr__(self):
        return f'{super().__repr__()}'

#    @validator('uniprotIDs')
#    def must_contain_valid_uniprotID(cls, v):
#        for _ in v:
#            if not re.match(,
#            _):
#                raise ValueError(f"{_} is not a valid uniprotID")
#        return v

class MapperList(BaseModel):
    uniprotIDs:List[UniprotAC]
    stringIDs:List[StringAC]

    @root_validator
    def must_be_even_sized(cls, values):
        l1, l2 = len(values.get('uniprotIDs')), len(values.get('stringIDs'))
        assert l1 == l2, 'uniprot and string accessors list must be even-sized'
            #raise ValueError('uniprot and string Accessors must be ')
        return values

class InteractionDatum(BaseModel):
    protein1:StringAC
    protein2:StringAC
    neighborhood:int
    fusion:int
    cooccurence:int
    coexpression:int
    experimental:int
    database:int
    textmining:int
    combined_score:int
    def asRedisArray(self):
        return [
            self.neighborhood,
            self.fusion,
            self.cooccurence,
            self.coexpression,
            self.experimental,
            self.database,
            self.textmining,
            self.combined_score
        ]


class StringMatrix(BaseModel):
    members:List[UniprotAC] #UniprotList
    indexedScores:List[Tuple[int, InteractionDatum]]

class StringMatrixSlim(BaseModel):
    members:List[UniprotAC] #UniprotList
    indexedScores:List[Tuple[ int, List[int] ]]

class UniprotInteractionDatum(BaseModel):
    protein1:UniprotAC
    protein1Tr:StringAC
    protein2:UniprotAC
    protein2Tr:StringAC    
    ppiStringID:str
    datum:InteractionDatum

class InteractionList(BaseModel):
    interactionList:List[InteractionDatum]


class SeededUniprotInteractionDict(BaseModel):
    query:UniprotAC
    data:Dict[UniprotAC, InteractionDatum]

MaybeTranslatedList = List[Tuple[UniprotAC,Union[StringAC, None]]]
