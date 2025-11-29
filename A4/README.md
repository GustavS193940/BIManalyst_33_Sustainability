# Tutorial
## Summary
Title: LCA calculation of the STR-model  
Category: Materials / LCA / Sustainability Assessment  
Description: The tool creates an entire LCA calculation of the STR-model. It does this by taking quantities and materials from the model and writing them into a json-file that can be imported directly into LCAbyg.
## Video tutorial
VIDEO LINK HERE
## Code Examples
### IDS
The IDS is the first thing to run when running the tool. It is essentially a function made up of multiple instances of the smaller function in the code block below. Basically, it will check if the element has a given property followed by checking whether that property has a value. If the property either does not exist or has no value, it will add the element and the missing property to an array, which keeps track of all the identified missing properties.

```
def propCheck(element, pset, prop, errorcount, errors):
    try:
        ifc.util.element.get_pset(element, pset, prop)
        if ifc.util.element.get_pset(element, pset, prop) is None:
            error = np.array([str(element.Name),str(pset),str(prop)])
            errors = np.vstack((errors,error))
            errorcount = errorcount+1
    except:
        error = np.array([str(element.Name),str(pset),str(prop)])
        errors = np.vstack((errors,error))
        errorcount = errorcount+1
    return errorcount, errors
```
    
### Data extraction
The data extraction happens by pulling the relevant properties for each element of a given type and placing them as a row in an array. It then sorts the array, putting identical elements next to each other, before summing identical elements together. The following code block extracts the beams. For other element types there is a similar piece of code, just adapted to pull the properties relevant to their types.
```
def getBeams(model):
    beams = model.by_type('IfcBeam')
    beamList = np.array([0,1,2,3,4,5,6])

    for beam in beams:
        name1 = beam.Name
        mat1 = ifcopenshell.util.element.get_pset(beam, name="Materials and Finishes")["Structural Material"]
        if "Concrete" in mat1:
            concrete1 = ifcopenshell.util.element.get_pset(beam, name="Pset_ConcreteElementGeneral")["StrengthClass"]
            reinforcement1 = ifcopenshell.util.element.get_pset(beam, name="Pset_ConcreteElementGeneral")["ReinforcementVolumeRatio"]
        else:
            concrete1 = None
            reinforcement1 = None
        length1 = ifcopenshell.util.element.get_pset(beam, name="Structural")["Cut Length"]/1000
        volume1 = ifcopenshell.util.element.get_pset(beam, name="Dimensions")["Volume"]
        reuse1 = ifcopenshell.util.element.get_pset(beam, name="Phasing")["Phase Created"]
        beamProps = np.array([name1,mat1,concrete1,reinforcement1,reuse1,volume1,length1])
        beamList = np.vstack((beamList,beamProps))

    beamList = np.delete(beamList, (0), axis=0)
    beamList = pd.DataFrame(beamList)
    beamList = beamList.sort_values(by=[0,1,2,3,4])
    beamList = np.array(beamList)

    for i in range(len(beamList)):
        if i != 0:
            if beamList[i,0] == beamList[i-1,0] and beamList[i,1] == beamList[i-1,1] and beamList[i,2] == beamList[i-1,2] and beamList[i,3] == beamList[i-1,3] and beamList[i,4] == beamList[i-1,4]:
                beamList[i,5] = float(beamList[i-1,5]) + float(beamList[i,5])
                beamList[i,6] = float(beamList[i-1,6]) + float(beamList[i,6])
                beamList[i-1] = [0,0,0,0,0,0,0]

    beamList = beamList[~np.all(beamList == 0, axis=1)]
    return beamList
```

### Output to json
Outputting the data in an LCAbyg-compatible json-file requires writing all the extracted data into one really long string. This meant a function like the following for each element type. Essentially, it is a piece of code that codes a building element into LCAbyg by placing all the extracted data into the relevant places in a long string.

