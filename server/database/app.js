const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

console.log("💥 ESTE É O APP.JS ATUALIZADO 💥");
app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));
app.use((req, res, next) => {
    console.log(` Requisição recebida: ${req.method} ${req.url}`);
    next();
  });

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB' });

const Reviews = require('./review');
const Dealerships = require('./dealership');

(async () => {
  try {
    const reviewCount = await Reviews.countDocuments();
    if (reviewCount === 0) {
      await Reviews.insertMany(reviews_data['reviews']);
      console.log("Reviews carregados no MongoDB.");
    } else {
      console.log("Reviews já existentes. Nenhuma inserção feita.");
    }

    const dealerCount = await Dealerships.countDocuments();
    if (dealerCount === 0) {
      await Dealerships.insertMany(dealerships_data['dealerships']);
      console.log("Dealers carregados no MongoDB.");
    } else {
      console.log("Dealers já existentes. Nenhuma inserção feita.");
    }

  } catch (error) {
    console.error('Erro ao inicializar dados do banco:', error);
  }
})();

// Home route
app.get('/', (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch reviews by dealer ID
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: parseInt(req.params.id) });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Fetch dealerships by state — aqui vai o diagnóstico
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const stateParam = req.params.state;
    console.log("Estado recebido:", JSON.stringify(stateParam));

    const documents = await Dealerships.find({
      $or: [
        { state: { $regex: new RegExp(`^${stateParam}$`, 'i') } },
        { st: { $regex: new RegExp(`^${stateParam}$`, 'i') } }
      ]
    });

    console.log("Dealers encontrados:", documents.length);
    res.json(documents);
  } catch (error) {
    console.error("Erro na rota /fetchDealers/:state:", error);
    res.status(500).json({ error: 'Erro interno' });
  }
});

// Fetch single dealer by ID
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id);
    const document = await Dealerships.findOne({ id: dealerId });
    if (document) {
      res.json(document);
    } else {
      res.status(404).json({ error: 'Dealer not found' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer by ID' });
  }
});

// Insert a new review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  try {
    const data = JSON.parse(req.body);
    const documents = await Reviews.find().sort({ id: -1 });
    const new_id = documents[0]?.id + 1 || 1;

    const review = new Reviews({
      id: new_id,
      name: data['name'],
      dealership: data['dealership'],
      review: data['review'],
      purchase: data['purchase'],
      purchase_date: data['purchase_date'],
      car_make: data['car_make'],
      car_model: data['car_model'],
      car_year: data['car_year'],
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});