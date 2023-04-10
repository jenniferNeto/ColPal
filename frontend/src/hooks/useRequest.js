import axios from "axios";
import { useState, useCallback } from "react";
import { useAuth } from "../context/UserContext";

const formalize = (data) => {
    let form_data = new FormData();
    for (let key in data) {
        form_data.append(key, data[key]);
    }
    return form_data;
}
const useRequest = (endpoint) => {
    const [response, setResponse] = useState(null);
    const [loading, setloading] = useState(true);
    const [error, seterror] = useState(null);
    const { getAccessToken } = useAuth()

    const doRequest = useCallback(
        async (data = {}) => {
            try {
                const res = await axios({
                    url: 'http://127.0.0.1:8000' + endpoint.url,
                    method: endpoint.method,
                    data: formalize(data),
                    headers: endpoint.isAuth ?
                        { ...endpoint.headers, Authorization: 'Bearer ' + getAccessToken() } :
                        endpoint.headers

                })

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