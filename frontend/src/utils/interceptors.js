const onRequest = () => {
    const token = JSON.parse(localStorage.getItem("token"));
    config.headers["Authorization"] = `Bearer ${token.access_token}`;
  
    return config;
  };
  
  const onRequestError =  () => {
    return Promise.reject(error);
  };
  
  const onResponse = () => {
    return response;
  };
  
  const onResponseError = async () => {
    if (error.response) {
      // Access Token was expired
      if (
        error.response.status === 401 &&
        error.response.data.message === "jwt expired"
      ) {
        const storedToken = JSON.parse(localStorage.getItem("token"));
  
        try {
          const rs = await axios.post(`${API_URL}/auth/refresh`, {
            refresh_token: storedToken.refresh_token,
          });
  
          const { token, user } = rs.data;
  
          localStorage.setItem("token", JSON.stringify(token));
          localStorage.setItem("user", JSON.stringify(user));
  
          return;
        } catch (_error) {
          return Promise.reject(_error);
        }
      }
    }
    return Promise.reject(error);
  };
  
  export const setupInterceptorsTo = () => {
    axiosInstance.interceptors.request.use(onRequest, onRequestError);
    axiosInstance.interceptors.response.use(onResponse, onResponseError);
    return axiosInstance;
  };