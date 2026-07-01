"""
Cloud Backend for Health Monitoring System
Aggregates predictions from multiple ARM devices
Detects health outbreaks
Provides analytics API
"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
import sqlite3
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from performance_metrics import perf_db, PerformanceMetric, PerformanceStats
from typing import Optional

app = FastAPI(
    title="Health Monitoring Cloud",
    description="Aggregates health data from ARM edge devices",
    version="1.0.0"
)
@app.get("/dashboard.html")
def get_dashboard():
    """Serve dashboard HTML"""
    return FileResponse("dashboard.html")
# Enable CORS for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Database setup
def init_db():
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY,
            device_id TEXT,
            risk_score INTEGER,
            heart_rate INTEGER,
            blood_pressure INTEGER,
            timestamp DATETIME,
            location TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Data models
class HealthPrediction(BaseModel):
    device_id: str
    risk_score: int
    heart_rate: int
    blood_pressure: int
    location: str = "Unknown"

class HealthStats(BaseModel):
    total_predictions: int
    average_risk: float
    high_risk_count: int
    outbreak_status: str

# Routes
@app.get("/")
def read_root():
    return {
        "message": "Health Monitoring Cloud Backend",
        "status": "🟢 Running",
        "version": "1.0.0",
        "endpoints": [
            "/predict (POST)",
            "/stats (GET)",
            "/outbreak (GET)",
            "/devices (GET)"
        ]
    }

@app.post("/predict")
def receive_prediction(prediction: HealthPrediction):
    """
    Receive a health prediction from an ARM device
    """
    try:
        conn = sqlite3.connect('health_data.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO predictions 
            (device_id, risk_score, heart_rate, blood_pressure, timestamp, location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            prediction.device_id,
            prediction.risk_score,
            prediction.heart_rate,
            prediction.blood_pressure,
            datetime.now(),
            prediction.location
        ))
        conn.commit()
        conn.close()
        
        return {
            "status": "✅ Prediction received",
            "device_id": prediction.device_id,
            "risk_score": prediction.risk_score,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_statistics() -> HealthStats:
    """
    Get aggregated health statistics from all devices
    """
    try:
        conn = sqlite3.connect('health_data.db')
        c = conn.cursor()
        
        # Total predictions
        c.execute('SELECT COUNT(*) FROM predictions')
        total = c.fetchone()[0]
        
        # Average risk
        c.execute('SELECT AVG(risk_score) FROM predictions')
        avg_risk = c.fetchone()[0] or 0
        
        # High risk count
        c.execute('SELECT COUNT(*) FROM predictions WHERE risk_score > 70')
        high_risk = c.fetchone()[0]
        
        conn.close()
        
        # Determine outbreak status
        outbreak_threshold = 0.15  # 15% of predictions are high risk
        outbreak_rate = high_risk / max(total, 1)
        outbreak_status = "🔴 OUTBREAK DETECTED" if outbreak_rate > outbreak_threshold else "🟢 Normal"
        
        return HealthStats(
            total_predictions=total,
            average_risk=round(avg_risk, 2),
            high_risk_count=high_risk,
            outbreak_status=outbreak_status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/outbreak")
def get_outbreak_info():
    """
    Get outbreak detection information
    """
    try:
        conn = sqlite3.connect('health_data.db')
        c = conn.cursor()
        
        # Get data from last 24 hours
        yesterday = datetime.now() - timedelta(days=1)
        c.execute('''
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN risk_score > 70 THEN 1 ELSE 0 END) as high_risk
            FROM predictions
            WHERE timestamp > ?
        ''', (yesterday,))
        
        result = c.fetchone()
        total_24h = result[0]
        high_risk_24h = result[1] or 0
        
        conn.close()
        
        risk_percentage = (high_risk_24h / max(total_24h, 1)) * 100
        
        return {
            "period": "Last 24 hours",
            "total_predictions": total_24h,
            "high_risk_predictions": high_risk_24h,
            "high_risk_percentage": round(risk_percentage, 2),
            "alert_level": "🔴 HIGH" if risk_percentage > 15 else "🟡 MODERATE" if risk_percentage > 5 else "🟢 LOW",
            "recommendation": "Monitor closely" if risk_percentage > 15 else "Continue monitoring"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/devices")
def get_device_summary():
    """
    Get summary of all connected devices
    """
    try:
        conn = sqlite3.connect('health_data.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT device_id, COUNT(*) as predictions, 
                   AVG(risk_score) as avg_risk,
                   MAX(risk_score) as max_risk
            FROM predictions
            GROUP BY device_id
            ORDER BY predictions DESC
        ''')
        
        devices = []
        for row in c.fetchall():
            devices.append({
                "device_id": row[0],
                "total_predictions": row[1],
                "average_risk": round(row[2], 2),
                "peak_risk": row[3]
            })
        
        conn.close()
        
        return {
            "total_devices": len(devices),
            "devices": devices
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test")
def test_prediction():
    """
    Test endpoint - sends sample prediction
    """
    test_data = HealthPrediction(
        device_id="device-001",
        risk_score=45,
        heart_rate=78,
        blood_pressure=125,
        location="Cambridge"
    )
    return receive_prediction(test_data)
# ============================================================================
# WEEK 5: PERFORMANCE METRICS ENDPOINTS
# ============================================================================

@app.get("/performance/benchmark")
async def get_benchmark_data():
    """Get ARM optimization benchmarks"""
    return perf_db.get_benchmark_data()

@app.get("/performance/summary")
async def get_performance_summary():
    """Performance summary for dashboard display"""
    benchmark = perf_db.get_benchmark_data()
    latency_stats = perf_db.get_metric_stats("latency")
    power_stats = perf_db.get_metric_stats("power")
    
    return {
        "headline": "ARM Cortex-A enables real-time health monitoring at the edge",
        "optimization": {
            "original_model_size_mb": benchmark.original_size_mb,
            "optimized_model_size_mb": benchmark.model_size_mb,
            "compression_percent": round(benchmark.compression_ratio, 1),
        },
        "performance": {
            "inference_latency_ms": latency_stats.current_value,
            "latency_avg_ms": latency_stats.avg_value,
            "power_consumption_mw": power_stats.current_value,
            "power_avg_mw": power_stats.avg_value,
            "accuracy_percent": 89.2
        }
    }

@app.get("/performance/metrics")
async def get_all_performance_metrics(metric_type: Optional[str] = None, device_id: Optional[str] = None):
    """Get all performance metrics, optionally filtered"""
    metrics = perf_db.get_all_metrics()
    
    if metric_type:
        metrics = [m for m in metrics if m.metric_type == metric_type]
    if device_id:
        metrics = [m for m in metrics if m.device_id == device_id]
    
    return {"count": len(metrics), "metrics": metrics}

@app.get("/performance/stats/{metric_type}")
async def get_performance_stats(metric_type: str, device_id: Optional[str] = None):
    """Get aggregated statistics for a performance metric"""
    stats = perf_db.get_metric_stats(metric_type, device_id)
    if not stats:
        raise HTTPException(status_code=404, detail=f"No data for {metric_type}")
    return stats

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Health Monitoring Cloud Backend...")
    print("📍 API running at http://localhost:8000")
    print("📚 Docs at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)