```
def writeBeams(beamList):
    beamElementID = str(uuid.uuid4())  
    beamString = ',{"Node": {"Element": {"id": "' + beamElementID + r'","name": {"English": "Beams"},"source": "User","comment": {"Danish": "","Norwegian": "","German": "","English": ""},"enabled": true,"excluded_scenarios": []}}},{"Edge": [{"CategoryToElement": {"id": "'+str(uuid.uuid4())+'"}},"ec9ee040-9c1d-4cae-864c-4c6a0e4b8c5b","'+ beamElementID +r'"]}'

    for i in range(len(beamList)):
        constUUID = str(uuid.uuid4())
        amount = round(beamList[i,6],2)
        constString = ',{"Edge": [{"ElementToConstruction": {"id": "'+ str(uuid.uuid4()) +'","amount": '+ str(amount) +',"enabled": true,"special_conditions": false,"excluded_scenarios": []}},"'+beamElementID+'","'+constUUID+'"]},{"Node": {"Construction": {"id": "'+ constUUID +'","name": {"English": "'+str(beamList[i,0])+'"},"unit": "M","source": "User","comment": {"German": "","Danish": "","Norwegian": "","English": ""},"locked": false}}},{"Edge": [{"CategoryToConstruction": {"id": "'+str(uuid.uuid4())+'","layers": [1]}},"ec9ee040-9c1d-4cae-864c-4c6a0e4b8c5b","'+constUUID+'"]}'
        beamString = beamString + constString
        if beamList[i,4] == "New Construction":
            RSL = 120
        else:
            RSL = 0

        if "Concrete" in beamList[i,1]:
            conAmount = float(beamList[i,5])/float(beamList[i,6])
            reinforcement = float(beamList[i,3])*conAmount
            for x in range(len(LCAConcrete)):
                if beamList[i,2] == LCAConcrete[x,0]:
                    concreteString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(conAmount,2))+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[x,1]+'"]}'
                    reinfString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(round(reinforcement,2))+',"unit": "KG","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAConcrete[10,1]+'"]}'
                    beamString = beamString + concreteString + reinfString
        elif "Glulam" in beamList[i,1]:
            gluAmount = round(float(beamList[i,5])/float(beamList[i,6]),4)
            gluString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(gluAmount)+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAMat[1,1]+'"]}'
            beamString = beamString + gluString
        elif "Steel" in beamList[i,1]:
            steAmount = round(float(beamList[i,5])/float(beamList[i,6])*7850,2)
            steString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(steAmount)+',"unit": "KG","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAMat[0,1]+'"]}'
            beamString = beamString + steString
        elif "Wood" in beamList[i,1]:
            timAmount = round(float(beamList[i,5])/float(beamList[i,6]),4)
            timString = ',{"Edge": [{"ConstructionToProduct": {"id": "'+str(uuid.uuid4())+'","amount": '+str(timAmount)+',"unit": "M3","lifespan": '+str(RSL)+',"demolition": false,"delayed_start": 0,"enabled": true,"excluded_scenarios": []}},"'+constUUID+'","'+LCAMat[2,1]+'"]}'
            beamString = beamString + timString
    return beamString
```

