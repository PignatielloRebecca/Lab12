from database.dao import DAO
from model.model import Model


results=DAO.readRifugio()
#print(results) # restituisce l'oggetto rifugio
model=Model()
connessioni =DAO.readConnessioni(model._dizionario_rifugio, 2020) # restiuisce l'oggetto rifugio per rifugio, con distanz e difficolta
print(connessioni)
print(model._dizionario_rifugio[1])


