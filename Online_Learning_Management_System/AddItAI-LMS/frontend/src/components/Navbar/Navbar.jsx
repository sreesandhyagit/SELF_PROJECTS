import { Link, useNavigate } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import logo from "../../assets/images/logo.png";
import SearchBar from "../SearchBar/SearchBar";
import ThemeToggle from "../ThemeToggle/ThemeToggle";
import LanguageDropdown from "../LanguageDropdown/LanguageDropdown";
import CoursesDropdown from "../CoursesDropdown/CoursesDropdown";
import { FaShoppingCart } from "react-icons/fa";
import { logoutUser } from "../../services/auth";

const Navbar = () => {

  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef();

  useEffect(() => {
    checkAuth();
    //listen for login/logout changes
    window.addEventListener("storage",checkAuth);

    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown",handleClickOutside);

    return()=>{
      window.removeEventListener("storage",checkAuth);
      document.removeEventListener("mousedown",handleClickOutside);
    };
  },[]);

  const checkAuth = () => {
    const token=localStorage.getItem("access");
    const userData=localStorage.getItem("user");
    setIsLoggedIn(!!token);
    try{
      setUser(userData && userData !== "undefined" ? JSON.parse(userData):null);
    } catch {
      setUser(null);
    }    
  };

  const handleLogout = () => {
    logoutUser();
  };

  return (
    <nav className="flex items-center justify-between px-6 py-3 shadow-md bg-white text-gray-700 
    dark:bg-gray-900 dark:text-white transition-all duration-300">

      <div className="flex items-center gap-6">        
        <Link to="/"><img src={logo} alt="AdditAI Logo" className="h-9 cursor-pointer rounded" /></Link>
        <CoursesDropdown />
      </div>

      <div className="flex-1 mx-6 hidden md:block">
        <SearchBar />
      </div>

      <div className="flex items-center gap-4">

        <Link to="/teach" className="hidden md:block hover:text-blue-600 transition hover:bg-gray-100 rounded">
          Teach with us
        </Link>
        
        <Link to="/cart" className="relative text-xl p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition">
          <FaShoppingCart className="text-xl text-blue-500 dark:text-gray-400 
            hover:text-blue-800 transition" />
          {/* <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs px-1 rounded-full">
            2
          </span> */}
        </Link>
      
        <LanguageDropdown />
        
        <ThemeToggle />

        {!isLoggedIn ? (
          <>
            <Link 
              to="/login" 
              className=" font-bold border border-orange-600 text-blue-900 dark:border-white px-4 py-1 rounded 
              hover:text-blue-800 hover:bg-gray-100 dark:hover:bg-gray-800 transition dark:text-gray-400"
            >
              Log in
            </Link>

            <Link 
              to="/register" 
              className="font-bold bg-blue-900 text-white px-4 py-1 rounded 
              hover:bg-blue-800 transition dark:text-gray-200"
            >
              Sign up
            </Link>

          </>
        ) : (
          <>
            {/* Profile */}
            <div className="relative" ref={dropdownRef}>

              {/* Avatar (initial) */}
              <div
                onClick={() => setOpen(!open)}
                className="w-9 h-9 rounded-full bg-blue-600 text-white flex items-center justify-center cursor-pointer font-semibold"
              >
                {user?.profile_image ? (
                  <img
                    src={user.profile_image}
                    className="w-9 h-9 rounded-full object-cover"
                  />
                ) : (
                  user?.username?.charAt(0).toUpperCase()
                )}
              </div>

              {/* Dropdown */}
              {open && (
                <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 shadow-lg rounded-lg overflow-hidden z-50">

                  <div className="px-4 py-2 border-b dark:border-gray-700 text-sm">
                    👋 {user?.username}
                  </div>

                  <button
                    onClick={() => {
                      navigate("/profile");
                      setOpen(false);
                    }}
                    className="w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    View Profile
                  </button>

                  <button
                    onClick={() => {
                      navigate("/profile/edit");
                      setOpen(false);
                    }}
                    className="w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    Edit Profile
                  </button>

                  <button
                    onClick={() => {
                      handleLogout();
                      setOpen(false);
                    }}
                    className="w-full text-left px-4 py-2 text-red-500 hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    Logout
                  </button>

                </div>
              )}
            </div>
          
          </>
        )}
        
      </div>
    </nav>
  );
};

export default Navbar;

