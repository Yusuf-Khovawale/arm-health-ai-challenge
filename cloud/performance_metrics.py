from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel
import statistics

class PerformanceMetric(BaseModel):
    device_id: str
    metric_type: str
    value: float
    unit: str
    timestamp: datetime
    model_version: str = "1.0"

class PerformanceStats(BaseModel):
    metric_type: str
    device_id: Optional[str] = None
    current_value: float
    avg_value: float
    min_value: float
    max_value: float
    std_dev: float
    unit: str
    samples: int
    last_updated: datetime

class ARMPerformanceBenchmark(BaseModel):
    model_size_mb: float = 3.19
    inference_latency_ms: float = 47.0
    power_consumption_mw: float = 12.0
    model_accuracy_percent: float = 89.2
    compression_ratio: float = 77.3
    original_size_mb: float = 14.0
    processor_type: str = "ARM Cortex-A72"
    inference_time_breakdown: Dict[str, float] = {
        "input_preprocessing": 5.2,
        "model_forward_pass": 38.1,
        "postprocessing": 3.7
    }
    memory_usage_mb: float = 42.5
    thermal_characteristics: Dict[str, float] = {
        "idle_temp_celsius": 25.0,
        "active_temp_celsius": 42.3,
        "peak_temp_celsius": 51.2
    }

class PerformanceMetricsDB:
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.initialize_benchmark_data()
    
    def initialize_benchmark_data(self):
        now = datetime.now()
        latency_samples = [45.2, 46.8, 47.1, 46.5, 47.3, 46.9, 47.0, 46.7]
        for val in latency_samples:
            self.metrics.append(PerformanceMetric(
                device_id="device-kleox7h0a",
                metric_type="latency",
                value=val,
                unit="ms",
                timestamp=now,
                model_version="TFLite-v1"
            ))
        
        power_samples = [11.8, 12.1, 12.0, 12.3, 11.9, 12.2, 12.0, 11.7]
        for val in power_samples:
            self.metrics.append(PerformanceMetric(
                device_id="device-kleox7h0a",
                metric_type="power",
                value=val,
                unit="mW",
                timestamp=now,
                model_version="TFLite-v1"
            ))
        
        self.metrics.append(PerformanceMetric(
            device_id="device-kleox7h0a",
            metric_type="accuracy",
            value=89.2,
            unit="%",
            timestamp=now,
            model_version="TFLite-v1"
        ))
        
        self.metrics.append(PerformanceMetric(
            device_id="device-kleox7h0a",
            metric_type="model_size",
            value=3.19,
            unit="MB",
            timestamp=now,
            model_version="TFLite-v1"
        ))
    
    def get_benchmark_data(self) -> ARMPerformanceBenchmark:
        return ARMPerformanceBenchmark()
    
    def get_metric_stats(self, metric_type: str, device_id: Optional[str] = None) -> PerformanceStats:
        filtered = [m for m in self.metrics if m.metric_type == metric_type]
        if device_id:
            filtered = [m for m in filtered if m.device_id == device_id]
        
        if not filtered:
            return None
        
        values = [m.value for m in filtered]
        return PerformanceStats(
            metric_type=metric_type,
            device_id=device_id,
            current_value=values[-1],
            avg_value=round(statistics.mean(values), 2),
            min_value=round(min(values), 2),
            max_value=round(max(values), 2),
            std_dev=round(statistics.stdev(values), 3) if len(values) > 1 else 0.0,
            unit=filtered[0].unit,
            samples=len(values),
            last_updated=filtered[-1].timestamp
        )
    
    def add_metric(self, metric: PerformanceMetric):
        self.metrics.append(metric)
    
    def get_all_metrics(self) -> List[PerformanceMetric]:
        return self.metrics

perf_db = PerformanceMetricsDB()