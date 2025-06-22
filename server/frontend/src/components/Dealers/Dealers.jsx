import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);

  const dealer_url = "/djangoapp/get_dealers/";

  const filterDealers = async (state) => {
    console.log("Estado selecionado:", state);
  
    if (state === "All") {
      get_dealers();
      return;
    }
  
    const url = `/djangoapp/get_dealers/${state}/`;
    try {
      const res = await fetch(url);
      const dealers = await res.json();
  
      console.log("Dealers recebidos:", dealers);
      console.log("É array?", Array.isArray(dealers), "| Tamanho:", dealers.length);
  
      setDealersList(Array.from(dealers));
    } catch (error) {
      console.error("Erro ao filtrar dealers:", error);
    }
  };

  const get_dealers = async () => {
    try {
      const res = await fetch(dealer_url);
      const retobj = await res.json();
      const all_dealers = retobj.dealers || [];
      const stateList = [...new Set(all_dealers.map((d) => d.state))];
      setStates(stateList);
      setDealersList(all_dealers);
    } catch (error) {
      console.error("Erro ao buscar todos os dealers:", error);
    }
  };

  useEffect(() => {
    get_dealers();
  }, []);

  const isLoggedIn = sessionStorage.getItem("username") !== null;

  return (
    <div>
      <Header />
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <select
                name="state"
                id="state"
                onChange={(e) => filterDealers(e.target.value)}
                defaultValue=""
              >
                <option value="" disabled hidden>State</option>
                <option value="All">All States</option>
                {states.map((state, idx) => (
                  <option key={idx} value={state}>{state}</option>
                ))}
              </select>
            </th>
            {isLoggedIn && <th>Review Dealer</th>}
          </tr>
        </thead>
    <tbody>
  {dealersList.length === 0 ? (
    <tr>
      <td colSpan={isLoggedIn ? 7 : 6} style={{ textAlign: "center", padding: "1rem" }}>
        Nenhum dealer encontrado para esse estado.
      </td>
    </tr>
  ) : (
    dealersList.map((dealer) => (
      <tr key={dealer.id}>
        <td>{dealer.id}</td>
        <td><a href={`/dealer/${dealer.id}`}>{dealer.full_name}</a></td>
        <td>{dealer.city}</td>
        <td>{dealer.address}</td>
        <td>{dealer.zip}</td>
        <td>{dealer.state}</td>
        {isLoggedIn && (
          <td>
            <a href={`/postreview/${dealer.id}`}>
              <img src={review_icon} className="review_icon" alt="Post Review" />
            </a>
          </td>
        )}
      </tr>
    ))
  )}
</tbody>
      </table>
    </div>
  );
};

export default Dealers;