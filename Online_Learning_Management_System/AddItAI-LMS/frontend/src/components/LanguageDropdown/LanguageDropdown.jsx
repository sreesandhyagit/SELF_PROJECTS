import { FaGlobe } from "react-icons/fa";

const LanguageDropdown = () => {
  return (
    <div className="relative group">

      {/* Icon Button */}
      <div className="flex items-center gap-2 cursor-pointer 
      hover:scale-110 transition p-2 rounded-full border">
        <FaGlobe className="text-gray-800 dark:text-gray-300" />
      </div>

      {/* Hover bridge (prevents gap issue) */}
      <div className="absolute top-full left-0 h-2 w-full"></div>

      {/* Dropdown */}
      <div className="absolute right-0 top-full mt-2 w-32 
      bg-white dark:bg-gray-800 
      text-black dark:text-white 
      shadow-lg rounded 
      hidden group-hover:block hover:block z-50">

        <p className="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer">
          English
        </p>

        <p className="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer">
          Hindi
        </p>

        <p className="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer">
          Malayalam
        </p>

      </div>
    </div>
  );
};

export default LanguageDropdown;