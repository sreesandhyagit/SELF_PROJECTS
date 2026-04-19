import { useEffect, useRef, useState } from "react";
import { getProfile, updateProfile } from "../../services/profile";

function Profile() {
    const [form,setForm]=useState({
        username:"",
        email:"",
        bio:"",
        profile_image:null,
    });

    const [preview,setPreview] = useState(null);    
    const [loading,setLoading] = useState(false);
    const previousPreview = useRef(null);

    // fetch profile
    useEffect(() => {
        fetchProfile();
    }, []);

    //cleanup effect
    useEffect(() => {        
        if (
            previousPreview.current &&
            previousPreview.current.startsWith("blob:")
        ) {
            URL.revokeObjectURL(previousPreview.current);
        }
        previousPreview.current = preview;
    }, [preview]);

    const fetchProfile =async() => {
        try {
            const res = await getProfile();
            setForm({
                username:res.data.username || "",
                email:res.data.email || "",
                bio:res.data.bio || "",
                profile_image: null,
            });

            if (res.data.profile_image){
                setPreview(`http://127.0.0.1:8000${res.data.profile_image}`);
            }            
        } catch(err){
            console.log(err);
        }
    };

    //handle change
    const handleChange = (e) => {
        setForm({...form,[e.target.name]:e.target.value});
    };

    //handle image
    const handleImageChange = (e) => {
        const file = e.target.files[0];
        console.log(file);
        setForm({...form, profile_image:file});
        if (file){
            setPreview(URL.createObjectURL(file));
        }
    };

    //submit
    const handleSubmit = async (e) =>{
        e.preventDefault();
        setLoading(true);

        const formData = new FormData();
        formData.append("username",form.username);
        formData.append("email",form.email);
        formData.append("bio",form.bio);

        if (form.profile_image){
            formData.append("profile_image",form.profile_image);
        }

        for (let pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }

        try{
            const res = await updateProfile(formData);
            console.log("SUCCESS", res.data);

            // update local storage
            const oldUser = JSON.parse(localStorage.getItem("user") || "{}");
            const newImage = res.data?.data?.profile_image;
            const fullImageUrl = newImage ? `http://127.0.0.1:8000${newImage}` : null;

            const updateUser = {
                ...oldUser, //
                username:form.username,
                email:form.email,
                profile_image:fullImageUrl,
            };

            localStorage.setItem("user", JSON.stringify(updateUser));

            if (newImage) {
                setPreview(fullImageUrl);
            }

            //refresh navbar
            window.dispatchEvent(new Event("storage"));

            alert("Profile updated successfully");            
        } catch(err){
            console.log(err.response?.data);
        }finally{
            setLoading(false);
        }
    };
    return (
        <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
            
            {/* Container */}
            <div className="max-w-4xl mx-auto">

            {/* HEADER */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow p-6 flex items-center gap-6 mb-6">

                {/* Avatar */}
                <div className="relative">
                {preview ? (
                    <img
                    src={preview}
                    alt="Profile"
                    className="w-24 h-24 rounded-full object-cover border"
                    />
                ) : (
                    <div className="w-24 h-24 rounded-full bg-blue-600 text-white flex items-center justify-center text-3xl font-bold">
                    {(form.username?.[0] || "U").toUpperCase()}
                    </div>
                )}

                {/* Upload button */}
                <label className="absolute bottom-0 right-0 bg-blue-600 text-white p-1 rounded-full cursor-pointer text-xs">
                    ✏️
                    <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    className="hidden"
                    />
                </label>
                </div>

                {/* User Info */}
                <div>
                <h2 className="text-xl font-bold">
                    {form.username || "Your Name"}
                </h2>
                <p className="text-gray-500">{form.email}</p>
                </div>
            </div>

            {/* FORM CARD */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow p-6">

                <h3 className="text-lg font-semibold mb-4">
                Edit Profile
                </h3>

                <form onSubmit={handleSubmit} className="space-y-4">

                {/* Username */}
                <div>
                    <label className="text-sm text-gray-500">Username</label>
                    <input
                    name="username"
                    value={form.username}
                    onChange={handleChange}
                    className="w-full mt-1 px-4 py-2 border rounded-lg bg-white dark:bg-gray-700"
                    />
                </div>

                {/* Email */}
                <div>
                    <label className="text-sm text-gray-500">Email</label>
                    <input
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    className="w-full mt-1 px-4 py-2 border rounded-lg bg-white dark:bg-gray-700"
                    />
                </div>

                {/* Bio */}
                <div>
                    <label className="text-sm text-gray-500">Bio</label>
                    <textarea
                    name="bio"
                    value={form.bio}
                    onChange={handleChange}
                    rows="4"
                    className="w-full mt-1 px-4 py-2 border rounded-lg bg-white dark:bg-gray-700"
                    />
                </div>

                {/* Button */}
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-500 transition"
                >
                    {loading ? "Updating..." : "Save Changes"}
                </button>
                </form>
            </div>
            </div>
        </div>
        );

    // return (
    //     <div className="min-h-screen flex justify-center items-center bg-gray-100 dark:bg-gray-900 p-4 ">
    //         <div className="w-full max-w-lg bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 p-6 rounded-2xl shadow-lg">
    //             <h2 className="text-2xl font-bold text-center mb-6">My Profile</h2>

    //             {/* image */}                
    //             <div className="flex flex-col items-center mb-4">

    //                 {/* Avatar */}
    //                 {preview ? (
    //                     <img
    //                     src={preview}
    //                     alt="Profile"
    //                     className="w-24 h-24 rounded-full object-cover mb-2"
    //                     />
    //                 ) : (
    //                     <div className="w-24 h-24 rounded-full bg-blue-600 text-white flex items-center justify-center text-3xl font-bold mb-2">
    //                     {(form.username?.[0] || "U").toUpperCase()}
    //                     </div>
    //                 )}

    //                 {/* File Input */}
    //                 <label className="text-sm cursor-pointer text-blue-600 hover:underline">
    //                     Change Photo
    //                     <input
    //                         type="file"
    //                         accept="image/*"
    //                         onChange={handleImageChange}
    //                         className="hidden"
    //                     />
    //                 </label>
    //             </div>

    //             {/* form */}
    //             <form onSubmit={handleSubmit} className="space-y-4">
    //                 <input
    //                 name="username"
    //                 value={form.username}
    //                 onChange={handleChange}
    //                 placeholder="Username"
    //                 className="w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700"
    //                 />

    //                 <input
    //                 name="email"
    //                 value={form.email}
    //                 onChange={handleChange}
    //                 placeholder="Email"
    //                 className="w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700"
    //                 />

    //                 <textarea
    //                 name="bio"
    //                 value={form.bio}
    //                 onChange={handleChange}
    //                 placeholder="Bio"
    //                 rows="3"
    //                 className="w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700"
    //                 />

    //                 <button
    //                 type="submit"
    //                 className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-500"
    //                 >
    //                     {loading ? "Updating..." : "Update Profile"}
    //                 </button>
    //             </form>
    //         </div>
    //     </div>
    // );
}

export default Profile;
