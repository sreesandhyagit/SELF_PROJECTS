import { useEffect, useState } from "react";
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

    // fetch profile
    useEffect(() => {
        fetchProfile();
    },[]);

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
                setPreview(res.data.profile_image);
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

        try{
            await updateProfile(formData);
            alert("Profile updated successfully");            
        } catch(err){
            console.log(err.response?.data);
        }finally{
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex justify-center items-center bg-gray-100 dark:bg-gray-900 p-4 ">
            <div className="w-full max-w-lg bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 p-6 rounded-2xl shadow-lg">
                <h2 className="text-2xl font-bold text-center mb-6">My Profile</h2>

                {/* image */}
                <div className="flex flex-col items-center mb-4">
                    <img
                        src={preview || "https://via.placeholder.com/100"}
                        alt="Profile"
                        className="w-24 h-24 rounded-full object-cover mb-2"
                    />
                    
                    <input type="file" accept="image/*" onChange={handleImageChange} />
                </div>

                {/* form */}
                <form onSubmit={handleSubmit} className="space-y-4">
                    <input
                    name="username"
                    value={form.username}
                    onChange={handleChange}
                    placeholder="Username"
                    className="w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700"
                    />

                    <input
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    placeholder="Email"
                    className="w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700"
                    />

                    <textarea
                    name="bio"
                    value={form.bio}
                    onChange={handleChange}
                    placeholder="Bio"
                    rows="3"
                    className="w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700"
                    />

                    <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-500"
                    >
                        {loading ? "Updating..." : "Update Profile"}
                    </button>
                </form>
            </div>
        </div>
    );
}

export default Profile;
