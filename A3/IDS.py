# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 15:20:12 2025

@author: gusta
"""

import numpy as np
import pandas as pd
import ifcopenshell as ifc

typeList = np.array(["IfcBeam","IfcColumn","IfcWall","IfcSlab"])
propList = np.array([["IfcBeam","Structural","Cut Length"],
                     ["IfcBeam","Dimensions","Volume"],
                     ["IfcColumn","Dimensions","Length"],
                     ["IfcColumn","Dimensions","Volume"],
                     ["IfcWall","Pset_WallCommon","IsExternal"],
                     ["IfcWall","Dimensions","Area"],
                     ["IfcWall","Construction","Width"],
                     ["IfcSlab","Pset_SlabCommon","IsExternal"],
                     ["IfcSlab","Dimensions","Area"],
                     ["IfcSlab","Dimensions","Thickness"]])

def propCheck(element, pset, prop, errorcount, errors):
    try:
        ifc.util.element.get_pset(element, pset, prop)
        if ifc.util.element.get_pset(element, pset, prop) is None:
            error = np.array([str(element.Name),str(pset),str(prop)])
            errors = np.vstack((errors,error))
            errorcount = errorcount+1
    except:
        error = np.array([str(element.Name),str(pset),str(prop)])
        errors = np.vstack((errors,error))
        errorcount = errorcount+1
    return errorcount, errors

def modelCheck(model):
    errorcount = 0
    errors = np.array([0,1,2])
    for i in range(len(typeList)):
        elements = model.by_type(typeList[i])
        for element in elements:
            pset1 = "Materials and Finishes"
            prop1 = "Structural Material"
            errorcount = propCheck(element, pset1, prop1, errorcount, errors)[0]
            errors = propCheck(element, pset1, prop1, errorcount, errors)[1]
            
            pset2 = "Phasing"
            prop2 = "Phase Created"
            errorcount = propCheck(element, pset2, prop2, errorcount, errors)[0]
            errors = propCheck(element, pset2, prop2, errorcount, errors)[1]

            if "Concrete" == ifc.util.element.get_pset(element, "Materials and Finishes", "Structural Material"):
                pset = "Pset_ConcreteElementGeneral"
                prop1 = "StrengthClass"
                errorcount = propCheck(element, pset, prop1, errorcount, errors)[0]
                errors = propCheck(element, pset, prop1, errorcount, errors)[1]
                prop2 = "ReinforcementVolumeRatio"            
                errorcount = propCheck(element, pset, prop2, errorcount, errors)[0]
                errors = propCheck(element, pset, prop2, errorcount, errors)[1]
                prop3 = "CastingMethod"
                errorcount = propCheck(element, pset, prop3, errorcount, errors)[0]
                errors = propCheck(element, pset, prop3, errorcount, errors)[1]
            for x in range(len(propList)):
                if propList[x,0] == typeList[i]:
                    pset = propList[x,1]
                    prop = propList[x,2]
                    errorcount = propCheck(element, pset, prop, errorcount, errors)[0]
                    errors = propCheck(element, pset, prop, errorcount, errors)[1]

    if errorcount > 0:
        errors = np.delete(errors, (0), axis=0)
        errors = pd.DataFrame(errors, columns=["Element Name","Pset","Missing Property"])
        errors.to_excel('Errors.xlsx',index = False)
        print(str(errorcount) + " missing properties identified. For a detailed description, see Errors.xlsx")
        valid = False
    else:
        print("Model contains all necessary properties")
        valid = True
        return valid