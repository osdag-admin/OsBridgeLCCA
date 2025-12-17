import React from 'react';
import img1 from '../media/image1.png';
import img2 from '../media/image2.png';
import img3 from '../media/image.png';
const tabs = ["Tutorials", "Project Details", "Results", "Compare"];

const TabNavigation = ({ activeTab, onTabChange, setShowTutorials, showTutorials }) => {
  return (
    <div className='flex items-center justify-between border-b py-1.5 px-4'>
      {/* Left: Logos */}
      <div className='flex items-center gap-5'>
        <img src={img1} alt="Logo" className="w-10" />
        <img src={img2} alt="Logo1" className="w-10" />
        <img src={img3} alt="Logo3" className="w-10" />
      </div>

      {/* Center: Windows + Tabs */}
      <div className='flex items-center justify-center flex-1'>
        <span className="mr-2">Windows :</span>
        <nav className="flex text-xs ">
          {tabs.map((tab) => {
            if (tab === "Tutorials") {
              return (
                <button
                  key={tab}
                  onClick={() => {
                    if (!showTutorials) {
                      setShowTutorials(true);
                    }
                  }}
                  className={`px-2 py-1 border border-gray-400 font-bold text-black ${
                    activeTab === tab ? 'bg-gray-300' : 'bg-gray-200'
                  }`}
                >
                  {tab}
                </button>
              );
            } else {
              return (
                <button
                  key={tab}
                  onClick={() => onTabChange(tab)}
                  className={`px-2 py-1 border border-gray-400 font-bold text-black ${
                    activeTab === tab ? 'bg-gray-300' : 'bg-gray-200'
                  }`}
                >
                  {tab}
                </button>
              );
            }
          })}
        </nav>
      </div>

      {/* Right: Empty or more buttons (optional) */}
      <div className="w-24" /> {/* Spacer to balance layout */}
    </div>
  );
};


export default TabNavigation;
