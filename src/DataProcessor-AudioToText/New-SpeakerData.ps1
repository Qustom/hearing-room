function New-SpeakerData {
    param(
        [CmdletBinding()]
        [hashtable]$Messages,

        [string]$TopicsPath
    )

    $result = @{ }

    $Messages.Values | ForEach-Object {
        if (!$result.ContainsKey($_.from.name)) {
            $result[$_.from.name] = @{
                "id" = $_.from.id
                "name" = $_.from.name
                "messages" = @{}
                "topics" = @{}
            }
        }

        $result[$_.from.name].messages[$_.id] = $_
    }

    $json = Get-Content $TopicsPath | Out-String
    $Obj = ConvertFrom-Json $json

    $Obj.topics | ForEach-Object {
        
        $topic = $_
        $_.messageIds | ForEach-Object {
            
            $msg = $Messages[$_]
            if(!$result[$msg.from.name].topics.ContainsKey($topic.text)) {
                $result[$msg.from.name].topics[$topic.text] = @()
            }

            $result[$msg.from.name].topics[$topic.text] += $_
        }
    }

    return $result
}