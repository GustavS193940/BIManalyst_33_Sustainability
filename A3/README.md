# About the Tool
# Claim the Tool is Solving

The tool solves the issue of incomplete, incosistent, or missing sustainability, related data in IFC models. This tool solves these problematic areas by:
 * Fixing the schema from IFC4X3 to IFC4X3_ADD2
 * Adding missing Psets to beams, columns, walls, and slabs
 * Enriching elements with standardized parameters
 * Ensuring completeness through IDS validation
 * Exporting structured data (JSON + Excel) for advanced building analysis

# Where the Problem was Found

The problems were discoverd during:
 * Model inspection in Blender (missing Psets, incorrect schema)
 * Use Case Analysis A2 (workflow inefficiencies, missing structured parameters)
The existing workflow required many manual corrections, which are now automated.

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

# Advanced Building Design

**Which stage is the tool useful for?**
The tool is most useful in Stage B – Model Development & Coordination because this is where:
* property sets must be correctly defined
* model completeness is checked
* structured data is required for sustainability analysis, costing, structural design, etc.
It could also support Stage C (Design Analysis) and Stage D (Documentation & LCA), but the primary value is early coordination (Stage B).

**Which subjects might use it?**
 * Architectural Engineering
 * Sustainability/LCA analysis
 * Material quantification and cost analysis

**What information is required in the model**
For the tool to work correctly, the IFC must contain:
 * Correct element types (IfcBeam, IfcColumn, IfcWall, IfcSlab)
 * Valid GlobalIds (used for populating slab dimensions & phasing)
 * Consistent structure and geometry (so extraction can calculate areas/volumes)
The tool adds missing Psets, but it still needs basic IFC structure to exist.







