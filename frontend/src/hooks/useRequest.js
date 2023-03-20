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
/*
const onTokenExpire = async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401) {

   
    
        console.log(sessionStorage.getItem('refresh'));

        const res = await axios.post('http://127.0.0.1:8000/users/refresh/', {"refresh": sessionStorage.getItem('refresh')})

        console.log(res)

        sessionStorage.setItem('access', res.data.access);

        //originalRequest.headers['Authorization'] = "Bearer " + res.data.access;

        return;
    
         
    }
    return Promise.reject(error);
  };
  */

const useRequest = (endpoint) => {
    const [response, setResponse] = useState(null);
    const [loading, setloading] = useState(true);
    const [error, seterror] = useState(null);
    const {getAccessToken} = useAuth()

    const doRequest = useCallback(
        async (data={}) => {
        try {
            
            const client = axios.create({
                baseURL: 'http://127.0.0.1:8000/',
                method: endpoint.method,
                data: formalize(data),
                headers: endpoint.isAuth ? {Authorization: 'Bearer ' +  getAccessToken()} : {}
                
            })

            //client.interceptors.response.use((response) => response, onTokenExpire);

            const res = await client.request(endpoint.url)

            console.log(endpoint.url, res)
            setResponse(res)

        } catch (err) {
            seterror("Error")
            console.log(err)
        }

        setloading(false)

    }, [getAccessToken])


    return { response, loading, error, doRequest };
};

export default useRequest;