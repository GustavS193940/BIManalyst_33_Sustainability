# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 13:46:29 2025

@author: gusta
"""

import ifcopenshell as ifc
import ifcopenshell.util.classification
import ifcopenshell.util.selector
import ifcopenshell.api.pset_template.add_pset_template

with open('25-16-D-STR.ifc','r') as file:
    filedata = file.read()
    filedata = filedata.replace("FILE_SCHEMA(('IFC4X3'))","FILE_SCHEMA(('IFC4X3_ADD2'))")
    
with open('25-16-D-STR-fixed.ifc','w') as file:
    file.write(filedata)

model = ifc.open('25-16-D-STR-fixed.ifc')
beams = model.by_type('IfcBeam')
columns = model.by_type('IfcColumn')
walls = model.by_type('IfcWall')
slabs = model.by_type('IfcSlab')

for beam in beams:
    pset = ifcopenshell.api.pset.add_pset(model, product=beam, name="Pset_ConcreteElementGeneral")
    if beam.Name == 'Structural Framing : Concrete - Rectangular (framing) : 200x520 mm':
        ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 110,"CastingMethod": "INSITU","StrengthClass":"C30"})
    elif beam.Name == 'Structural Framing : Concrete - Rectangular (framing) : 250x400mm':
        ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 110,"CastingMethod": "INSITU","StrengthClass":"C30"})
    elif beam.Name == 'Structural Framing : Concrete - Rectangular (framing) : 300x400mm':
        ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 110,"CastingMethod": "INSITU","StrengthClass":"C30"})

for column in columns:
    pset = ifcopenshell.api.pset.add_pset(model, product=column, name="Pset_ConcreteElementGeneral")
    pset2 = ifcopenshell.api.pset.add_pset(model, product=column, name="Materials and Finishes")
    if column.Name == 'Structural Columns : Concrete - Rectangular (column) : 200x200 mm':
        ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 150,"CastingMethod": "INSITU","StrengthClass":"C30"})
    elif column.Name == 'Structural Columns : Concrete - Rectangular (column) : 320x200 mm':
        ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 150,"CastingMethod": "INSITU","StrengthClass":"C30"})
    elif column.Name == 'Structural Columns : Concrete - Rectangular (column) : 450x200 mm':
        ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 150,"CastingMethod": "INSITU","StrengthClass":"C30"})
    elif column.Name == 'Structural Columns : Concrete - Rectangular (column) : 700x200 mm':
        ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 150,"CastingMethod": "INSITU","StrengthClass":"C30"})
    elif column.Name == 'Structural Columns : Wood - Rectangular (column) : 165x165 mm':
        ifcopenshell.api.pset.edit_pset(model,pset=pset2, properties={"Structural Material": "Construction Wood"})

for wall in walls:
    pset = ifcopenshell.api.pset.add_pset(model, product=wall, name="Pset_ConcreteElementGeneral")
    pset2 = ifcopenshell.api.pset.add_pset(model, product=wall, name="Construction")
    pset3 = ifcopenshell.api.pset.add_pset(model, product=wall, name="Materials and Finishes")
    if wall.Name == 'Walls : Basic Wall : Exterior - 515mm Woood / Insulation - facadelements':
        model.remove(wall)
    elif wall.Name == 'Walls : Basic Wall : Exterior - 560mm Masonry / Insulation / Concrete':
        ifcopenshell.api.pset.edit_pset(model,pset=pset2, properties={"Width": 150})
        ifcopenshell.api.pset.edit_pset(model,pset=pset3, properties={"Structural Material": "Concrete"})
        ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 60,"CastingMethod": "INSITU","StrengthClass":"C30"})
    elif wall.Name == 'Walls : Basic Wall : Fire wall - 37mm':
        ifcopenshell.api.pset.edit_pset(model,pset=pset2, properties={"Width": 37})
        ifcopenshell.api.pset.edit_pset(model,pset=pset3, properties={"Structural Material": "Fire Batts"})
    else:
        ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 60,"CastingMethod": "PRECAST","StrengthClass":"C30"})

for slab in slabs:
    pset = ifcopenshell.api.pset.add_pset(model, product=slab, name="Pset_ConcreteElementGeneral")
    ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 130,"CastingMethod": "INSITU","StrengthClass":"C25"})
    pset2 = ifcopenshell.api.pset.add_pset(model, product=slab, name="Dimensions")
    pset3 = ifcopenshell.api.pset.add_pset(model, product=slab, name="Phasing")
    pset4 = ifcopenshell.api.pset.add_pset(model, product=slab, name="Materials and Finishes")
    if slab.GlobalId == "3U2sAiBvDBrA_SHCDuGT7q":
        ifcopenshell.api.pset.edit_pset(model,pset=pset2, properties={"Area": 966.4,"Thickness": 120.0})
        ifcopenshell.api.pset.edit_pset(model,pset=pset3, properties={"Phase Created": "New Construction"})
    elif slab.GlobalId == "3U2sAiBvDBrA_SHC9uGT7q":
        ifcopenshell.api.pset.edit_pset(model,pset=pset2, properties={"Area": 19.9,"Thickness": 120.0})
        ifcopenshell.api.pset.edit_pset(model,pset=pset3, properties={"Phase Created": "New Construction"})
    elif slab.GlobalId == "3U2sAiBvDBrA_SHC5uGT7q":
        ifcopenshell.api.pset.edit_pset(model,pset=pset4, properties={"Structural Material": "Concrete"})


model.write('25-16-D-STR-fixed.ifc')