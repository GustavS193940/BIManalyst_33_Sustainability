# A2: Use Case

## A2a: About The Group 
Our group 33 has chosen to focus on environmental performance validation through **Life Cycle Assessment (LCA)** and **Global Warming Potential (GWP)** evaluation of Buliding 2516.

**Group Role**: Analyst  
We are responsible for identifying and verifying sustainability relaited claims in the BIM model, focusing on material quantities and their environmental impact. <br/>
**Group Coding Confidence**: We on average rate our Python confidence at 2 (Neutral), as Nafsika Theou s253100 is a 1 and Gustav Søgaard s193940 is a 3. <br/>
**Focus Area**: Sustainability - Materials/LCA  
We are particularly interested in developing a tool that extracts material data directly from the IFC model and connects it to environmental data in software such as LCAbyg, and to verify carbon footprint claims.

## A2b: Identify Claim
We have chosen to work with **Building 2516 (Building 115)**. After reviewing the available structural and sustainability documentation, we adentified a strong focus on reducing embodied carbon through material choices, and specifically by combining reinforced concrete with new timber and steel structures.

**Page 7 of the client report** presents LCA results with an environmental impact of **4.73 kg CO<sub>2</sub>-eq./m<sup>2</sup>/year** according to BR18 standards.

Our claim to validate is that the proposed renovation achieves this low carbon footprint through the material composition and reuse strategy described. To verify this, we propose creating an analytical tool capable of calculating total embodied carbon by:
* Extracting **all material quantities**
* Linking them to **LCAbyg environmental data**.
* Estimating total **kg CO<sub>2</sub>-eq/m<sup>2</sup>/year** for comparison with the reported LCA results.
Due to time and experience limitations, we will be limiting ourselves to only the STR-model.

**Justification for Selection**: LCA limit values in Danish building regulation were lowered earlier this year, and are expected to be lowered even more in 2027. Therefore, it is important to accurately calculate the carbon footprint of buildings to ensure that these requirements are met.

## A2c: Use Case
* How we would check this claim
  1. Ensure that the BIM-model(s) contain all required information.
  2. **Extract material data and quantities** from the BIM-model.
  3. **Input extracted data** into an appropriate LCA-software, like LCAbyg.
  4. **Calculate total embodied CO<sub>2</sub>-eq** for all materials combined.
  5. **Normalize results** per m<sup>2</sup> of gross floor area to obtain the carbon footprint in kg CO<sub>2</sub>-eq/m<sup>2</sup>/year
  6. **Compare output** with the reported LCA results to validate the claim.
* When this claim needs to be checked
The claim should be checked towards the end of each design phase, once BIM-models are completed.
* Information required for this claim
  * Material specifications and types used in the model
  * Volume, density, and surface area of each element
  * CO<sub>2</sub>-eq emission factors from LCAbyg
  * Building area for normalization
* Phase
During the **design phase**, when material selection and stuctural strategies are defined. The verification process ensures that design decisions align with the project's sustainability goals and Danish regulations.
* BIM Purpose
  * Analyse: Quantify material impacts and evaluate CO2 footprint
  * Communicate: Present LCA findings clearly for design teams anc certification purposes (e.g. DGNB Gold)
* Review of Closest Use Cases
  * A relevant example was found in a previous Advanced Building Design (Building 2406), where the group 35 verified a **CO2 footprint claim** by calculating the volume of concrete from the IFC model and comparing it with **LCAbyg** emission factors.
This use case demonstrates how BIM data can be used to automatically extract material quantities and link them to environmental databases for validation.
The process aligns closely with our approach, as both focus in material-driven life cycle assessment and the automation of GWP calculations.
The main difference is that our case expands the focus beyond concrete to incluce all major structural materials, aiming for a more holistic and comparative analysis of the total carbon impact.

* BPMN Diagram showing the use case
![BPMN Diagram for the whole use case](https://raw.githubusercontent.com/GustavS193940/BIManalyst_33_Sustainability/refs/heads/main/A2/IMG/UseCase.svg)

## A2d: Scope the Use Case
A tool is needed to make creating the LCA-calculation easier and faster, covering the steps surrounded by the dotted line on the diagram below.
![BPMN Diagram highlighting our scope](https://raw.githubusercontent.com/GustavS193940/BIManalyst_33_Sustainability/refs/heads/main/A2/IMG/UseCaseScope.svg)

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
The flow of the tool idea is summarized in the diagram below.

![BPMN Diagram showcasing the tool idea](https://raw.githubusercontent.com/GustavS193940/BIManalyst_33_Sustainability/refs/heads/main/A2/IMG/ToolIdea.svg)

## A2f: Information Requirements
For this tool to work the following information needs to be extracted from the elements in the STR-model
- Type (beam, column, slab etc.)
  - This is located in the **"Object Metadata"** of of each element in the IFC-model.
- Dimensions
  - This is found under **"Property Sets"**, specifically **"Inherited Type Properties"** with differing names depending on the element type. 
- Material
  - This is found under **"Property Sets"**, specifically **"Inherited Type Properties"** as **"Materials and Finishes"**.
- Quantity
  - This is found under **"Property Sets"**, specifically **"Occurence Properties"** as **"Dimensions"**.
For the information to be converted into an LCAbyg-compatible json-file, some of the material data will have to be edited to be easily recognized by the tool.

For all elements, we will need to add a property that describes, whether the element is new or reused.

Specifically for concrete elements, we will need to add some more information to the model.
We will need to know whether the element is precast or cast-in-place.
We will need the strength class of the concrete, which can hopefully be added in the material property as well, eg. "Concrete C30".
Lastly, we will need to know how much reinforcement steel is in the element

## A2g: Identify Appropriate Software License
We will be using LGPL 3.0 as a license, as it allows for others to use our code in closed systems as well as open.
