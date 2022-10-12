$CurrentRoot = [System.Environment]::CurrentDirectory
$VenvPath = $CurrentRoot + '\venv'

if (Test-Path -Path $VenvPath) {
    "Path exists!"`
} else {
    "Path not exists!"
    pip3 install -u virtualenv
    virtualenv venv
    venv\scripts\activate
    pip install -r requirements.txt
}
