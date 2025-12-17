import React, { useState } from 'react';
const Accordionp = ({ title, children, level = 0 }) => {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div>
      <button
        className={`${(level>0)? "text-sm" : "hover:bg-rose-100"} ml-${level * 12}  rounded-sm w-full text-left text-base  `}
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? '\u2BC6' : '\u2BC8'}  &nbsp;
         {title}
      </button>
      {isOpen && <div className=" text-sm">{ children}</div>}
    </div>
  );
};
export default Accordionp;