# About the Tool
# Claim the Tool is Solving

The tool solves the issue of incomplete, incosistent, or missing sustainability- related data in IFC models. In real projects, designers often omit key Psets or material informations which leads to:
 * unrealiable CO2 calculations
 * difficulties performing LCA
 * gaps in DGNB documentation

# Where the Proble was Found

The issue became clear when analysing the Structural IFC model of Building 2516 (Building 115). Several structural elements lacked necessary information such as material, volume, and thickness, which directly affects the calculated value of the CO2-eq.

# Description of the Tool

The tool is a Python script using IfcOpenShell that automatically validates sustainability-relevant model data. 
It performs four main operations:

**1. Extract element data**
 * material
 * volume
 * length
 * cross-section
 * element type

**2. Group identical elements**
Elements with the same type, material, dimensions are grouped. This makes LCA preparation easier and avoids duplicates.

**3. Validate required Psets**
The tool checks whether the model contains required data such as:
 * Pset_Material
 * Pset_Reinforcement
 * Pset_Precast

Missing information is returned as a list.

**4. Export results**
Outputs are generated as:
 * JSON
 * Excel

# Instructions to Run the Tool

# Advanced Building Desing

**Which stage is the tool useful for?**
The tool is most useful in Stage C, for analyzing because this is where:
* LCA begins
* sustainability targets are evaluated
* data comppleteness becomes critical
* material alternatives are compared

**Which subjects might use it?**
 * Architectural Engineering
 * Structural Engineering
 * Sustainability/LCA analysis
 * Material quantification and cost analysis

**What information is required in the model**
For the tool to work correctly, the IFC must contain:
 * Materials
 * Geometric information
 * Psets
 * Element type







