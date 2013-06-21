import reports
import cPickle as pickle



weather = reports.weather_report()
pickle.dump( weather, open( "/home/pi/scripts/weather.p", "wb") )

surf = reports.surf_report()
pickle.dump( surf, open( "/home/pi/scripts/surf.p", "wb") )
