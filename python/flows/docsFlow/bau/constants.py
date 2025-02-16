from enum import Enum


ContextType : list[str] = [
    "PLANUNG",
    "BRANDSCHUTZ"
    "ABNAHME"
    "STATIK"
]
   
class DocType(str, Enum):
    BAUGENEHMIGUNG = "BAUGENEHMIGUNG"
    ZERTIFIKAT = "ZERTIFIKAT"
    PROTOKOLL = "ABNAHMEPROTOKOLL"
    BERECHNUNG = "BERECHNUNG"
    PRUEFDOKUMENT = "PRUEFDOKUMENT"

