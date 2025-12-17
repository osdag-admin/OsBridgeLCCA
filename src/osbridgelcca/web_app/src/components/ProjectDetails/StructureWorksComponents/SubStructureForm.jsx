"use client"
import Form from "./Form"

// Foundation form specific configuration
const SubStructureForm = ({ onClose,currentForm = 'SubStructure', onNavigate, setActiveTabs,Activetabs,onclicktabs }) => {
  // Component options for the foundation form
  const componentOptions = [
    { value: "Piers", label: "Piers" },
    { value: "Abutment", label: "Abutment" },
  ]

  // Material options for each component
  const materialOptions = {
    Piers: [
      { value: "Soil", label: "Soil" },
      { value: "Sand", label: "Sand" },
      { value: "Gravel", label: "Gravel" },
    ],
    "Abutment": [
      { value: "Concrete", label: "Concrete" },
      { value: "Steel", label: "Steel" },
      { value: "Formwork", label: "Formwork" },
    ],
  }

  // Initial materials for the foundation form
  const initialFoundationMaterials = [
    {
      id: 1,
      component: "Piers",
      materialType: "",
      quantity: "",
      unit: "m³",
      rate: "",
      rateDataSource: "",
    },
    {
      id: 2,
      component: "Piers",
      materialType: "",
      quantity: "",
      unit: "kg",
      rate: "",
      rateDataSource: "",
    },
    {
      id: 3,
      component: "Abutment",
      materialType: "Concrete",
      quantity: "",
      unit: "m³",
      rate: "",
      rateDataSource: "",
    },
    {
      id: 4,
      component: "Abutment",
      materialType: "Steel",
      quantity: "",
      unit: "kg",
      rate: "",
      rateDataSource: "",
    },
  ]

  return (
    <div >
      <Form
        title="SubStructure"
        initialMaterials={initialFoundationMaterials}
        componentOptions={componentOptions}
        materialOptions={materialOptions}
        onClose={onClose || (() => console.log("Close form"))}
        currentForm={currentForm}
        onNavigate={onNavigate}
        setActiveTabs={setActiveTabs}
        Activetabs={Activetabs}
          onclicktabs={onclicktabs}
      />
    </div>
  )
}

export default SubStructureForm
