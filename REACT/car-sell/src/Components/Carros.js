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
        <div className="row">
          {this.state.carros.map((carro) => (
                <div key={carro.id} className="card mt-3 ms-3 col-3" style={{width: '18rem'}}>
                  <img src={carro.photoUrl} className="card-img-top" alt="..." ></img>
                  <div className="card-body">
                    <h5 className="card-title">{carro.nome} • {carro.modelo} • {carro.marca}</h5>
                    <ul className="list-group list-group-flush">
                    <li className="list-group-item infoAnoKm">Ano: {carro.ano} | KM{carro.km}</li>
                    <li className="list-group-item valor">R$: {carro.valor}</li>
                    <li className="list-group-item descricao">{carro.descricao}</li>
                    </ul>
                  </div>
                </div>
          ))}
        </div>
      );
    }
  }
  
  export default Carros;