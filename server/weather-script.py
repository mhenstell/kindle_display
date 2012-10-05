#!/usr/bin/python2

# Kindle Weather Display
# Matthew Petroff (http://www.mpetroff.net/)
# September 2012

import urllib2
from xml.dom import minidom
import datetime
import codecs
import json
import sys
import datetime

api_key = sys.argv[1]
zip_code = sys.argv[2]


try:
    wunderground_current_url = "http://api.wunderground.com/api/%s/conditions/q/%s.json" % (api_key, zip_code)
    wunderground_current_data = json.loads(urllib2.urlopen(wunderground_current_url).read())
    lat = wunderground_current_data['current_observation']['observation_location']['latitude']
    lon = wunderground_current_data['current_observation']['observation_location']['longitude']
    observed_temp = '%.1f' % wunderground_current_data['current_observation']['temp_f']

    wunderground_forecast_url = "http://api.wunderground.com/api/%s/forecast/q/%s.json" % (api_key, zip_code)
    wunderground_forecast_data = json.loads(urllib2.urlopen(wunderground_forecast_url).read())

    pop = wunderground_forecast_data['forecast']['simpleforecast']['forecastday'][0]['pop']
    qpf = wunderground_forecast_data['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['in']
    snow = wunderground_forecast_data['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['in']

    wunderground_alerts_url = "http://api.wunderground.com/api/%s/alerts/q/%s.json" % (api_key, zip_code)
    wunderground_alerts_data = json.loads(urllib2.urlopen(wunderground_alerts_url).read())
    alerts = wunderground_alerts_data['alerts']

except Exception as e:
    print "Error consulting Weather Underground: %s" % e

# observed_temp = 00
# pop = 10
# qpf = 0.023
# snow = 0.23
# alerts = []

try: 
    #NWS_url = "http://graphical.weather.gov/xml/SOAP_server/ndfdSOAPclientByDay.php?whichClient=NDFDgenByDay&lat=%s&lon=%s&format=24+hourly&numDays=4&Unit=e" % (lat, lon)
    NWS_url = "http://graphical.weather.gov/xml/SOAP_server/ndfdSOAPclientByDay.php?whichClient=NDFDgenByDay&lat=40.7142&lon=-74.0064&format=24+hourly&numDays=4&Unit=e"
    
    weather_xml = urllib2.urlopen(NWS_url).read()
    dom = minidom.parseString(weather_xml)
except Exception as e:
    print "Error consulting the NOAA: %s" % e

# Parse temperatures
xml_temperatures = dom.getElementsByTagName('temperature')
highs = [None]*4
lows = [None]*4
for item in xml_temperatures:
    if item.getAttribute('type') == 'maximum':
        values = item.getElementsByTagName('value')
        for i in range(len(values)):
            highs[i] = int(values[i].firstChild.nodeValue)
    if item.getAttribute('type') == 'minimum':
        values = item.getElementsByTagName('value')
        for i in range(len(values)):
            lows[i] = int(values[i].firstChild.nodeValue)

# pop = dom.getElementsByTagName('probability-of-precipitation')
# for item in pop:
# 	values = item.getElementsByTagName('value')
	#for i in range(len(values)):
		#print values[i].firstChild.nodeValue


# time_layout = dom.getElementsByTagName('time-layout')
# for item in time_layout:
# 	values = item.getElementsByTagName('summarization')
# 	for i in range(len(values)):
# 		print values[i].firstChild.nodeValue


# Parse icons
xml_icons = dom.getElementsByTagName('icon-link')
icons = [None]*4
for i in range(len(xml_icons)):
    icons[i] = xml_icons[i].firstChild.nodeValue.split('/')[-1].split('.')[0].rstrip('0123456789')

# Parse dates
xml_day_one = dom.getElementsByTagName('start-valid-time')[0].firstChild.nodeValue[0:10]
day_one = datetime.datetime.strptime(xml_day_one, '%Y-%m-%d')



print icons


precips = {'qpf': qpf, 'snow': snow}

#
# Preprocess SVG
#

# Open SVG to process
output = codecs.open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()

timestamp = datetime.datetime.now().strftime('%-m/%-d/%y %-I:%M%p')

# Insert icons and temperatures
output = output.replace('ICON_ONE',icons[0]).replace('ICON_TWO',icons[1]).replace('ICON_THREE',icons[2]).replace('ICON_FOUR',icons[3])
output = output.replace('HIGH_ONE',str(highs[0])).replace('HIGH_TWO',str(highs[1])).replace('HIGH_THREE',str(highs[2])).replace('HIGH_FOUR',str(highs[3]))
output = output.replace('LOW_ONE',str(lows[0])).replace('LOW_TWO',str(lows[1])).replace('LOW_THREE',str(lows[2])).replace('LOW_FOUR',str(lows[3]))
output = output.replace('CURRENT', str(observed_temp))

if len(alerts) == 0: output = output.replace('ALERT', '')

if pop != 0: output = output.replace('POP_BOOL', 'PoP: ').replace('POP_NUM', str(pop) + '%')
else: output = output.replace('POP_BOOL', '').replace('POP_NUM', '')

if qpf != 0: output = output.replace('PRECIP1', 'Rain: ').replace('PRECIP_NUM1', '%.2f"' % qpf)
else: output = output.replace('PRECIP1', '').replace('PRECIP_NUM1', '')

if snow != 0: output = output.replace('PRECIP2', 'Snow: ').replace('PRECIP_NUM2', '%.2f"' % snow)
else: output = output.replace('PRECIP2', '').replace('PRECIP_NUM2', '')

output = output.replace('TIME', timestamp)

# Insert days of week
one_day = datetime.timedelta(days=1)
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
output = output.replace('DAY_THREE',days_of_week[(day_one + 2*one_day).weekday()]).replace('DAY_FOUR',days_of_week[(day_one + 3*one_day).weekday()])

# Write output
codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)
