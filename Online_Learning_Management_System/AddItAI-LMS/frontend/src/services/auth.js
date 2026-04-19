import API from "./api";

// register
export const registerUser = (data) => {
    return API.post("register/",data);
};

// login
export const loginUser = async (data) => {
    try{
        const res = await API.post("login/",data);

        localStorage.setItem("access",res.data.access);
        localStorage.setItem("refresh",res.data.refresh);

        let profileData ={};

        try{
            //fetch full profile after login
            const profileRes = await API.get("profile/");
            profileData = profileRes.data;
        }catch(err) {
            console.warn("Profile fetch failed")
        }        

        const fullUser = {
            ...res.data,
            ...profileData,
        };

        localStorage.setItem("user", JSON.stringify(fullUser));       

        //update UI
        window.dispatchEvent(new Event("storage"));

        return fullUser;
    }catch (error){
        throw error.response?.data || {error: "Login failed"};
    }    
};

export const logoutUser = () => {
  localStorage.clear();
  window.dispatchEvent(new Event("storage"));
  window.location.href = "/login";
};