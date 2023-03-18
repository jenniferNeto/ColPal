import axios from "axios";
import {  useState, useCallback } from "react";
import { useAuth } from "../context/UserContext";

function formalize(data){
    let form_data = new FormData();

    for ( let key in data ) {
        form_data.append(key, data[key]);
    }

    return form_data
}

const useRequest = (endpoint, isAuth=false) => {
    const [response, setResponse] = useState(null);
    const [loading, setloading] = useState(true);
    const [error, seterror] = useState(null);
    const {accessToken} = useAuth()

    const doRequest = useCallback(
        async (data={}) => {
        try {
            
            const res = await axios({
                baseURL: 'http://127.0.0.1:8000/',
                url: endpoint, 
                method: 'get',
                data: formalize(data),
                headers: isAuth ? {Authorization: 'Bearer ' +  accessToken} : {}
                
            })

            console.log(endpoint, res)
            setResponse(res)

        } catch (err) {
            seterror("Error")
            console.log(err)
        }

        setloading(false)

    }, [endpoint, accessToken])

 

    return { response, loading, error, doRequest };
};

export default useRequest;