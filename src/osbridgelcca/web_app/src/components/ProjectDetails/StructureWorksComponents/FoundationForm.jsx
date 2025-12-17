"use client"
import Form from "./Form"
import useFormNavigation from '../UseFormNavigation'

// Foundation form specific configuration
const FoundationForm = ({ onClose, currentForm = 'Foundation', onNavigate,  setActiveTabs,Activetabs, onclicktabs }) => {
  // Component options for the foundation form
  const componentOptions = [
    { value: "Earthwork", label: "Earthwork" },
    { value: "RCC in Foundation", label: "RCC in Foundation" },
  ]

  // Material options for each component
  const materialOptions = {
    Earthwork: [
      { value: "Soil", label: "Soil" },
      { value: "Sand", label: "Sand" },
      { value: "Gravel", label: "Gravel" },
    ],
    "RCC in Foundation": [
      { value: "Concrete", label: "Concrete" },
      { value: "Steel", label: "Steel" },
      { value: "Formwork", label: "Formwork" },
    ],
  }

  // Initial materials for the foundation form
  const initialFoundationMaterials = [
    {
      id: 1,
      component: "Earthwork",
      materialType: "",
      quantity: "",
      unit: "m³",
      rate: "",
      rateDataSource: "",
    },
    {
      id: 2,
      component: "Earthwork",
      materialType: "",
      quantity: "",
      unit: "kg",
      rate: "",
      rateDataSource: "",
    },
    {
      id: 3,
      component: "RCC in Foundation",
      materialType: "Concrete",
      quantity: "",
      unit: "m³",
      rate: "",
      rateDataSource: "",
    },
    {
      id: 4,
      component: "RCC in Foundation",
      materialType: "Steel",
      quantity: "",
      unit: "kg",
      rate: "",
      rateDataSource: "",
    },
  ]

  return (
    <div>
      <Form
        title="Foundation"
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

export default FoundationForm