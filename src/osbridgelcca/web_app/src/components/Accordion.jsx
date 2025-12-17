import React, { useState } from 'react';
const Accordion = ({ title, children, level = 0 }) => {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div>
      <button
        className={`${(level>0)? "text-sm mb-2 bg-[#F0E6E6]":" bg-[#F0E6E6] hover:bg-rose-100"} ml-${level * 6} rounded-sm w-full text-left text-base px-4 py-2  `}
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? '\u2BC6' : '\u2BC8'}  &nbsp;
         {title}
      </button>
      {isOpen && <div className="pb-2 text-sm">{children}</div>}
    </div>
  );
};
export default Accordion;