// import React, { useState } from "react";
// import { ChevronLeft, ChevronRight } from "lucide-react";
// import RadialChartsComponent from "./RadialChartsComponent";
// import SocialCostRadialChart from "./SocialCostRadialChart";
// import EnvironmentalCostRadialChart from "./EnvironmentalCostRadialChart";
// import EconomicCost100YearsRadialChart from "./EconomicCost100YearsRadialChart";
// import SocialCost100YearsRadialChart from "./SocialCost100YearsRadialChart";
// import EnvironmentalCost100YearsRadialChart from "./EnvironmentalCost100YearsRadialChart";
// import PieChart from "./PieChart";
// import BarChart from "./BarChart";
// import BubbleChart from "./BubbleChart";
// import HorizontalBarChart from "./HorizontalBarChart";

// const Results = () => {
//   const [currentPage, setCurrentPage] = useState(0);

//   const pages = [
//     {
//       topHalf: [
//         { component: <RadialChartsComponent /> },
//         { component: <SocialCostRadialChart /> },
//         { component: <EnvironmentalCostRadialChart /> }
//       ],
//       bottomHalf: { component: <BarChart /> }
//     },
//     {
//       topHalf: [
//         { component: <RadialChartsComponent /> },
//         { component: <SocialCostRadialChart /> },
//         { component: <EnvironmentalCostRadialChart /> }
//       ],
//       bottomHalf: { component: <PieChart /> }
//     },
//     {
//       topHalf: [
//         { component: <EconomicCost100YearsRadialChart /> },
//         { component: <SocialCost100YearsRadialChart /> },
//         { component: <EnvironmentalCost100YearsRadialChart /> }
//       ],
//       bottomHalf: { component: <HorizontalBarChart /> }
//     },
//     {
//       topHalf: [],
//       bottomHalf: { component: <BubbleChart />, fullPage: true }
//     }
//   ];

//   const currentPageData = pages[currentPage];

//   const handleNext = () => {
//     if (currentPage < pages.length - 1) setCurrentPage(currentPage + 1);
//   };

//   const handleBack = () => {
//     if (currentPage > 0) setCurrentPage(currentPage - 1);
//   };
//  const colors = ['#273B5C', '#961818', '#5A003B', '#708090'];
//   const labels = ['Initial Stage', 'Use Stage', 'End-of-Life Stage', 'Beyond-Life Stage'];
//   return (
//     <div className="w-full">
//       {/* Result Window Tab */}
//       <div className="w-full  ">
//         <div className="overflow-x-auto w-full scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-transparent">
//           <div className="flex w-fit min-w-full">
//             <div
//               className="flex items-center px-4 py-2 rounded-sm border border-gray-300 whitespace-nowrap cursor-default bg-[#F0E6E6] border-b-[#522828b0] border-b-[0.25rem]"
//               style={{ fontSize: '1rem' }}
//             >
//               <span className="font-medium">Result Window</span>
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* Main Results Content */}
//       <div className="min-h-screen bg-gray-50 py-8">
//         <div className="container mx-auto px-4">
//           <div className="min-h-[80vh] flex flex-col">
//             {currentPageData.topHalf.length > 0 && (
//               <div className="flex-1 mb-8">
//                 <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-full">
//                   {currentPageData.topHalf.map((chart, index) => (
//                     <div key={index} className="bg-white rounded-lg shadow-lg p-4 flex items-center justify-center">
//                       {chart.component}
//                     </div>
//                   ))}
//                 </div>
//               </div>
//             )}

//               <div className="flex flex-wrap items-center justify-center gap-4 p-4 bg-white rounded-lg shadow-sm">
//       {colors.map((color, index) => (
//         <div key={index} className="flex items-center gap-2">
//           <div 
//             className="w-4 h-4 rounded-sm"
//             style={{ backgroundColor: color }}
//           ></div>
//           <span className="text-sm font-medium text-gray-700">
//             {labels[index]}
//           </span>
//         </div>
//       ))}
//     </div>

//             <div className="flex-1">
//               <div className="bg-white rounded-lg shadow-lg p-4 h-full flex items-center justify-center">
//                 {currentPageData.bottomHalf.component}
//               </div>
//             </div>
//           </div>

