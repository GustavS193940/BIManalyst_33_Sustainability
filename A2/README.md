# A2: Use Case

## A2a: About Your Group

## A2b: Identify Claim

## A2c: Use Case

![BPMN Diagram for the whole use case](https://github.com/GustavS193940/BIManalyst_33_Sustainability/main/A2/IMG/UseCase.svg)

## A2d: Scope the Use Case

## A2e: Tool Idea
Our idea is a tool that can create an LCA calculation of the entire STR-model.
Essentially, it should be able to convert the BIM-data into LCAbyg-compatible data.
First, it needs to ensure that all elements have the required information, and let us know of any elements that do not.
Second, it needs to sort the elements in the model by type, ie. Beams, Columns, Walls etc.
Then, it needs to sum all the elements with identical dimensions and materials.

The initial goal is to then export this to an Excel-file, where it is easily readable for someone modelling an LCA in LCAbyg.
Ideally, we will be able to expand from there, making the tool export into a json-file that can be imported directly into LCAbyg.
This would be done by connecting the material properties in the model to the UUID of the same material in LCAbyg.

This tool, if fully realized, will significantly shorten the time it takes to create a building LCA, allowing for the time saved to be used for better analysis of the results or on other sustainability efforts.

![BPMN Diagram showcasing the tool idea](https://github.com/GustavS193940/BIManalyst_33_Sustainability/main/A2/IMG/ToolIdea.svg)

## A2f: Information Requirements
For this tool to work the following information needs to be extracted from the elements in the STR-model
- Type
- Dimensions
- Material
- Quantity
For the information to be converted into an LCAbyg-compatible json-file, some of the material data will have to be edited to be easily recognized by the tool.

Specifically for concrete elements, we will need to add some more information to the model.
We will need to know whether the element is precast or cast-in-place.
We will need the strength class of the concrete, which can hopefully be added in the material property as well, eg. "Concrete C30".
Lastly, we will need to know how much reinforcement steel is in the element

## A2g: Identify Appropriate Software License
We will be using LGPL 3.0 as a license for our tool as it is completely open.
