import { Link } from "react-router-dom";
import logo from "../../assets/images/logonew.png";
import SearchBar from "../SearchBar/SearchBar";
import ThemeToggle from "../ThemeToggle/ThemeToggle";
import LanguageDropdown from "../LanguageDropdown/LanguageDropdown";
import CoursesDropdown from "../CoursesDropdown/CoursesDropdown";
import { FaShoppingCart } from "react-icons/fa";

const Navbar = () => {
  return (
    <nav className="flex items-center justify-between px-6 py-3 shadow-md bg-white text-gray-700 
    dark:bg-gray-900 dark:text-white transition-all duration-300">

      <div className="flex items-center gap-6">        
        <Link to="/"><img src={logo} alt="AdditAI Logo" className="h-12 cursor-pointer rounded-2xl" /></Link>
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
          hover:bg-blue-700 transition dark:text-gray-200"
        >
          Sign up
        </Link>

      </div>
    </nav>
  );
};

export default Navbar;