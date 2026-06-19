from pydantic import BaseModel
from typing import Optional

class SettingsBase(BaseModel):
    company_name: str = "My Company"
    currency: str = "USD"
    tax_rate: float = 0.0
    email_host: Optional[str] = None
    email_port: Optional[int] = None
    email_username: Optional[str] = None
    email_password: Optional[str] = None
    theme: str = "light"
