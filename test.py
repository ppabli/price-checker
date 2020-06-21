import json

from Tracker import Tracker

t1 = Tracker('Prueba 1', 'google.es', 50)
t1.addTracker();

t2 = Tracker('Prueba 2', 'amazon.es', 50)
t2.addTracker()

t2.setName('new name')
