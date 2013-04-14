# Skrypt tworzy kod ze wspolrzednymi relatywnymi na podstawie natywnych
# Uzycie:
# - Odpalamy pythona i jego konsole z katalogu w ktorym jest skrypy
# - import relfromreal
# - Uzywamy sobie funkcji 'nx' i 'ny' 
import os

# rozmiar rozdzialki dla ktorej chcemy zeby funkcje dzialaly
ResW = 320
ResH = 480

def nx(x):
	str = 'gScreen.height - %d' % (480-x)
	# kopiowanie do schowka
	cmd = 'echo %s | tr -d "\n" | pbcopy' % str
	os.system(cmd)
	return str

def ny(y):
	str = 'gScreen.height - %d' % (480-y)
	# kopiowanie do schowka
	cmd = 'echo %s | tr -d "\n" | pbcopy' % str
	os.system(cmd)
	return str
