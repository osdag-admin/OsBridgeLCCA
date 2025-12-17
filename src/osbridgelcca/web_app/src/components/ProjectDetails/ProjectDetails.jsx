import FoundationForm from "./StructureWorksComponents/FoundationForm";
import SuperStructureForm from "./StructureWorksComponents/SuperStructureForm";
import SubStructureForm from "./StructureWorksComponents/SubStructureForm";
import MiscellaneousForm from "./StructureWorksComponents/MiscellaneousForm";
import { useState } from "react";
import Accordion from "../Accordion";
import GeneralInfoForm from "../InputForms/GeneralInfoForm";
import StructureWorksData from "./StructureWorksData";
import EconomicParameter  from "./EconomicParameter";
import MaintenanceandRepairData from "./MaintenanceandRepairData";
import BridgeandTraffic from "./BridgeandTraffic";
import DemolitionandRecycling from "./DemolitionandRecycling";
import CarbonEmissionData from "./CarbonEmissionData";
import CarbonEmissionCostData from "./CarbonEmissionCostData";
import Accordionp from "../Accordianp";

const ProjectDetails = ({
  SelectedProjectDetailWindow,
  setSelectedProjectDetailWindow,
  setShowTutorials,
}) => {
  const [tabToClose, setTabToClose] = useState(null);
  const [showCloseConfirm, setShowCloseConfirm] = useState(false);
  const [structureWorksExpanded, setStructureWorksExpanded] = useState(true);
  const [carbonEmissionExpanded, setCarbonEmissionExpanded] = useState(false);

  // Navigation handler for forms
  const handleFormNavigation = (formName) => {
    setSelectedProjectDetailWindow(formName);
    setActiveTabs((tabs) => {
      if (!tabs.includes(formName)) {
        return [...tabs, formName];
      }
      return tabs;
    });
  };

  const [Activetabs, setActiveTabs] = useState([]);

  const cancelTabClose = () => {
    setShowCloseConfirm(false);
    setTabToClose(null);
  };

  const confirmTabClose = () => {
    setActiveTabs((prevTabs) => {
      const index = prevTabs.indexOf(tabToClose);
      const newTabs = prevTabs.filter((tab) => tab !== tabToClose);

      let nextTab = null;
      if (newTabs.length > 0) {
        if (index < newTabs.length) {
          nextTab = newTabs[index];
        } else {
          nextTab = newTabs[index - 1];
        }
      }

      setSelectedProjectDetailWindow(nextTab);
      return newTabs;
    });

    setShowCloseConfirm(false);
    setTabToClose(null);
  };

  const handleTabClose = (tab) => {
    setTabToClose(tab);
    setShowCloseConfirm(true);
  };

  const onclicktabs = (tab) => {
    setSelectedProjectDetailWindow(tab);
  };
   const items = [
    { text: "Initial Construction Cost", color: "#CC9933" },
    { text: "Initial Carbon Emission Cost", color:  "#CC9933" }, 
    { text: "Time Cost", color:  "#CC9933" },
    { text: "Road User Cost", color:  "#CC9933" },
    { text: "Carbon Emission due to Re-Routing", color:  "#CC9933" },
    { text: "Periodic Maintenance Costs", color:  "#CC9933"},
    { text: "Maintenance Emission Costs", color:  "#CC9933" },
    { text: "Routine Inspection Costs", color:  "#CC9933" },
    { text: "Repair & Rehabilitation Costs", color: "#CC9933" },
    { text: "Reconstruction Costs", color:  "#CC9933" },
    { text: "Recycling Cost", color:  "#CC9933" },
    { text: "Total Life-Cycle Cost", color:  "#CC9933" },
  ];

  return (
    <div className="flex gap-4 mx-4 ">
      {/* Left Panel - Project Details */}
      <div
        className={`flex flex-col  ${
          SelectedProjectDetailWindow ? "w-1/6" : "w-full"
        }`}
      >
        <span className="bg-[#F0E6E6] border border-t-black border-r-black border-l-black rounded-t-sm px-2 py-2 text-sm font-semibold max-w-[200px]">
          Project Details Window
          <button className="ml-3 text-sm font-bold">✕</button>
        </span>

        <div
          className={`"bg-[#FFF9F9] rounded-sm overflow-auto ${
            SelectedProjectDetailWindow ? "" : "space-y-5"
          } rounded-t-sm border border-black font-semibold text-[13px] ${
            SelectedProjectDetailWindow ? "p-0" : "p-5"
          }`}
          style={{ maxHeight: "80vh" }}
        >
          {/* Show full layout when no form is selected */}
          {SelectedProjectDetailWindow === null && (
            <>
              <div className="bg-[#F0E6E6] border border-black">
                <Accordion title="General Information">
                  <GeneralInfoForm />
                </Accordion>
              </div>

              <div className="bg-[#F0E6E6] border border-black">
                <Accordion title="Input Parameters">
                  <Accordionp title=" Structure Works Data" level={1}>
                    <StructureWorksData
                      setActiveTabs={setActiveTabs}
                      Activetabs={Activetabs}
                      onSelectForm={(formName) => {
                        setActiveTabs((tabs) => {
                          if (!tabs.includes(formName)) {
                            return [...tabs, formName];
                          }
                          return tabs;
                        });
                        setSelectedProjectDetailWindow(formName);
                        setShowTutorials(false);
                      }}
                    />
                  </Accordionp>

                  <button
                    onClick={() => {
                      setSelectedProjectDetailWindow("Economic Parameter");
                      setShowTutorials(false);
                      setActiveTabs((tabs) => {
                        if (!tabs.includes("Economic Parameter")) {
                          return [...tabs, "Economic Parameter"];
                        }
                        return tabs;
                      });
                    }}
                    className="rounded-sm w-full text-left text-sm ml-12"
                  >
                    {"\u2BC8"} &nbsp; Economic Parameter
                  </button>

                  <Accordionp
                    title={
                      <span
                        onClick={() => {
                          setSelectedProjectDetailWindow(
                            " Carbon Emission Data"
                          );
                          setShowTutorials(false);
                          setActiveTabs((tabs) => {
                            if (!tabs.includes(" Carbon Emission Data")) {
                              return [...tabs, " Carbon Emission Data"];
                            }
                            return tabs;
                          });
                        }}
                      >
                      &nbsp;Carbon Emission Data
                      </span>
                    }
                    level={1}
                  >
                    <button
                      onClick={() => {
                        setSelectedProjectDetailWindow(
                          "Carbon Emission Cost Data"
                        );
                        setShowTutorials(false);
                        setActiveTabs((tabs) => {
                          if (!tabs.includes("Carbon Emission Cost Data")) {
                            return [...tabs, "Carbon Emission Cost Data"];
                          }
                          return tabs;
                        });
                      }}
                      className="rounded-sm w-full text-left text-sm ml-20"
                    >
                      {"\u2BC8"} &nbsp;Carbon Emission Cost Data
                    </button>
                  </Accordionp>

                  <button
                    onClick={() => {
                      setSelectedProjectDetailWindow("Bridge and Traffic");
                      setShowTutorials(false);
                      setActiveTabs((tabs) => {
                        if (!tabs.includes("Bridge and Traffic")) {
                          return [...tabs, "Bridge and Traffic"];
                        }
                        return tabs;
                      });
                    }}
                    className="rounded-sm w-full text-left text-sm ml-12"
                  >
                    {"\u2BC8"} &nbsp; Bridge and Traffic Data
                  </button>

                  <button
                    onClick={() => {
                      setSelectedProjectDetailWindow(
                        "Maintenance and Repair Data"
                      );
                      setShowTutorials(false);
                      setActiveTabs((tabs) => {
                        if (!tabs.includes("Maintenance and Repair Data")) {
                          return [...tabs, "Maintenance and Repair Data"];
                        }
                        return tabs;
                      });
                    }}
                    className="rounded-sm w-full text-left text-sm ml-12"
                  >
                    {"\u2BC8"} &nbsp; Maintenance and Repair
                  </button>

                  <button
                    onClick={() => {
                      setSelectedProjectDetailWindow(
                        "Demolition and Recycling"
                      );
                      setShowTutorials(false);
                      setActiveTabs((tabs) => {
                        if (!tabs.includes("Demolition and Recycling")) {
                          return [...tabs, "Demolition and Recycling"];
                        }
                        return tabs;
                      });
                    }}
                    className="rounded-sm w-full text-left text-sm ml-12"
                  >
                    {"\u2BC8"} &nbsp; Disposal and Recycling
                  </button>
                </Accordion>
              </div>

              <div className="bg-[#F0E6E6] border border-black">
                <Accordion title="Outputs">
                  Initial Construction Cost Initial Carbon emission Cost Time
                  Cost Road User Cost Carbon Emission due to Re-Routing Periodic
                  Maintenance Costs Maintenance Emission Costs Routine
                  Inspectection Costs Repair & Rehabilitation Costs
                  Reconstruction Costs Demolition & Disposal Cost Recycling Cost
                  Total Life-Cycle Cost
                </Accordion>
              </div>
            </>
          )}

          {/* Show compressed layout when a form is selected */}
          {SelectedProjectDetailWindow !== null && (
            <>
              {/* Input Parameters Heading with up arrow */}
              <div
                className="bg-[#F0E6E6] px-3 py-2 text-lg w-full font-semibold border border-b-black flex justify-center
 items-center"
              >
                Input Parameters
              </div>

              {/* Tree Structure */}
              <div className=" border-black bg-[#FFF9F9]">
                {/* Structure Works Data with expand/collapse */}
                <div>
                  <div
                    className="flex items-center px-3 py-0.5 text-[13px] hover:bg-gray-100 cursor-pointer"
                    onClick={() =>
                      setStructureWorksExpanded(!structureWorksExpanded)
                    }
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
                          SelectedProjectDetailWindow === "Foundation"
                            ? "bg-gray-700 text-white"
                            : "hover:bg-gray-100"
                        }`}
                        onClick={() => {
                          setSelectedProjectDetailWindow("Foundation");
                          setShowTutorials(false);
                          setActiveTabs((tabs) => {
                            if (!tabs.includes("Foundation")) {
                              return [...tabs, "Foundation"];
                            }
                            return tabs;
                          });
                        }}
                      >
                        <span className="mr-2">{"\u2BC8"}</span>
                        Foundation
                      </div>


                      <div
                        className={`flex items-center px-3 py-0.5 text-[13] cursor-pointer ${
                          SelectedProjectDetailWindow === "Sub-Structure"
                            ? "bg-gray-700 text-white"
                            : "hover:bg-gray-100"
                        }`}
                        onClick={() => {
                          setSelectedProjectDetailWindow("Sub-Structure");
                          setShowTutorials(false);
                          setActiveTabs((tabs) => {
                            if (!tabs.includes("Sub-Structure")) {
                              return [...tabs, "Sub-Structure"];
                            }
                            return tabs;
                          });
                        }}
                      >
                        <span className="mr-2">{"\u2BC8"}</span>
                        Sub-Structure
                      </div>
                      
                      <div
                        className={`flex items-center px-3 py-0.5 text-[13] cursor-pointer ${
                          SelectedProjectDetailWindow === "Super-Structure"
                            ? "bg-gray-700 text-white"
                            : "hover:bg-gray-100"
                        }`}
                        onClick={() => {
                          setSelectedProjectDetailWindow("Super-Structure");
                          setShowTutorials(false);
                          setActiveTabs((tabs) => {
                            if (!tabs.includes("Super-Structure")) {
                              return [...tabs, "Super-Structure"];
                            }
                            return tabs;
                          });
                        }}
                      >
                        <span className="mr-2">{"\u2BC8"}</span>
                        Super-Structure
                      </div>
                      <div
                        className={`flex items-center px-3 py-0.5 text-[13] cursor-pointer ${
                          SelectedProjectDetailWindow === "Miscellaneous"
                            ? "bg-gray-700 text-white"
                            : "hover:bg-gray-100"
                        }`}
                        onClick={() => {
                          setSelectedProjectDetailWindow("Miscellaneous");
                          setShowTutorials(false);
                          setActiveTabs((tabs) => {
                            if (!tabs.includes("Miscellaneous")) {
                              return [...tabs, "Miscellaneous"];
                            }
                            return tabs;
                          });
                        }}
                      >
                        <span className="mr-2">{"\u2BC8"}</span>
                        Miscellaneous
                      </div>
                    </div>
                  )}
                </div>

                {/* Economic Parameter  */}
                <div
                  className={`flex items-center px-3 py-0.5 text-[13] cursor-pointer ${
                    SelectedProjectDetailWindow === "Economic Parameter"
                      ? "bg-gray-700 text-white"
                      : "hover:bg-gray-100"
                  }`}
                  onClick={() => {
                    setSelectedProjectDetailWindow("Economic Parameter");
                    setShowTutorials(false);
                    setActiveTabs((tabs) => {
                      if (!tabs.includes("Economic Parameter")) {
                        return [...tabs, "Economic Parameter"];
                      }
                      return tabs;
                    });
                  }}
                >
                  Economic Parameter
                </div>

                {/* Carbon Emission Data with expand/collapse */}
                <div>
                  <div
                    className={`flex items-center px-3 py-0.5 text-[13] cursor-pointer ${
                      SelectedProjectDetailWindow === "Carbon Emission Data"
                        ? "bg-gray-700 text-white"
                        : "hover:bg-gray-100"
                    }`}
                    onClick={() => {
                      setSelectedProjectDetailWindow("Carbon Emission Data");
                      setShowTutorials(false);
                      setActiveTabs((tabs) => {
                        if (!tabs.includes("Carbon Emission Data")) {
                          return [...tabs, "Carbon Emission Data"];
                        }
                        return tabs;
                      });
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
                        className={`flex items-center px-3 py-0.5 text-[13] cursor-pointer ${
                          SelectedProjectDetailWindow ===
                          "Carbon Emission Cost Data"
                            ? "bg-gray-700 text-white"
                            : "hover:bg-gray-100"
                        }`}
                        onClick={() => {
                          setSelectedProjectDetailWindow(
                            "Carbon Emission Cost Data"
                          );
                          setShowTutorials(false);
                          setActiveTabs((tabs) => {
                            if (!tabs.includes("Carbon Emission Cost Data")) {
                              return [...tabs, "Carbon Emission Cost Data"];
                            }
                            return tabs;
                          });
                        }}
                      >
                        <span className="mr-2">{"\u2BC8"}</span>
                        Carbon Emission Cost Data
                      </div>
                    </div>
                  )}
                </div>

                {/* Bridge and Traffic Data */}
                <div
                  // className={`flex items-center px-3 py-0.5 text-[13] cursor-pointer
                  //    ${
                  //   SelectedProjectDetailWindow === "Bridge and Traffic"
                  //     ? "bg-gray-700 text-white"
                  //     : "hover:bg-gray-100"
                  // }
                  // `}
                  className="flex items-center px-3 py-0.5 text-[13] cursor-pointer "
                  onClick={() => {
                    setSelectedProjectDetailWindow("Bridge and Traffic");
                    setShowTutorials(false);
                    setActiveTabs((tabs) => {
                      if (!tabs.includes("Bridge and Traffic")) {
                        return [...tabs, "Bridge and Traffic"];
                      }
                      return tabs;
                    });
                  }}
                >
                  Bridge and Traffic Data
                </div>

                {/* Maintenance and Repair */}
                <div
                  className={`flex items-center px-3 py-0.5 text-[13] cursor-pointer ${
                    SelectedProjectDetailWindow ===
                    "Maintenance and Repair Data"
                      ? "bg-gray-700 text-white"
                      : "hover:bg-gray-100"
                  }`}
                  onClick={() => {
                    setSelectedProjectDetailWindow(
                      "Maintenance and Repair Data"
                    );
                    setShowTutorials(false);
                    setActiveTabs((tabs) => {
                      if (!tabs.includes("Maintenance and Repair Data")) {
                        return [...tabs, "Maintenance and Repair Data"];
                      }
                      return tabs;
                    });
                  }}
                >
                  Maintenance and Repair
                </div>

                {/* Demolition and Recycling */}
                <div
                  className={`flex items-center px-3 py-0.5 text-[13] cursor-pointer ${
                    SelectedProjectDetailWindow === "Demolition and Recycling"
                      ? "bg-gray-700 text-white"
                      : "hover:bg-gray-100"
                  }`}
                  onClick={() => {
                    setSelectedProjectDetailWindow("Demolition and Recycling");
                    setShowTutorials(false);
                    setActiveTabs((tabs) => {
                      if (!tabs.includes("Demolition and Recycling")) {
                        return [...tabs, "Demolition and Recycling"];
                      }
                      return tabs;
                    });
                  }}
                >
                  Demolition and Recycling
                </div>
              </div>

              {/* Output Heading with down arrow */}
              <div className="bg-[#F0E6E6] px-3 py-2  text-lg font-semibold border border-black flex justify-center items-center ">
                Output
              </div>
              <div className="bg-[#FFF9F9] border  px-2  text-gray-500 cursor-not-allowed select-none">
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
                  {/* <div className="bg-[#FFF9F9] border border-gray-300 p-3 rounded text-[13] text-gray-800 w-64">
      {items.map((item, index) => (
        <label
          key={index}
          className="flex items-center space-x-2 mb-0.5 cursor-pointer hover:bg-gray-50 py-0.5"
        >
          <input
            type="checkbox"
            className="w-3 h-3 text-blue-600 border-gray-400 rounded-sm focus:ring-blue-500 focus:ring-1"
          />
          <span className={`text-xs leading-tight ${item.color}`}>{item.text}</span>
        </label>
      ))}
    </div> */}

              {/* Output Items */}
            </>
          )}
        </div>
      </div>

      {/* Right Panel - Selected Form */}
      {SelectedProjectDetailWindow && (
        <div className="w-3/4 overflow-auto" style={{ maxHeight: "80vh" }}>
          {SelectedProjectDetailWindow === "Foundation" && (
            <FoundationForm
              setActiveTabs={setActiveTabs}
              Activetabs={Activetabs}
              currentForm="Foundation"
              onNavigate={handleFormNavigation}
              onClose={handleTabClose}
              onclicktabs={onclicktabs}
            />
          )}
          {SelectedProjectDetailWindow === "Sub-Structure" && (
            <SubStructureForm
              setActiveTabs={setActiveTabs}
              Activetabs={Activetabs}
              currentForm="Sub-Structure"
              onNavigate={handleFormNavigation}
              onClose={handleTabClose}
              onclicktabs={onclicktabs}
            />
          )}
          {SelectedProjectDetailWindow === "Super-Structure" && (
            <SuperStructureForm
              setActiveTabs={setActiveTabs}
              Activetabs={Activetabs}
              currentForm="Super-Structure"
              onNavigate={handleFormNavigation}
              onClose={handleTabClose}
              onclicktabs={onclicktabs}
            />
          )}
          {SelectedProjectDetailWindow === "Miscellaneous" && (
            <MiscellaneousForm
              setActiveTabs={setActiveTabs}
              Activetabs={Activetabs}
              currentForm="Miscellaneous"
              onNavigate={handleFormNavigation}
              onClose={handleTabClose}
              onclicktabs={onclicktabs}
            />
          )}
          {SelectedProjectDetailWindow === "Economic Parameter" && (
            <EconomicParameter 
              currentForm="Economic Parameter"
              onNavigate={handleFormNavigation}
              onClose={handleTabClose}
              onclicktabs={onclicktabs}
              setActiveTabs={setActiveTabs}
              Activetabs={Activetabs}
            />
          )}
          {SelectedProjectDetailWindow === "Carbon Emission Data" && (
            <CarbonEmissionData
              currentForm="Carbon Emission Data"
              onNavigate={handleFormNavigation}
              onClose={handleTabClose}
              onclicktabs={onclicktabs}
              setActiveTabs={setActiveTabs}
              Activetabs={Activetabs}
            />
          )}
          {SelectedProjectDetailWindow === "Carbon Emission Cost Data" && (
            <CarbonEmissionCostData
              currentForm="Carbon Emission Cost Data"
              onNavigate={handleFormNavigation}
              onClose={handleTabClose}
              onclicktabs={onclicktabs}
              setActiveTabs={setActiveTabs}
              Activetabs={Activetabs}
            />
          )}
          {SelectedProjectDetailWindow === "Bridge and Traffic" && (
            <BridgeandTraffic
              currentForm="Bridge and Traffic"
              onNavigate={handleFormNavigation}
              onClose={handleTabClose}
              onclicktabs={onclicktabs}
              setActiveTabs={setActiveTabs}
              Activetabs={Activetabs}
            />
          )}
          {SelectedProjectDetailWindow === "Maintenance and Repair Data" && (
            <MaintenanceandRepairData
              currentForm="Maintenance and Repair Data"
              onNavigate={handleFormNavigation}
              onClose={handleTabClose}
              onclicktabs={onclicktabs}
              setActiveTabs={setActiveTabs}
              Activetabs={Activetabs}
            />
          )}
          {SelectedProjectDetailWindow === "Demolition and Recycling" && (
            <DemolitionandRecycling
              currentForm="Demolition and Recycling"
              onNavigate={handleFormNavigation}
              onClose={handleTabClose}
              onclicktabs={onclicktabs}
              setActiveTabs={setActiveTabs}
              Activetabs={Activetabs}
            />
          )}
        </div>
      )}

      {showCloseConfirm && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div className="bg-white p-6 rounded shadow-md w-96">
            <h2 className="text-xl font-semibold mb-4">Confirm Close</h2>
            <p className="mb-4">
              Do you want to save changes before closing this tab?
            </p>
            <div className="flex justify-end space-x-2">
              <button
                className="px-4 py-2 bg-gray-300 rounded"
                onClick={cancelTabClose}
              >
                Cancel
              </button>
              <button
                className="px-4 py-2 bg-red-500 text-white rounded"
                onClick={confirmTabClose}
              >
                Close Without Saving
              </button>
              <button
                className="px-4 py-2 bg-blue-500 text-white rounded"
                onClick={() => {
                  // optional save logic here if needed
                  confirmTabClose();
                }}
              >
                Save and Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProjectDetails;
