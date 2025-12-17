import { useState } from "react";

const DropdownMenu = () => {
  const [activeMenu, setActiveMenu] = useState(null);

  const menus = {
    File: [
      "New", "Open", "Save", "Save As...", "Create a copy",
      "Print", "Rename", "Export", "Version History", "Info"
    ],
    Home: [],
    Reports: [],
    Help: ["Contact Us", "Feedback", "Video Tutorials", "Join our Community"],
  };

  function handleMenuClick(label) {
    setActiveMenu(activeMenu === label ? null : label);
  }
  return (
    <div className="bg-white border-b flex items-center px-8 py-1 font-semibold text-black space-x-6 relative z-20">
      {Object.entries(menus).map(([label, items]) => (
        <div
          key={label}
          className="relative"
          onClick={() => handleMenuClick(label)}
        >
          <button className="hover:text-green-600 text-sm">{label}</button>

          {activeMenu === label && activeMenu != "Home" && activeMenu != "Reports" &&  (
            <div className="absolute top-6 mt-1 w-44 bg-white border shadow-xl rounded-md py-2 z-50" onMouseLeave={() => setActiveMenu(null)}>
              {items.map((item, idx) => (
                <div
                  key={idx}
                  className="px-4 py-1.5 text-sm hover:bg-green-50 hover:text-green-700 cursor-pointer flex items-center text-gray-700"
                >
                {item}
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default DropdownMenu;
