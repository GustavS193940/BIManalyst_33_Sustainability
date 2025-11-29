# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 13:31:28 2025

@author: gusta
"""
import numpy as np
import uuid
import os
import json
import pandas as pd

LCAConcrete = np.array([["C20","d1a78805-f2b1-4131-8f1d-08845be37654"],
                        ["C25","2a58dc5d-42ce-46ed-98de-53b201d29da0"],
                        ["C30","b4d08927-4070-45cc-ace0-e970c004b51d"],
                        ["C35","c8a63193-f3f7-49df-bfa4-2ba1d764dd9d"],
                        ["C40","9d1a1b13-0b03-44ce-80e2-9833c95245e9"],
                        ["C45","46b603ab-84e0-46dc-86a0-afa84bf24253"],
                        ["WE150","02d2f058-cfed-4732-8730-e212bb8e7d5f"],
                        ["WE200","97e29fb3-c8c3-57bf-a8b1-d823af2a3256"],
                        ["HC220","daa11502-050c-40b1-83fe-aeb78a97dc4d"],
                        ["HC320","ebfd477a-4b8f-44c9-8af5-f9f3930aa89b"],
                        ["Reinforcement","b3c6e51a-db0c-52e5-a0f1-1d416dbf5c33"]])
LCAMat = np.array([["Steel","900de71b-a8b2-5b14-ab42-a60da9f557db"],
                   ["Glulam","b4a3712a-f5a4-47e0-8ab0-8f716855a258"],
                   ["Wood","88e8f961-0a50-410b-a247-467ab6fb663d"],
                   ["Fire Batts","d735bf4f-1dcf-5866-8e7c-8382897a891f"]])

def writeBeams(beamList):
    beamElementID = str(uuid.uuid4())  
    beamString = ',{"Node": {"Element": {"id": "' + beamElementID + r'","name": {"English": "Beams"},"source": "User","comment": {"Danish": "","Norwegian": "","German": "","English": ""},"enabled": true,"excluded_scenarios": []}}},{"Edge": [{"CategoryToElement": {"id": "'+str(uuid.uuid4())+'"}},"ec9ee040-9c1d-4cae-864c-4c6a0e4b8c5b","'+ beamElementID +r'"]}'

    for i in range(len(beamList)):
        constUUID = str(uuid.uuid4())
        amount = round(beamList[i,6],2)
        constString = ',{"Edge": [{"ElementToConstruction": {"id": "'+ str(uuid.uuid4()) +'","amount": '+ str(amount) +',"enabled": true,"special_conditions": false,"excluded_scenarios": []}},"'+beamElementID+'","'+constUUID+'"]},{"Node": {"Construction": {"id": "'+ constUUID +'","name": {"English": "'+str(beamList[i,0])+'"},"unit": "M","source": "User","comment": {"German": "","Danish": "","Norwegian": "","English": ""},"locked": false}}},{"Edge": [{"CategoryToConstruction": {"id": "'+str(uuid.uuid4())+'","layers": [1]}},"ec9ee040-9c1d-4cae-864c-4c6a0e4b8c5b","'+constUUID+'"]}'
        beamString = beamString + constString
        if beamList[i,4] == "New Construction":
            RSL = 120
        else:
            RSL = 0

        if "Concrete" in beamList[i,1]:
            conAmount = float(beamList[i,5])/float(beamList[i,6])
            reinforcement = float(beamList[i,3])*conAmount
            for x in range(len(LCAConcrete)):
                if beamList[i,2] == LCAConcrete[x,0]:
                    concreteString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(conAmount,2))+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[x,1]+'"]}'
                    reinfString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(reinforcement,2))+',"unit": "KG","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[10,1]+'"]}'
                    beamString = beamString + concreteString + reinfString
        elif "Glulam" in beamList[i,1]:
            gluAmount = round(float(beamList[i,5])/float(beamList[i,6]),4)
            gluString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(gluAmount)+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAMat[1,1]+'"]}'
            beamString = beamString + gluString
        elif "Steel" in beamList[i,1]:
            steAmount = round(float(beamList[i,5])/float(beamList[i,6])*7850,2)
            steString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(steAmount)+',"unit": "KG","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAMat[0,1]+'"]}'
            beamString = beamString + steString
        elif "Wood" in beamList[i,1]:
            timAmount = round(float(beamList[i,5])/float(beamList[i,6]),4)
            timString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(timAmount)+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAMat[2,1]+'"]}'
            beamString = beamString + timString
    return beamString
    
def writeColumns(columnList):
    columnElementID = str(uuid.uuid4())  
    columnString = ',{"Node": {"Element": {"id": "' + columnElementID + r'","name": {"English": "Columns"},"source": "User","comment": {"Danish": "","Norwegian": "","German": "","English": ""},"enabled": true,"excluded_scenarios": []}}},{"Edge": [{"CategoryToElement": {"id": "'+str(uuid.uuid4())+'"}},"506a420e-c3cd-4849-a759-3117f10937b1","'+ columnElementID +r'"]}'

    for i in range(len(columnList)):
        constUUID = str(uuid.uuid4())
        amount = round(columnList[i,6],2)
        constString = ',{"Edge": [{"ElementToConstruction": {"id": "'+ str(uuid.uuid4()) +'","amount": '+ str(amount) +',"enabled": true,"special_conditions": false,"excluded_scenarios": []}},"'+columnElementID+'","'+constUUID+'"]},{"Node": {"Construction": {"id": "'+ constUUID +'","name": {"English": "'+str(columnList[i,0])+'"},"unit": "M","source": "User","comment": {"German": "","Danish": "","Norwegian": "","English": ""},"locked": false}}},{"Edge": [{"CategoryToConstruction": {"id": "'+str(uuid.uuid4())+'","layers": [1]}},"ec9ee040-9c1d-4cae-864c-4c6a0e4b8c5b","'+constUUID+'"]}'
        columnString = columnString + constString
        if columnList[i,4] == "New Construction":
            RSL = 120
        else:
            RSL = 0

        if "Concrete" in columnList[i,1]:
            conAmount = float(columnList[i,5])/float(columnList[i,6])
            reinforcement = float(columnList[i,3])*conAmount
            for x in range(len(LCAConcrete)):
                if columnList[i,2] == LCAConcrete[x,0]:
                    concreteString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(conAmount,2))+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[x,1]+'"]}'
                    reinfString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(reinforcement,2))+',"unit": "KG","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[10,1]+'"]}'
                    columnString = columnString + concreteString + reinfString
        elif "Glulam" in columnList[i,1]:
            gluAmount = round(float(columnList[i,5])/float(columnList[i,6]),4)
            gluString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(gluAmount)+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAMat[1,1]+'"]}'
            columnString = columnString + gluString
        elif "Steel" in columnList[i,1]:
            steAmount = round(float(columnList[i,5])/float(columnList[i,6])*7850,2)
            steString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(steAmount)+',"unit": "KG","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAMat[0,1]+'"]}'
            columnString = columnString + steString
        elif "Wood" in columnList[i,1]:
            timAmount = round(float(columnList[i,5])/float(columnList[i,6]),4)
            timString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(timAmount)+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAMat[2,1]+'"]}'
            columnString = columnString + timString
    return columnString

def writeWalls(wallList):
    exWallElementID = str(uuid.uuid4())  
    exWallString = ',{"Node": {"Element": {"id": "' + exWallElementID + r'","name": {"English": "External Walls"},"source": "User","comment": {"Danish": "","Norwegian": "","German": "","English": ""},"enabled": true,"excluded_scenarios": []}}},{"Edge": [{"CategoryToElement": {"id": "'+str(uuid.uuid4())+'"}},"10a52123-48d7-466a-9622-d463511a6df0","'+ exWallElementID +r'"]}'

    for i in range(len(wallList)):
        constUUID = str(uuid.uuid4())
        amount = round(float(wallList[i,8]),2)
        if str(wallList[i,1]) == 'True':
            constString = ',{"Edge": [{"ElementToConstruction": {"id": "'+ str(uuid.uuid4()) +'","amount": '+ str(amount) +',"enabled": true,"special_conditions": false,"excluded_scenarios": []}},"'+exWallElementID+'","'+constUUID+'"]},{"Node": {"Construction": {"id": "'+ constUUID +'","name": {"English": "'+str(wallList[i,0])+'"},"unit": "M2","source": "User","comment": {"German": "","Danish": "","Norwegian": "","English": ""},"locked": false}}},{"Edge": [{"CategoryToConstruction": {"id": "'+str(uuid.uuid4())+'","layers": [1]}},"10a52123-48d7-466a-9622-d463511a6df0","'+constUUID+'"]}'
            exWallString = exWallString + constString

            if wallList[i,6] == "New Construction":
                RSL = 120
            else:
                RSL = 0
            if "Fire Batts" in wallList[i,2]:
                if RSL == 120:
                    RSL = 80
                fireString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(float(wallList[i,4])/1000)+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAMat[3,1]+'"]}'
                exWallString = exWallString + fireString
                    
            elif "Concrete" in wallList[i,2]:
                if wallList[i,7] == 'PRECAST' and float(wallList[i,4]) <= 150:
                    elemString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(float(wallList[i,4])/150)+',"unit": "M2","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[6,1]+'"]}'
                    exWallString = exWallString + elemString
                elif wallList[i,7] == 'PRECAST' and float(wallList[i,4]) > 150:
                    elemString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(float(wallList[i,4])/200)+',"unit": "M2","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[7,1]+'"]}'
                    exWallString = exWallString + elemString
                elif wallList[i,7] == 'INSITU':
                    conAmount = float(wallList[i,4])/1000
                    reinforcement = float(wallList[i,5])*conAmount
                    for x in range(len(LCAConcrete)):
                        if wallList[i,3] == LCAConcrete[x,0]:
                            concreteString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(conAmount,2))+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[x,1]+'"]}'
                            reinfString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(reinforcement,2))+',"unit": "KG","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[10,1]+'"]}'
                            exWallString = exWallString + concreteString + reinfString

    intWallElementID = str(uuid.uuid4())  
    intWallString = ',{"Node": {"Element": {"id": "' + intWallElementID + r'","name": {"English": "Load-bearing Internal Walls"},"source": "User","comment": {"Danish": "","Norwegian": "","German": "","English": ""},"enabled": true,"excluded_scenarios": []}}},{"Edge": [{"CategoryToElement": {"id": "'+str(uuid.uuid4())+'"}},"59ab59a5-2482-45ae-85f1-d0e39e640712","'+ intWallElementID +r'"]}'

    for i in range(len(wallList)):
        constUUID = str(uuid.uuid4())
        amount = round(float(wallList[i,8]),2)
        if str(wallList[i,1]) == 'False':
            constString = ',{"Edge": [{"ElementToConstruction": {"id": "'+ str(uuid.uuid4()) +'","amount": '+ str(amount) +',"enabled": true,"special_conditions": false,"excluded_scenarios": []}},"'+intWallElementID+'","'+constUUID+'"]},{"Node": {"Construction": {"id": "'+ constUUID +'","name": {"English": "'+str(wallList[i,0])+'"},"unit": "M2","source": "User","comment": {"German": "","Danish": "","Norwegian": "","English": ""},"locked": false}}},{"Edge": [{"CategoryToConstruction": {"id": "'+str(uuid.uuid4())+'","layers": [1]}},"59ab59a5-2482-45ae-85f1-d0e39e640712","'+constUUID+'"]}'
            intWallString = intWallString + constString

            if wallList[i,6] == "New Construction":
                RSL = 100
            else:
                RSL = 0
            if "Fire Batts" in wallList[i,2]:
                fireString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(float(wallList[i,4])/1000)+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAMat[3,1]+'"]}'
                intWallString = intWallString + fireString
                    
            elif "Concrete" in wallList[i,2]:
                if wallList[i,7] == 'PRECAST' and float(wallList[i,4]) <= 150:
                    elemString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(float(wallList[i,4])/150)+',"unit": "M2","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[6,1]+'"]}'
                    intWallString = intWallString + elemString
                elif wallList[i,7] == 'PRECAST' and float(wallList[i,4]) > 150:
                    elemString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(float(wallList[i,4])/200)+',"unit": "M2","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[7,1]+'"]}'
                    intWallString = intWallString + elemString
                elif wallList[i,7] == 'INSITU':
                    conAmount = float(wallList[i,4])/1000
                    reinforcement = float(wallList[i,5])*conAmount
                    for x in range(len(LCAConcrete)):
                        if wallList[i,3] == LCAConcrete[x,0]:
                            concreteString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(conAmount,2))+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[x,1]+'"]}'
                            reinfString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(reinforcement,2))+',"unit": "KG","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[10,1]+'"]}'
                            intWallString = intWallString + concreteString + reinfString
    return exWallString, intWallString

def writeSlabs(slabList):
    roofElementID = str(uuid.uuid4())  
    roofString = ',{"Node": {"Element": {"id": "' + roofElementID + r'","name": {"English": "Roof"},"source": "User","comment": {"Danish": "","Norwegian": "","German": "","English": ""},"enabled": true,"excluded_scenarios": []}}},{"Edge": [{"CategoryToElement": {"id": "'+str(uuid.uuid4())+'"}},"d734712a-d27d-42c5-936f-98fe4c4df90b","'+ roofElementID +r'"]}'

    for i in range(len(slabList)):
        constUUID = str(uuid.uuid4())
        amount = round(float(slabList[i,8]),2)
        if str(slabList[i,1]) == 'True':
            constString = ',{"Edge": [{"ElementToConstruction": {"id": "'+ str(uuid.uuid4()) +'","amount": '+ str(amount) +',"enabled": true,"special_conditions": false,"excluded_scenarios": []}},"'+roofElementID+'","'+constUUID+'"]},{"Node": {"Construction": {"id": "'+ constUUID +'","name": {"English": "'+str(slabList[i,0])+'"},"unit": "M2","source": "User","comment": {"German": "","Danish": "","Norwegian": "","English": ""},"locked": false}}},{"Edge": [{"CategoryToConstruction": {"id": "'+str(uuid.uuid4())+'","layers": [1]}},"d734712a-d27d-42c5-936f-98fe4c4df90b","'+constUUID+'"]}'
            roofString = roofString + constString

            if slabList[i,6] == "New Construction":
                RSL = 120
            else:
                RSL = 0
                   
            if "Concrete" in slabList[i,2]:
                if slabList[i,7] == 'INSITU':
                    conAmount = float(slabList[i,4])/1000
                    reinforcement = float(slabList[i,5])*conAmount
                    for x in range(len(LCAConcrete)):
                        if slabList[i,3] == LCAConcrete[x,0]:
                            concreteString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(conAmount,2))+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[x,1]+'"]}'
                            reinfString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(reinforcement,2))+',"unit": "KG","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[10,1]+'"]}'
                            roofString = roofString + concreteString + reinfString
                elif slabList[i,7] == 'PRECAST' and float(slabList[i,4]) <= 220:
                    elemString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(float(slabList[i,4])/220)+',"unit": "M2","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[8,1]+'"]}'
                    roofString = roofString + elemString
                elif slabList[i,7] == 'PRECAST' and float(slabList[i,4]) > 220:
                    elemString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(float(slabList[i,4])/320)+',"unit": "M2","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[9,1]+'"]}'
                    roofString = roofString + elemString
                    
    deckElementID = str(uuid.uuid4())  
    deckString = ',{"Node": {"Element": {"id": "' + deckElementID + r'","name": {"English": "Floor Deck"},"source": "User","comment": {"Danish": "","Norwegian": "","German": "","English": ""},"enabled": true,"excluded_scenarios": []}}},{"Edge": [{"CategoryToElement": {"id": "'+str(uuid.uuid4())+'"}},"f4c234ec-77f1-4ee0-92d0-f1819e0307d4","'+ deckElementID +r'"]}'

    for i in range(len(slabList)):
        constUUID = str(uuid.uuid4())
        amount = round(float(slabList[i,8]),2)
        if str(slabList[i,1]) == 'False':
            constString = ',{"Edge": [{"ElementToConstruction": {"id": "'+ str(uuid.uuid4()) +'","amount": '+ str(amount) +',"enabled": true,"special_conditions": false,"excluded_scenarios": []}},"'+deckElementID+'","'+constUUID+'"]},{"Node": {"Construction": {"id": "'+ constUUID +'","name": {"English": "'+str(slabList[i,0])+'"},"unit": "M2","source": "User","comment": {"German": "","Danish": "","Norwegian": "","English": ""},"locked": false}}},{"Edge": [{"CategoryToConstruction": {"id": "'+str(uuid.uuid4())+'","layers": [1]}},"f4c234ec-77f1-4ee0-92d0-f1819e0307d4","'+constUUID+'"]}'
            deckString = deckString + constString

            if slabList[i,6] == "New Construction":
                RSL = 100
            else:
                RSL = 0
                   
            if "Concrete" in slabList[i,2]:
                if slabList[i,7] == 'INSITU':
                    conAmount = float(slabList[i,4])/1000
                    reinforcement = float(slabList[i,5])*conAmount
                    for x in range(len(LCAConcrete)):
                        if slabList[i,3] == LCAConcrete[x,0]:
                            concreteString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(conAmount,2))+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[x,1]+'"]}'
                            reinfString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(reinforcement,2))+',"unit": "KG","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[10,1]+'"]}'
                            deckString = deckString + concreteString + reinfString
                elif slabList[i,7] == 'PRECAST' and float(slabList[i,4]) <= 220:
                    elemString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(float(slabList[i,4])/220)+',"unit": "M2","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[8,1]+'"]}'
                    deckString = deckString + elemString
                elif slabList[i,7] == 'PRECAST' and float(slabList[i,4]) > 220:
                    elemString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(float(slabList[i,4])/320)+',"unit": "M2","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[9,1]+'"]}'
                    deckString = deckString + elemString
    return roofString, deckString

def writeJson(beams,columns,walls,slabs):
    baseString = '[  {    "Node": {      "Project": {        "id": "2f95c41e-0cc4-4b6e-90ac-ffa796aecd6d",        "name": {          "Danish": ""        },        "address": "",        "owner": "",        "lca_advisor": "",        "building_regulation_version": ""      }    }  },  {    "Edge": [      {        "MainBuilding": "bd294743-9c10-47c8-bce2-6b0593cb6852"      },      "2f95c41e-0cc4-4b6e-90ac-ffa796aecd6d",      "7791681b-40a2-401d-ac38-a2f73d736ab4"    ]  },  {    "Node": {      "Building": {        "id": "7791681b-40a2-401d-ac38-a2f73d736ab4",        "scenario_name": "Original bygningsmodel",        "locked": "Unlocked",        "description": {          "German": "",          "Danish": "",          "English": "",          "Norwegian": ""        },        "building_type": "Office",        "heated_floor_area": 0.0,        "gross_area": 0.0,        "integrated_garage": 0.0,        "external_area": 0.0,        "gross_area_above_ground": 0.0,        "person_count": 0,        "building_topology": "Unknown",        "project_type": "New",        "storeys_above_ground": 0,        "storeys_below_ground": 0,        "storey_height": 0.0,        "initial_year": 2023,        "calculation_timespan": 50,        "calculation_mode": "BR23",        "outside_area": 0.0,        "plot_area": 0.0,        "energy_class": "LowEnergy"      }    }  },  {    "Edge": [      {        "BuildingToRoot": "e2ff039e-2328-4d9c-a792-01bd101f93a1"      },      "7791681b-40a2-401d-ac38-a2f73d736ab4",      "216cf5d6-3e9d-43ec-b0d8-5aee02240c28"    ]  },  {    "Edge": [      {        "BuildingToOperation": "67f5d798-3456-43b0-b6b9-fccdee63b17b"      },      "7791681b-40a2-401d-ac38-a2f73d736ab4",      "0338d31e-3876-440d-a88c-2daa2dd81942"    ]  },  {    "Edge": [      {        "BuildingToDGNBOperation": "4fab0de9-5738-4a1c-9a15-0a257a0f7743"      },      "7791681b-40a2-401d-ac38-a2f73d736ab4",      "181acc05-4bd0-4131-bbf5-eef64c9bf164"    ]  },  {    "Node": {      "EmbodiedRoot": {        "id": "216cf5d6-3e9d-43ec-b0d8-5aee02240c28"      }    }  },  {    "Edge": [      {        "RootToModel": "1191a67b-c672-43fc-b2b7-724bc62b974a"      },      "216cf5d6-3e9d-43ec-b0d8-5aee02240c28",      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2"    ]  },  {    "Edge": [      {        "RootToConstructionProcess": "48781119-3992-4e48-9099-e8e8654a4935"      },      "216cf5d6-3e9d-43ec-b0d8-5aee02240c28",      "349738da-9747-4d5c-b508-2a810317166f"    ]  },  {    "Node": {      "Operation": {        "id": "0338d31e-3876-440d-a88c-2daa2dd81942",        "electricity_usage": 0.0,        "heat_usage": 0.0,        "electricity_production": 0.0      }    }  },  {    "Edge": [      {        "ElectricitySource": "af579fc8-0cad-40df-a3a4-ca36966aab9c"      },      "0338d31e-3876-440d-a88c-2daa2dd81942",      "e967c8e7-e73d-47f3-8cba-19569ad76b4d"    ]  },  {    "Edge": [      {        "HeatingSource": "e7601042-b8f2-4226-ae0a-2c1a4c5686bf"      },      "0338d31e-3876-440d-a88c-2daa2dd81942",      "6cdeb050-90e5-46b3-89ad-bfcc8e246b47"    ]  },  {    "Node": {      "DGNBOperationReference": {        "id": "181acc05-4bd0-4131-bbf5-eef64c9bf164",        "heat_supplement": 0.0,        "electricity_supplement": 0.0      }    }  },  {    "Node": {      "ElementModel": {        "id": "aeefab8a-e825-4d14-b0c3-e87b7759e5b2"      }    }  },  {    "Edge": [      {        "ParentTo": "49bb8f71-6d02-48bf-986d-3fa6db9e9b92"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "0ae65810-51bc-4130-89a0-9c107f1aca3f"    ]  },  {    "Edge": [      {        "ParentTo": "4640fd41-1a2c-4bb9-bd0a-7d1cd85b102e"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "20c75334-735c-442f-a541-985ac5a130c8"    ]  },  {    "Edge": [      {        "ParentTo": "7911defb-6013-4cd7-ae97-ed870ed7cb47"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "9e7adf74-5281-4aa4-9cff-d903a4266aae"    ]  },  {    "Edge": [      {        "ParentTo": "b879ae4c-15d5-4f6a-91e1-4b575702436b"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "bae7f4b9-967c-4542-bc99-f744aa261424"    ]  },  {    "Edge": [      {        "ParentTo": "4ff922e8-982f-436e-a3b7-efecb987c5a6"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "ca17092d-2a42-4941-b478-669b12001556"    ]  },  {    "Edge": [      {        "ParentTo": "6d2c715d-847c-4866-9bd7-a2b8defdf6a7"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "487184b7-5568-497b-b7e2-e8d2269e51ef"    ]  },  {    "Edge": [      {        "ParentTo": "0e59acae-729c-4bc5-bea8-5b4b2abba72a"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "a1746ce9-3d06-424c-a701-34a090f08433"    ]  },  {    "Edge": [      {        "ParentTo": "1cf888c3-deb9-42d0-a702-1cc1818e5dc1"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "571650a7-4259-4cc1-9d56-a12e516fd495"    ]  },  {    "Edge": [      {        "ParentTo": "e009ab41-7be2-40ce-aafe-78b2cc86fb47"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "e5937376-1d7f-4edf-9710-cafd7fe91606"    ]  },  {    "Edge": [      {        "ParentTo": "708fa945-e639-43f5-90dc-2d9719963254"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "6808ac7b-2a79-45a6-8013-5f89ad13c337"    ]  },  {    "Edge": [      {        "ParentTo": "b576344e-eccf-4735-94f3-23ce5a6e2d0c"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "f7737ac7-ea51-488e-81de-9c1bab1c08bf"    ]  },  {    "Edge": [      {        "ParentTo": "0efa66cb-2308-4e75-8d38-34c9b130af78"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "3cb417d3-d615-402e-81dc-d7d587e83ac1"    ]  },  {    "Edge": [      {        "ParentTo": "badc823a-c90b-4ef9-890c-34690bb410eb"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "ac7112e7-ccea-4e1b-a6a2-9c9c3b9a7177"    ]  },  {    "Edge": [      {        "ParentTo": "a2320d34-9ef5-42c3-a9ca-6e48303e7656"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "1e853d01-fce5-4947-850d-e0b43e51b1fc"    ]  },  {    "Edge": [      {        "ParentTo": "4fa14d2c-f70f-4cd5-b1c6-c303821aa2a6"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "d50ad0a5-636a-4169-b4d7-21e9b64d94a8"    ]  },  {    "Edge": [      {        "ParentTo": "25b12d48-dbd3-4851-aa40-306a099d45f1"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "dad100a3-f570-4c96-bec0-9028bc5f6835"    ]  },  {    "Edge": [      {        "ParentTo": "af67e91b-9651-46e2-9abe-caaa46b6ea0f"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "de3a2393-388c-4079-9e7d-6529c14f8a69"    ]  },  {    "Node": {      "ConstructionProcess": {        "id": "349738da-9747-4d5c-b508-2a810317166f"      }    }  },  {    "Edge": [      {        "ProcessToInstallation": "dd928199-b70a-43f8-8556-4f740dccd1ef"      },      "349738da-9747-4d5c-b508-2a810317166f",      "020cc362-536b-484e-b8f9-6507b40ab675"    ]  },  {    "Edge": [      {        "ProcessToTransport": "15867192-86b7-40a8-9936-83d9e998516e"      },      "349738da-9747-4d5c-b508-2a810317166f",      "915c5162-93bc-49c0-bdaf-9f470b4c7998"    ]  },  {    "Node": {      "ConstructionInstallation": {        "id": "020cc362-536b-484e-b8f9-6507b40ab675"      }    }  },  {    "Edge": [      {        "FuelUsage": "f069389f-b870-4c63-9362-88dc8c9912c9"      },      "020cc362-536b-484e-b8f9-6507b40ab675",      "5e5ccea5-5243-494b-9a49-292ada027abe"    ]  },  {    "Edge": [      {        "InstallationOperation": "082b809c-9850-4a72-8dbb-7ec74d0fec15"      },      "020cc362-536b-484e-b8f9-6507b40ab675",      "c33cf608-9ceb-47f3-9ccf-c3ecb58ddb96"    ]  },  {    "Node": {      "ProductTransportRoot": {        "id": "915c5162-93bc-49c0-bdaf-9f470b4c7998"      }    }  },  {    "Node": {      "FuelConsumption": {        "id": "5e5ccea5-5243-494b-9a49-292ada027abe"      }    }  },  {    "Edge": [      {        "TransportTypeUsage": {          "id": "899c9a7c-b616-49ac-8937-088ac10b2537",          "distance": 0.0        }      },      "5e5ccea5-5243-494b-9a49-292ada027abe",      "1adea09d-d954-4b9f-9a95-fa3cee0c4787"    ]  },  {    "Edge": [      {        "TransportTypeUsage": {          "id": "59292514-bf7b-4c89-a816-fe528cb07530",          "distance": 0.0        }      },      "5e5ccea5-5243-494b-9a49-292ada027abe",      "b0ca9d35-fdfe-4e29-8d65-1032bf5a220a"    ]  },  {    "Node": {      "Operation": {        "id": "c33cf608-9ceb-47f3-9ccf-c3ecb58ddb96",        "electricity_usage": 0.0,        "heat_usage": 0.0,        "electricity_production": 0.0      }    }  },  {    "Edge": [      {        "ElectricitySource": "5a38b95a-e2ce-4802-8576-39511c9fd155"      },      "c33cf608-9ceb-47f3-9ccf-c3ecb58ddb96",      "e967c8e7-e73d-47f3-8cba-19569ad76b4d"    ]  },  {    "Edge": [      {        "HeatingSource": "a37552fd-fb25-4d95-bf09-64df9f752a29"      },      "c33cf608-9ceb-47f3-9ccf-c3ecb58ddb96",      "6cdeb050-90e5-46b3-89ad-bfcc8e246b47"    ]  }'

    if not os.path.exists(r'Json'):
        os.makedirs(r'Json')
    FullJson = baseString + writeBeams(beams) + writeColumns(columns) + writeWalls(walls)[0] + writeWalls(walls)[1] + writeSlabs(slabs)[0] + writeSlabs(slabs)[1] + ']'
    FullJson = json.loads(FullJson.replace("\'", '"'))
    with open('Json/LCACalc.json', 'w') as outfile:
        json.dump(FullJson, outfile)
    return

def writeExcel(beams,columns,walls,slabs):
    beams = pd.DataFrame(beams,columns=["Name","Material","Concrete Strength Class","Reinforcement Amount [kg/m3]","Phase","Total Volume [m3]","Total Length [m]"])
    columns = pd.DataFrame(columns,columns=["Name","Material","Concrete Strength Class","Reinforcement Amount [kg/m3]","Phase","Total Volume [m3]","Total Length [m]"])
    walls = pd.DataFrame(walls,columns=["Name","IsExternal","Material","Concrete Strength Class","Width [mm]","Reinforcement Amount [kg/m3]","Phase","Casting Method","Total Area [m2]"])
    slabs = pd.DataFrame(slabs,columns=["Name","IsExternal","Material","Concrete Strength Class","Thickness [mm]","Reinforcement Amount [kg/m3]","Phase","Casting Method","Total Area [m2]"])

    if not os.path.exists(r'Excel'):
        os.makedirs(r'Excel')
    beams.to_excel('Excel/beams.xlsx',index = False)
    columns.to_excel('Excel/columns.xlsx',index = False)
    walls.to_excel('Excel/walls.xlsx',index = False)
    slabs.to_excel('Excel/slabs.xlsx',index = False)
    return