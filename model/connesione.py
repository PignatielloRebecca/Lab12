from model.rifugio import Rifugio
from dataclasses import dataclass

@dataclass
class Connessione:
    r1:Rifugio
    r2:Rifugio
    distanza: float
    difficolta:str
    peso: int










