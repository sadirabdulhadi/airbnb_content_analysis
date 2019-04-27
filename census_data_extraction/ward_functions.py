import fiona
import csv

main_path = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/"

class Ward:
    def __init__(self, id=0, name=None, number_reviews = 0, number_listings = 0):
        self.id = id
        self.name = name
        self.number_reviews = number_reviews
        self.number_listings = number_listings
        self.numberSubdivisions = 0


def fillWardsWithData(wards_shapefile):
    ward_list = {}
    for feat in fiona.open(main_path + wards_shapefile):
        ward_properties = feat['properties']
        #ward_list[ward_properties['ward_id']] = Ward(ward_properties['ward_id'], ward_properties['name'], 0, 0) #bristol
        ward_list[ward_properties['ward_id']] = Ward(ward_properties['ward_id'], "", 0, 0)  #manchester


    #for name, ward in ward_list.items():
        #print(f'\tNAME: {ward.name}, ID {ward.id}')

    return ward_list
'''
def postcode_to_ward(ward_list):
    subToWard= {}
    #with open(main_path +'ward_files/bristol/conversion.csv') as csv_file:
    with open(main_path +'ward_files/bristol/conversion.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                city = row[5]
                wardID = row[2]
                localID = row[1]

                if city == "Bristol, City of":
                    if wardID in ward_list:
                        subToWard[localID] = wardID
            line_count += 1
        print(f'Processed {line_count} lines.')
    return subToWard
'''

def lsoa_to_ward(ward_list):
    subToWard= {}
    #manchester/london/bristol
    #with open(main_path +'ward_files/manchester/conversion.csv') as csv_file:
    with open(main_path +'ward_files/manchester/conversion.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                city = row[4]
                wardID = row[2]
                localID = row[0]
                #if city == "E06000023": #bristol
                #if city in ["E08000001", "E08000002", "E08000003", "E08000004", "E08000005", "E08000006", "E08000007", "E08000008", "E08000009", "E08000010"]: #manchester
                #if city in ['E09000001', 'E09000002', 'E09000003', 'E09000004', 'E09000005', 'E09000006', 'E09000007', 'E09000008', 'E09000009', 'E09000010', 'E09000011', 'E09000012', 'E09000013', 'E09000014', 'E09000015', 'E09000016', 'E09000017', 'E09000018', 'E09000019', 'E09000020', 'E09000021', 'E09000022', 'E09000023', 'E09000024', 'E09000025', 'E09000026', 'E09000027', 'E09000028', 'E09000029', 'E09000030', 'E09000031', 'E09000032' ,'E09000033']:
                if wardID in ward_list:
                    subToWard[localID] = wardID
                if city == 'E09000001':
                    print(wardID)
            line_count += 1
        print(f'Processed {line_count} lines.')
    return subToWard

