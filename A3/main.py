# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 13:18:40 2025

@author: gusta
"""

import ifcopenshell as ifc

from extract import getBeams, getColumns, getWalls, getSlabs
from export import writeJson, writeExcel
from IDS import modelCheck

model = ifc.open('MODEL FILEPATH HERE')

valid = modelCheck(model)

if valid == True:
    ### BEAMS ###
    beams = getBeams(model)

    ### COLUMNS ###
    columns = getColumns(model)

    ### WALLS ###
    walls = getWalls(model)

    ### SLABS ###
    slabs = getSlabs(model)

    ### Create the json-file ###
    writeJson(beams,columns,walls,slabs)

    ### Create Excel-files ###
    writeExcel(beams,columns,walls,slabs)