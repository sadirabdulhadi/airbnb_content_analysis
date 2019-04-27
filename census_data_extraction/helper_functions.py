import csv
import skbio
import statistics
main_path = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/census_files/UK/"

def column(path, column_lsoa, column_value, list_of_wards,lsoa_to_ward):
    #we use this function when the data we want to extract is in one column. We calculate the average across LSOAs.
    wards_return = {}
    wards_subdivisions = {}
    with open(main_path+path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                id = row[column_lsoa]
                if id in lsoa_to_ward:
                    corresponding_ward = lsoa_to_ward[id]
                    if corresponding_ward not in wards_return.keys():
                        wards_return[corresponding_ward] = 0
                        wards_subdivisions[corresponding_ward] = 0
                    wards_return[corresponding_ward] += float(row[column_value].replace(',', ''))
                    wards_subdivisions[corresponding_ward] += 1
                line_count += 1
    for key in wards_return.keys():
        wards_return[key] = wards_return[key]/wards_subdivisions[key]
    return wards_return

def column_dep(path, column_lsoa, column_value, list_of_wards,lsoa_to_ward):
    #we use this function when the data we want to extract is in one column. We calculate the average across LSOAs.
    wards_return = {}
    wards_subdivisions = {}
    with open(main_path+path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                id = row[column_lsoa][-9:]
                if id in lsoa_to_ward:
                    corresponding_ward = lsoa_to_ward[id]
                    if corresponding_ward not in wards_return.keys():
                        wards_return[corresponding_ward] = 0
                        wards_subdivisions[corresponding_ward] = 0
                    wards_return[corresponding_ward] += float(row[column_value].replace(',', ''))
                    wards_subdivisions[corresponding_ward] += 1
                line_count += 1
    for key in wards_return.keys():
        wards_return[key] = wards_return[key]/wards_subdivisions[key]
    return wards_return

'''
def column_postcode(path, column_postcode, column_value, list_of_wards,postcode_to_ward):
    #we use this function when the data we want to extract is in one column. We calculate the average across LSOAs.
    wards_return = {}
    wards_subdivisions = {}
    with open(main_path+path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                id = row[column_postcode]
                if id in postcode_to_ward:
                    corresponding_ward = postcode_to_ward[id]
                    if corresponding_ward not in wards_return.keys():
                        wards_return[corresponding_ward] = 0
                        wards_subdivisions[corresponding_ward] = 0
                    wards_return[corresponding_ward] += float(row[column_value].replace(',', ''))
                    wards_subdivisions[corresponding_ward] += 1
                line_count += 1
    for key in wards_return.keys():
        wards_return[key] = wards_return[key]/wards_subdivisions[key]
    return wards_return
'''
def proportion(path, column_lsoa, columns_value, column_total,lsoa_to_ward):
    #we use this function when the data we want to extract is in one column. We calculate the average across LSOAs
    wards_tocount = {}
    wards_total = {}
    with open(main_path+path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                id = row[column_lsoa]
                if id in lsoa_to_ward:
                    corresponding_ward = lsoa_to_ward[id]
                    if corresponding_ward not in wards_tocount.keys():
                        wards_tocount[corresponding_ward] = 0
                        wards_total[corresponding_ward] = 0
                    for column in columns_value:
                        wards_tocount[corresponding_ward] += float(row[column].replace(',', ''))
                    wards_total[corresponding_ward] += float(row[column_total].replace(',', ''))
                line_count += 1
    for key in wards_tocount.keys():
        wards_tocount[key] = wards_tocount[key]/wards_total[key]
    return wards_tocount

def diversity(path, column_lsoa, columns, lsoa_to_ward):
    wards = {}
    wards_diversity = {}
    with open(main_path+path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                id = row[column_lsoa]
                if id in lsoa_to_ward:
                    corresponding_ward = lsoa_to_ward[id]
                    if corresponding_ward not in wards.keys():
                        wards[corresponding_ward]= {}
                    for column in columns:
                        wards[corresponding_ward][column] = float(row[column].replace(',', ''))
                line_count += 1
    for key in wards.keys():
        wards_diversity[key] = skbio.diversity.alpha.shannon(list(wards[key].values()))
    print(wards_diversity)
    return wards_diversity

