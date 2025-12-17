// import React, { useState } from "react";
// import {useFormNavigation, ConfirmationModal} from './UseFormNavigation'

// // Form sequence constant
// const BridgeandTraffic = ({ currentForm, onNavigate, onClose, setActiveTabs,Activetabs, onclicktabs }) => {
//   const navigation = useFormNavigation(currentForm, onNavigate);

//    const [showConfirmation, setShowConfirmation] = useState(false)
//   const [confirmationType, setConfirmationType] = useState(null)
//   const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
//   const [formData, setFormData] = useState({
//     numberOfLanes: "",
//     additionalReRouteDistance: "",
//     roadRoughness: "",
//     roadRiseAndFall: "",
//     typeOfRoad: "",
//     annualIncreaseInTraffic: "",
//     vehicleComposition: {
//       cars: "",
//       buses: "",
//       hcv: "",
//       mcv: "",
//       lcv: ""
//     }
//   });

//   const handleChange = (field, value) => {
//     setFormData({
//       ...formData,
//       [field]: value
//     });

//   };

//   const handleVehicleCompositionChange = (field, value) => {
//     setFormData({
//       ...formData,
//       vehicleComposition: {
//         ...formData.vehicleComposition,
//         [field]: value
//       }
//     });
//   };

  
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


//   const handleConfirm = () => {
//     if (confirmationType === 'next') {
//       // Here you would typically save the form data to your context or API
//       console.log('Saving form data:', formData);
//       setHasUnsavedChanges(false);
//       navigation.navigate(navigation.getNextForm());
//     } else if (confirmationType === 'back') {
//       navigation.navigate(navigation.getPreviousForm());
//     }
//     setShowConfirmation(false);
//     setConfirmationType(null);
//   };

//   const handleCloseConfirmation = () => {
//     setShowConfirmation(false);
//     setConfirmationType(null);
//   };
// const handleSave = async () => {
//   try {
//     // First save the traffic data
//     const saveResponse = await fetch('http://127.0.0.1:5000/api/save-traffic-data', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify(formData)
//     });
    
//     if (saveResponse.ok) {
//       console.log('Traffic data saved successfully');
      
//       // Then calculate road user cost
//       const costResponse = await fetch('http://127.0.0.1:5000/api/calculate-road-user-cost', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(formData)
//       });
      
//       if (costResponse.ok) {
//         const costData = await costResponse.json();
//         console.log('Road User Cost:', costData.road_user_cost);
//         console.log('Calculation Details:', costData.calculation_details);
//       } else {
//         console.error('Failed to calculate road user cost');
//       }
//     } else {
//       console.error('Failed to save traffic data');
//     }
//   } catch (error) {
//     console.error('Error:', error);
//   }
// };

//bridge and traffic form
import React, { useState } from "react"; 
import {useFormNavigation, ConfirmationModal} from './UseFormNavigation' 
 
