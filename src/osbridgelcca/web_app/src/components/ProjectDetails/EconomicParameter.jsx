
"use client"
import {useFormNavigation, ConfirmationModal} from './UseFormNavigation'
import { useState } from "react"

const EconomicParameter  = ({ currentForm, onNavigate, onClose, setActiveTabs, Activetabs, onclicktabs }) => {
  const navigation = useFormNavigation(currentForm, onNavigate);
  
  const [showConfirmation, setShowConfirmation] = useState(false)
  const [confirmationType, setConfirmationType] = useState(null)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const [showInterestWarning, setShowInterestWarning] = useState(false);
  const [pendingInterestRate, setPendingInterestRate] = useState(null);

  const handleInterestChange = (value) => {
    const numericValue = parseFloat(value);
    if (numericValue > 10) {
      setPendingInterestRate(value);
      setShowInterestWarning(true);
    } else {
      handleChange("interestRate", value);
    }
  };

  const confirmInterestChange = () => {
    handleChange("interestRate", pendingInterestRate);
    setShowInterestWarning(false);
    setPendingInterestRate(null);
  };

  const cancelInterestChange = () => {
    setShowInterestWarning(false);
    setPendingInterestRate(null);
  };

  // Initial state for Economic Parameter  fields
  const [EconomicParameter , setFinancialData] = useState({
    realDiscountRate: "",
    interestRate: "",
    investmentRatio: "",
    durationOfStudy: "",
    constructionTime: ""
  })

  // Handle field changes
  const handleChange = (field, value) => {
    setFinancialData({
      ...EconomicParameter ,
      [field]: value
    })
    setHasUnsavedChanges(true);
  }

  const handleNext = () => {
    if (navigation.canGoNext) {
      setConfirmationType('next');
      setShowConfirmation(true);
    }
  }

  const handleBack = () => {
    setConfirmationType('back')
    setShowConfirmation(true)
  }

  const handleSave = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/save-financial-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(EconomicParameter )
      })

      if (response.ok) {
        const result = await response.json()
        console.log('Economic Parameter  saved successfully:', result)
        setHasUnsavedChanges(false)
        return true;
      } else {
        const errorData = await response.json();
        console.error('Failed to save Economic Parameter :', errorData)
        return false;
      }
    } catch (error) {
      console.error('Error saving Economic Parameter :', error)
      return false;
    }
  }

  const calculateTimeCost = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/calculate-time-cost', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          interestRate: parseFloat(EconomicParameter .interestRate),
          constructionTime: parseFloat(EconomicParameter .constructionTime),
          investmentRatio: parseFloat(EconomicParameter .investmentRatio)
        })
      });

      if (response.ok) {
        const result = await response.json();
        console.log('=== TIME COST CALCULATION RESULT ===');
        console.log('Time Cost:', result.time_cost);
        console.log('Construction Cost:', result.construction_cost);
        console.log('Interest Rate:', result.interest_rate + '%');
        console.log('Construction Time:', result.construction_time + ' years');
        console.log('Investment Ratio:', result.investment_ratio);
        console.log('Formula Used:', result.formula_used);
        console.log('==================================');
        return result;
      } else {
        const errorData = await response.json();
        console.error('Failed to calculate time cost:', errorData);
        return null;
      }
    } catch (error) {
      console.error('Error in time cost calculation:', error);
      return null;
    }
  }

