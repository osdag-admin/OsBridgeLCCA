// import React, { useState } from "react";
// import {useFormNavigation, ConfirmationModal} from './UseFormNavigation'

// // Form sequence constant
// const MaintenanceandRepairData = ({ currentForm, onNavigate, onClose, setActiveTabs,Activetabs, onclicktabs }) => {
//   const navigation = useFormNavigation(currentForm, onNavigate);

//    const [showConfirmation, setShowConfirmation] = useState(false)
//   const [confirmationType, setConfirmationType] = useState(null)
//   const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
//   const [formData, setFormData] = useState({
//     periodicMaintenanceCost: "0.5500",
//     annualRoutineInspectionCost: "1",
//     repairRehabilitationCost: "10",
//     frequencyOfPeriodicMaintenance: "5",
//     frequencyOfRoutineInspection: "1"
//   });

//   const handleChange = (field, value) => {
//     setFormData({
//       ...formData,
//       [field]: value
//     });
//   };

//   // Suggested indicator component
//   const SuggestedTag = () => (
//     <span className="text-xs text-gray-400 ml-2">Suggested</span>
//   );

  
//   const handleNext = () => {
//     if (navigation.canGoNext) {
//       setConfirmationType('next');
//       setShowConfirmation(true);
//     }
//   };

//   // const handleBack = () => {
//   //   if (navigation.canGoBack) {
//   //     if (hasUnsavedChanges) {
//   //       setConfirmationType('back');
//   //       setShowConfirmation(true);
//   //     } else {
//   //       navigation.navigate(navigation.getPreviousForm());
//   //     }
//   //   }
//   // };
//     const handleBack = () => {
//   setConfirmationType('back')
//   setShowConfirmation(true)
// }


// const handleConfirm = async () => {
//   if (confirmationType === 'next') {
//     try {
//       // Save form data to storage
//       console.log('Saving form data:', formData);
//       await saveMaintenanceData(formData);
      
//       // Calculate maintenance costs
//       console.log('Calculating maintenance costs...');
//       const calculationResult = await calculateMaintenanceCosts(formData);
//       console.log('Maintenance costs calculated:', calculationResult);
      
//       setHasUnsavedChanges(false);
//       navigation.navigate(navigation.getNextForm());
//     } catch (error) {
//       console.error('Error processing maintenance data:', error);
//       // You might want to show an error message to the user here
//       alert('Error processing maintenance data. Please try again.');
//       return; // Don't navigate if there's an error
//     }
//   } else if (confirmationType === 'back') {
//     navigation.navigate(navigation.getPreviousForm());
//   }
//   setShowConfirmation(false);
//   setConfirmationType(null);
// };
//   const handleCloseConfirmation = () => {
//     setShowConfirmation(false);
//     setConfirmationType(null);
//   };

// const saveMaintenanceData = async (data) => {
//   try {
//     const response = await fetch('http://127.0.0.1:5000/api/save-maintenance-data', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify(data),
//     });
    
//     if (!response.ok) {
//       throw new Error(`HTTP error! status: ${response.status}`);
//     }
    
//     return await response.json();
//   } catch (error) {
//     console.error('Error saving maintenance data:', error);
//     throw error;
//   }
// };

// const calculateMaintenanceCosts = async (data) => {
//   try {
//     const response = await fetch('http://127.0.0.1:5000/api/calculate-maintenance-costs', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify(data),
//     });
    
//     if (!response.ok) {
//       throw new Error(`HTTP error! status: ${response.status}`);
//     }
    
//     return await response.json();
//   } catch (error) {
//     console.error('Error calculating maintenance costs:', error);
//     throw error;
//   }
// };
import React, { useState } from "react";
import {useFormNavigation, ConfirmationModal} from './UseFormNavigation'

