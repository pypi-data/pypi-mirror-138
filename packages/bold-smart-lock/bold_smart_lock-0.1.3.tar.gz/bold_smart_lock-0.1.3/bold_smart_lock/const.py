"""Constants"""

# API endpoints
API_URI = "https://api.sesamtechnology.com/v1/"
VALIDATIONS_ENDPOINT = "validations"
AUTHENTICATIONS_ENDPOINT = "authentications"
REMOTE_ACTIVATION_ENDPOINT = "devices/{}/remote-activation"
EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT = "effective-device-permissions?size=1000"

# Default headers
POST_HEADERS = {"Content-Type": "application/json"}

# Default JSON request data
AUTHENTICATION_REQUEST_JSON = {
    "language": "en",
    "clientLocale": "en-US",
}
