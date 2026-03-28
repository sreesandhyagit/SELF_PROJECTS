import { FaSearch } from "react-icons/fa";

const SearchBar = () => {
  return (
    <div className="relative w-full">
      
      {/* Search Icon */}
      <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 
      text-gray-500 dark:text-gray-300" />

      {/* Input */}
      <input
        type="text"
        placeholder="Search for courses..."
        className="w-full pl-10 pr-4 py-2 border rounded-full 
        bg-gray-100 text-black 
        dark:bg-gray-800 dark:text-white 
        focus:outline-none"
      />
      
    </div>
  );
};

export default SearchBar;