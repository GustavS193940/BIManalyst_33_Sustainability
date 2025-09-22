import ifcopenshell

from rules import NFARule

model = ifcopenshell.open("path/to/ifcfile.ifc")

NFAResult = NFARule.checkRule(model)

print("NFA result: The net floor area in the model is", NFAResult,"m²")
