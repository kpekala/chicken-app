# Chicken App

A FastAPI backend and SvelteKit frontend for displaying shops and geographic areas on a Leaflet map.

## Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer and npm

## Project structure

- `backend/` - FastAPI API and JSON data files
- `frontend/` - SvelteKit application with Leaflet

## Setup

Clone the repository and open a terminal in the project root:

```text
chicken-app/
```

### 1. Set up the Python backend

Create and activate a virtual environment:

#### Windows PowerShell

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### macOS/Linux

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

Install the backend dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Set up the Svelte frontend

Open a second terminal in the project root, then install the frontend dependencies:

```bash
cd frontend
npm install
```

## Run the application

Run the backend in the terminal where its virtual environment is activated:

```bash
cd backend
python -m uvicorn main:app --reload
```

The API is available at <http://localhost:8000>. The interactive API documentation is at <http://localhost:8000/docs>.

Run the frontend in the second terminal:

```bash
cd frontend
npm run dev
```

Open <http://localhost:5173> in a browser.

The frontend requests data from these backend endpoints:

- `GET http://localhost:8000/stores`
- `GET http://localhost:8000/polygons`

## Useful commands

Run frontend checks:

```bash
cd frontend
npm run check
npm run lint
```

Create and preview a production frontend build:

```bash
cd frontend
npm run build
npm run preview
```

Stop either development server with `Ctrl+C`. To leave the Python virtual environment, run:

```bash
deactivate
```
