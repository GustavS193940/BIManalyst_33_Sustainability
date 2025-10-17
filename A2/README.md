# A2: Use Case

## A2a: About The Group 
Our group 33 has chosen to focus on environmental performance validation through **Life Cycle Assessment (LCA)** and **Global Warming Potential (GWP)** evaluation of Buliding 2516.

**Group Role**: Analyst We are responsible for identifying and verifying sustainability relaited claims in the BIM model, focusing on material quantities anc their environmental impact. 
**Group Coding Confidence**: We collectively rate our Python confidence at 4 (Strongly agree), as Nafsika Theou s253100 is a 1 and Søgaard, Gustav Guldager Marker s193940 is a 3. 
**Focus Area**: Environmental Sustainability - LCA and GWP We are particularly interested in developing a tool that extracts material data directly from the IFC model and connects it to environemntal databases such as LCAbyg, and to verify CO2 footprint claims.

## A2b: Identify Claim
We have chosen to work with **Building 2516 (Building 115)**. After reviewing the available structural anc sustainability documentation, we adentified a strong focus on reducing embodied carbon through material choices, and specifically by combining reinforced concrete with new timber and steel structures.

**The client report** presents an LCA calculation with an environmental impact of **32.83 kg CO2-eq./m2/user/year**, equivalent to **4.723 kg CO2-eq./m2/year** according to BR18 standards.

Our claim to validate is that the proposed renovation achieves this low CO2 footprint through the material composition anc reuse strategy described. To verify this, we propose creating an analytical tool capable of calculating total embodied carbon by:
* Extracting **all material quantities** (concrete, steel, timber, insulation, cladding) from the structural IFC models.
* Linking them to **LCAbyg CO2-equivalent factors**.
* Estimating total **kg CO2-eq/m2/year** for comparison with the reported LCA results.
By focusing on all structural and envelope materials, we can assess whether the renovation's CO2 footprint is realistic and aligned with Danish sustainability benchmarks (e.g.<12 kg CO2-eq./m2/year).

**Justification for Selection**: This claim reflects a core sustainability challenge by balancing **material reuse, biogenic substitution, and structural adaptation**. By simulating available BIM and environemtal data, we can inform how BIM tools can automate and validate sustainability metrics.

## A2c: Use Case
* How we would check this claim
  1. First we will **extract material data** from the IFC model using Python scripts in Spyder
  Identify all structural and envelope elements and their associated materials (concrete, steel, timber, insulation, and cladding)
  2. **Quantify material volumes or masses** using parameters in the model (dimensions, density)
  3. **Link each material** to the appropriate CO2 conversion factors from LCAbyg
  4. **Calculate total embodied CO2** for all materials combined
  5. **Normalize results** per m2 of grozs floor area to obtain kg CO2-eq./m2/year
  6. **Compare output** with the relorted LCA results to validate the claim
* When this claim needs to be checked
During the **design phase**, when material selection and stuctural strategies are defined. The verification process ensures that design decisions align with the project's sustainability goals and danish regulations.
* Information required for this claim
  * Material specifications anc types used in the model
  * Volume, density, and surface area of each element
  * CO2 emission factors from LCAbyg
  * Building area for normalization
  * Structural Ifc model files
* Phase
In the design phase when the assessement supports design optimization and regulatory documentation
* BIM Purpose
  * Analyse: Quantify material impacts and evaluate CO2 footprint
  * Communicate: Present LCA findings clearly for design teams anc certification purposes (e.g. DGNB Gold)
  * Review of Closest Use Cases
* A relevant example was found in a previous Advanced Building Design (Building 2406), where the group 35 verified a **CO2 footprint claim** by calculating the volume of concrete from the IFC model and comparing it with **LCAbyg** emission factors.
This use case demonstrates how BIM data can be used to automatically extract material quantities and link them to environmental databases for validation.
The process aligns closely with our approach, as both focus in material-driven life cycle assessment and the automation of GWP calculations.
The main difference is that our case expands the focus beyond concrete to incluce all major structural materials, aiming for a more holistic and comparative analysis of the total carbon impact.

* BPMN Diagram
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
