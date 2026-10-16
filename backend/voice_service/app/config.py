import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    api_token: str  # clients must send this as "Authorization: Bearer <token>"
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_from_number: str
    public_base_url: str  # where Twilio can reach this service, e.g. https://voice.example.com

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            api_token=os.environ["VOICE_API_TOKEN"],
            twilio_account_sid=os.environ["TWILIO_ACCOUNT_SID"],
            twilio_auth_token=os.environ["TWILIO_AUTH_TOKEN"],
            twilio_from_number=os.environ["TWILIO_FROM_NUMBER"],
            public_base_url=os.environ["PUBLIC_BASE_URL"].rstrip("/"),
        )
