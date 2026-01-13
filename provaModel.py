from model.model import Model
from datetime import date
model = Model()
d_start = date(2016,1,1)
d_end = date(2018,12,28)
model.getGrafo(7,d_start,d_end)
model.getPercorsoOttimo(166,167,4)
print(model.bestPeso)
print(model.bestPercorso)