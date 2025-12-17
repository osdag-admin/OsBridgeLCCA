import React, { useState } from 'react';

const ReusableSidebar = ({ 
  selectedWindow, 
  setSelectedWindow, 
  setShowTutorials, 
  setActiveTabs, 
  activeTabs,
  showOutputAsCheckboxes = false,
  outputItems = []
}) => {
  const [structureWorksExpanded, setStructureWorksExpanded] = useState(true);
  const [carbonEmissionExpanded, setCarbonEmissionExpanded] = useState(false);

  const handleItemClick = (itemName) => {
    setSelectedWindow(itemName);
    setShowTutorials(false);
    setActiveTabs((tabs) => {
      if (!tabs.includes(itemName)) {
        return [...tabs, itemName];
      }
      return tabs;
    });
  };

  return (
    <div className="flex flex-col w-1/5">
      <span className="bg-[#F0E6E6] border border-t-black border-r-black border-l-black rounded-t-sm px-2 py-2 text-sm font-semibold max-w-[200px]">
        Project Details Window
        <button className="ml-3 text-sm font-bold">✕</button>
      </span>

      <div 
        className="bg-[#FFF9F9] rounded-sm overflow-auto rounded-t-sm border border-black font-semibold text-[13px] p-0"
        style={{ maxHeight: "80vh" }}
      >
        {/* Input Parameters Heading */}
        <div className="bg-[#F0E6E6] px-3 py-2 text-lg w-full font-semibold border border-b-black flex justify-center items-center">
          Input Parameters
        </div>

        {/* Tree Structure */}
        <div className="border-black bg-[#FFF9F9]">
          {/* Structure Works Data with expand/collapse */}
          <div>
            <div
              className="flex items-center px-3 py-0.5 text-[13px] hover:bg-gray-100 cursor-pointer"
              onClick={() => setStructureWorksExpanded(!structureWorksExpanded)}
            >
              <span className="mr-2">
                {structureWorksExpanded ? "▼" : "\u2BC8"}
              </span>
              Structure Works Data
            </div>

            {structureWorksExpanded && (
              <div className="ml-5">
                <div
                  className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                    selectedWindow === "Foundation"
                      ? "bg-gray-700 text-white"
                      : "hover:bg-gray-100"
                  }`}
                  onClick={() => handleItemClick("Foundation")}
                >
                  <span className="mr-2">{"\u2BC8"}</span>
                  Foundation
                </div>

                <div
                  className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                    selectedWindow === "Super-Structure"
                      ? "bg-gray-700 text-white"
                      : "hover:bg-gray-100"
                  }`}
                  onClick={() => handleItemClick("Super-Structure")}
                >
                  <span className="mr-2">{"\u2BC8"}</span>
                  Super-Structure
                </div>

                <div
                  className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                    selectedWindow === "Sub-Structure"
                      ? "bg-gray-700 text-white"
                      : "hover:bg-gray-100"
                  }`}
                  onClick={() => handleItemClick("Sub-Structure")}
                >
                  <span className="mr-2">{"\u2BC8"}</span>
                  Sub-Structure
                </div>

                <div
                  className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                    selectedWindow === "Miscellaneous"
                      ? "bg-gray-700 text-white"
                      : "hover:bg-gray-100"
                  }`}
                  onClick={() => handleItemClick("Miscellaneous")}
                >
                  <span className="mr-2">{"\u2BC8"}</span>
                  Miscellaneous
                </div>
              </div>
            )}
          </div>

          {/* Economic Parameter  */}
          <div
            className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
              selectedWindow === "Economic Parameter "
                ? "bg-gray-700 text-white"
                : "hover:bg-gray-100"
            }`}
            onClick={() => handleItemClick("Economic Parameter ")}
          >
            Economic Parameter 
          </div>

          {/* Carbon Emission Data with expand/collapse */}
          <div>
            <div
              className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                selectedWindow === "Carbon Emission Data"
                  ? "bg-gray-700 text-white"
                  : "hover:bg-gray-100"
              }`}
              onClick={() => {
                handleItemClick("Carbon Emission Data");
                setCarbonEmissionExpanded(!carbonEmissionExpanded);
              }}
            >
              <span className="mr-2">
                {carbonEmissionExpanded ? "▼" : "\u2BC8"}
              </span>
              Carbon Emission Data
            </div>

            {carbonEmissionExpanded && (
              <div className="ml-5">
                <div
                  className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                    selectedWindow === "Carbon Emission Cost Data"
                      ? "bg-gray-700 text-white"
                      : "hover:bg-gray-100"
                  }`}
                  onClick={() => handleItemClick("Carbon Emission Cost Data")}
                >
                  <span className="mr-2">{"\u2BC8"}</span>
                  Carbon Emission Cost Data
                </div>
              </div>
            )}
          </div>

          {/* Bridge and Traffic Data */}
          <div
            className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
              selectedWindow === "Bridge and Traffic"
                ? "bg-gray-700 text-white"
                : "hover:bg-gray-100"
            }`}
            onClick={() => handleItemClick("Bridge and Traffic")}
          >
            Bridge and Traffic Data
          </div>

          {/* Maintenance and Repair */}
          <div
            className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
              selectedWindow === "Maintenance and Repair Data"
                ? "bg-gray-700 text-white"
                : "hover:bg-gray-100"
            }`}
            onClick={() => handleItemClick("Maintenance and Repair Data")}
          >
            Maintenance and Repair
          </div>

          {/* Demolition and Recycling */}
          <div
            className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
              selectedWindow === "Demolition and Recycling"
                ? "bg-gray-700 text-white"
                : "hover:bg-gray-100"
            }`}
            onClick={() => handleItemClick("Demolition and Recycling")}
          >
            Demolition and Recycling
          </div>
        </div>

        {/* Output Heading */}
        <div className="bg-[#F0E6E6] px-3 py-2 text-lg font-semibold border border-black flex justify-center items-center">
          Output
        </div>

        {/* Output Content */}
        {showOutputAsCheckboxes ? (
          <div className="bg-[#FFF9F9] border border-gray-300 p-3 rounded text-[13px] text-gray-800">
            {outputItems.map((item, index) => (
              <label
                key={index}
                className="flex items-center space-x-2 mb-0.5 cursor-pointer hover:bg-gray-50 py-0.5"
              >
                <input
                  type="checkbox"
                  className="w-3 h-3 text-blue-600 border-gray-400 rounded-sm focus:ring-blue-500 focus:ring-1"
                />
                <span className={`text-xs leading-tight`} style={{ color: item.color }}>
                  {item.text}
                </span>
              </label>
            ))}
          </div>
        ) : (
          <div className="bg-[#FFF9F9] border px-2 text-gray-500 cursor-not-allowed select-none">
            <div>Initial Construction Cost</div>
            <div>Initial Carbon Emission Cost</div>
            <div>Time Cost</div>
            <div>Road User Cost</div>
            <div>Carbon Emission due to Re-Routing</div>
            <div>Periodic Maintenance Costs</div>
            <div>Maintenance Emission Costs</div>
            <div>Routine Inspection Costs</div>
            <div>Repair & Rehabilitation Costs</div>
            <div>Reconstruction Costs</div>
            <div>Demolition & Disposal Cost</div>
            <div>Recycling Cost</div>
            <div>Total Life-Cycle Cost</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ReusableSidebar;