// Form sequence constant
const MaintenanceandRepairData = ({ currentForm, onNavigate, onClose, setActiveTabs,Activetabs, onclicktabs }) => {
  const navigation = useFormNavigation(currentForm, onNavigate);

   const [showConfirmation, setShowConfirmation] = useState(false)
  const [confirmationType, setConfirmationType] = useState(null)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const [formData, setFormData] = useState({
    periodicMaintenanceCost: "0.5500",
    annualRoutineInspectionCost: "1",
    repairRehabilitationCost: "10",
    frequencyOfPeriodicMaintenance: "5",
    frequencyOfRoutineInspection: "1"
  });

  const handleChange = (field, value) => {
    setFormData({
      ...formData,
      [field]: value
    });
    setHasUnsavedChanges(true);
  };

  // Suggested indicator component
  const SuggestedTag = () => (
    <span className="text-xs text-gray-400 ml-2">Suggested</span>
  );

  
  const handleNext = () => {
    if (navigation.canGoNext) {
      setConfirmationType('next');
      setShowConfirmation(true);
    }
  };

 
    const handleBack = () => {
  setConfirmationType('back')
  setShowConfirmation(true)
}


const handleConfirm = async () => {
  if (confirmationType === 'next') {
    try {
      // Calculate and store maintenance costs using the new endpoint
      console.log('Calculating and storing maintenance costs...');
      const response = await fetch('http://127.0.0.1:5000/api/calculate-and-store-maintenance-costs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      console.log('✅ Maintenance costs calculated successfully:', result.results);
      
      // Log detailed breakdown
      console.log('=== MAINTENANCE COST BREAKDOWN ===');
      console.log('Periodic Maintenance Cost:', result.results.periodic_maintenance_cost);
      console.log('Periodic Maintenance Carbon Cost:', result.results.periodic_maintenance_carbon_cost);
      console.log('Routine Inspection Cost:', result.results.routine_inspection_cost);
      console.log('Repair & Rehabilitation Cost:', result.results.repair_rehabilitation_cost);
      console.log('Total Maintenance Cost:', result.results.total_maintenance_cost);
      console.log('=====================================');
      
      setHasUnsavedChanges(false);
      navigation.navigate(navigation.getNextForm());
    } catch (error) {
      console.error('❌ Error processing maintenance data:', error);
      alert('Error processing maintenance data: ' + error.message);
      return; // Don't navigate if there's an error
    }
  } else if (confirmationType === 'back') {
    navigation.navigate(navigation.getPreviousForm());
  }
  setShowConfirmation(false);
  setConfirmationType(null);
};

const handleCloseConfirmation = () => {
    setShowConfirmation(false);
    setConfirmationType(null);
  };

const saveMaintenanceData = async (data) => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/save-maintenance-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error saving maintenance data:', error);
    throw error;
  }
};

const calculateMaintenanceCosts = async (data) => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/calculate-maintenance-costs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error calculating maintenance costs:', error);
    throw error;
  }
};
  return (
     <div className="w-full max-w-4xl mx-auto ">
      {/* Title bar */}
    <div
  className="overflow-x-auto w-full scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-transparent"
  style={{
    scrollbarWidth: 'thin', // for Firefox
  }}
>
  <div className="flex  w-fit min-w-full">
    {Activetabs.map((tab, index) => (
      <div
        onClick={() => onclicktabs(tab)}
        key={index}
        className={`flex items-center px-4 py-2 rounded-sm border border-gray-300 whitespace-nowrap cursor-pointer
          ${tab === currentForm ? 'bg-[#F0E6E6] border-b-[#522828b0] border-b-[0.25rem]' : 'bg-[#F0E6E6]'}
        `}
        style={{
          fontSize: Activetabs.length > 5 ? '0.85rem' : '1rem',
        }}
      >
        <span className="font-medium">{tab}</span>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onClose(tab);
          }}
          className="ml-2 text-gray-500 hover:text-gray-700"
        >
          ×
        </button>
      </div>
    ))}
  </div>
