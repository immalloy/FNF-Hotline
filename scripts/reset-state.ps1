# Resets state.json so next run posts fresh Discord messages
'{}' | Out-File -Encoding utf8 -NoNewline -LiteralPath "$PSScriptRoot\..\state.json"
Write-Host "state.json reset to {}" -ForegroundColor Green