//           <div className="flex justify-between items-center mt-8">
//             <button
//               onClick={handleBack}
//               disabled={currentPage === 0}
//               className={`flex items-center px-6 py-3 rounded-lg font-medium transition-colors ${
//                 currentPage === 0
//                   ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
//                   : 'bg-blue-600 text-white hover:bg-blue-700'
//               }`}
//             >
//               <ChevronLeft className="w-5 h-5 mr-2" />
//               Back
//             </button>

//             <div className="flex space-x-2">
//               {pages.map((_, index) => (
//                 <div
//                   key={index}
//                   className={`w-3 h-3 rounded-full ${
//                     index === currentPage ? 'bg-blue-600' : 'bg-gray-300'
//                   }`}
//                 />
//               ))}
//             </div>

//             <button
//               onClick={handleNext}
//               disabled={currentPage === pages.length - 1}
//               className={`flex items-center px-6 py-3 rounded-lg font-medium transition-colors ${
//                 currentPage === pages.length - 1
//                   ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
//                   : 'bg-blue-600 text-white hover:bg-blue-700'
//               }`}
//             >
//               Next
//               <ChevronRight className="w-5 h-5 ml-2" />
//             </button>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default Results;
// #version 2
// import React, { useState } from "react";
// import { useEffect } from "react";
// import { ChevronLeft, ChevronRight } from "lucide-react";
// import RadialChartsComponent from "./RadialChartsComponent";
// import SocialCostRadialChart from "./SocialCostRadialChart";
// import EnvironmentalCostRadialChart from "./EnvironmentalCostRadialChart";
// import EconomicCost100YearsRadialChart from "./EconomicCost100YearsRadialChart";
// import SocialCost100YearsRadialChart from "./SocialCost100YearsRadialChart";
// import EnvironmentalCost100YearsRadialChart from "./EnvironmentalCost100YearsRadialChart";
// import PieChart from "./PieChart";
// import BarChart from "./BarChart";
// import BubbleChart from "./BubbleChart";
// import HorizontalBarChart from "./HorizontalBarChart";

// const Results = ( { setSelectedProjectDetailWindow,
//   setShowTutorials}) => {
//   const [currentPage, setCurrentPage] = useState(0);
//   const [sidebarVisible, setSidebarVisible] = useState(true);
//     useEffect(() => {
//     setShowTutorials(false);
//     setSelectedProjectDetailWindow("results");
//   }, [setShowTutorials, setSelectedProjectDetailWindow]); 
//   const pages = [
//     {
//       topCharts: [
//         { component: <RadialChartsComponent width={280} height={220} /> },
//         { component: <SocialCostRadialChart width={280} height={220} /> },
//         { component: <EnvironmentalCostRadialChart width={280} height={220} /> }
//       ],
//       bottomChart: { component: <BarChart /> },
//       showLegend: true
//     },
//     {
//       topCharts: [
//         { component: <RadialChartsComponent width={280} height={220} /> },
//         { component: <SocialCostRadialChart width={280} height={220} /> },
//         { component: <EnvironmentalCostRadialChart width={280} height={220} /> }
//       ],
//       bottomChart: { component: <PieChart /> },
//       showLegend: true
//     },
//     {
//       topCharts: [
//         { component: <EconomicCost100YearsRadialChart width={280} height={220} /> },
//         { component: <SocialCost100YearsRadialChart width={280} height={220} /> },
//         { component: <EnvironmentalCost100YearsRadialChart width={280} height={220} /> }
//       ],
//       bottomChart: { component: <HorizontalBarChart /> },
//       showLegend: true
//     },
//     {
//       topCharts: [],
//       bottomChart: { component: <BubbleChart />, fullPage: true },
//       showLegend: false
//     }
//   ];

//   const currentPageData = pages[currentPage];

//   const handleNext = () => {
//     if (currentPage < pages.length - 1) setCurrentPage(currentPage + 1);
//   };

//   const handleBack = () => {
//     if (currentPage > 0) setCurrentPage(currentPage - 1);
//   };

//   const colors = ['#273B5C', '#961818', '#5A003B', '#708090'];
//   const labels = ['Initial Stage', 'Use Stage', 'End-of-Life Stage', 'Beyond-Life Stage'];

