import React, { useState } from "react";
import {useFormNavigation, ConfirmationModal} from './UseFormNavigation'

const DemolitionandRecycling = ({currentForm, onNavigate, onClose, setActiveTabs, Activetabs, onclicktabs }) => {
  const navigation = useFormNavigation(currentForm, onNavigate);

  const [showConfirmation, setShowConfirmation] = useState(false)
  const [confirmationType, setConfirmationType] = useState(null)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const [formData, setFormData] = useState({
    demolitionCostRate: "10",
    scrapValueOfStructuralSteel: "50000",
    structuralSteelScrap: "98"
  });

  const handleChange = (field, value) => {
    setFormData({
      ...formData,
      [field]: value
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

  const handleCalculate = async () => {
    try {
      console.log('Calculating demolition costs with data:', formData);
      
      const response = await fetch('http://127.0.0.1:5000/api/calculate-and-store-demolition-costs', {
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
      
      console.log('=== DEMOLITION & RECYCLING CALCULATION ===');
      console.log('Demolition Cost:', result.results.demolition_cost);
      console.log('Recycling Revenue:', result.results.recycling_revenue);
      console.log('Net Demolition Cost:', result.results.net_demolition_cost);
      console.log('Recoverable Steel (MT):', result.results.calculation_parameters.recoverable_steel_mt);
      console.log('Total Steel Used (MT):', result.results.calculation_parameters.total_steel_mt);
      console.log('==========================================');
      
      alert('Calculation completed! Check console for results.');
      
    } catch (error) {
      console.error('Error calculating demolition costs:', error);
      alert('Error: ' + error.message);
    }
  };

  const handleConfirm = async () => {
    if (confirmationType === 'next') {
      try {
        console.log('Calculating and storing demolition costs...');
        
        const response = await fetch('http://127.0.0.1:5000/api/calculate-and-store-demolition-costs', {
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
        console.log('✅ Demolition costs calculated successfully:', result.results);
        
        console.log('=== DEMOLITION & RECYCLING COST BREAKDOWN ===');
        console.log('Demolition Cost:', result.results.demolition_cost);
        console.log('Recycling Revenue:', result.results.recycling_revenue);
        console.log('Net Demolition Cost:', result.results.net_demolition_cost);
        console.log('Recoverable Steel (MT):', result.results.calculation_parameters.recoverable_steel_mt);
        console.log('Total Steel Used (MT):', result.results.calculation_parameters.total_steel_mt);
        console.log('=============================================');
        
        setHasUnsavedChanges(false);
        navigation.navigate(navigation.getNextForm());
      } catch (error) {
        console.error('❌ Error processing demolition data:', error);
        alert('Error processing demolition data: ' + error.message);
        return;
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

  const SuggestedTag = () => (
    <span className="text-xs text-gray-400 ml-2">Suggested</span>
  );

  return (
    <div className="w-full max-w-4xl mx-auto ">
      {/* Title bar */}
      <div
        className="overflow-x-auto w-full scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-transparent"
        style={{
          scrollbarWidth: 'thin',
        }}
      >
        <div className="flex w-fit min-w-full">
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
          {/* Demolition Cost Rate */}
          <div className="flex items-start">
            <div className="w-1/2">
              <label className="block text-gray-700 leading-tight">
                Demolition Cost rate as percentage to total construction cost
              </label>
            </div>
            <div className="w-1/2">
              <div className="flex items-center">
                <input
                  type="text"
                  value={formData.demolitionCostRate}
                  onChange={(e) => handleChange("demolitionCostRate", e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm"
                />
                <span className="ml-2 text-sm text-gray-600">(%)</span>
                <SuggestedTag />
              </div>
            </div>
          </div>

          {/* Scrap Value of Structural Steel */}
          <div className="flex items-center">
            <div className="w-1/2">
              <label className="block text-gray-700">Scrap Value of Structural Steel</label>
            </div>
            <div className="w-1/2">
              <div className="flex items-center">
                <input
                  type="text"
                  value={formData.scrapValueOfStructuralSteel}
                  onChange={(e) => handleChange("scrapValueOfStructuralSteel", e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm"
                />
                <span className="ml-2 text-sm text-gray-600">(INR/MT)</span>
                <SuggestedTag />
              </div>
            </div>
          </div>

          {/* Structural Steel Scrap */}
          <div className="flex items-center">
            <div className="w-1/2">
              <label className="block text-gray-700">Structural Steel Scrap</label>
            </div>
            <div className="w-1/2">
              <div className="flex items-center">
                <input
                  type="text"
                  value={formData.structuralSteelScrap}
                  onChange={(e) => handleChange("structuralSteelScrap", e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm"
                />
                <span className="ml-2 text-sm text-gray-600">(%)</span>
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
              onClick={handleCalculate} 
              className="bg-[#522828b0] border-black hover:bg-[#814040] text-black rounded-md px-8 py-1 text-sm transition-colors"
            >
              Calculate
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

export default DemolitionandRecycling;