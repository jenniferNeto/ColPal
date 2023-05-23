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
    const [loading, setloading] = useState(false);
    const [error, seterror] = useState(null);
    const { getAccessToken } = useAuth()

    const doRequest = useCallback(
        async (data = {}) => {
            try {
                setloading(true)
                const res = await axios({
                    url: 'http://127.0.0.1:8000' + endpoint.url,
                    method: endpoint.method,
                    data: data,
                    headers: endpoint.isAuth ?
                        { ...endpoint.headers, Authorization: 'Bearer ' + getAccessToken() } :
                        endpoint.headers

                })

                console.log(endpoint.url, res)
                seterror(null)
                setResponse(res)

            } catch (err) {
                console.log(err)
                seterror(err)
                setResponse(null)
            } finally {
                setloading(false)
            }

            

        }, [getAccessToken])

        const invalidate = useCallback(() => {
            setResponse(null)
            setloading(true)
            seterror(null)
        }, [])

    return { response, loading, error, doRequest, invalidate };
};

export default useRequest;