//   return (
//     <div className="w-full h-[calc(100vh*11/14)] flex flex-col overflow-hidden">
//       {/* Result Window Tab */}
//       <div className="flex-shrink-0">
//         <div className="overflow-x-auto w-full scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-transparent">
//           <div className="flex w-fit min-w-full">
//             <div
//               className="flex items-center px-4 py-2 rounded-sm border border-gray-300 whitespace-nowrap cursor-default bg-[#F0E6E6] border-b-[#522828b0] border-b-[0.25rem]"
//               style={{ fontSize: '1rem' }}
//             >
//               <span className="font-medium">Result Window</span>
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* Main Content Container */}
//       <div className="flex-1 bg-gray-50 overflow-hidden relative">
//         <div className="h-full flex flex-col">
//           {/* Charts Container */}
//           <div className="flex-1 flex flex-col min-h-0">
//             {/* Top Charts Row */}
//             {currentPageData.topCharts.length > 0 && (
//               <div className="h-64 ">
//                 <div className="grid grid-cols-1 md:grid-cols-3 gap-6 px-2 h-full">
//                   {currentPageData.topCharts.map((chart, index) => (
//                     <div key={index} className="bg-white rounded-lg shadow-lg pt-1  flex items-center justify-center overflow-hidden">
//                       <div className="w-full h-full flex items-center justify-center">
//                         {chart.component}
//                       </div>
//                     </div>
//                   ))}
//                 </div>
//               </div>
//             )}

//             {/* Legend */}
//             {currentPageData.showLegend && (
//               <div className="flex-shrink-0 ">
//                 <div className="flex flex-wrap items-center justify-center gap-4 p-2 rounded-lg shadow-sm">
//                   {colors.map((color, index) => (
//                     <div key={index} className="flex items-center gap-2">
//                       <div 
//                         className="w-3 h-3 rounded-sm"
//                         style={{ backgroundColor: color }}
//                       ></div>
//                       <span className="text-xs font-medium text-gray-700">
//                         {labels[index]}
//                       </span>
//                     </div>
//                   ))}
//                 </div>
//               </div>
//             )}

//             {/* Bottom Chart */}
//             <div className={`${currentPageData.bottomChart.fullPage ? 'flex-1' : 'flex-1'} min-h-0 overflow-hidden`}>
//               <div className="bg-white rounded-lg shadow-lg  h-full overflow-hidden">
//                 <div className="w-full h-full overflow-hidden">
//                   {currentPageData.bottomChart.component}
//                 </div>
//               </div>
//             </div>
//           </div>
//         </div>

//         {/* Navigation Controls - Positioned in bottom right */}
//         <div className="absolute bottom-6 right-6 flex items-center gap-4">
//           {/* Page Indicators */}
         

//           {/* Navigation Buttons */}
//           <div className="flex gap-2">
//             <button
//               onClick={handleBack}
//               disabled={currentPage === 0}
//               className={`flex items-center px-4 py-2 rounded-lg font-medium shadow-md ${
//                 currentPage === 0
//                   ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
//                   : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
//               }`}
//             >
            
//               Back
//             </button>

//             <button
//               onClick={handleNext}
//               disabled={currentPage === pages.length - 1}
//               className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors shadow-md ${
//                 currentPage === pages.length - 1
//                   ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
//                   : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
//               }`}
//             >
//               Next
             
//             </button>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default Results;

// import React, { useState } from "react";
// import { useEffect } from "react";
// import { ChevronLeft, ChevronRight } from "lucide-react";
// import RadialChartsComponent from "./RadialChartsComponent";
// import SocialCostRadialChart from "./SocialCostRadialChart";
// import EnvironmentalCostRadialChart from "./EnvironmentalCostRadialChart";
// import EconomicCost100YearsRadialChart from "./EconomicCost100YearsRadialChart";
// import SocialCost100YearsRadialChart from "./SocialCost100YearsRadialChart";
// import EnvironmentalCost100YearsRadialChart from "./EnvironmentalCost100YearsRadialChart";
// import PieChart from "./PieChart";
// import BarChart from "./BarChart";
// import BubbleChart from "./BubbleChart";
// import HorizontalBarChart from "./HorizontalBarChart";
// import ProjectSidebar from "./ResultsSideBar"; // Import the new sidebar component

// const Results = ({ 
//   setSelectedProjectDetailWindow,
//   setShowTutorials,
//   selectedProjectDetailWindow, // Add this prop
//   setActiveTabs, // Add this prop
//   activeTabs // Add this prop
// }) => {
//   const [currentPage, setCurrentPage] = useState(0);
//   const [sidebarVisible, setSidebarVisible] = useState(true);

