function Update-TranscriptVideoTimes {
    [CmdletBinding()]
    param (
        [string]$TranscriptPath,

        [string]$OutputPath
    )

    $json = Get-Content $TranscriptPath | Out-String

    $Obj = ConvertFrom-Json $json
    
    $currentTime = New-TimeSpan
    $lastDateTime = [datetime]::Parse($Obj.Messages[0].startTime)

    $Obj.Messages | ForEach-Object {
        # Convert string to Datetimes
        $startDateTime = [datetime]::Parse($_.startTime)
        $endDateTime = [datetime]::Parse($_.endTime)

        # Get time speaker started after period of silence
        $silentTime = New-TimeSpan -Start $lastDateTime -End $startDateTime
        $currentTime = $currentTime + $silentTime

        # Get time speaker stopped
        $speakingTime = New-TimeSpan -Start $startDateTime -End $endDateTime
        $endTime = $currentTime + $speakingTime

        # Set start and stop time stamps
        Add-Member -InputObject $_ -NotePropertyName StartVideoTime -NotePropertyValue $currentTime.TotalMilliseconds
        Add-Member -InputObject $_ -NotePropertyName EndVideoTime -NotePropertyValue $endTime.TotalMilliseconds

        # Prepare for next message
        $currentTime = $endTime
        $lastDateTime = $endDateTime
    }

    $result = ConvertTo-Json $Obj

    $result | Out-File -FilePath $OutputPath -NoClobber

}