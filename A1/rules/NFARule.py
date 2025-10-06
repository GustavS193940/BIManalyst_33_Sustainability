import ifcopenshell as ifc
import ifcopenshell.util.classification

def checkRule(model):
    spaces = model.by_type('IfcSpace')
    ifc_NFA = 0
    for i in range(0,len(spaces)):
        space = spaces[i]
        ifc_dimensions = ifc.util.element.get_pset(space,'Dimensions')
        if 'Area' in ifc_dimensions:
            ifc_area = ifc_dimensions['Area']
            ifc_NFA += ifc_area

    return ifc_NFA

