# About the Tool
## Claim the Tool is Solving
The tool makes the LCA process significantly faster and easier by automatically creating an LCA of the STR-model.
This leaves more time for analysing and optimising the building's carbon footprint, making for a more sustainable final product.

## Where the Problem was Found
The Danish building regulations (BR18) are continually raising ambitions for sustainability in buildings, requiring significantly more effort to meet the requirements.
Therefore, any tool our ressource that can make the LCA process easier or faster can be a huge help.

## Description of the Tool

The tool is a Python script using IfcOpenShell that automatically creates an LCA calulation of the STR-model. 
It performs four main operations:

**1. IDS**
 * checks that every relevant element (beams, columns, walls, slabs) has all the necessary properties defined
 * counts the number of missing properties and outputs them in a Microsoft Excel-file
 * the rest of the tool will run only if the IDS is passed

**2. Extract material properties**
* extract element type and material property
* extract dimensions and quantities
* if material is concrete the tool extracts concrete element properties (reinforcement, strength class, casting method)
* group identical elements together (eg. beams with the same dimensions and material will be grouped into one element with the total length)

**3. Export to Excel**
* element quantities and properties are exported to Microsoft Excel-sheets for easy readability

**4. Export to json**
* material properties are connected to LCAbyg environmental data
* element quantities and properties are written into a json-file made to fit the structure in LCAbyg
* the json file can be directly imported into LCAbyg

# Instructions to Run the Tool

# Advanced Building Design

## Which stage is the tool useful for?
The tool is most useful in Stage B – Model Development & Coordination because this is where:
* models start to be created
* different structural concepts are assessed
It could also support Stage C (Design Analysis) and Stage D (Documentation & LCA).

## Which subjects might use it?
 * **Sustainability/LCA** for quicker LCA calculation and analysis
 * **Structural** for comparison of structural concepts/solutions

## What information is required in the model
The tool only uses elements with the types IfcBeam (beams), IfcColumn (columns), IfcWall (walls), and IfcSlab (slabs).
All elements (of those 4 types) must have the following properties:
* Materials and Finishes -> Structural Material
* Phasing -> Phase created

All concrete elements must have the following properties:
* Pset_ConcreteElementGeneral -> StrengthClass
* Pset_ConcreteElementGeneral -> ReinforcementVolumeRatio
* Pset_ConcreteElementGeneral -> CastingMethod

All beams must have the following properties:
* Structural -> Cut Length
* Dimensions -> Volume

All columns must have the following properties:
* Dimensions -> Length
* Dimensions -> Volume

All walls must have the following properties:
* Pset_WallCommon -> IsExternal
* Dimensions -> Area
* Construction -> Width

All slabs must have the following properties:
* Pset_SlabCommon -> IsExternal
* Dimensions -> Area
* Dimensions -> Thickness







