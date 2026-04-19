import { useEffect, useState } from "react";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";

const images = [
  "https://images.unsplash.com/photo-1519389950473-47ba0277781c",
  "https://images.unsplash.com/photo-1501504905252-473c47e087f8",
  "https://images.unsplash.com/photo-1498050108023-c5249f4df085",
];

const HeroSlider = () => {
  const [index, setIndex] = useState(0);

  // Auto slide
  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % images.length);
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  // Manual navigation
  const prevSlide = () => {
    setIndex((prev) => (prev - 1 + images.length) % images.length);
  };

  const nextSlide = () => {
    setIndex((index + 1) % images.length);
  };

  return (
    <div className="w-full h-[400px] relative overflow-hidden">
      
      {/* Image */}
      <img
        src={images[index]}
        alt="banner"
        className="w-full h-full object-cover"
      />

      {/* Dark overlay */}
      <div className="absolute inset-0 bg-black/40"></div>

      {/* Overlay Text */}
      <div className="absolute top-1/3 left-10 text-white z-10 bg-black/30 p-4 rounded">
        <h1 className="text-4xl font-bold">
          Learn Anytime, Anywhere
        </h1>
        <p className="mt-2">
          Upgrade your skills with AdditAI
        </p>

        {/* Button */}
        <button className="mt-4 bg-purple-600 px-4 py-2 rounded hover:bg-purple-700">
          Explore Courses
        </button>
      </div>

      {/* Left Arrow */}
      <button
        onClick={prevSlide}
        className="absolute left-4 top-1/2 -translate-y-1/2 
        bg-black/50 hover:bg-black/70 text-white 
        p-3 rounded-full z-10 transition hover:scale-110"
      >
        <FaChevronLeft />
      </button>

      {/* Right Arrow */}
      <button
        onClick={nextSlide}
        className="absolute right-4 top-1/2 -translate-y-1/2 
        bg-black/50 hover:bg-black/70 text-white 
        p-3 rounded-full z-10 transition hover:scale-110"
      >
        <FaChevronRight />
      </button>

      {/* Dots */}
      <div className="absolute bottom-4 w-full flex justify-center gap-2">
        {images.map((_, i) => (
          <div
            key={i}
            onClick={() => setIndex(i)}
            className={`w-3 h-3 rounded-full cursor-pointer ${
              i === index
                ? "bg-white scale-125"
                : "bg-gray-400"
            }`}
          />
        ))}
      </div>
    </div>
  );
};

export default HeroSlider;