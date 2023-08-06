from typing import List
from pathlib import Path


from fastapi import (
    Depends,
    HTTPException,
    APIRouter,
    File,
    UploadFile,
    Form,
    Depends,
    status,
)


from fastapi.security import HTTPBasic, HTTPBasicCredentials
from . import schemas
from .. import store
from ..store.customError import PpiKeyMissing
router = APIRouter()

# Discreapencies may occur due to :
# failed uniprotAC translation
# unknown PPi
# We try to get all translatable keys

# unprotlist Id may have be 
@router.post("/matrix", response_model=schemas.StringMatrix)
async def read_proteins(uniprotList: schemas.UniprotList):
    maybeTranslateManyToStringID = store.maybeTranslateManyToStringID(uniprotList.uniprotIDs)
    indexedScores = store.getVectorizedSparsePpiMatrix(maybeTranslateManyToStringID)
    print(indexedScores)
    return schemas.StringMatrix(
        members=uniprotList.uniprotIDs,
        indexedScores=indexedScores
    )

@router.post("/matrix/slim", response_model=schemas.StringMatrixSlim)
async def read_proteins_display_slim(uniprotList: schemas.UniprotList):
    maybeTranslateManyToStringID = store.maybeTranslateManyToStringID(uniprotList.uniprotIDs)
    indexedScores = store.getVectorizedSparsePpiMatrix(maybeTranslateManyToStringID, slim=True)
    print(indexedScores)
    return schemas.StringMatrixSlim(
        members=uniprotList.uniprotIDs,
        indexedScores=indexedScores
    )


@router.post("/partners/{uniprot_ID}", response_model=schemas.SeededUniprotInteractionDict)#, response_model=List[schemas.InteractionDatum])
async def get_partners_vector(uniprotID: schemas.UniprotAC):
    _ = store.getPartners(uniprotID)
    #print(_.data)
    return _

@router.put("/load/interactions")
async def put_interaction_info(data: schemas.InteractionList, status_code=201):
    print(data)
    store.storeInteractions(data.interactionList)
    return "Interaction addition Successfull"

@router.put("/load/mappers")
async def put_mapper_rules(mapperList: schemas.MapperList, status_code=201):    
    store.storeMappingRules(mapperList)
    return "Mapper addition Successfull"

@router.delete("/delete/mappers/all")
async def wipe_mapper(status_code=204):    
    _ = store.deleteMappingRules()
    print(_)
   
@router.delete("/delete/interactions/all")
async def wipe_mapper(status_code=204):    
    _ = store.deleteInteractions()
    print(_)


@router.get("/translate/uniprot/{mol_id}")
async def translate_between_uniprot_and_string(mol_id: schemas.UniprotAC):
    print("=>", mol_id)
    _ = store.translateToStringID(mol_id)
    print(mol_id, _)
    if not _:
        raise HTTPException(status_code=404, detail=f"No StringID tranlsation for {mol_id}")
    return _


# A FINIR ?
@router.get("/get/interactions")
async def get_interactions():
    it = store.listInteractions()
    for _ in it: 
        print(_)

@router.get("/get/interaction/{p1}/{p2}", response_model=schemas.UniprotInteractionDatum)
async def get_interaction(p1:schemas.UniprotAC, p2:schemas.UniprotAC):
 
    _ = store.getPairwiseUniprotInteraction(p1, p2)
    if not _:
        raise HTTPException(status_code=404, detail=f"{p1} {p2} interaction not found")
    
    return _
    #_ = store.translateToStringID(mol_id)
    #print(mol_id, _)

    #if not _:
    #    raise HTTPException(status_code=404, detail=f"No StringID tranlsation for {mol_id}")
    #return _