const handleConfirm = async () => {
  if (confirmationType === 'next') {
    console.log('Saving form data:', EconomicParameter);
    
    // ADD VALIDATION HERE - Show warning but still allow saving
    try {
      const validationResponse = await fetch('http://127.0.0.1:5000/api/validate-form-sequence', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_form: 'economic parameter' })
      });
      
      const validationResult = await validationResponse.json();
      
      if (!validationResult.can_navigate) {
        // Show warning but allow user to continue
        const userConfirm = window.confirm(
          `Warning: ${validationResult.message}\n\nDo you want to continue anyway? Your data will be saved but calculations may be incomplete.`
        );
        
        if (!userConfirm) {
          setShowConfirmation(false);
          setConfirmationType(null);
          return;
        }
      }
    } catch (error) {
      console.error('Validation error:', error);
      const userConfirm = window.confirm(
        'Warning: Could not validate form completion. Some structure forms may be incomplete.\n\nDo you want to continue anyway?'
      );
      
      if (!userConfirm) {
        setShowConfirmation(false);
        setConfirmationType(null);
        return;
      }
    }
    
    // Validate required fields (existing validation)
    if (!EconomicParameter.constructionTime || EconomicParameter.constructionTime === "") {
      alert('Please fill in the construction time before proceeding.');
      setShowConfirmation(false);
      setConfirmationType(null);
      return;
    }

    try {
      // Save Economic Parameter first
      const saveSuccess = await handleSave();
      
      if (saveSuccess) {
        // Then calculate time cost
        await calculateTimeCost();
        
        setHasUnsavedChanges(false);
        navigation.navigate(navigation.getNextForm());
        
      } else {
        alert('Failed to save Economic Parameter. Please try again.');
      }
    } catch (error) {
      console.error('Error in form submission:', error);
      alert('An error occurred while saving the data. Please try again.');
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
  // Info tooltip component
  const InfoTooltip = () => (
    <span className="inline-flex items-center justify-center w-4 h-4 rounded-full bg-gray-200 text-gray-500 text-xs ml-1 cursor-help">
      ?
    </span>
  )

  // Suggested indicator component
  const SuggestedTag = () => (
    <span className="text-xs text-gray-400 ml-2">Suggested</span>
  )

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
          {/* Real Discount Rate */}
          <div className="flex items-center">
            <div className="w-1/3">
              <label className="flex items-center text-gray-700">
                Discount Rate(Inflation Adjusted)
                <InfoTooltip />
              </label>
            </div>
            <div className="w-1/3 flex items-center">
              <input
                type="text"
                placeholder='4.2500'
                value={EconomicParameter.realDiscountRate}
                onChange={(e) => handleChange("realDiscountRate", e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm"
              />
              <span className="ml-2">(%)</span>
            </div>
            <div className="w-1/3">
              <SuggestedTag />
            </div>
          </div>

          {/* Interest Rate */}
{/* Interest Rate */}
          <div className="flex items-center">
            <div className="w-1/3">
              <label className="text-gray-700">Interest Rate</label>
            </div>
            <div className="w-1/3 flex items-center">
              <div className="relative w-full">
                <input
                  type="text"
                  placeholder="7.5"
                  value={EconomicParameter.interestRate}
                  onChange={(e) => {
                    const value = e.target.value;
                    const numericValue = parseFloat(value);

                    if (numericValue > 10) {
                      setPendingInterestRate(value);
                      setShowInterestWarning(true);
                    } else {
                      handleChange("interestRate", value);
                    }
                  }}
                  className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm appearance-none"
                />
                {showInterestWarning && (
                  <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-md shadow-lg w-96">
                      <p className="text-sm text-gray-800 mb-4">
                        Interest rate exceeds the recommended 10%. Are you sure you want to proceed?
                      </p>
                      <div className="flex justify-end gap-3">
                        <button
                          onClick={cancelInterestChange}
                          className="px-3 py-1 text-sm rounded bg-gray-300 hover:bg-gray-400 text-gray-800"
                        >
                          Cancel
                        </button>
                        <button
                          onClick={confirmInterestChange}
                          className="px-3 py-1 text-sm rounded bg-blue-600 hover:bg-blue-700 text-white"
                        >
                          Yes, Proceed
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
              <span className="ml-2">(RBI repo rate +2%)</span>
            </div>
            <div className="w-1/3">
              <SuggestedTag />
            </div>
          </div>

          {/* Investment Ratio */}
          <div className="flex items-center">
            <div className="w-1/3">
              <label className="text-gray-700">Investment Ratio</label>
            </div>
            <div className="w-1/3">
              <div className="relative w-full">
                <input
                 type="text"
                 placeholder='0.5000'
                  value={EconomicParameter .investmentRatio}
                  onChange={(e) => handleChange("investmentRatio", e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm appearance-none"
                />
   
              </div>
            </div>
            <div className="w-1/3">
              <SuggestedTag />
            </div>
          </div>

          {/* Duration of Study */}
          <div className="flex items-center">
            <div className="w-1/3">
              <label className="text-gray-700">Life Cycle Duration</label>
            </div>
            <div className="w-1/3 flex items-center">
              <input
                type="text"
                value={EconomicParameter.durationOfStudy}
                placeholder="50 & 100"
                onChange={(e) => handleChange("durationOfStudy", e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm"
              />
              
              <span className="ml-2">(years)</span>
            </div>
            <div className="w-1/3">
              <SuggestedTag />
            </div>
          </div>

          {/* Time for construction of Base Project */}
          <div className="flex items-center">
            <div className="w-1/3">
              <label className="text-gray-700 leading-tight">
                Duration of Initial Construction
              </label>
            </div>
            <div className="w-1/3 flex items-center">
              <input
                type="text"
                value={EconomicParameter .constructionTime}
                onChange={(e) => handleChange("constructionTime", e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-1 text-sm"
              />
              { <span className="ml-2">(months)</span>/* make sure you change it to year in backend */}
            </div>
            <div className="w-1/3"></div>
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
  )
}

export default EconomicParameter 