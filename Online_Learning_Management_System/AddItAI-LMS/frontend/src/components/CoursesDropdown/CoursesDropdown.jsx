const CoursesDropdown = () => {
  return (
    <div className="relative group">
      
      <button className="px-3 py-2 hover:bg-gray-100 rounded hover:text-blue-600">
        Courses
      </button>

      <div className="absolute top-full left-0 h-2 w-full"></div>
     

      <div className="absolute left-0 top-full mt-2 w-56 bg-white dark:bg-gray-800 
      text-black dark:text-white shadow-lg rounded hidden group-hover:block hover:block z-50">

        <ul className="flex flex-col">

          <li className="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer">
            Development
          </li>

          <li className="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer">
            Business
          </li>

          <li className="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer">
            Design
          </li>

          <li className="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer">
            Marketing
          </li>

        </ul>
      
      </div>
    </div>
  );
};

export default CoursesDropdown;