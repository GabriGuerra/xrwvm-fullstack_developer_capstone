import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(null);

  const params = useParams();
  const id = params.id;

  const curr_url = window.location.href;
  const root_url = curr_url.substring(0, curr_url.indexOf("dealer"));
  const dealer_url = `${root_url}djangoapp/dealer/${id}`;
  const reviews_url = `${root_url}djangoapp/reviews/dealer/${id}`;
  const post_review_url = `${root_url}postreview/${id}`;

  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url);
      const data = await res.json();
      if (data.status === 200 && Array.isArray(data.dealer) && data.dealer.length > 0) {
        setDealer(data.dealer[0]);
      }
    } catch (error) {
      console.error("Erro ao buscar dealer:", error);
    }
  };

  const get_reviews = async () => {
    try {
      const res = await fetch(reviews_url);
      const data = await res.json();
      if (data.status === 200) {
        if (data.reviews.length > 0) {
          setReviews(data.reviews);
        } else {
          setUnreviewed(true);
        }
      }
    } catch (error) {
      console.error("Erro ao buscar reviews:", error);
    }
  };

  const senti_icon = (sentiment) => {
    if (sentiment === "positive") return positive_icon;
    if (sentiment === "negative") return negative_icon;
    return neutral_icon;
  };

  useEffect(() => {
    get_dealer();
    get_reviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(
        <a href={post_review_url}>
          <img
            src={review_icon}
            alt="Post Review"
            style={{ width: "10%", marginLeft: "10px", marginTop: "10px" }}
          />
        </a>
      );
    }
  }, []);

  return (
    <div style={{ margin: "20px" }}>
      <Header />
      {dealer ? (
        <>
          <div style={{ marginTop: "10px" }}>
            <h1 style={{ color: "grey" }}>
              {dealer.full_name} {postReview}
            </h1>
            <h4 style={{ color: "grey" }}>
              {dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}
            </h4>
          </div>
        </>
      ) : (
        <p>Carregando informações do concessionário...</p>
      )}
      <div className="reviews_panel">
        {reviews.length === 0 && !unreviewed ? (
          <p>Loading Reviews...</p>
        ) : unreviewed ? (
          <div>No reviews yet!</div>
        ) : (
          reviews.map((review, index) => (
            <div className="review_panel" key={index}>
              <img
                src={senti_icon(review.sentiment)}
                className="emotion_icon"
                alt="Sentiment"
              />
              <div className="review">{review.review}</div>
              <div className="reviewer">
                {review.name} {review.car_make} {review.car_model} {review.car_year}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dealer;