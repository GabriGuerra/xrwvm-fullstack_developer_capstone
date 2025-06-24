# Dealership Review Platform — Capstone Project

![Last Commit](https://img.shields.io/github/last-commit/GabriGuerra/xrwvm-fullstack_developer_capstone)
![Repo Size](https://img.shields.io/github/repo-size/GabriGuerra/xrwvm-fullstack_developer_capstone)
![License](https://img.shields.io/github/license/GabriGuerra/xrwvm-fullstack_developer_capstone)

Aplicação fullstack para visualização e avaliação de concessionárias de carros, construída como parte do IBM Fullstack Developer Capstone. A solução integra frontend em React, backend Django, microsserviços Node.js, integração com MongoDB e análise de sentimentos  — tudo orquestrado com Docker, Kubernetes e deploy na IBM Cloud.

---

##  Arquitetura

A plataforma é composta por múltiplos serviços:

- **Django Web Application**
  - Autenticação de usuários
  - Páginas dinâmicas com templates
  - Views e models para Car Make e Car Model (SQLite)
  - Proxy para microsserviços externos e análise de sentimento
- **Node.js + Express API** (Dockerized)
  - Banco de dados MongoDB
  - Endpoints para `fetchDealers`, `fetchReviews`, `insertReview`
- **Sentiment Analyzer**
  - Serviço externo hospedado via IBM Code Engine
  - Retorna sentimento `positive`, `neutral` ou `negative` baseado em texto
- **Frontend SPA**
  - React JS para autenticação de usuários e experiência interativa

---

##  Tecnologias Utilizadas

- **Linguagens & Frameworks:**
  - Python 3.12, Django 4.x, Node.js (Express)
  - React.js (SPA)
- **Banco de dados:**
  - MongoDB (para reviews e dealers)
  - SQLite (para carros)
- **Integração e Deploy:**
  - IBM Cloud Code Engine
  - IBM Cloud Container Registry (ICR)
  - Docker & Kubernetes
  - Gunicorn + Docker entrypoint scripts
- **Qualidade e CI/CD:**
  - pre-commit hooks (`black`, `flake8`, `autoflake`, `jshint`)
  - GitHub Actions (CI pipelines)
- **Outros:**
  - IBM Cloud CLI
  - JSON parsing com Node.js
  - Regex search no MongoDB
  - Templates Django + consumo de APIs REST