//   useEffect(() => {
//     setShowTutorials(false);
//     setSelectedProjectDetailWindow("results");
//   }, [setShowTutorials, setSelectedProjectDetailWindow]); 

//   const pages = [
//     {
//       topCharts: [
//         { component: <RadialChartsComponent width={280} height={220} /> },
//         { component: <SocialCostRadialChart width={280} height={220} /> },
//         { component: <EnvironmentalCostRadialChart width={280} height={220} /> }
//       ],
//       bottomChart: { component: <BarChart /> },
//       showLegend: true
//     },
//     {
//       topCharts: [
//         { component: <RadialChartsComponent width={280} height={220} /> },
//         { component: <SocialCostRadialChart width={280} height={220} /> },
//         { component: <EnvironmentalCostRadialChart width={280} height={220} /> }
//       ],
//       bottomChart: { component: <PieChart /> },
//       showLegend: true
//     },
//     {
//       topCharts: [
//         { component: <EconomicCost100YearsRadialChart width={280} height={220} /> },
//         { component: <SocialCost100YearsRadialChart width={280} height={220} /> },
//         { component: <EnvironmentalCost100YearsRadialChart width={280} height={220} /> }
//       ],
//       bottomChart: { component: <HorizontalBarChart /> },
//       showLegend: true
//     },
//     {
//       topCharts: [],
//       bottomChart: { component: <BubbleChart />, fullPage: true },
//       showLegend: false
//     }
//   ];

//   const currentPageData = pages[currentPage];

//   const handleNext = () => {
//     if (currentPage < pages.length - 1) setCurrentPage(currentPage + 1);
//   };

//   const handleBack = () => {
//     if (currentPage > 0) setCurrentPage(currentPage - 1);
//   };

//   const colors = ['#273B5C', '#961818', '#5A003B', '#708090'];
//   const labels = ['Initial Stage', 'Use Stage', 'End-of-Life Stage', 'Beyond-Life Stage'];

//   return (
//     <div className="flex gap-4 mx-4">
//       {/* Left Panel - Project Sidebar */}
//       {sidebarVisible && (
//         <div className="w-1/6">
//           <ProjectSidebar 
//             selectedWindow={selectedProjectDetailWindow}
//             setSelectedWindow={setSelectedProjectDetailWindow}
//             setShowTutorials={setShowTutorials}
//             setActiveTabs={setActiveTabs}
//             activeTabs={activeTabs}
//             showResultsOutput={true} // This will show the checkboxes in output
//           />
//         </div>
//       )}

//       {/* Right Panel - Charts */}
//       <div className={`${sidebarVisible ? 'w-5/6' : 'w-full'} h-[calc(100vh*11/14)] flex flex-col overflow-hidden`}>
//         {/* Result Window Tab */}
//         <div className="flex-shrink-0">
//           <div className="overflow-x-auto w-full scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-transparent">
//             <div className="flex w-fit min-w-full">
//               <div
//                 className="flex items-center px-4 py-2 rounded-sm border border-gray-300 whitespace-nowrap cursor-default bg-[#F0E6E6] border-b-[#522828b0] border-b-[0.25rem]"
//                 style={{ fontSize: '1rem' }}
//               >
//                 <span className="font-medium">Result Window</span>
//                 {/* Toggle sidebar button */}
               
//               </div>
//             </div>
//           </div>
//         </div>

//         {/* Main Content Container */}
//         <div className="flex-1 bg-gray-50 overflow-hidden relative">
//           <div className="h-full flex flex-col">
//             {/* Charts Container */}
//             <div className="flex-1 flex flex-col min-h-0">
//               {/* Top Charts Row */}
//               {currentPageData.topCharts.length > 0 && (
//                 <div className="h-64">
//                   <div className="grid grid-cols-1 md:grid-cols-3 gap-6 px-2 h-full">
//                     {currentPageData.topCharts.map((chart, index) => (
//                       <div key={index} className="bg-white rounded-lg shadow-lg pt-1 flex items-center justify-center overflow-hidden">
//                         <div className="w-full h-full flex items-center justify-center">
//                           {chart.component}
//                         </div>
//                       </div>
//                     ))}
//                   </div>
//                 </div>
//               )}

