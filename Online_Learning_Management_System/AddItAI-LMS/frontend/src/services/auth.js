import API from "./api";

// register
export const registerUser = (data) => {
    return API.post("register/",data);
};

// login
export const loginUser = async (data) => {
    try{
        const res = await API.post("login/",data);
        localStorage.setItem("user", JSON.stringify(res.data));
        localStorage.setItem("access",res.data.access);
        localStorage.setItem("refresh",res.data.refresh);

        window.dispatchEvent(new Event("storage"));

        return res.data;
    }catch (error){
        throw error.response?.data || {error: "Login failed"};
    }    
};

export const logoutUser = () => {
  localStorage.clear();
  window.dispatchEvent(new Event("storage"));
  window.location.href = "/login";
};