import React from "react";
import Carros from "./Components/Carros";
import './App.css'

const App = () => {
  return (
    <div>
      <nav className="navbar navbar-dark bg-primary">
        <div className="container-fluid">
          <a className="navbar-brand" hre="#">
            Car Shop
          </a>
        </div>
      </nav>
      <div className="ps-5">
        <Carros div="veiculos" />
      </div>
    </div>
    
  );
};

export default App;
