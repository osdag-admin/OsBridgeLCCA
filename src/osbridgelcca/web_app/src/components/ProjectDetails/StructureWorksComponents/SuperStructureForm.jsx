"use client"
import Form from "./Form"

// Foundation form specific configuration
const SuperStructureForm = ({ onClose,currentForm = 'SuperStructure', onNavigate, setActiveTabs,Activetabs,onclicktabs }) => {
  // Component options for the foundation form
  const componentOptions = [
    { value: "Deck", label: "Deck" },
    { value: "Cables", label: "Cables" },
  ]

  // Material options for each component
  const materialOptions = {
    Deck: [
      { value: "Soil", label: "Soil" },
      { value: "Sand", label: "Sand" },
      { value: "Gravel", label: "Gravel" },
    ],
    "Cables": [
      { value: "Concrete", label: "Concrete" },
      { value: "Steel", label: "Steel" },
      { value: "Formwork", label: "Formwork" },
    ],
  }

  // Initial materials for the foundation form
  const initialFoundationMaterials = [
    {
      id: 1,
      component: "Deck",
      materialType: "",
      quantity: "",
      unit: "m³",
      rate: "",
      rateDataSource: "",
    },
    {
      id: 2,
      component: "Deck",
      materialType: "",
      quantity: "",
      unit: "kg",
      rate: "",
      rateDataSource: "",
    },
    {
      id: 3,
      component: "Cables",
      materialType: "Concrete",
      quantity: "",
      unit: "m³",
      rate: "",
      rateDataSource: "",
    },
    {
      id: 4,
      component: "Cables",
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
        title="SuperStructure"
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

export default SuperStructureForm
