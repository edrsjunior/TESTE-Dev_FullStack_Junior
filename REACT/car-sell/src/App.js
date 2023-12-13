import React, { Component } from "react";
import axios from "axios";

class Carros extends Component {
  state = {
    carros: [],
  };

  componentDidMount() {
    axios
      .get("http://localhost:8000/carros")
      .then((response) => {
        if (response.status === 200) {
          this.setState({ carros: JSON.parse(response.data).map((carro) => ({
            id: carro.id,
            nome: carro.nome,
            marca: carro.marca,
            modelo: carro.modelo,
            ano: carro.ano,
            km: carro.km,
            valor: carro.valor,
            descricao: carro.descricao,
            photoUrl: carro.photoUrl,
          })) });
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }

  render() {
    return (
      <div>
        <h1>Carros</h1>
        {this.state.carros.map((carro) => (
          <div key={carro.id}>
            <h2>{carro.nome}</h2>
            <p>{carro.marca}</p>
            <p>{carro.modelo}</p>
            <p>{carro.ano}</p>
            <p>{carro.km}</p>
            <p>{carro.valor}</p>
            <p>{carro.descricao}</p>
            <img src={carro.photoUrl}></img>
          </div>
        ))}
      </div>
    );
  }
}

export default Carros;
