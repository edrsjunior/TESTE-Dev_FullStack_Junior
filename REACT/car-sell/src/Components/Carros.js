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
        <div className="row mt-3 ">
          {this.state.carros.map((carro) => (
                <div key={carro.id} className="card ms-3 mt-4 col-3" style={{width: '18rem'}}>
                  <img src={carro.photoUrl} className="card-img-top" alt="..." ></img>
                  <div className="card-body ">
                    <h5 className="card-title">{carro.nome} • {carro.modelo} • {carro.marca}</h5>
                    <ul className="list-group list-group-flush ">
                    <li className="list-group-item infoAnoKm">Ano: {carro.ano} | KM {carro.km.toLocaleString('pt-br',{number: 'BRL' })}</li>
                    <li className="list-group-item valor">{carro.valor.toLocaleString('pt-br',{ style: 'currency', currency: 'BRL' })}</li>
                    <li className="list-group-item descricao">{carro.descricao.substr(0,150)}...</li>
                    </ul>
                    <a href="#" class="btn btn-primary mt-2 col-12">Comprar</a>
                  </div>
                </div>
          ))}
        </div>
      );
    }
  }
  
  export default Carros;