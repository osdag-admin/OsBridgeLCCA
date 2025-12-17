import React, { useState } from 'react';

import Accordion from '../Accordion';
import FoundationForm from './StructureWorksComponents/FoundationForm';
import SuperStructureForm from './StructureWorksComponents/SuperStructureForm';
import SubStructureForm from './StructureWorksComponents/SubStructureForm';
import MiscellaneousForm from './StructureWorksComponents/MiscellaneousForm';

const StructureWorksData = ({  setActiveTabs,Activetabs, onSelectForm }) => {
  return (
    <div className="flex flex-col  text-sm">
      <button 
        onClick={() => onSelectForm('Foundation')} 
        className=" rounded-sm w-full text-left  ml-20"
      >
          {"\u2BC8"} &nbsp; Foundation
      </button>
      <button 
        onClick={() => onSelectForm('Sub-Structure')} 
        className=" rounded-sm w-full text-left   ml-20"
      >
          {"\u2BC8"} &nbsp; Sub-Structure
      </button>
      <button 
        onClick={() => onSelectForm('Super-Structure')} 
        className=" rounded-sm w-full text-left    ml-20"
      >
          {"\u2BC8"} &nbsp; Super-Structure
      </button>
      <button 
        onClick={() => onSelectForm('Miscellaneous')} 
        className=" rounded-sm w-full text-left    ml-20"
      >
          {"\u2BC8"} &nbsp; Miscellaneous
      </button>
    </div>
  );
};

export default StructureWorksData;