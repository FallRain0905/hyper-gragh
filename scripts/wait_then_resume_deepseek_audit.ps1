$ErrorActionPreference = 'Stop'
$oldPid = 38328
$repo = 'C:\Users\19855\Desktop\Hyper-rag\hyper-gragh'
$out = Join-Path $repo 'outputs\final_experiment_v1_old_embedding\deepseek_audit'
$endpointFile = 'C:\Users\19855\Desktop\Hyper-rag\real_flow_80_chunk1000_v3\llm_endpoints.accdb'
$python = 'C:\Users\19855\AppData\Local\Programs\Python\Python312\python.exe'
$stdout = Join-Path $out 'deepseek_audit_restart_stdout.log'
$stderr = Join-Path $out 'deepseek_audit_restart_stderr.log'
$lock = Join-Path $out 'deepseek_audit_restart.waiting'

if (Test-Path -LiteralPath $lock) {
    exit 0
}
New-Item -ItemType File -Path $lock -Force | Out-Null

while (Get-Process -Id $oldPid -ErrorAction SilentlyContinue) {
    Start-Sleep -Seconds 15
}

Set-Location -LiteralPath $repo
$args = @(
    '-X', 'utf8', 'scripts\run_deepseek_final_audit.py',
    '--repo', $repo,
    '--output', $out,
    '--endpoint-file', $endpointFile,
    '--phase', 'all',
    '--model', 'deepseek-v4.1-flash',
    '--timeout', '120',
    '--max-retries', '3',
    '--concurrency', '30',
    '--request-min-interval', '0.1'
)
Start-Process -FilePath $python -ArgumentList $args -WorkingDirectory $repo -RedirectStandardOutput $stdout -RedirectStandardError $stderr -WindowStyle Hidden
Remove-Item -LiteralPath $lock -Force -ErrorAction SilentlyContinue
