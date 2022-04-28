import './App.scss';
import { Routes, Route } from "react-router-dom";
import Home from "./components/pages/home/Home";
import About from "./components/pages/about/About";
import Navbar from "./components/navbar/Navbar";

function App() {
  return (
      <>
          <Navbar/>
          <Routes>
            <Route path="/" element={<Home/>}/>
            <Route path="about" element={<About/>}/>
          </Routes>
      </>
  );
}

export default App;
