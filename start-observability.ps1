$ErrorActionPreference = "Stop"

$processes = @(
    @{
        Name = "Jaeger"
        FilePath = "C:\observability\jaeger\jaeger-2.18.0-windows-amd64\jaeger.exe"
        WorkingDirectory = "C:\observability\jaeger\jaeger-2.18.0-windows-amd64"
        Arguments = @()
    },
    @{
        Name = "Loki"
        FilePath = "C:\observability\loki\loki-windows-amd64.exe"
        WorkingDirectory = "C:\observability\loki"
        Arguments = @("--config.file=C:\observability\loki\loki-config.yaml")
    },
    @{
        Name = "OpenTelemetry Collector"
        FilePath = "C:\observability\otelcol_0.152.0_windows_amd64\otelcol.exe"
        WorkingDirectory = "C:\observability\otelcol_0.152.0_windows_amd64"
        Arguments = @("--config=C:\observability\otelcol_0.152.0_windows_amd64\otel-collector-config.yaml")
    },
    @{
        Name = "Prometheus"
        FilePath = "C:\observability\prometheus\prometheus-3.10.0.windows-amd64\prometheus.exe"
        WorkingDirectory = "C:\observability\prometheus\prometheus-3.10.0.windows-amd64"
        Arguments = @("--config.file=C:\observability\prometheus\prometheus-3.10.0.windows-amd64\prometheus.yml")
    },
    @{
        Name = "Grafana"
        FilePath = "C:\observability\grafana-13.0.1+security-01\bin\grafana.exe"
        WorkingDirectory = "C:\observability\grafana-13.0.1+security-01\bin"
        Arguments = @("server")
    },
    @{
        Name = "Grafana Alloy"
        FilePath = "C:\observability\alloy-windows-amd64.exe\alloy-windows-amd64.exe"
        WorkingDirectory = "C:\observability\alloy-windows-amd64.exe"
        Arguments = @("run", "C:\observability\alloy-windows-amd64.exe\config.alloy")
    },
    @{
        Name = "Streamlit app"
        FilePath = "python"
        WorkingDirectory = "C:\Users\GuptaGa\Documents\DemoUStall0513\doc_demo"
        Arguments = @("-m", "streamlit", "run", "src/app.py", "--server.port", "8501")
    }
)

Write-Host "Starting observability stack..." -ForegroundColor Cyan

foreach ($process in $processes) {
    if ($process.FilePath -ne "python" -and -not (Test-Path $process.FilePath)) {
        throw "Missing executable for $($process.Name): $($process.FilePath)"
    }

    Write-Host "Starting $($process.Name)..."
    $startArgs = @{
        FilePath = $process.FilePath
        WorkingDirectory = $process.WorkingDirectory
        WindowStyle = "Normal"
    }
    if ($process.Arguments.Count -gt 0) {
        $startArgs.ArgumentList = $process.Arguments
    }
    Start-Process @startArgs
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "Started. Open:" -ForegroundColor Green
Write-Host "  Grafana:    http://localhost:3000"
Write-Host "  Prometheus: http://localhost:9090"
Write-Host "  Loki:       http://localhost:3100/ready"
Write-Host "  Jaeger:     http://localhost:16686"
Write-Host "  Streamlit:  http://localhost:8501"
Write-Host "  Metrics:    http://localhost:8889/metrics"
