import API from "./api";

//get profile
export const getProfile =() => {
    return API.get("profile/");
};

//update profile
export const updateProfile =(FormData) => {
    return API.patch("profile/", FormData, {
        headers: {
            "Content-Type":"multipart/form-data",
        },
    });
};