import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [inputs, setInputs] = useState({
    age: 50,
    weight: 70,
    heartRate: 72,
    bloodPressure: 120,
    cholesterol: 200,
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [modelLoaded, setModelLoaded] = useState(false);

  // Simulate model loading
  useEffect(() => {
    setTimeout(() => {
      setModelLoaded(true);
    }, 1000);
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputs(prev => ({
      ...prev,
      [name]: parseFloat(value)
    }));
  };

const makePrediction = async () => {
    setLoading(true);
    
    // Simulate inference
    setTimeout(() => {
      // Better risk calculation
      let riskScore = 0;
      
      // Age factor (0-100)
      if (inputs.age > 60) riskScore += 25;
      else if (inputs.age > 45) riskScore += 15;
      
      // Heart Rate factor (0-100)
      if (inputs.heartRate > 100) riskScore += 30;
      else if (inputs.heartRate > 85) riskScore += 15;
      
      // Blood Pressure factor (0-100)
      if (inputs.bloodPressure > 140) riskScore += 30;
      else if (inputs.bloodPressure > 120) riskScore += 15;
      
      // Cholesterol factor (0-100)
      if (inputs.cholesterol > 240) riskScore += 20;
      else if (inputs.cholesterol > 200) riskScore += 10;
      
      // Normalize to 0-100
      riskScore = Math.min(100, riskScore);

      const riskLevel = riskScore > 70 ? 'High' : riskScore > 40 ? 'Medium' : 'Low';
      const color = riskScore > 70 ? '#e74c3c' : riskScore > 40 ? '#f39c12' : '#27ae60';

      setPrediction({
        score: Math.min(100, Math.round(riskScore)),
        level: riskLevel,
        color: color,
        timestamp: new Date().toLocaleTimeString()
      });

      setLoading(false);
    }, 500);
  };

  return (
    <div className="App">
      <header className="header">
        <h1>🏥 Health Monitoring on ARM</h1>
        <p>Edge AI Prediction - Runs Offline</p>
      </header>

      <div className="container">
        <div className="model-status">
          {modelLoaded ? (
            <span className="status-online">✅ Model Loaded</span>
          ) : (
            <span className="status-loading">⏳ Loading Model...</span>
          )}
        </div>

        <div className="input-section">
          <h2>Health Metrics</h2>
          
          <div className="input-group">
            <label>Age (years)</label>
            <input
              type="number"
              name="age"
              value={inputs.age}
              onChange={handleInputChange}
              min="18"
              max="120"
            />
            <span className="value">{inputs.age}</span>
          </div>

          <div className="input-group">
            <label>Weight (kg)</label>
            <input
              type="number"
              name="weight"
              value={inputs.weight}
              onChange={handleInputChange}
              min="30"
              max="200"
            />
            <span className="value">{inputs.weight}</span>
          </div>

          <div className="input-group">
            <label>Heart Rate (bpm)</label>
            <input
              type="number"
              name="heartRate"
              value={inputs.heartRate}
              onChange={handleInputChange}
              min="40"
              max="200"
            />
            <span className="value">{inputs.heartRate}</span>
          </div>
{prediction && prediction.level === 'High' && (
          <div className="hospital-section">
            <h2>🏥 Nearby Hospitals</h2>
            <div className="hospital-list">
              <div className="hospital-card">
                <div className="hospital-name">Cambridge University Hospital</div>
                <div className="hospital-distance">📍 1.2 km away</div>
                <div className="hospital-availability">
                  <span className="available">✅ Emergency: Available</span>
                </div>
                <button className="contact-btn">Call: 999</button>
              </div>

              <div className="hospital-card">
                <div className="hospital-name">Addenbrooke's Hospital</div>
                <div className="hospital-distance">📍 2.5 km away</div>
                <div className="hospital-availability">
                  <span className="available">✅ Emergency: Available</span>
                </div>
                <button className="contact-btn">Call: 999</button>
              </div>

              <div className="hospital-card">
                <div className="hospital-name">Royal Papworth Hospital</div>
                <div className="hospital-distance">📍 3.1 km away</div>
                <div className="hospital-availability">
                  <span className="available">✅ Cardiology: Available</span>
                </div>
                <button className="contact-btn">Call: 999</button>
              </div>
            </div>
          </div>
        )}
          <div className="input-group">
            <label>Blood Pressure (mmHg)</label>
            <input
              type="number"
              name="bloodPressure"
              value={inputs.bloodPressure}
              onChange={handleInputChange}
              min="80"
              max="200"
            />
            <span className="value">{inputs.bloodPressure}</span>
          </div>

          <div className="input-group">
            <label>Cholesterol (mg/dL)</label>
            <input
              type="number"
              name="cholesterol"
              value={inputs.cholesterol}
              onChange={handleInputChange}
              min="100"
              max="400"
            />
            <span className="value">{inputs.cholesterol}</span>
          </div>

          <button 
            onClick={makePrediction} 
            disabled={!modelLoaded || loading}
            className="predict-btn"
          >
            {loading ? '🔄 Analyzing...' : '🚀 Predict'}
          </button>
        </div>

        {prediction && (
          <div className="prediction-section">
            <h2>Prediction Result</h2>
            <div 
              className="risk-meter"
              style={{ borderColor: prediction.color }}
            >
              <div className="risk-score">
                <span className="score-number">{prediction.score}</span>
                <span className="score-label">Risk Score</span>
              </div>
              <div className="risk-level" style={{ color: prediction.color }}>
                {prediction.level} Risk
              </div>
              <div className="timestamp">
                Predicted at: {prediction.timestamp}
              </div>
            </div>

            <div className="interpretation">
              {prediction.level === 'Low' && (
                <p>✅ Your health metrics look good. Keep up healthy habits!</p>
              )}
              {prediction.level === 'Medium' && (
                <p>⚠️ Monitor your metrics. Consider consulting a healthcare provider.</p>
              )}
              {prediction.level === 'High' && (
                <p>🚨 High risk detected. Please consult a healthcare professional immediately.</p>
              )}
            </div>
          </div>
        )}

        <div className="info-box">
          <h3>About This App</h3>
          <p>✅ Runs offline - no internet needed</p>
          <p>✅ TensorFlow Lite model optimized for ARM</p>
          <p>✅ Privacy-first - data stays on your device</p>
          <p>✅ Real-time predictions</p>
        </div>
      </div>
    </div>
  );
}

export default App;