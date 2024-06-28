import pandas as pd
import json

# def run():
#     df = pd.read_csv('prms/regions_districts.csv')
#     # get regions and their districts in a dictionary
#     regions = df['REGION'].unique()
#     regions_dict = {}
#     for region in regions:
#         regions_dict[region] = list(df[df['REGION'] == region]['DISTRICT'])
#         # add category to each district either district, municipal or metropolitan
#         for district in regions_dict[region]:
#             if 'Municipal' in district:
#                 regions_dict[region][regions_dict[region].index(district)] = (district, 'Municipal')
#             elif 'Metropolitan' in district:
#                 regions_dict[region][regions_dict[region].index(district)] = (district, 'Metropolitan')
#             else:
#                 regions_dict[region][regions_dict[region].index(district)] = (district, 'District')
#     # save the dictionary to a file as a json
#     import json
#     with open('data/regions_districts.json', 'w') as f:
#         json.dump(regions_dict, f)
   
# run()


# import requests
# from bs4 import BeautifulSoup
# import re
# import pandas as pd
# import json

# def get_data():
#     url = 'https://citypopulation.de/en/ghana/admin/'
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     tables = soup.find_all('table')
#     data = []
#     for table in tables:
#         rows = table.find_all('tr')
#         for row in rows:
#             cells = row.find_all('td')
#             if len(cells) > 0:
#                 data.append([cell.text for cell in cells])
#     return data

# def clean_data(data):
#     data = data[1:]
#     for i in range(len(data)):
#         data[i] = [re.sub(r'\n', '', cell) for cell in data[i]]
#     return data

# data = get_data()
# data = clean_data(data)
# df = pd.DataFrame(data, columns=['Name', 'Status', 'Population 2010', 'Population 2021', 'Area km²',])
# df.to_csv('data/ghana_population.csv', index=False)

# get the regions and districts and population for 2010 and 2021 into a json file
# Initialize a dictionary to store regions and their districts

# def get_districts_by_region(filename):
#   """
#   This function reads an Excel file with columns 'name', 'status',
#   'population_2010', and 'population_2021'. It assumes the first row
#   has a 'Region' status and iterates through the data, identifying
#   districts belonging to each region and their population data for 2010 and 2021.

#   Args:
#       filename (str): Path to the Excel file.

#   Returns:
#       dict: A dictionary where keys are region names and values are dictionaries.
#             The inner dictionary has keys 'districts' (list of district names),
#             'population_2010' (list of population values for 2010), and
#             'population_2021' (list of population values for 2021).
#   """

#   # Read the Excel file
#   data = pd.read_csv(filename)

#   # Initialize a dictionary to store regions and their districts
#   regions_and_districts = {}
#   current_region = None  # Track the current region
#   current_district_data = {}  # Track data for the current district

#   # Iterate through each row of data
#   for index, row in data.iterrows():
#     status = row['Status']

#     # Handle rows with 'Region' status
#     if status == 'Region':
#       current_region = row['Name'] # Add region name
#       regions_and_districts[current_region] = {
#           'districts': [],
#           'Population 2010': row['Population 2010'] if pd.notna(row['Population 2010']) else None,  # Handle missing values
#           'Population 2021': row['Population 2021'] if pd.notna(row['Population 2021'])else None,  # Handle missing values
#           'map_url': f'https://google.com/maps?q=ghana+{current_region}' # Add map URL for region
#       }
#       current_district_data = {}  # Reset district data for new region

#     # Handle rows with 'District' or 'Municipal District' status
#     elif status in ('District', 'Municipal District'):
#       if current_region is not None:
#         # remove unwanted characters from the district name
#         current_district_data['name'] = row['Name'] # Add district name
#         current_district_data['Population 2010'] = row['Population 2010'] if pd.notna(row['Population 2010']) else None  # Handle missing values
#         current_district_data['Population 2021'] = row['Population 2021'] if pd.notna(row['Population 2021']) else None  # Handle missing values
#         current_district_data['Status'] = status  # Add district status
#         current_district_data['map_url'] = f'https://google.com/maps?q=ghana+{current_region}+{current_district_data["name"]}'
#         regions_and_districts[current_region]['districts'].append(current_district_data.copy())  # Append data with copy to avoid reference issues
#         current_district_data = {}  # Reset district data for next district
#       else:
#         print(f"Warning: Found district '{row['Name']}' before encountering a region.")

#   return regions_and_districts

# regions_and_districts = get_districts_by_region('data/ghana_population.csv')

# # Save the regions and districts data to a JSON file
# with open('data/regions_districts_population.json', 'w') as f:
#   json.dump(regions_and_districts, f, indent=2)

from pnms.models import Region, District, Population
from django.contrib.contenttypes.models import ContentType



def populate_data():
    with open('data/regions_districts_population.json') as f:
        data = json.load(f)
    for region_name, region_data in data.items():
        region = Region.objects.create(name=str(region_name).strip(), map_url=region_data['map_url'])
        # Create population data for 2010
        if region_data['Population 2010'] is not None:
            region_population_2010 = int(region_data['Population 2010'].replace(',', ''))
            Population.objects.create(population=region_population_2010, year=2010, content_object=region, content_type=ContentType.objects.get_for_model(region), object_id=region.id)

        # Create population data for 2021
        if region_data['Population 2021'] is not None:
            region_population_2021 = int(region_data['Population 2021'].replace(',', ''))
            Population.objects.create(population=region_population_2021, year=2021, content_object=region, content_type=ContentType.objects.get_for_model(region), object_id=region.id)
        print(f"Creating region {region_name}")
        for district_data in region_data['districts']:
            district = District.objects.create(name=str(district_data['name']).strip(), region=region, map_url=district_data['map_url'])

            if district_data['Population 2010']  == '...' or district_data['Population 2021'] == '...':
                continue

            # Create population data for 2010
            if district_data['Population 2010'] is not None:
                district_population_2010 = int(district_data['Population 2010'].replace(',', ''))
                Population.objects.create(population=district_population_2010, year=2010, content_object=district, content_type=ContentType.objects.get_for_model(district), object_id=district.id)

            # Create population data for 2021
            if district_data['Population 2021'] is not None:
                district_population_2021 = int(district_data['Population 2021'].replace(',', ''))
                Population.objects.create(population=district_population_2021, year=2021, content_object=district, content_type=ContentType.objects.get_for_model(district), object_id=district.id)
            print(f"Creating district {district_data['name']} in {region_name}")
     
populate_data()

# df = pd.read_csv('data/ghana_population.csv')
# print(df[df['Population 2010'] == '...']['Name'])