//               {/* Legend */}
//               {currentPageData.showLegend && (
//                 <div className="flex-shrink-0">
//                   <div className="flex flex-wrap items-center justify-center gap-4 p-2 rounded-lg shadow-sm">
//                     {colors.map((color, index) => (
//                       <div key={index} className="flex items-center gap-2">
//                         <div 
//                           className="w-3 h-3 rounded-sm"
//                           style={{ backgroundColor: color }}
//                         ></div>
//                         <span className="text-xs font-medium text-gray-700">
//                           {labels[index]}
//                         </span>
//                       </div>
//                     ))}
//                   </div>
//                 </div>
//               )}

//               {/* Bottom Chart */}
//               <div className={`${currentPageData.bottomChart.fullPage ? 'flex-1' : 'flex-1'} min-h-0 overflow-hidden`}>
//                 <div className="bg-white rounded-lg shadow-lg h-full overflow-hidden">
//                   <div className="w-full h-full overflow-hidden">
//                     {currentPageData.bottomChart.component}
//                   </div>
//                 </div>
//               </div>
//             </div>
//           </div>

//           {/* Navigation Controls - Positioned in bottom right */}
//           <div className="absolute bottom-6 right-6 flex items-center gap-4">
//             {/* Navigation Buttons */}
//             <div className="flex gap-2">
//               <button
//                 onClick={handleBack}
//                 disabled={currentPage === 0}
//                 className={`flex items-center px-4 py-2 rounded-lg font-medium shadow-md ${
//                   currentPage === 0
//                     ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
//                     : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
//                 }`}
//               >
//                 Back
//               </button>

//               <button
//                 onClick={handleNext}
//                 disabled={currentPage === pages.length - 1}
//                 className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors shadow-md ${
//                   currentPage === pages.length - 1
//                     ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
//                     : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
//                 }`}
//               >
//                 Next
//               </button>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default Results;
import React, { useState, useEffect } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import RadialChartsComponent from "./RadialChartsComponent";
import SocialCostRadialChart from "./SocialCostRadialChart";
import EnvironmentalCostRadialChart from "./EnvironmentalCostRadialChart";
import EconomicCost100YearsRadialChart from "./EconomicCost100YearsRadialChart";
import SocialCost100YearsRadialChart from "./SocialCost100YearsRadialChart";
import EnvironmentalCost100YearsRadialChart from "./EnvironmentalCost100YearsRadialChart";
import PieChart from "./PieChart";
import BarChart from "./BarChart";
import BubbleChart from "./BubbleChart";
import HorizontalBarChart from "./HorizontalBarChart";
import ReusableSidebar from "./ResultsSideBar";
import FoundationForm from "../ProjectDetails/StructureWorksComponents/FoundationForm";
import SuperStructureForm from "../ProjectDetails/StructureWorksComponents/SuperStructureForm";
import SubStructureForm from "../ProjectDetails/StructureWorksComponents/SubStructureForm";
import MiscellaneousForm from "../ProjectDetails/StructureWorksComponents/MiscellaneousForm";
import EconomicParameter  from "../ProjectDetails/EconomicParameter";
import CarbonEmissionData from "../ProjectDetails/CarbonEmissionData";
import CarbonEmissionCostData from "../ProjectDetails/CarbonEmissionCostData";
import BridgeandTraffic from "../ProjectDetails/BridgeandTraffic";
import MaintenanceandRepairData from "../ProjectDetails/MaintenanceandRepairData";
import DemolitionandRecycling from "../ProjectDetails/DemolitionandRecycling";
// ...existing code...

