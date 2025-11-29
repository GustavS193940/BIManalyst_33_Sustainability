# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 13:08:31 2025

@author: gusta
"""

import ifcopenshell.util.classification
import ifcopenshell.util.selector
import ifcopenshell.api.pset_template.add_pset_template

import numpy as np
import pandas as pd

def getBeams(model):
    beams = model.by_type('IfcBeam')
    beamList = np.array([0,1,2,3,4,5,6])

    for beam in beams:
        name1 = beam.Name
        mat1 = ifcopenshell.util.element.get_pset(beam, name="Materials and Finishes")["Structural Material"]
        if "Concrete" in mat1:
            concrete1 = ifcopenshell.util.element.get_pset(beam, name="Pset_ConcreteElementGeneral")["StrengthClass"]
            reinforcement1 = ifcopenshell.util.element.get_pset(beam, name="Pset_ConcreteElementGeneral")["ReinforcementVolumeRatio"]
        else:
            concrete1 = None
            reinforcement1 = None
        length1 = ifcopenshell.util.element.get_pset(beam, name="Structural")["Cut Length"]/1000
        volume1 = ifcopenshell.util.element.get_pset(beam, name="Dimensions")["Volume"]
        reuse1 = ifcopenshell.util.element.get_pset(beam, name="Phasing")["Phase Created"]
        beamProps = np.array([name1,mat1,concrete1,reinforcement1,reuse1,volume1,length1])
        beamList = np.vstack((beamList,beamProps))

    beamList = np.delete(beamList, (0), axis=0)
    beamList = pd.DataFrame(beamList)
    beamList = beamList.sort_values(by=[0,1,2,3,4])
    beamList = np.array(beamList)

    for i in range(len(beamList)):
        if i != 0:
            if beamList[i,0] == beamList[i-1,0] and beamList[i,1] == beamList[i-1,1] and beamList[i,2] == beamList[i-1,2] and beamList[i,3] == beamList[i-1,3] and beamList[i,4] == beamList[i-1,4]:
                beamList[i,5] = float(beamList[i-1,5]) + float(beamList[i,5])
                beamList[i,6] = float(beamList[i-1,6]) + float(beamList[i,6])
                beamList[i-1] = [0,0,0,0,0,0,0]

    beamList = beamList[~np.all(beamList == 0, axis=1)]
    return beamList

def getColumns(model):
    columns = model.by_type('IfcColumn')
    columnList = np.array([0,1,2,3,4,5,6])

    for column in columns:
        name1 = column.Name
        mat1 = ifcopenshell.util.element.get_pset(column, name="Materials and Finishes")["Structural Material"]
        if "Concrete" in mat1:
            concrete1 = ifcopenshell.util.element.get_pset(column, name="Pset_ConcreteElementGeneral")["StrengthClass"]
            reinforcement1 = ifcopenshell.util.element.get_pset(column, name="Pset_ConcreteElementGeneral")["ReinforcementVolumeRatio"]
        else:
            concrete1 = None
            reinforcement1 = None
        length1 = ifcopenshell.util.element.get_pset(column, name="Dimensions")["Length"]/1000
        volume1 = ifcopenshell.util.element.get_pset(column, name="Dimensions")["Volume"]
        reuse1 = ifcopenshell.util.element.get_pset(column, name="Phasing")["Phase Created"]
        columnProps = np.array([name1,mat1,concrete1,reinforcement1,reuse1,volume1,length1])
        columnList = np.vstack((columnList,columnProps))

    columnList = np.delete(columnList, (0), axis=0)
    columnList = pd.DataFrame(columnList)
    columnList = columnList.sort_values(by=[0,1,2,3,4])
    columnList = np.array(columnList)

    for i in range(len(columnList)):
        if i != 0:
            if columnList[i,0] == columnList[i-1,0] and columnList[i,1] == columnList[i-1,1] and columnList[i,2] == columnList[i-1,2] and columnList[i,3] == columnList[i-1,3] and columnList[i,4] == columnList[i-1,4]:
                columnList[i,5] = float(columnList[i-1,5]) + float(columnList[i,5])
                columnList[i,6] = float(columnList[i-1,6]) + float(columnList[i,6])
                columnList[i-1] = [0,0,0,0,0,0,0]

    columnList = columnList[~np.all(columnList == 0, axis=1)]
    return columnList

def getWalls(model):
    walls = model.by_type('IfcWall')
    wallList = np.array([0,1,2,3,4,5,6,7,8])

    for wall in walls:
        name1 = wall.Name
        mat1 = ifcopenshell.util.element.get_pset(wall, name="Materials and Finishes")["Structural Material"]
        ext1 = ifcopenshell.util.element.get_pset(wall, name="Pset_WallCommon")["IsExternal"]
        if "Concrete" in mat1:
            concrete1 = ifcopenshell.util.element.get_pset(wall, name="Pset_ConcreteElementGeneral")["StrengthClass"]
            reinforcement1 = ifcopenshell.util.element.get_pset(wall, name="Pset_ConcreteElementGeneral")["ReinforcementVolumeRatio"]
            precast1 = ifcopenshell.util.element.get_pset(wall, name="Pset_ConcreteElementGeneral")["CastingMethod"]
        else:
            concrete1 = None
            reinforcement1 = None
            precast1 = None
        area1 = ifcopenshell.util.element.get_pset(wall, name="Dimensions")["Area"]
        width1 = ifcopenshell.util.element.get_pset(wall, name="Construction")["Width"]
        reuse1 = ifcopenshell.util.element.get_pset(wall, name="Phasing")["Phase Created"]
        wallProps = np.array([name1,ext1,mat1,concrete1,width1,reinforcement1,reuse1,precast1,area1])
        wallList = np.vstack((wallList,wallProps))

    wallList = np.delete(wallList, (0), axis=0)
    wallList = pd.DataFrame(wallList)
    wallList = wallList.sort_values(by=[0,1,2,3,4,5,6,7])
    wallList = np.array(wallList)

    for i in range(len(wallList)):
        if i != 0:
            if wallList[i,0] == wallList[i-1,0] and wallList[i,1] == wallList[i-1,1] and wallList[i,2] == wallList[i-1,2] and wallList[i,3] == wallList[i-1,3] and wallList[i,4] == wallList[i-1,4] and wallList[i,5] == wallList[i-1,5] and wallList[i,6] == wallList[i-1,6] and wallList[i,7] == wallList[i-1,7]:
                wallList[i,8] = round(float(wallList[i-1,8]) + float(wallList[i,8]),2)
                wallList[i-1] = [0,0,0,0,0,0,0,0,0]

    wallList = wallList[~np.all(wallList == 0, axis=1)]
    return wallList

def getSlabs(model):
    slabs = model.by_type('IfcSlab')
    slabList = np.array([0,1,2,3,4,5,6,7,8])

    for slab in slabs:
        name1 = slab.Name
        mat1 = ifcopenshell.util.element.get_pset(slab, name="Materials and Finishes")["Structural Material"]
        ext1 = ifcopenshell.util.element.get_pset(slab, name="Pset_SlabCommon")["IsExternal"]
        if "Concrete" in mat1:
            concrete1 = ifcopenshell.util.element.get_pset(slab, name="Pset_ConcreteElementGeneral")["StrengthClass"]
            reinforcement1 = ifcopenshell.util.element.get_pset(slab, name="Pset_ConcreteElementGeneral")["ReinforcementVolumeRatio"]
            precast1 = ifcopenshell.util.element.get_pset(slab, name="Pset_ConcreteElementGeneral")["CastingMethod"]
        else:
            concrete1 = None
            reinforcement1 = None
            precast1 = None
        area1 = ifcopenshell.util.element.get_pset(slab, name="Dimensions")["Area"]
        thickness1 = ifcopenshell.util.element.get_pset(slab, name="Dimensions")["Thickness"]
        reuse1 = ifcopenshell.util.element.get_pset(slab, name="Phasing")["Phase Created"]
        slabProps = np.array([name1,ext1,mat1,concrete1,thickness1,reinforcement1,reuse1,precast1,area1])
        slabList = np.vstack((slabList,slabProps))

    slabList = np.delete(slabList, (0), axis=0)
    slabList = pd.DataFrame(slabList)
    slabList = slabList.sort_values(by=[0,1,2,3,4,5,6,7])
    slabList = np.array(slabList)

    for i in range(len(slabList)):
        if i != 0:
            if slabList[i,0] == slabList[i-1,0] and slabList[i,1] == slabList[i-1,1] and slabList[i,2] == slabList[i-1,2] and slabList[i,3] == slabList[i-1,3] and slabList[i,4] == slabList[i-1,4] and slabList[i,5] == slabList[i-1,5] and slabList[i,6] == slabList[i-1,6] and slabList[i,7] == slabList[i-1,7]:
                slabList[i,8] = round(float(slabList[i-1,8]) + float(slabList[i,8]),2)
                slabList[i-1] = [0,0,0,0,0,0,0,0,0]

    slabList = slabList[~np.all(slabList == 0, axis=1)]
    return slabList