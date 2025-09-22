# BIManalyst group 33
## Materials / LCA / Sustainability
We have created a rule to check net floor area (NFA) by getting the area property from the spaces in the model.
The NFA is stated in the report '25-16-D-Client' on page 7 to be 5295 m².

The script pulls all the spaces from the model. For each space, if it has an 'Area' property, the area is added to the total NFA.

