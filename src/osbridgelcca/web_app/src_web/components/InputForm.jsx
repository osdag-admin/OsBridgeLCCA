import React, { useState } from "react";
import axios from "../services/api";

const InputForm = ({ setResults }) => {
    const [inputs, setInputs] = useState({ project_name: "", bill_of_quantity: {} });

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await axios.post("/calculate", inputs);
        setResults(response.data);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Project Name" onChange={(e) => setInputs({ ...inputs, project_name: e.target.value })} />
            <button type="submit">Calculate LCC</button>
        </form>
    );
};

export default InputForm;
