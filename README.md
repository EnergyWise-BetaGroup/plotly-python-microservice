# 🌍 EnergyWise Python Micro Service

## 📌 Overview

The aim of this python microservice is to create plotly visualisations which seamlessly integrate with frontend and backend applications.

- The EnergyWise front end application: https://github.com/EnergyWise-BetaGroup/energy-wise-frontend
- The EnergyWise back end application: https://github.com/EnergyWise-BetaGroup/energy-wise-backend

## 🚀 Features

- Live data visualisations
- Interactive charts
- Dockerization

## 🛠️ Setup

1. Fork the repository

2. Clone your fork locally.

```sh
git clone [REPO_URL]
cd [REPO_NAME]
```

3. Build a docker image for this repository and for the backend application:

```sh
docker build -t [username]/[image name]:[release] [Dockerfile path]
```

4. Update the docker-compose file with the name of your images

5. Start your application:

```sh
docker compose up
```

## 🛠️ Visualisation check

This repository contains a client folder to check visualisations before implementing them to a front end application

## 🔧 Backend Connection

This application is connected to the backend via the designated app.route path:

```
@app.route("/generate-visualisation", methods=["POST"])
```

This path has been specified within the backend application controller

## 📜 License

This project is licensed under La Fosse Academy.
