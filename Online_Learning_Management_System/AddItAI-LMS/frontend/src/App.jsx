import { BrowserRouter,Routes, Route } from "react-router-dom";
import Home from "./pages/Home/Home";
import Login from "./pages/Login/Login";
import Register from "./pages/Register/Register";
import CourseDetails from "./pages/CourseDetails/CourseDetails";
import Navbar from "./components/Navbar/Navbar";
import Profile from "./pages/Profile/Profile";
import ProtectedRoute from "./routes/ProtectedRoute";


function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        
        {/* public */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />                        
        <Route path="/register" element={<Register />} />
        <Route path="/course/:id" element={<CourseDetails />} />

        {/* protected route */}
        <Route 
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>        
          }
        /> 

      </Routes>
    </BrowserRouter>
  );
}

export default App;