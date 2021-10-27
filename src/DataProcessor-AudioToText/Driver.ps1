$originalTranscriptPath = "{insert-your-path}\hearing-room\data\messages\2021041286-April25Transcript.json"
$timestampTranscriptPath = "{insert-your-path}\hearing-room\prod_data\messages\2021041286-April25.json"
$topicsOutputPath = "{insert-your-path}\hearing-room\prod_data\topics\2021041286-April25Topics.json"
$speakerOutputPath = "{insert-your-path}\hearing-room\transcript-analytics\output\2021041286-April25\2021041286-April25SpeakerInfo.json"

. src\DataProcessor-AudioToText\Update-TranscriptVideoTimes.ps1

Update-TranscriptVideoTimes -TranscriptPath $originalTranscriptPath `
                            -OutputPath $timestampTranscriptPath

. src\DataProcessor-AudioToText\Get-MessageDictionary
$messages = Get-MessageDictionary -TranscriptPath $timestampTranscriptPath

. src\DataProcessor-AudioToText\New-SpeakerData.ps1
$result = New-SpeakerData -Messages $messages `
                          -TopicsPath $topicsOutputPath

$txtJson = ConvertTo-Json $result -Depth 4

$txtJson | Out-File -FilePath $speakerOutputPath -NoClobber
