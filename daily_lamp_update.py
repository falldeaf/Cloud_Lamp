import reports
import cPickle as pickle



weather = reports.weather_report()
pickle.dump( weather, open( "weather.p", "wb") )

surf = reports.surf_report()
pickle.dump( surf, open( "surf.p", "wb") )
