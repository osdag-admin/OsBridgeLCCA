"use client"
import Form from "./Form"

// Foundation form specific configuration
const MiscellaneousForm = ({ onClose,currentForm = 'Miscellaneous', onNavigate, setActiveTabs,Activetabs,onclicktabs }) => {
  // Component options for the foundation form
  const componentOptions = [
    { value: "Expansion Joint", label: "Expansion Joint" },
    { value: "Bearing", label: "Bearing" },
  ]

  // Material options for each component
  const materialOptions = {
    ExpansionJoint: [
      { value: "Soil", label: "Soil" },
      { value: "Sand", label: "Sand" },
      { value: "Gravel", label: "Gravel" },
    ],
    "Bearing": [
      { value: "Concrete", label: "Concrete" },
      { value: "Steel", label: "Steel" },
      { value: "Formwork", label: "Formwork" },
    ],
  }

  // Initial materials for the foundation form
  const initialFoundationMaterials = [
    {
      id: 1,
      component: "Expansion Joint",
      materialType: "",
      quantity: "",
      unit: "m³",
      rate: "",
      rateDataSource: "",
    },
    {
      id: 2,
      component: "Expansion Joint",
      materialType: "",
      quantity: "",
      unit: "kg",
      rate: "",
      rateDataSource: "",
    },
    {
      id: 3,
      component: "Bearing",
      materialType: "Concrete",
      quantity: "",
      unit: "m³",
      rate: "",
      rateDataSource: "",
    },
    {
      id: 4,
      component: "Bearing",
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
        title="Miscellaneous"
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

export default MiscellaneousForm
