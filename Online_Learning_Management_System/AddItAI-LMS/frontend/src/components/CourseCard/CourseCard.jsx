const CourseCard = ({ course }) => {
  return (
    <div className="bg-white rounded shadow hover:shadow-lg">
      <img src={course.image} alt="" className="w-full rounded-t" />
      <div className="p-4">
        <h4 className="font-bold">{course.title}</h4>
        <p className="text-sm text-gray-600">{course.instructor}</p>
        <p className="text-purple-600 font-semibold mt-2">
          {course.price}
        </p>
      </div>
    </div>
  );
};

export default CourseCard;