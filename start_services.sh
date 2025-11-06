#!/bin/bash

# Start FastAPI server
echo "Starting FastAPI server..."
python api.py &
API_PID=$!

# Wait for API to be ready
sleep 5

# Start Streamlit app
echo "Starting Streamlit frontend..."
streamlit run streamlit_app.py --server.port 8501 &
STREAMLIT_PID=$!

echo "=========================="
echo "Services started:"
echo "FastAPI API: http://localhost:8000"
echo "Streamlit UI: http://localhost:8501"
echo "=========================="
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $API_PID $STREAMLIT_PID" INT
wait