// Form sequence constant 
const BridgeandTraffic = ({ currentForm, onNavigate, onClose, setActiveTabs,Activetabs, onclicktabs }) => { 
  const navigation = useFormNavigation(currentForm, onNavigate); 
 
  const [showConfirmation, setShowConfirmation] = useState(false) 
  const [confirmationType, setConfirmationType] = useState(null) 
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false) 
  const [formData, setFormData] = useState({ 
    numberOfLanes: "", 
    additionalReRouteDistance: "", 
    roadRoughness: "", 
    roadRiseAndFall: "", 
    typeOfRoad: "", 
    annualIncreaseInTraffic: "", 
    vehicleComposition: { 
      cars: "", 
      buses: "", 
      hcv: "", 
      mcv: "", 
      lcv: "" 
    } 
  }); 
 
  const handleChange = (field, value) => { 
    setFormData({ 
      ...formData, 
      [field]: value 
    }); 
    setHasUnsavedChanges(true);
  }; 
 
  const handleVehicleCompositionChange = (field, value) => { 
    setFormData({ 
      ...formData, 
      vehicleComposition: { 
        ...formData.vehicleComposition, 
        [field]: value 
      } 
    }); 
    setHasUnsavedChanges(true);
  }; 
 
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
const calculateAndLogAllCosts = async () => {
  try {
    // Get initial construction cost from DB
    const initialCostResponse = await fetch('http://127.0.0.1:5000/api/get-initial-construction-cost');
    const initialCostData = await initialCostResponse.json();
    
    // Get time cost from DB
    const timeCostResponse = await fetch('http://127.0.0.1:5000/api/get-stored-time-cost');
    const timeCostData = await timeCostResponse.json();
    
    // Get stored road user cost instead of calculating again
    const roadUserResponse = await fetch('http://127.0.0.1:5000/api/get-stored-road-user-cost');
    const roadUserData = await roadUserResponse.json();
    
    // Calculate initial carbon emission cost
    const carbonResponse = await fetch('http://127.0.0.1:5000/api/calculate-initial-carbon-emission-cost', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });
    const carbonData = await carbonResponse.json();
    
    // Calculate additional carbon emission cost (this one is working)
    const additionalCarbonResponse = await fetch('http://127.0.0.1:5000/api/calculate-additional-carbon-cost', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });
    const additionalCarbonData = await additionalCarbonResponse.json();
    
    console.log('=== ALL COST CALCULATIONS ===');
    
    // Fix: Access the correct properties based on backend response format
    const initialCost = initialCostData.success && initialCostData.result 
      ? initialCostData.result.total_initial_cost 
      : 'Not found';
      
    const timeCost = timeCostData.success && timeCostData.result 
      ? timeCostData.result.time_cost 
      : 'Not found';
      
    const roadUserCost = roadUserData.success 
      ? roadUserData.road_user_cost 
      : 'Not found';
      
    const carbonCost = carbonData.success 
      ? carbonData.initial_carbon_emission_cost 
      : 'Not calculated';
      
    const additionalCarbonCost = additionalCarbonData.success 
      ? additionalCarbonData.additional_carbon_emission_cost 
      : 'Not calculated';
    
    console.log('Initial Construction Cost:', initialCost);
    console.log('Time Cost:', timeCost);
    console.log('Initial Carbon Emission Cost:', carbonCost);
    console.log('Road User Cost:', roadUserCost);
    console.log('Additional Carbon Emission Cost:', additionalCarbonCost);
    
    // Optional: Log raw responses for debugging
    console.log('=== RAW RESPONSES DEBUG ===');
    console.log('Initial Cost Response:', initialCostData);
    console.log('Time Cost Response:', timeCostData);
    console.log('Road User Response:', roadUserData);
    
  } catch (error) {
    console.error('Error calculating costs:', error);
  }
};
  const handleConfirm = () => { 
   if (confirmationType === 'next') {
    handleSave().then(async () => {
      // Calculate and log all three costs
      await calculateAndLogAllCosts();
      setHasUnsavedChanges(false);
      navigation.navigate(navigation.getNextForm());
    });
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

  // Transform form data to match backend expected format
// Add this mapping function before your transformDataForBackend function

const mapLaneType = (laneDescription) => {
  const mapping = {
    "Single lane": "2",
    "Intermediate lane": "2", 
    "Two lane": "2",
    "Three lane": "4",
    "Four lane divided roads": "4",
    "Four lane divided Expressways": "4"
  };
  return mapping[laneDescription] || "2"; // Default to "2"
};

const mapRoughness = (roughnessValue) => {
  const numValue = parseInt(roughnessValue);
  if (numValue <= 3000) return "Good";
  if (numValue <= 5000) return "Fair";
  return "Poor";
};

const mapRiseAndFall = (rfValue) => {
  const numValue = parseInt(rfValue);
  if (numValue <= 25) return "Rolling";
  return "Hilly";
};

// Replace your existing transformDataForBackend function with this:
const transformDataForBackend = () => {
  // Map the form values to backend expected format
  const mappedLaneType = mapLaneType(formData.numberOfLanes);
  const mappedRoughness = mapRoughness(formData.roadRoughness);
  const mappedRF = mapRiseAndFall(formData.roadRiseAndFall);
  
  console.log("=== FRONTEND MAPPING DEBUG ===");
  console.log("Original values:", {
    numberOfLanes: formData.numberOfLanes,
    roadRoughness: formData.roadRoughness, 
    roadRiseAndFall: formData.roadRiseAndFall
  });
  console.log("Mapped values:", {
    Lane_Type: mappedLaneType,
    Roughness: mappedRoughness,
    RF: mappedRF
  });
  
  return {
    road_user_inputs: {
      Lane_Type: mappedLaneType,
      Roughness: mappedRoughness,
      RF: mappedRF,
      Vehicles: [
        {
          Vehicle_Type: "Car",
          Count: parseInt(formData.vehicleComposition.cars) || 0
        },
        {
          Vehicle_Type: "Bus", 
          Count: parseInt(formData.vehicleComposition.buses) || 0
        },
        {
          Vehicle_Type: "HCV",
          Count: parseInt(formData.vehicleComposition.hcv) || 0
        },
        {
          Vehicle_Type: "MCV",
          Count: parseInt(formData.vehicleComposition.mcv) || 0
        },
        {
          Vehicle_Type: "LCV",
          Count: parseInt(formData.vehicleComposition.lcv) || 0
        }
      ].filter(vehicle => vehicle.Count > 0)
    },
    financial_inputs: {
      construction_time: 12,
      reroute_distance: parseFloat(formData.additionalReRouteDistance) || 0
    },
    typeOfRoad: formData.typeOfRoad,
    annualIncreaseInTraffic: formData.annualIncreaseInTraffic
  };
};

  const handleSave = async () => { 
    try { 
      console.log('Saving traffic data...');
      
      // Transform data to backend format
      const backendData = transformDataForBackend();
      console.log('Transformed data for backend:', backendData);
      
      // Save traffic data first
      const saveResponse = await fetch('http://127.0.0.1:5000/api/save-traffic-data', { 
        method: 'POST', 
        headers: { 
          'Content-Type': 'application/json', 
        }, 
        body: JSON.stringify(backendData) 
      }); 
       
      if (saveResponse.ok) { 
        const saveResult = await saveResponse.json();
        console.log('Traffic data saved successfully:', saveResult); 
         
        // Then calculate road user cost using the new endpoint
        const costResponse = await fetch('http://127.0.0.1:5000/api/calculate-road-user-cost', { 
          method: 'POST', 
          headers: { 
            'Content-Type': 'application/json', 
          }, 
          body: JSON.stringify(backendData) 
        }); 
         
        if (costResponse.ok) { 
          const costData = await costResponse.json(); 
          console.log('=== ROAD USER COST CALCULATION RESULT ===');
          console.log('Road User Cost:', costData.road_user_cost); 
          console.log('Success:', costData.success);
          console.log('Message:', costData.message);
          
          // Set unsaved changes to false after successful save
          setHasUnsavedChanges(false);
          
          return costData; // Return the result for potential chaining
        } else { 
          const errorData = await costResponse.json();
          console.error('Failed to calculate road user cost:', errorData); 
          throw new Error('Failed to calculate road user cost');
        } 
      } else { 
        const errorData = await saveResponse.json();
        console.error('Failed to save traffic data:', errorData); 
        throw new Error('Failed to save traffic data');
      } 
    } catch (error) { 
      console.error('Error in handleSave:', error); 
      throw error; // Re-throw so calling code can handle it
    } 
  };

  // Add a manual save button handler if needed
  const handleManualSave = () => {
    handleSave().catch(error => {
      console.error('Manual save failed:', error);
    });
  };

  // Rest of your component remains the same...
  // Your existing JSX return statement goes here
  

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
          {/* Number of Lanes */}
          <div className="flex items-center">
            <div className="w-1/2">
              <label className="block text-gray-700">Number of Lanes</label>
            </div>
            <div className="w-1/2">
              <div className="relative">
                <select
                //   type="text"
                  value={formData.numberOfLanes}
                  onChange={(e) => handleChange("numberOfLanes", e.target.value)}
                  className="w-5/6 border border-gray-300 rounded-md px-3 py-1 text-sm"
                >
                  <option value="Single lane">Single lane</option>
                  <option value="Intermediate lane">Intermediate lane</option>
                  <option value="Two lane">Two lane</option>
                  <option value="Three lane">Three lane</option>
                  <option value="Four lane divided roads">Four lane divided roads</option>
                  <option value="Four lane divided Expressways">Four lane divided Expressways</option>
                   </select>
               
              </div>
            </div>
          </div>

          {/* Additional Re-Route Distance */}
          <div className="flex items-center">
            <div className="w-1/2">
              <label className="block text-gray-700">Additional Re-Route Distance</label>
            </div>
            <div className="w-1/2">
              <div className="flex items-center">
                <input
                  type="text"
                  value={formData.additionalReRouteDistance}
                  onChange={(e) => handleChange("additionalReRouteDistance", e.target.value)}
                  className="w-5/6 border border-gray-300 rounded-md px-3 py-1 text-sm"
                />
                <span className="ml-2 text-sm text-gray-600">(km)</span>
              </div>
            </div>
          </div>

          {/* Road Roughness */}
          <div className="flex items-center">
            <div className="w-1/2">
              <label className="block text-gray-700">Road Roughness</label>
            </div>
            <div className="w-1/2">
              <div className="relative flex items-center">
                <select
                    // type="text"
                    value={formData.roadRoughness}
                    onChange={(e) => handleChange("roadRoughness", e.target.value)}
                    className="w-5/6 border border-gray-300 rounded-md px-3 py-1 text-sm pr-8"
                >
                  <option value="2000">2000</option>
                  <option value="3000">3000</option>
                  <option value="4000">4000</option>
                  <option value="5000">5000</option>
                  <option value="6000">6000</option>
                  <option value="7000">7000</option>
                  <option value="8000">8000</option>
                  
                  </select>
                <span className="ml-2 text-sm text-gray-600 whitespace-nowrap">
                    (mm/km)
                </span>
                </div>
            </div>
          </div>

          {/* Road Rise and Fall */}
          <div className="flex items-center">
            <div className="w-1/2">
              <label className="block text-gray-700">Road Rise and Fall (RF)</label>
            </div>
            <div className="w-1/2">
              <div className="flex items-center">
                <select
                  
                  
                  onChange={(e) => handleChange("roadRiseAndFall", e.target.value)}
                  className="w-5/6 border border-gray-300 rounded-md px-3 py-1 text-sm"
                >
                <option value="0">0</option>
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="15">15</option>
                <option value="20">20</option>
                <option value="25">25</option>
                <option value="30">30</option>
                <option value="35">35</option>
                <option value="40">40</option>
                <option value="45">45</option>
                <option value="50">50</option>
                </select>
                <span className="ml-2 text-sm text-gray-600">(m/km)</span>
              </div>
            </div>
          </div>

          {/* Type of Road */}
          <div className="flex items-center">
            <div className="w-1/2">
              <label className="block text-gray-700">Type of Road</label>
            </div>
            <div className="w-1/2">
              <div className="relative">
                <select
                //  type="text"
                  value={formData.typeOfRoad}
                  onChange={(e) => handleChange("typeOfRoad", e.target.value)}
                  className="w-5/6 border border-gray-300 rounded-md px-3 py-1 text-sm"
                >
                  <option value="Urban">Urban</option>
                    <option value="Rural">Rural</option>
                    </select>
               
              </div>
            </div>
          </div>

          {/* Annual Increase in Traffic */}
       <div className="flex items-start">
  <div className="w-1/2">
    <label className="block text-gray-700 leading-tight">
      Annual Increase in Traffic if Re-Routing duration increases more than a year
    </label>
  </div>
  <div className="w-1/2">
    <div className="relative flex items-center">
      {formData.annualIncreaseInTraffic === 'custom' ? (
        <input
          type="text"
          value={formData.customTrafficIncrease || ''}
          onChange={(e) => handleChange("customTrafficIncrease", e.target.value)}
          onBlur={() => {
            if (!formData.customTrafficIncrease) {
              handleChange("annualIncreaseInTraffic", "8");
            }
          }}
          placeholder="Enter custom percentage"
          className="w-5/6 border border-gray-300 rounded-md px-3 py-1 text-sm"
          autoFocus
        />
      ) : (
        <select
          value={formData.annualIncreaseInTraffic}
          onChange={(e) => handleChange("annualIncreaseInTraffic", e.target.value)}
          className="w-5/6 border border-gray-300 rounded-md px-3 py-1 text-sm"
        >
          <option value="8">8</option>
          <option value="9">9</option>
          <option value="10">10</option>
          <option value="11">11</option>
          <option value="12">12</option>
          <option value="custom">Custom</option>
        </select>
      )}
      <span className="ml-2 text-sm text-gray-600">(%)</span>
    </div>
  </div>
</div>

          {/* Composition of Various Vehicles */}
          <div className="flex items-start ">
            <span className="mr-48">
              <label className="block text-gray-700 mb-2">Composition of Various Vehicles</label>
            </span>
            <div className=" bg-white">
              <div className="space-y-2 border border-gray-200 rounded-md p-3">
                {/* Cars */}
                <div className="flex items-center">
                  <label className="w-20 block text-sm text-gray-700">Cars:</label>
                  <input
                    type="text"
                    value={formData.vehicleComposition.cars}
                    onChange={(e) => handleVehicleCompositionChange("cars", e.target.value)}
                    className="flex-1 border border-gray-300 rounded-md px-3 py-1 text-sm"
                  />
                </div>
                
                {/* Buses */}
                <div className="flex items-center">
                  <label className="w-20 block text-sm text-gray-700">Buses:</label>
                  <input
                    type="text"
                    value={formData.vehicleComposition.buses}
                    onChange={(e) => handleVehicleCompositionChange("buses", e.target.value)}
                    className="flex-1 border border-gray-300 rounded-md px-3 py-1 text-sm"
                  />
                </div>
                
                {/* HCV */}
                <div className="flex items-center">
                  <label className="w-20 block text-sm text-gray-700">HCV:</label>
                  <input
                    type="text"
                    value={formData.vehicleComposition.hcv}
                    onChange={(e) => handleVehicleCompositionChange("hcv", e.target.value)}
                    className="flex-1 border border-gray-300 rounded-md px-3 py-1 text-sm"
                  />
                  
                </div>
                
                {/* MCV */}
                <div className="flex items-center">
                  <label className="w-20 block text-sm text-gray-700">MCV:</label>
                  <input
                    type="text"
                    value={formData.vehicleComposition.mcv}
                    onChange={(e) => handleVehicleCompositionChange("mcv", e.target.value)}
                    className="flex-1 border border-gray-300 rounded-md px-3 py-1 text-sm"
                  />
                </div>
                
                {/* LCV */}
                <div className="flex items-center">
                  <label className="w-20 block text-sm text-gray-700">LCV:</label>
                  <input
                    type="text"
                    value={formData.vehicleComposition.lcv}
                    onChange={(e) => handleVehicleCompositionChange("lcv", e.target.value)}
                    className="flex-1 border border-gray-300 rounded-md px-3 py-1 text-sm"
                  />
              
                </div>
                
              </div>
              
            </div>
                <span className="ml-2 text-sm text-gray-600 self-center">(PCU/D)</span>
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
                 onClick={() => {
                  handleSave()
                  handleNext()
                }}
              disabled={!navigation.canGoNext}
              className={`px-8 py-1 text-sm rounded-md border ${
                navigation.canGoNext 
                  ? 'bg-[#522828b0] border-black hover:bg-[#814040] text-black' 
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

export default BridgeandTraffic;