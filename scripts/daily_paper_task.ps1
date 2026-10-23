# daily_paper_task.ps1 — 计划任务入口：抓取论文数据 + 尝试触发 agent 分析
# 由 Windows 计划任务每天 21:05 调用（比 Cursor 内的循环脚本更可靠，不依赖 Cursor 进程）
# 日志: data/logs/daily-task-YYYY-MM.log（git 忽略）
param(
    [string]$PaperDir = "D:\paper"
)

$ErrorActionPreference = "Continue"
$logDir = Join-Path $PaperDir "data\logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$log = Join-Path $logDir ("daily-task-{0}.log" -f (Get-Date -Format "yyyy-MM"))
$py = "C:\Windows\py.exe"
$gitPath = "C:\Program Files\Git\cmd"

function Write-Log([string]$msg) {
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg
    $line | Out-File -FilePath $log -Append -Encoding utf8
    Write-Output $line
}

Write-Log "==== daily paper task start ===="

# 1) 抓取今天论文数据（补齐机制：fetch 支持 --date，若昨天漏抓可手动补）
$today = Get-Date -Format "yyyy-MM-dd"
try {
    $env:Path = "$gitPath;$env:Path"
    $out = & $py -3 (Join-Path $PaperDir "scripts\fetch_papers.py") --date $today 2>&1
    $out | ForEach-Object { Write-Log "fetch: $_" }
} catch {
    Write-Log "fetch FAILED: $($_.Exception.Message)"
}

# 2) 尝试调用 cursor-agent 做分析层（未认证时跳过，数据已落地不影响次日补齐）
$agentCli = "C:\Users\Administrator\AppData\Local\cursor-agent\cursor-agent.cmd"
if (Test-Path $agentCli) {
    $probe = & $agentCli -p "reply OK only" 2>&1 | Select-Object -First 1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "cursor-agent auth OK, dispatching analysis task"
        $prompt = "执行 D:\paper\.cursor\prompts\daily-paper.md 每日任务（从 daily/ 最新日期的下一天开始补齐缺失日期，含今天 $today），完成后简报并提交推送。不要向用户提问，自主完成。"
        & $agentCli -p --output-format json $prompt 2>&1 | ForEach-Object { Write-Log "agent: $_" }
        Write-Log "cursor-agent dispatch done, exit=$LASTEXITCODE"
    } else {
        Write-Log "cursor-agent not authenticated ($probe) — data fetched, analysis deferred to next session"
    }
} else {
    Write-Log "cursor-agent CLI not found — data fetched, analysis deferred"
}

Write-Log "==== daily paper task end ===="
