# BIManalyst group 33
## Materials / LCA / Sustainability
We have created a rule to check net floor area (NFA) by getting the area property from the spaces in the model.
The NFA is stated in the report '25-16-D-Client' on page 7 to be 5295 m².

### Description
The script pulls all the spaces from the model. For each space, if it has an 'Area' property, the area is added to the total NFA.
If a space does not have an 'Area' property it is ignored.

### Result
Running the script on '25-16-D-ARCH.ifc' returns a NFA of 4513 m², which differs from the client report by almost 800 m².
This suggests that either the group measured their floor area wrong or they have not properly defined all their spaces in their model.
The latter can be confirmed by selecting all the spaces in Blender, where we can see that the defined spaces do not cover the whole building.

<img width="1081" height="743" alt="image" src="https://github.com/user-attachments/assets/33dd06d3-33a8-493e-b371-be0f5ff37937" />
