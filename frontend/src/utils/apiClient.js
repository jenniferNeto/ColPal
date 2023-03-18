import axios from 'axios'

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/',
    timeout: 5000
});

/*
apiClient.interceptors.response.use(
    response => response,
    error => {
      const originalRequest = error.config;
      
      if (error.response.status === 401) {
          const refresh_token = sessionStorage.getItem('refresh');
            
          return apiClient.post('/users/refresh/', {refresh: refresh_token})
              .then((response) => {

                  sessionStorage.setItem('access', response.data.access);
                  sessionStorage.setItem('refresh', response.data.refresh);

                  apiClient.defaults.headers['Authorization'] = "Bearer " + response.data.access;
                  originalRequest.headers['Authorization'] = "Bearer " + response.data.access;

                  return apiClient(originalRequest);
              })
              .catch(err => {
                  console.log(err)
              });
      }
      return Promise.reject(error);
  }
);*/
export default apiClient