const Results = ({ setSelectedProjectDetailWindow, setShowTutorials }) => {
  const [currentPage, setCurrentPage] = useState(0);
  const [sidebarVisible, setSidebarVisible] = useState(true);
  const [selectedForm, setSelectedForm] = useState(null);
  const [structureWorksExpanded, setStructureWorksExpanded] = useState(true);
  const [carbonEmissionExpanded, setCarbonEmissionExpanded] = useState(false);
  const [activeTabs, setActiveTabs] = useState([]);
  const [tabToClose, setTabToClose] = useState(null);
  const [showCloseConfirm, setShowCloseConfirm] = useState(false);

  useEffect(() => {
    setShowTutorials(false);
    setSelectedProjectDetailWindow("results");
  }, [setShowTutorials, setSelectedProjectDetailWindow]);

  const pages = [
    {
      topCharts: [
        { component: <RadialChartsComponent width={280} height={220} /> },
        { component: <SocialCostRadialChart width={280} height={220} /> },
        { component: <EnvironmentalCostRadialChart width={280} height={220} /> }
      ],
      bottomChart: { component: <BarChart /> },
      showLegend: true
    },
    {
      topCharts: [
        { component: <RadialChartsComponent width={280} height={220} /> },
        { component: <SocialCostRadialChart width={280} height={220} /> },
        { component: <EnvironmentalCostRadialChart width={280} height={220} /> }
      ],
      bottomChart: { component: <PieChart /> },
      showLegend: true
    },
    {
      topCharts: [
        { component: <EconomicCost100YearsRadialChart width={280} height={220} /> },
        { component: <SocialCost100YearsRadialChart width={280} height={220} /> },
        { component: <EnvironmentalCost100YearsRadialChart width={280} height={220} /> }
      ],
      bottomChart: { component: <HorizontalBarChart /> },
      showLegend: true
    },
    {
      topCharts: [],
      bottomChart: { component: <BubbleChart />, fullPage: true },
      showLegend: false
    }
  ];

  const currentPageData = pages[currentPage];

  const handleNext = () => {
    if (currentPage < pages.length - 1) setCurrentPage(currentPage + 1);
  };

  const handleBack = () => {
    if (currentPage > 0) setCurrentPage(currentPage - 1);
  };

  const colors = ['#273B5C', '#961818', '#5A003B', '#708090'];
  const labels = ['Initial Stage', 'Use Stage', 'End-of-Life Stage', 'Beyond-Life Stage'];

  const outputItems = [
    { text: "Initial Construction Cost", color: "#CC9933" },
    { text: "Initial Carbon Emission Cost", color: "#808000" },
    { text: "Time Cost", color: "#CC9933" },
    { text: "Road User Cost", color: "#8B4513" },
    { text: "Carbon Emission due to Re-Routing", color: "#808000" },
    { text: "Periodic Maintenance Costs", color: "#CC9933" },
    { text: "Maintenance Emission Costs", color: "#808000" },
    { text: "Routine Inspection Costs", color: "#CC9933" },
    { text: "Repair & Rehabilitation Costs", color: "#CC9933" },
    { text: "Reconstruction Costs", color: "#CC9933" },
    { text: "Recycling Cost", color: "#CC9933" },
    { text: "Total Life-Cycle Cost", color: "#CC9933" },
  ];

  // Form navigation handlers
  const handleFormNavigation = (formName) => {
    setSelectedForm(formName);
    setActiveTabs((tabs) => {
      if (!tabs.includes(formName)) {
        return [...tabs, formName];
      }
      return tabs;
    });
  };

  const handleTabClose = (tab) => {
    setTabToClose(tab);
    setShowCloseConfirm(true);
  };

  const onClickTabs = (tab) => {
    setSelectedForm(tab);
  };

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

      setSelectedForm(nextTab);
      return newTabs;
    });

    setShowCloseConfirm(false);
    setTabToClose(null);
  };

  return (
    <div className="flex gap-4 mx-4">
      {/* Left Panel - Sidebar */}
      <div className={`flex flex-col ${selectedForm ? "w-1/6" : "w-1/6"}`}>
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
                      selectedForm === "Foundation"
                        ? "bg-gray-700 text-white"
                        : "hover:bg-gray-100"
                    }`}
                    onClick={() => {
                      setSelectedForm("Foundation");
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
                    className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                      selectedForm === "Super-Structure"
                        ? "bg-gray-700 text-white"
                        : "hover:bg-gray-100"
                    }`}
                    onClick={() => {
                      setSelectedForm("Super-Structure");
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
                    className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                      selectedForm === "Sub-Structure"
                        ? "bg-gray-700 text-white"
                        : "hover:bg-gray-100"
                    }`}
                    onClick={() => {
                      setSelectedForm("Sub-Structure");
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
                    className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                      selectedForm === "Miscellaneous"
                        ? "bg-gray-700 text-white"
                        : "hover:bg-gray-100"
                    }`}
                    onClick={() => {
                      setSelectedForm("Miscellaneous");
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
              className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                selectedForm === "Economic Parameter "
                  ? "bg-gray-700 text-white"
                  : "hover:bg-gray-100"
              }`}
              onClick={() => {
                setSelectedForm("Economic Parameter ");
                setShowTutorials(false);
                setActiveTabs((tabs) => {
                  if (!tabs.includes("Economic Parameter ")) {
                    return [...tabs, "Economic Parameter "];
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
                className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                  selectedForm === "Carbon Emission Data"
                    ? "bg-gray-700 text-white"
                    : "hover:bg-gray-100"
                }`}
                onClick={() => {
                  setSelectedForm("Carbon Emission Data");
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
                    className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                      selectedForm === "Carbon Emission Cost Data"
                        ? "bg-gray-700 text-white"
                        : "hover:bg-gray-100"
                    }`}
                    onClick={() => {
                      setSelectedForm("Carbon Emission Cost Data");
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
              className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                selectedForm === "Bridge and Traffic"
                  ? "bg-gray-700 text-white"
                  : "hover:bg-gray-100"
              }`}
              onClick={() => {
                setSelectedForm("Bridge and Traffic");
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
              className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                selectedForm === "Maintenance and Repair Data"
                  ? "bg-gray-700 text-white"
                  : "hover:bg-gray-100"
              }`}
              onClick={() => {
                setSelectedForm("Maintenance and Repair Data");
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
              className={`flex items-center px-3 py-0.5 text-[13px] cursor-pointer ${
                selectedForm === "Demolition and Recycling"
                  ? "bg-gray-700 text-white"
                  : "hover:bg-gray-100"
              }`}
              onClick={() => {
                setSelectedForm("Demolition and Recycling");
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

          {/* Output Heading */}
          <div className="bg-[#F0E6E6] px-3 py-2 text-lg font-semibold border border-black flex justify-center items-center">
            Output
          </div>

          {/* Output Items with Checkboxes */}
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
                <span className="text-xs leading-tight" style={{ color: item.color }}>
                  {item.text}
                </span>
              </label>
            ))}
          </div>
        </div>
      </div>

      {/* Right Panel - Charts or Form */}
      <div className={`${selectedForm ? "w-3/4" : "w-5/6"} overflow-auto`} style={{ maxHeight: "80vh" }}>
        {selectedForm ? (
          // Show Form
          <div>
            {selectedForm === "Foundation" && (
              <FoundationForm
                setActiveTabs={setActiveTabs}
                Activetabs={activeTabs}
                currentForm="Foundation"
                onNavigate={handleFormNavigation}
                onClose={handleTabClose}
                onclicktabs={onClickTabs}
              />
            )}
            {selectedForm === "Sub-Structure" && (
              <SubStructureForm
                setActiveTabs={setActiveTabs}
                Activetabs={activeTabs}
                currentForm="Sub-Structure"
                onNavigate={handleFormNavigation}
                onClose={handleTabClose}
                onclicktabs={onClickTabs}
              />
            )}
            {selectedForm === "Super-Structure" && (
              <SuperStructureForm
                setActiveTabs={setActiveTabs}
                Activetabs={activeTabs}
                currentForm="Super-Structure"
                onNavigate={handleFormNavigation}
                onClose={handleTabClose}
                onclicktabs={onClickTabs}
              />
            )}
            {selectedForm === "Miscellaneous" && (
              <MiscellaneousForm
                setActiveTabs={setActiveTabs}
                Activetabs={activeTabs}
                currentForm="Miscellaneous"
                onNavigate={handleFormNavigation}
                onClose={handleTabClose}
                onclicktabs={onClickTabs}
              />
            )}
            {selectedForm === "Economic Parameter " && (
              <EconomicParameter 
                currentForm="Economic Parameter "
                onNavigate={handleFormNavigation}
                onClose={handleTabClose}
                onclicktabs={onClickTabs}
                setActiveTabs={setActiveTabs}
                Activetabs={activeTabs}
              />
            )}
            {selectedForm === "Carbon Emission Data" && (
              <CarbonEmissionData
                currentForm="Carbon Emission Data"
                onNavigate={handleFormNavigation}
                onClose={handleTabClose}
                onclicktabs={onClickTabs}
                setActiveTabs={setActiveTabs}
                Activetabs={activeTabs}
              />
            )}
            {selectedForm === "Carbon Emission Cost Data" && (
              <CarbonEmissionCostData
                currentForm="Carbon Emission Cost Data"
                onNavigate={handleFormNavigation}
                onClose={handleTabClose}
                onclicktabs={onClickTabs}
                setActiveTabs={setActiveTabs}
                Activetabs={activeTabs}
              />
            )}
            {selectedForm === "Bridge and Traffic" && (
              <BridgeandTraffic
                currentForm="Bridge and Traffic"
                onNavigate={handleFormNavigation}
                onClose={handleTabClose}
                onclicktabs={onClickTabs}
                setActiveTabs={setActiveTabs}
                Activetabs={activeTabs}
              />
            )}
            {selectedForm === "Maintenance and Repair Data" && (
              <MaintenanceandRepairData
                currentForm="Maintenance and Repair Data"
                onNavigate={handleFormNavigation}
                onClose={handleTabClose}
                onclicktabs={onClickTabs}
                setActiveTabs={setActiveTabs}
                Activetabs={activeTabs}
              />
            )}
            {selectedForm === "Demolition and Recycling" && (
              <DemolitionandRecycling
                currentForm="Demolition and Recycling"
                onNavigate={handleFormNavigation}
                onClose={handleTabClose}
                onclicktabs={onClickTabs}
                setActiveTabs={setActiveTabs}
                Activetabs={activeTabs}
              />
            )}
          </div>
        ) : (
          // Show Charts
          <div className="w-full h-[calc(100vh*11/14)] flex flex-col overflow-hidden">
            {/* Result Window Tab - Only show when no form is selected */}
            <div className="flex-shrink-0">
              <div className="overflow-x-auto w-full scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-transparent">
                <div className="flex w-fit min-w-full">
                  <div
                    className="flex items-center px-4 py-2 rounded-sm border border-gray-300 whitespace-nowrap cursor-default bg-[#F0E6E6] border-b-[#522828b0] border-b-[0.25rem]"
                    style={{ fontSize: '1rem' }}
                  >
                    <span className="font-medium">Result Window</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Main Content Container */}
            <div className="flex-1 bg-gray-50 overflow-hidden relative">
              <div className="h-full flex flex-col">
                {/* Charts Container */}
                <div className="flex-1 flex flex-col min-h-0">
                  {/* Top Charts Row */}
                  {currentPageData.topCharts.length > 0 && (
                    <div className="h-64">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 px-2 h-full">
                        {currentPageData.topCharts.map((chart, index) => (
                          <div key={index} className="bg-white rounded-lg shadow-lg pt-1 flex items-center justify-center overflow-hidden">
                            <div className="w-full h-full flex items-center justify-center">
                              {chart.component}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Legend */}
                  {currentPageData.showLegend && (
                    <div className="flex-shrink-0">
                      <div className="flex flex-wrap items-center justify-center gap-4 p-2 rounded-lg shadow-sm">
                        {colors.map((color, index) => (
                          <div key={index} className="flex items-center gap-2">
                            <div 
                              className="w-3 h-3 rounded-sm"
                              style={{ backgroundColor: color }}
                            ></div>
                            <span className="text-xs font-medium text-gray-700">
                              {labels[index]}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Bottom Chart */}
                  <div className={`${currentPageData.bottomChart.fullPage ? 'flex-1' : 'flex-1'} min-h-0 overflow-hidden`}>
                    <div className="bg-white rounded-lg shadow-lg h-full overflow-hidden">
                      <div className="w-full h-full overflow-hidden">
                        {currentPageData.bottomChart.component}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Navigation Controls - Positioned in bottom right */}
              <div className="absolute bottom-6 right-6 flex items-center gap-4">
                {/* Navigation Buttons */}
                <div className="flex gap-2">
                  <button
                    onClick={handleBack}
                    disabled={currentPage === 0}
                    className={`flex items-center px-4 py-2 rounded-lg font-medium shadow-md ${
                      currentPage === 0
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
                    }`}
                  >
                    Back
                  </button>

                  <button
                    onClick={handleNext}
                    disabled={currentPage === pages.length - 1}
                    className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors shadow-md ${
                      currentPage === pages.length - 1
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
                    }`}
                  >
                    Next
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Close Confirmation Modal */}
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

export default Results;