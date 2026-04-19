import axios from "axios";

const API =axios.create({baseURL: "http://127.0.0.1:8000/api/",});

// attach token automatically
// request interceptor
API.interceptors.request.use((req) => {
    const token = localStorage.getItem("access");
    if (token) {
        req.headers.Authorization = `Bearer ${token}`;
    }
    console.log("Request URL:", req.url);
    console.log("Token:", token);
    return req;
});

// response interceptor ( auto refresh)
API.interceptors.response.use(
  (res) => res,
  async (error) => {
    const originalRequest = error.config;

    // if token expired
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
        const refresh = localStorage.getItem("refresh");

        if (!refresh) {
            localStorage.clear();
            window.location.href = "/login";
            return Promise.reject(error);
        }
        
        try{        
            const res = await axios.post(
            "http://127.0.0.1:8000/api/token/refresh/",
            { refresh }
            );

            const newAccess = res.data.access;

            localStorage.setItem("access", newAccess);
            
            if (!originalRequest.headers) {
                originalRequest.headers = {};
            }

            // retry original request
            originalRequest.headers.Authorization = `Bearer ${newAccess}`;
            return API(originalRequest);
        }catch (err) {
            // refresh failed → logout
            localStorage.clear();
            window.location.href = "/login";
        }
    }

    return Promise.reject(error);
  }
);
export default API;