import { createContext, useContext, useState } from "react";

const FormDataContext = createContext();

export const useFormData = () => useContext(FormDataContext);

export const FormDataProvider = ({ children }) => {
  const [formData, setFormData] = useState({
    generalInfo: {
      companyName: "",
      projectTitle: "",
      projectDescription: "",
      valuerName: "",
      jobNumber: "",
      client: "",
      country: "India",
      baseYear: "",
    },
    inputParameters: {
      // Structure this based on your next accordion levels
    },
    outputResults: {
      // You can also store output here
    },
  });

  return (
    <FormDataContext.Provider value={{ formData, setFormData }}>
      {children}
    </FormDataContext.Provider>
  );
};
