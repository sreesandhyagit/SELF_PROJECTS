import CourseCard from "../../components/CourseCard/CourseCard";
import HeroSlider from "../../components/HeroSlider/HeroSlider";

const Home = () => {
  return (
    <div className="bg-gray-100 text-black dark:bg-gray-800 dark:text-white min-h-screen">

      <HeroSlider />
            
      <div className="p-6">
        <h2 className="text-2xl font-bold mb-4">Courses</h2>

        <div className="grid md:grid-cols-3 gap-6">
          {/* <CourseCard /> */}
        </div>
      </div>

    </div>
  );
};

export default Home;