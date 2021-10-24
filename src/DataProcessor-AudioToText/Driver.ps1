# . src\DataProcessor-AudioToText\Invoke-AudioToText.ps1

# Invoke-AudioToText -ComputerName "test"


# . src\DataProcessor-AudioToText\Update-TranscriptVideoTimes.ps1

# Update-TranscriptVideoTimes -TranscriptPath "{Your-FullPath-Here}\ai-news-reader\data\Transcripts\c-spanTranscript1Speaker.json" `
#                             -OutputPath "{Your-FullPath-Here}\test.json"

. src\DataProcessor-AudioToText\Get-MessageDictionary
$messages = Get-MessageDictionary -TranscriptPath "{Your-FullPath-Here}\ai-news-reader\data\Transcripts\c-spanTranscript1Speaker-VideoTime.json"

. src\DataProcessor-AudioToText\New-SpeakerData.ps1
$result = New-SpeakerData -Messages $messages `
                          -TopicsPath "{Your-FullPath-Here}\ai-news-reader\data\Transcripts\c-spanTranscript-Topics.json"

$txtJson = ConvertTo-Json $result -Depth 4

$txtJson | Out-File -FilePath "{Your-FullPath-Here}\SpeakerInfo.json" -NoClobber
