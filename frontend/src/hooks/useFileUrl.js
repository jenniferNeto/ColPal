import { useState, useEffect } from "react";
import axios from "axios";

const useFileUrl = (fileUrl) => {
    
    const [file, setFile] = useState(null);
    const [loading, setloading] = useState(false);
    const [error, seterror] = useState(null);

    useEffect(() => {
        if (!fileUrl) return;

        const getFile = async () => {
            const baseUrl = "https://storage.cloud.google.com/dataplatformcolgate_cloudbuild/"
            const fileName = fileUrl.split("/").pop()
            try {
                setloading(true)
                const config = { responseType: 'blob' };
                const res = await axios.get(baseUrl+fileUrl, config)
                setFile(new File([res.data], fileName))  
            } catch (err) {
                seterror("Error")
                console.log(err)
            } finally{
                setloading(false)
            }
        }

        getFile()

    }, [fileUrl])


    return {file, loading, error};
};

export default useFileUrl;