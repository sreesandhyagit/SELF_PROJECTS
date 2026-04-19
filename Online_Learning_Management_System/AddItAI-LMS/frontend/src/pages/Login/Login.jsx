import { useState } from "react";
import { loginUser } from "../../services/auth";
import { useNavigate } from "react-router-dom";

function Login () {
  const navigate =useNavigate();

  const [form,setForm] = useState({
    email:"",
    password:""    
  });

  const handleChange =(e) => {
    setForm({...form,[e.target.name]:e.target.value});
  };

  const handleSubmit = async (e) =>{
    e.preventDefault();
    
    try{
      const data = await loginUser(form);
      alert("Login successful");
      // console.log(data);
      navigate("/");
    } catch(err){
      // console.log(err.response.data);
      alert("Invalid credentials");
    }
  };

  return (  

    <div className="flex h-screen bg-white dark:bg-gray-900 transition">

      {/* Left side */}
      <div className="hidden md:block w-1/2 relative">
        <img
          src="https://images.unsplash.com/photo-1498050108023-c5249f4df085"
          alt="LMS"
          className="h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-black/60 flex items-center justify-center">
          <div className="text-white text-center px-10">
            <h1 className="text-4xl font-bold mb-4">AdditAI LMS</h1>
            <p className="text-lg">Learn smarter with AI-powered courses 🚀</p>
          </div>
        </div>
      </div>

      {/* Right side */}
      <div className="flex w-full md:w-1/2 items-center justify-center">

        <form
          onSubmit={handleSubmit}
          className="bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 p-8 rounded-2xl shadow-lg w-[90%] max-w-md transition"
        >
          <h2 className="text-2xl font-bold mb-2">Welcome Back 👋</h2>
          <p className="text-gray-500 dark:text-gray-400 mb-6">
            Login to continue learning
          </p>

          <input
            type="email"
            name="email"
            placeholder="Email"
            onChange={handleChange}
            required
            className="w-full mb-4 px-4 py-3 border rounded-lg bg-white dark:bg-gray-700 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 outline-none"
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            onChange={handleChange}
            required
            className="w-full mb-4 px-4 py-3 border rounded-lg bg-white dark:bg-gray-700 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 outline-none"
          />

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-500 transition"
          >
            Login
          </button>

          <p className="mt-4 text-sm text-gray-600 dark:text-gray-400 text-center">
            Don't have an account?{" "}
            <span
              onClick={() => navigate("/register")}
              className="text-blue-500 cursor-pointer"
            >
              Register
            </span>
          </p>
        </form>
      </div>
    </div>
  );
}

export default Login;