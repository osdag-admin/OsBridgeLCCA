import './App.css'

import TabNavigation from './components/TabNavigation';
import DropDown from './components/DropDown';
import Tutorials from './components/Tutorials/Tutorials';
import ProjectDetails from './components/ProjectDetails/ProjectDetails';
import Results from './components/Results/Results';
import Compare from './components/Compare/Compare';
import { FormDataProvider } from './components/FormDataContext';
import { useState, useEffect } from 'react'; // ✅ correct
// ← this might already exist


function App() {

  const [activeTab, setActiveTab] = useState("Project Details");
  const [showTutorials, setShowTutorials] = useState(true);
  const [SelectedProjectDetailWindow, setSelectedProjectDetailWindow] = useState(null); // ✅ new state

  function handleTabChange(tab) {
    setActiveTab(tab);
    setSelectedProjectDetailWindow(null); // Clear structure view on tab switch
  }
   // ✅ Only reset the detail window when tutorials are shown
  useEffect(() => {
    if (showTutorials === true) {
      setSelectedProjectDetailWindow(null);
    }
  }, [showTutorials]);

  // function handleTabChange(tab) {
  //   setActiveTab(tab);
  // }

  return (
    <FormDataProvider>
      <div className="min-h-screen">

        <header
          className="text-md font-semibold flex items-center justify-center h-9 text-white"
          style={{ backgroundColor: '#45913E' }}
        >
        Bridge 3PS-LCC 
        </header>

        <DropDown />

        <TabNavigation activeTab={activeTab} onTabChange={handleTabChange} showTutorials={showTutorials} setShowTutorials={setShowTutorials} />


        <div className={` ${showTutorials ? "grid grid-cols-[auto_1fr] " : " "}"
  } gap-24  px-8 mt-4`}>
          {showTutorials && (
            <Tutorials onClose={() => setShowTutorials(false)} showTutorials={showTutorials} />
          )}

          {activeTab === "Project Details" &&  ( <ProjectDetails 
              SelectedProjectDetailWindow={SelectedProjectDetailWindow} 
              setSelectedProjectDetailWindow={setSelectedProjectDetailWindow}
              setShowTutorials={setShowTutorials}
            />)}
          {activeTab === "Results" && <Results   setShowTutorials={setShowTutorials}
  setSelectedProjectDetailWindow={setSelectedProjectDetailWindow} />}
          {activeTab === "Compare" && <Compare />}

        </div>

      </div>
    </FormDataProvider>

  )
}

export default App
