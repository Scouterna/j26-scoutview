from datetime import date, datetime
from enum import Enum  # Importera Enum
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    username: str
    roles: list[str] = []

    def has_role(self, role):
        res = (role in self.roles) or ("admin" in self.roles)
        print(f"{self.username} in roles {self.roles}, request {role}: {res}")
        return res

    def __str__(self) -> str:
        return self.username


class Question(BaseModel):
    id: int
    tab_id: int
    tab_title: str | None
    tab_description: str | None
    section_id: int
    section_title: str | None
    filterable: bool
    status: bool | None
    question: str
    description: str
    type: str
    default_value: str | None
    choices: Optional[Any] = None


class Participant(BaseModel):
    member_no: int
    first_name: str
    last_name: str
    registration_date: datetime
    cancelled_date: Optional[datetime]
    sex: int
    date_of_birth: date
    primary_email: EmailStr
    questions: Any


class ItemSchema(BaseModel):
    name: str = Field(...)
    description: Optional[str] = Field(None)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "My Item",
                "description": "A description of my item.",
            }
        }
    )


class EanCodeSchema(BaseModel):
    ean_code: str = Field(..., description="The EAN-13 code of the product.")
    product_number: str = Field(..., description="The internal product number to associate with the EAN.")
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ean_code": "7310340012345",
                "product_number": "543201",
            }
        }
    )


class EanCodeResponseSchema(BaseModel):
    ean_code: str = Field(..., description="The EAN-13 code.")
    product_number: str = Field(..., description="The associated internal product number.")


# Response model for the GET /wine-info/{product_number} endpoint
class WineInfoResponse(BaseModel):
    productNumber: str = Field(..., description="The product number of the wine.")
    productNameBold: str = Field(..., description="The main name of the wine.")
    productNameThin: Optional[str] = Field(None, description="The secondary name of the wine.")
    country: str = Field(..., description="The country of origin.")
    categoryLevel2: Optional[str] = Field(None, description="The primary category of the wine.")
    current_stock: int = Field(..., description="The current number of this wine in stock.")
    categoryLevel3: Optional[str] = Field(None, description="The secondary category of the wine.")
    usage: Optional[str] = Field(None, description="Recommended usage for the wine.")
    # You can easily add more fields here later, e.g., year: Optional[int] = None


# Response model for the POST /check-in/{product_number} endpoint
class CheckInResponse(BaseModel):
    productNumber: str = Field(..., description="The product number that was checked in.")
    current_stock: int = Field(..., description="The total number of this wine in stock after check-in.")


# Modell som representerar ett komplett dokument från "in_stock"-samlingen
class InStockItem(BaseModel):
    id: str = Field(..., alias="_id")  # Vi mappar MongoDB's _id till ett fält som heter id
    productNumber: str
    checkin_date: date
    productNameBold: Optional[str] = None
    price: Optional[float] = None
    country: Optional[str] = None
    productNameThin: Optional[str] = None
    categoryLevel2: Optional[str] = None
    categoryLevel3: Optional[str] = None
    usage: Optional[str] = None
    tasteSymbols: List[str] = []  # Se till att detta är en lista

    class Config:
        populate_by_name = True  # Allows using alias like "_id"
        # Pydantic V2 uses populate_by_name instead of allow_population_by_field_name or validate_by_name for this


# Modell för svaret i "count"-läget. Vi använder en alias för tydlighetens skull.
SearchCountResponse = dict[str, int]


# --- ADD THIS NEW ENUM ---
# Skapar en Enum för att säkerställa att endast giltiga värden kan användas i filtret.
class TasteSymbol(str, Enum):
    GRONSAKER = "Grönsaker"
    FISK = "Fisk"
    SALLSKAPSDRYCK = "Sällskapsdryck"
    FAGEL = "Fågel"
    SKALDJUR = "Skaldjur"
    OST = "Ost"
    BUFFEMAT = "Buffémat"
    FLASK = "Fläsk"
    APERITIF = "Aperitif"
    ASIATISKT = "Asiatiskt"
    VILT = "Vilt"
    DESSERT = "Dessert"
    NOT = "Nöt"
    LAMM = "Lamm"
    KRYDDSTARKT = "Kryddstarkt"


class CategoryLevel2(str, Enum):
    ROTT_VIN = "Rött vin"
    VITT_VIN = "Vitt vin"
    ROSEVIN = "Rosévin"
    STARKVIN = "Starkvin"
    MOUSSERANDE_VIN = "Mousserande vin"


# --- ADD THIS NEW MODEL ---
# Denna modell representerar en unik produkt med dess lagersaldo.
# Används som svar i list-läget.
class AggregatedWineInfo(BaseModel):
    productNumber: str
    in_stock: int = Field(..., description="Antal flaskor i lager.")
    productNameBold: Optional[str] = None
    country: Optional[str] = None
    categoryLevel2: Optional[str] = None
    categoryLevel3: Optional[str] = None
    tasteSymbols: List[str] = []


# --- ADD THESE NEW MODELS FOR WINE TASTE HISTORY ---


class HistoryItem(BaseModel):
    id: str = Field(..., alias="_id", description="The unique ID of the history record.")
    date: datetime = Field(..., description="The date the wine was consumed/logged.")
    productNumber: str = Field(..., description="The product number of the wine.")
    eatenWith: Optional[str] = Field("", description="What the wine was eaten with.")
    rating: Optional[int] = Field(0, ge=0, le=10, description="Rating from 0 to 10.")
    comment: Optional[str] = Field("", description="User comments about the wine.")
    productNameBold: Optional[str] = Field(None, description="Namnet på vinet.")
    country: Optional[str] = Field(None, description="Vinets ursprungsland.")

    model_config = ConfigDict(
        populate_by_name=True,  # Allows using "_id" as an alias for "id"
        json_schema_extra={
            "example": {
                "id": "60d0fe4f5311236168a109ca",
                "date": "2023-10-27",
                "productNumber": "543201",
                "eatenWith": "Grilled Salmon",
                "rating": 8,
                "comment": "Paired wonderfully with the fish, notes of citrus.",
            }
        },
    )


class UpdateHistory(BaseModel):
    eatenWith: Optional[str] = Field(None, description="Update what the wine was eaten with.")
    rating: Optional[int] = Field(None, ge=1, le=10, description="Update rating (0-10).")
    comment: Optional[str] = Field(None, description="Update user comments.")
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "eatenWith": "Aged cheddar cheese",
                "rating": 9,
                # "comment": "Comment can be omitted if not updating"
            }
        }
    )
