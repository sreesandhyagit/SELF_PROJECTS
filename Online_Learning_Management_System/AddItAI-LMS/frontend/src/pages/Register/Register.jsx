import { useState } from "react";
import { registerUser } from "../../services/auth";
import { useNavigate } from "react-router-dom";

function Register() {
  const navigate = useNavigate();

  const [errors, setErrors] = useState({});

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: null });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    if (form.password !== form.confirm_password) {
      
      alert("Passwords do not match");
      setLoading(false);
      return;
    }

    try {
      const res = await registerUser(form);
      alert(res.data.message);
      navigate("/login");
    } catch (err) {
      setErrors(err.response?.data || {});
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900 transition">
      <div className="w-full max-w-md bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 p-8 rounded-2xl shadow-lg">

        <h2 className="text-2xl font-bold text-center mb-6">
          Create Account
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">

          <input
            name="username"
            placeholder="Username"
            onChange={handleChange}
            value={form.username}
            className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700 dark:border-gray-600
              ${errors.username ? "border-red-500" : ""}
            `}
          />

          {errors.username && (
            <p className="text-red-500 text-sm">{errors.username[0]}</p>
          )}

          <input
            name="email"
            type="email"
            placeholder="Email"
            onChange={handleChange}
            value={form.email}
            className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700 dark:border-gray-600
              ${errors.username ? "border-red-500" : ""}
            `}
          />

          {errors.email && (
            <p className="text-red-500 text-sm">{errors.email[0]}</p>
          )}

          <input
            name="password"
            type="password"
            placeholder="Password"
            onChange={handleChange}
            value={form.password}
            className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700 dark:border-gray-600
              ${errors.username ? "border-red-500" : ""}
            `}
          />
          {errors.password && (
            <p className="text-red-500 text-sm">{errors.password[0]}</p>
          )}

          <input
            name="confirm_password"
            type="password"
            placeholder="Confirm Password"
            onChange={handleChange}
            value={form.confirm_password}
            className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700 dark:border-gray-600
              ${errors.username ? "border-red-500" : ""}
            `}
          />
          {errors.confirm_password && (
            <p className="text-red-500 text-sm">{errors.confirm_password[0]}</p>
          )}

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-500"
          >
            {loading ? "Registering..." : "Register"}
          </button>
        </form>

        <p className="text-sm text-center mt-4 text-gray-500 dark:text-gray-400">
          Already have an account?{" "}
          <span
            onClick={() => navigate("/login")}
            className="text-blue-500 cursor-pointer"
          >
            Login
          </span>
        </p>
      </div>
    </div>
  );
}

export default Register;