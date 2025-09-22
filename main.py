import ifcopenshell

from rules import NFARule

model = ifcopenshell.open('25-16-D-ARCH.ifc')

NFAResult = NFARule.checkRule(model)

print("NFA result: The net floor area in the model is", round(NFAResult,0),"m²")
