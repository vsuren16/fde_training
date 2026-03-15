$ErrorActionPreference = "Stop"

$pythonExe = "C:\Users\Administrator\AppData\Local\Programs\Python\Python310\python.exe"
$serverScript = "C:\Users\Administrator\Documents\GenAI Training\Week6 (26-30)\Day_28\MCP Server Demo\server.py"
$npxCmd = "C:\Program Files\nodejs\npx.cmd"
$sseUrl = "http://127.0.0.1:8000/sse"

$serverProcess = $null
$exitCode = 1

try {
    # Start the SSE MCP server in the background.
    $serverProcess = Start-Process -FilePath $pythonExe -ArgumentList @("-u", $serverScript) -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 2

    # Bridge SSE -> stdio for Claude Desktop.
    & $npxCmd -y mcp-remote $sseUrl --transport sse-only --allow-http
    $exitCode = $LASTEXITCODE
}
finally {
    if ($serverProcess -and -not $serverProcess.HasExited) {
        Stop-Process -Id $serverProcess.Id -Force
    }
}

exit $exitCode
