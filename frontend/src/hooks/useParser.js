import { useState, useEffect } from "react";
import Papa from "papaparse";

const useParser = (file) => {
    
    const [columns, setColumns] = useState(null);
    const [rows, setRows] = useState(null);

    useEffect(() => {
        if (!file) return;

        const reader = new FileReader();
        // Event listener on reader when the file
        // loads, we parse it and set the data.
        reader.onload = async ({ target }) => {
          
            const csv = Papa.parse(target.result, { header: true });
            const parsedData = csv?.data;
           
            setRows(parsedData)
            setColumns(Object.keys(parsedData[0]));
    
        };
    
        reader.readAsText(file);

    }, [file])


    return {columns, rows};
};

export default useParser;