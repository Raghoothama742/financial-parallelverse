#!/bin/bash
echo "Starting Financial Parallelverse services..."
export PYTHONPATH=.

# Start backend in background
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Start Streamlit UI
python -m streamlit run frontend_streamlit/app.py --server.port 8501 &
STREAMLIT_PID=$!

echo "Backend running on PID $BACKEND_PID (http://localhost:8000/api/docs)"
echo "Streamlit running on PID $STREAMLIT_PID (http://localhost:8501)"

trap "kill $BACKEND_PID $STREAMLIT_PID" SIGINT SIGTERM
wait
