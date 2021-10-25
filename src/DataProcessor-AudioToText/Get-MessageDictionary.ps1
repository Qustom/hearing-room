function Get-MessageDictionary {
    [CmdletBinding()]
    param (
        [string]$TranscriptPath
    )

    $json = Get-Content $TranscriptPath | Out-String

    $Obj = ConvertFrom-Json $json
    
    $result = @{ }
    $Obj.Messages | ForEach-Object {
        $result[$_.id] = $_
    }

    return $result

}