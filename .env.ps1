$Env:TWILIO_ACCOUNT_SID = "AC9abd4a54209c7da2081f881c918ff591"
$Env:TWILIO_TWIML_APP_SID = "AP62aa6ce1a53f6fd53236c9fd955ed648"
$Env:TWILIO_CALLER_ID = "+18482666431"
$Env:API_KEY = "SK3b4261cb982b38c11ed9090b80dab1a6"
$Env:API_SECRET = "YcsujrT2TfFb7xwl5wF8oU8DcAOJ8FYz"

# Uncomment the following if you'd like the environment variables
# to be permanently set on your user account for this machine.



[Environment]::SetEnvironmentVariable("TWILIO_ACCOUNT_SID", $Env:TWILIO_ACCOUNT_SID, "User")
[Environment]::SetEnvironmentVariable("TWILIO_TWIML_APP_SID", $Env:TWILIO_TWIML_APP_SID, "User")
[Environment]::SetEnvironmentVariable("TWILIO_CALLER_ID", $Env:TWILIO_CALLER_ID, "User")
[Environment]::SetEnvironmentVariable("API_KEY", $Env:API_KEY, "User")
[Environment]::SetEnvironmentVariable("API_SECRET", $Env:API_SECRET, "User")