Once that is done, it will then create a folder named 'Json' (if it doesn't already exist). Then it will take all the strings created for each element and turn them into one really long string, which is then written into a json-file in the created folder. That json-file can then be imported directly into LCAbyg.

```
def writeJson(beams,columns,walls,slabs):
    baseString = '[  {    "Node": {      "Project": {        "id": "2f95c41e-0cc4-4b6e-90ac-ffa796aecd6d",        "name": {          "Danish": ""        },        "address": "",        "owner": "",        "lca_advisor": "",        "building_regulation_version": ""      }    }  },  {    "Edge": [      {        "MainBuilding": "bd294743-9c10-47c8-bce2-6b0593cb6852"      },      "2f95c41e-0cc4-4b6e-90ac-ffa796aecd6d",      "7791681b-40a2-401d-ac38-a2f73d736ab4"    ]  },  {    "Node": {      "Building": {        "id": "7791681b-40a2-401d-ac38-a2f73d736ab4",        "scenario_name": "Original bygningsmodel",        "locked": "Unlocked",        "description": {          "German": "",          "Danish": "",          "English": "",          "Norwegian": ""        },        "building_type": "Office",        "heated_floor_area": 0.0,        "gross_area": 0.0,        "integrated_garage": 0.0,        "external_area": 0.0,        "gross_area_above_ground": 0.0,        "person_count": 0,        "building_topology": "Unknown",        "project_type": "New",        "storeys_above_ground": 0,        "storeys_below_ground": 0,        "storey_height": 0.0,        "initial_year": 2023,        "calculation_timespan": 50,        "calculation_mode": "BR23",        "outside_area": 0.0,        "plot_area": 0.0,        "energy_class": "LowEnergy"      }    }  },  {    "Edge": [      {        "BuildingToRoot": "e2ff039e-2328-4d9c-a792-01bd101f93a1"      },      "7791681b-40a2-401d-ac38-a2f73d736ab4",      "216cf5d6-3e9d-43ec-b0d8-5aee02240c28"    ]  },  {    "Edge": [      {        "BuildingToOperation": "67f5d798-3456-43b0-b6b9-fccdee63b17b"      },      "7791681b-40a2-401d-ac38-a2f73d736ab4",      "0338d31e-3876-440d-a88c-2daa2dd81942"    ]  },  {    "Edge": [      {        "BuildingToDGNBOperation": "4fab0de9-5738-4a1c-9a15-0a257a0f7743"      },      "7791681b-40a2-401d-ac38-a2f73d736ab4",      "181acc05-4bd0-4131-bbf5-eef64c9bf164"    ]  },  {    "Node": {      "EmbodiedRoot": {        "id": "216cf5d6-3e9d-43ec-b0d8-5aee02240c28"      }    }  },  {    "Edge": [      {        "RootToModel": "1191a67b-c672-43fc-b2b7-724bc62b974a"      },      "216cf5d6-3e9d-43ec-b0d8-5aee02240c28",      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2"    ]  },  {    "Edge": [      {        "RootToConstructionProcess": "48781119-3992-4e48-9099-e8e8654a4935"      },      "216cf5d6-3e9d-43ec-b0d8-5aee02240c28",      "349738da-9747-4d5c-b508-2a810317166f"    ]  },  {    "Node": {      "Operation": {        "id": "0338d31e-3876-440d-a88c-2daa2dd81942",        "electricity_usage": 0.0,        "heat_usage": 0.0,        "electricity_production": 0.0      }    }  },  {    "Edge": [      {        "ElectricitySource": "af579fc8-0cad-40df-a3a4-ca36966aab9c"      },      "0338d31e-3876-440d-a88c-2daa2dd81942",      "e967c8e7-e73d-47f3-8cba-19569ad76b4d"    ]  },  {    "Edge": [      {        "HeatingSource": "e7601042-b8f2-4226-ae0a-2c1a4c5686bf"      },      "0338d31e-3876-440d-a88c-2daa2dd81942",      "6cdeb050-90e5-46b3-89ad-bfcc8e246b47"    ]  },  {    "Node": {      "DGNBOperationReference": {        "id": "181acc05-4bd0-4131-bbf5-eef64c9bf164",        "heat_supplement": 0.0,        "electricity_supplement": 0.0      }    }  },  {    "Node": {      "ElementModel": {        "id": "aeefab8a-e825-4d14-b0c3-e87b7759e5b2"      }    }  },  {    "Edge": [      {        "ParentTo": "49bb8f71-6d02-48bf-986d-3fa6db9e9b92"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "0ae65810-51bc-4130-89a0-9c107f1aca3f"    ]  },  {    "Edge": [      {        "ParentTo": "4640fd41-1a2c-4bb9-bd0a-7d1cd85b102e"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "20c75334-735c-442f-a541-985ac5a130c8"    ]  },  {    "Edge": [      {        "ParentTo": "7911defb-6013-4cd7-ae97-ed870ed7cb47"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "9e7adf74-5281-4aa4-9cff-d903a4266aae"    ]  },  {    "Edge": [      {        "ParentTo": "b879ae4c-15d5-4f6a-91e1-4b575702436b"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "bae7f4b9-967c-4542-bc99-f744aa261424"    ]  },  {    "Edge": [      {        "ParentTo": "4ff922e8-982f-436e-a3b7-efecb987c5a6"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "ca17092d-2a42-4941-b478-669b12001556"    ]  },  {    "Edge": [      {        "ParentTo": "6d2c715d-847c-4866-9bd7-a2b8defdf6a7"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "487184b7-5568-497b-b7e2-e8d2269e51ef"    ]  },  {    "Edge": [      {        "ParentTo": "0e59acae-729c-4bc5-bea8-5b4b2abba72a"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "a1746ce9-3d06-424c-a701-34a090f08433"    ]  },  {    "Edge": [      {        "ParentTo": "1cf888c3-deb9-42d0-a702-1cc1818e5dc1"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "571650a7-4259-4cc1-9d56-a12e516fd495"    ]  },  {    "Edge": [      {        "ParentTo": "e009ab41-7be2-40ce-aafe-78b2cc86fb47"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "e5937376-1d7f-4edf-9710-cafd7fe91606"    ]  },  {    "Edge": [      {        "ParentTo": "708fa945-e639-43f5-90dc-2d9719963254"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "6808ac7b-2a79-45a6-8013-5f89ad13c337"    ]  },  {    "Edge": [      {        "ParentTo": "b576344e-eccf-4735-94f3-23ce5a6e2d0c"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "f7737ac7-ea51-488e-81de-9c1bab1c08bf"    ]  },  {    "Edge": [      {        "ParentTo": "0efa66cb-2308-4e75-8d38-34c9b130af78"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "3cb417d3-d615-402e-81dc-d7d587e83ac1"    ]  },  {    "Edge": [      {        "ParentTo": "badc823a-c90b-4ef9-890c-34690bb410eb"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "ac7112e7-ccea-4e1b-a6a2-9c9c3b9a7177"    ]  },  {    "Edge": [      {        "ParentTo": "a2320d34-9ef5-42c3-a9ca-6e48303e7656"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "1e853d01-fce5-4947-850d-e0b43e51b1fc"    ]  },  {    "Edge": [      {        "ParentTo": "4fa14d2c-f70f-4cd5-b1c6-c303821aa2a6"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "d50ad0a5-636a-4169-b4d7-21e9b64d94a8"    ]  },  {    "Edge": [      {        "ParentTo": "25b12d48-dbd3-4851-aa40-306a099d45f1"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "dad100a3-f570-4c96-bec0-9028bc5f6835"    ]  },  {    "Edge": [      {        "ParentTo": "af67e91b-9651-46e2-9abe-caaa46b6ea0f"      },      "aeefab8a-e825-4d14-b0c3-e87b7759e5b2",      "de3a2393-388c-4079-9e7d-6529c14f8a69"    ]  },  {    "Node": {      "ConstructionProcess": {        "id": "349738da-9747-4d5c-b508-2a810317166f"      }    }  },  {    "Edge": [      {        "ProcessToInstallation": "dd928199-b70a-43f8-8556-4f740dccd1ef"      },      "349738da-9747-4d5c-b508-2a810317166f",      "020cc362-536b-484e-b8f9-6507b40ab675"    ]  },  {    "Edge": [      {        "ProcessToTransport": "15867192-86b7-40a8-9936-83d9e998516e"      },      "349738da-9747-4d5c-b508-2a810317166f",      "915c5162-93bc-49c0-bdaf-9f470b4c7998"    ]  },  {    "Node": {      "ConstructionInstallation": {        "id": "020cc362-536b-484e-b8f9-6507b40ab675"      }    }  },  {    "Edge": [      {        "FuelUsage": "f069389f-b870-4c63-9362-88dc8c9912c9"      },      "020cc362-536b-484e-b8f9-6507b40ab675",      "5e5ccea5-5243-494b-9a49-292ada027abe"    ]  },  {    "Edge": [      {        "InstallationOperation": "082b809c-9850-4a72-8dbb-7ec74d0fec15"      },      "020cc362-536b-484e-b8f9-6507b40ab675",      "c33cf608-9ceb-47f3-9ccf-c3ecb58ddb96"    ]  },  {    "Node": {      "ProductTransportRoot": {        "id": "915c5162-93bc-49c0-bdaf-9f470b4c7998"      }    }  },  {    "Node": {      "FuelConsumption": {        "id": "5e5ccea5-5243-494b-9a49-292ada027abe"      }    }  },  {    "Edge": [      {        "TransportTypeUsage": {          "id": "899c9a7c-b616-49ac-8937-088ac10b2537",          "distance": 0.0        }      },      "5e5ccea5-5243-494b-9a49-292ada027abe",      "1adea09d-d954-4b9f-9a95-fa3cee0c4787"    ]  },  {    "Edge": [      {        "TransportTypeUsage": {          "id": "59292514-bf7b-4c89-a816-fe528cb07530",          "distance": 0.0        }      },      "5e5ccea5-5243-494b-9a49-292ada027abe",      "b0ca9d35-fdfe-4e29-8d65-1032bf5a220a"    ]  },  {    "Node": {      "Operation": {        "id": "c33cf608-9ceb-47f3-9ccf-c3ecb58ddb96",        "electricity_usage": 0.0,        "heat_usage": 0.0,        "electricity_production": 0.0      }    }  },  {    "Edge": [      {        "ElectricitySource": "5a38b95a-e2ce-4802-8576-39511c9fd155"      },      "c33cf608-9ceb-47f3-9ccf-c3ecb58ddb96",      "e967c8e7-e73d-47f3-8cba-19569ad76b4d"    ]  },  {    "Edge": [      {        "HeatingSource": "a37552fd-fb25-4d95-bf09-64df9f752a29"      },      "c33cf608-9ceb-47f3-9ccf-c3ecb58ddb96",      "6cdeb050-90e5-46b3-89ad-bfcc8e246b47"    ]  }'

    if not os.path.exists(r'Json'):
        os.makedirs(r'Json')
    FullJson = baseString + writeBeams(beams) + writeColumns(columns) + writeWalls(walls)[0] + writeWalls(walls)[1] + writeSlabs(slabs)[0] + writeSlabs(slabs)[1] + ']'
    FullJson = json.loads(FullJson.replace("\'", '"'))
    with open('Json/LCACalc.json', 'w') as outfile:
        json.dump(FullJson, outfile)
    return
```

### Model Fix
The STR-model we have used is missing a lot of the necessary properties to work with the tool. Normally, if you are working on a project, you would return the model to the STR-engineer in charge of it and they would add the relevant properties. Since we do not have access to whoever created the model, we have made a piece of code that simulates a STR-engineer "fixing" the model. It is not considered a part of the tool, however, it is necessary for showcasing the tool's capabilities. It is essentially a python-file hard-coded to add the missing properties to this specific model. We have identified, through use of an early iteration of the IDS, what properties are missing from the model, and created this code to specifically add those properties only to the elements that are missing them. Note that it only fixes the model to a degree that makes it compatible with the tool. Any properties that have been defined wrong (eg. internal walls being modelled as external, existing elements being modelled as new) without affecting the functionality of the tool have not been corrected.

```
for beam in beams:
    pset = ifcopenshell.api.pset.add_pset(model, product=beam, name="Pset_ConcreteElementGeneral")
    if beam.Name == 'Structural Framing : Concrete - Rectangular (framing) : 200x520 mm':
        ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 110,"CastingMethod": "INSITU","StrengthClass":"C30"})
    elif beam.Name == 'Structural Framing : Concrete - Rectangular (framing) : 250x400mm':
        ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 110,"CastingMethod": "INSITU","StrengthClass":"C30"})
    elif beam.Name == 'Structural Framing : Concrete - Rectangular (framing) : 300x400mm':
        ifcopenshell.api.pset.edit_pset(model,pset=pset, properties={"ReinforcementVolumeRatio": 110,"CastingMethod": "INSITU","StrengthClass":"C30"})
```
