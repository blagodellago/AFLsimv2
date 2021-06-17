import pandas as pd
import re

# scrape current afl stadium data and construct DF:
stadiums = pd.read_html('https://en.wikipedia.org/wiki/List_of_Australian_Football_League_grounds')[0]\
             .drop(index=[14,15], columns=['Image', 'Other/sponsored names', 'State/territory', 'First used'])

# present stadium names in the form to match afl_stats.csv:
stad_mapper = {
      'Melbourne Cricket Ground' : 'M.C.G.',
      'Docklands Stadium' : 'Docklands',
      'Sydney Cricket Ground' : 'S.C.G.',
      'The Gabba' : 'Gabba',
      'Carrara Stadium' : 'Carrara',
      'Sydney Showground Stadium' : 'Sydney Showground'
}
stadiums.Ground = stadiums.Ground.replace(stad_mapper)

# format values:
stadiums.Capacity = [re.sub(r'\[.+\]', '', vals) for vals in stadiums.Capacity]
stadiums['Current tenant(s)'] = [re.sub(r'\[.+\]', '', vals) for vals in stadiums['Current tenant(s)']]
stadiums['Current tenant(s)'] = [re.sub(r"([a-z])([A-Z])", r"\1, \2", tenant).split(', ') for tenant in stadiums['Current tenant(s)']]
stadiums.Capacity = stadiums.Capacity.str.replace(',', '').astype(int)
stadiums.iat[5,3] = ['Brisbane Lions']

# isolate the weather for each Stadium location as a DF:
weather_urls = {
    'Wendouree' : 'https://www.eldersweather.com.au/climate-history/vic/wendouree',
    'Melbourne' : 'https://www.eldersweather.com.au/climate-history/vic/melbourne',
    'Perth' : 'https://www.eldersweather.com.au/climate-history/wa/perth',
    'Adelaide' : 'https://www.eldersweather.com.au/climate-history/sa/adelaide',
    'Sydney' : 'https://www.eldersweather.com.au/climate-history/nsw/sydney',
    'Brisbane' : 'https://www.eldersweather.com.au/climate-history/qld/brisbane',
    'Geelong' : 'https://www.eldersweather.com.au/climate-history/vic/geelong',
    'Gold Coast' : 'https://www.eldersweather.com.au/climate-history/qld/coolangatta',
    'Launceston' : 'https://www.eldersweather.com.au/climate-history/tas/launceston',
    'Hobart' : 'https://www.eldersweather.com.au/climate-history/tas/hobart',
    'Canberra' : 'https://www.eldersweather.com.au/climate-history/act/canberra',
    'Darwin' : 'https://www.eldersweather.com.au/climate-history/nt/darwin',
    'Alice Springs' : 'https://www.eldersweather.com.au/climate-history/nt/alice-springs'
}

# format _weather DFs attached to each Stadium object:
weather_mapper = {
    'Jan' : 1,
    'Feb' : 2,
    'Mar' : 3,
    'Apr' : 4,
    'May' : 5,
    'Jun' : 6,
    'Jul' : 7,
    'Aug' : 8,
    'Sep' : 9,
    'Oct' : 10,
    'Nov' : 11,
    'Dec' : 12
}
