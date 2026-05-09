$content = Get-Content index.html
$styleStart = -1
$styleEnd = -1
$scriptStart = -1
$scriptEnd = -1

for ($i=0; $i -lt $content.Length; $i++) {
    if ($content[$i] -like '*<style>*') { $styleStart = $i }
    if ($content[$i] -like '*</style>*') { $styleEnd = $i }
    if ($content[$i] -like '*<script>*' -and $i -gt 1500) { $scriptStart = $i }
    if ($content[$i] -like '*</script>*' -and $i -gt 1500) { $scriptEnd = $i }
}

$newContent = $content[0..($styleStart-1)]
$newContent += '    <link rel="stylesheet" href="/src/index.css">'
$newContent += $content[($styleEnd+1)..($scriptStart-1)]
$newContent += '    <script type="module" src="/src/main.js"></script>'
$newContent += $content[($scriptEnd+1)..($content.Length-1)]

$newContent | Set-Content index.html -Encoding UTF8