</div>

      {/* Form content */}
      <div className="bg-[#FFF9F9] p-6 border border-gray-300 rounded-b-sm">
        <div className="space-y-6">
          {/* Periodic Maintenance Cost */}
          <div className="flex items-start">
            <div className="w-1/2">
              <label className="block text-gray-700 leading-tight">
                Periodic Maintenance Cost rate as percentage to total construction cost
              </label>
            </div>
            <div className="w-1/2">
              <div className="flex items-center">
                <input
                  type="text"
                  value={formData.periodicMaintenanceCost}
                  onChange={(e) => handleChange("periodicMaintenanceCost", e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm"
                />
                <span className="ml-2 text-sm text-gray-600">(%)</span>
                <SuggestedTag />
              </div>
            </div>
          </div>

          {/* Annual Routine Inspection Cost */}
          <div className="flex items-start">
            <div className="w-1/2">
              <label className="block text-gray-700 leading-tight">
                Annual Routine Inspection cost rate as percentage to total construction cost
              </label>
            </div>
            <div className="w-1/2">
              <div className="flex items-center">
                <input
                  type="text"
                  value={formData.annualRoutineInspectionCost}
                  onChange={(e) => handleChange("annualRoutineInspectionCost", e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm"
                />
                <span className="ml-2 text-sm text-gray-600">(%)</span>
                <SuggestedTag />
              </div>
            </div>
          </div>

          {/* Repair and Rehabilitation Cost */}
          <div className="flex items-start">
            <div className="w-1/2">
              <label className="block text-gray-700 leading-tight">
                Repair and Rehabilitation cost rate as percentage of total construction cost
              </label>
            </div>
            <div className="w-1/2">
              <div className="flex items-center">
                <input
                  type="text"
                  value={formData.repairRehabilitationCost}
                  onChange={(e) => handleChange("repairRehabilitationCost", e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm"
                />
                <span className="ml-2 text-sm text-gray-600">(%)</span>
                <SuggestedTag />
              </div>
            </div>
          </div>

          {/* Frequency of Periodic Maintenance */}
          <div className="flex items-center">
            <div className="w-1/2">
              <label className="block text-gray-700">Frequency of Periodic Maintenance</label>
            </div>
            <div className="w-1/2">
              <div className="flex items-center">
                <input
                  type="text"
                  value={formData.frequencyOfPeriodicMaintenance}
                  onChange={(e) => handleChange("frequencyOfPeriodicMaintenance", e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm"
                />
                <span className="ml-2 text-sm text-gray-600">(years)</span>
                <SuggestedTag />
              </div>
            </div>
          </div>

          {/* Frequency of Routine Inspection */}
          <div className="flex items-center">
            <div className="w-1/2">
              <label className="block text-gray-700">Frequency of Routine Inspection</label>
            </div>
            <div className="w-1/2">
              <div className="flex items-center">
                <input
                  type="text"
                  value={formData.frequencyOfRoutineInspection}
                  onChange={(e) => handleChange("frequencyOfRoutineInspection", e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm"
                />
                <span className="ml-2 text-sm text-gray-600">(years)</span>
                <SuggestedTag />
              </div>
            </div>
          </div>

          {/* Navigation buttons */}
          <div className="flex justify-end gap-4 mt-8">
            <button 
              onClick={handleBack}
              disabled={!navigation.canGoBack}
              className={`px-8 py-1 text-sm rounded-md border ${
                navigation.canGoBack 
                  ? 'bg-white border-gray-300 hover:bg-gray-50 text-gray-700' 
                  : 'bg-gray-100 border-gray-200 text-gray-400 cursor-not-allowed'
              }`}
            >
              Back
            </button>
           <button 
              onClick={handleNext}
              disabled={!navigation.canGoNext}
              className={`px-8 py-1 text-sm rounded-md border ${
                navigation.canGoNext 
                  ?  'bg-[#522828b0] border-black hover:bg-[#814040] text-black' 
                  : 'bg-gray-100 border-gray-200 text-gray-400 cursor-not-allowed'
              }`}
            >
              Next
            </button>
          </div>
        </div>
      </div>
        <ConfirmationModal
              isOpen={showConfirmation}
              onClose={handleCloseConfirmation}
              onConfirm={handleConfirm}
              type={confirmationType}
              nextForm={confirmationType === 'next' ? navigation.getNextForm() : navigation.getPreviousForm()}
            />
    </div>
  );
};

export default MaintenanceandRepairData;