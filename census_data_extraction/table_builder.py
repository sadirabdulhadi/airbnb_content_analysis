#import statements
import ward_functions as wrd
import helper_functions as hp

#define paths #bristol, manchester
#wards_shapefile_path = "ward_files/bristol/wards.shp"
wards_shapefile_path = "ward_files/london/wards.shp"

#wards_shapefile_path = "ward_files/manchester/manch.shp"

#dict definitions
wards_list = {}
lsoa_to_ward = {}

#demographics
median_age = {} #median

#diversity
proportion_nonenglish_household = {} #prop
proportion_pop_outside_uk = {} #diversity
ethnic_diversity = {} #diversity

#household
average_number_bedrooms = {} #average
average_household_size = {} #average
proportion_household_dep_children = {} #proportion

#economics
proportion_economic_active = {} #number/total
average_distance_to_work = {} #average
deprivation_index = {} #median - average?

#education
proportion_qual4 = {} #number/total
proportion_students = {} #number/total
proportion_stem = {}
proportion_bohemian = {}


#ward-setup
wards_list = wrd.fillWardsWithData(wards_shapefile_path)
lsoa_to_ward = wrd.lsoa_to_ward(wards_list)
#print("lsoa to ward")
#print(lsoa_to_ward)
#postcode_to_ward = wrd.postcode_to_ward(wards_list)

#calculate column dictionaries:
average_distance_to_work = hp.column(path = "distance-to-work.csv", column_lsoa = 2, column_value = 16, list_of_wards = wards_list, lsoa_to_ward = lsoa_to_ward)
#print(average_distance_to_work)
deprivation_index = hp.column_dep(path="deprivation.csv", column_lsoa = 0, column_value = 2, list_of_wards = wards_list, lsoa_to_ward = lsoa_to_ward)
median_age = hp.column(path = "age-structure.csv", column_lsoa = 2, column_value = 21, list_of_wards = wards_list, lsoa_to_ward = lsoa_to_ward)
average_number_bedrooms = hp.column(path = "heating-no-rooms.csv", column_lsoa = 2, column_value = 11, list_of_wards = wards_list, lsoa_to_ward = lsoa_to_ward)
average_household_size = hp.column(path = "heating-no-rooms.csv", column_lsoa = 2, column_value = 9, list_of_wards = wards_list, lsoa_to_ward = lsoa_to_ward)

#calculate proportions
proportion_economic_active = hp.proportion(path="economic-activity.csv", column_lsoa = 2, columns_value = [4], column_total = 3, lsoa_to_ward = lsoa_to_ward)
proportion_students = hp.proportion(path="economic-activity.csv", column_lsoa = 2, columns_value = [10,13], column_total = 3, lsoa_to_ward = lsoa_to_ward)
proportion_stem = hp.proportion(path="industries-minor.csv", column_lsoa = 2, columns_value = [8,13], column_total = 3, lsoa_to_ward = lsoa_to_ward)
proportion_bohemian = hp.proportion(path="industries-minor.csv", column_lsoa = 2, columns_value = [16], column_total = 3, lsoa_to_ward = lsoa_to_ward)
    #bohemian - culture, media and sports
proportion_household_dep_children = hp.proportion(path = "household-composition.csv", column_lsoa = 2, columns_value = [11,15,18,21], column_total = 3, lsoa_to_ward = lsoa_to_ward)
proportion_nonenglish_household =  hp.proportion(path="household-language.csv", column_lsoa = 2, columns_value = [6,7,8], column_total = 4, lsoa_to_ward = lsoa_to_ward)
proportion_pop_outside_uk =  hp.proportion(path="country-of-birth.csv", column_lsoa = 2, columns_value = [12,15], column_total = 4, lsoa_to_ward = lsoa_to_ward)
proportion_qual4 =  hp.proportion(path="highest-level-qualification.csv", column_lsoa = 2, columns_value = [9], column_total = 3, lsoa_to_ward = lsoa_to_ward)

#calculate diversity indices
ethnic_diversity = hp.diversity(path ="ethnicity.csv", column_lsoa = 2, columns = [5,10,15,21,25], lsoa_to_ward = lsoa_to_ward)

print("KEYS")
print(sorted(proportion_students.keys()))
#print(sorted(wards_list.keys()))

#move to CSV

def moveToCSV():
    #manchester bristol london
    #print("yayy")
    #print(average_household_size)

    download_dir = "/Users/Sadir/Documents/Computer_science/Year4/term2/individual_project/results/london/socio-economic.csv"
    #print("yooo")
    csv = open(download_dir, "w")
    #bristol
    #columnTitleRow = "Ward,distance_to_work,deprivation_index,median_age,number_bedrooms,household_size,economic_activity,students,stem,bohemian,educated,dep_children,nonenglish_household,foreign_born,diversity\n"
    #manchester
    columnTitleRow = "Ward,distance_to_work,median_age,number_bedrooms,household_size,economic_activity,students,stem,bohemian,educated,dep_children,nonenglish_household,foreign_born,diversity,deprivation\n"

    csv.write(columnTitleRow)
    for code, ward in wards_list.items():
        if code in average_household_size.keys():
            #print(average_household_size)
            #print(code)
            #print(code, average_household_size[code])
            #bristol
            #row = ward.id + "," + str(average_distance_to_work[code]) + "," + str(deprivation_index[code]) + "," + str(median_age[code]) + "," + str(average_number_bedrooms[code]) + "," + str(average_household_size[code]) + "," + str(proportion_economic_active[code]) + "," + str(proportion_students[code]) + "," + str(proportion_stem[code]) +  "," + str(proportion_bohemian[code]) + "," + str(proportion_qual4[code]) + "," + str(proportion_household_dep_children[code])+ ","  + str(proportion_nonenglish_household[code]) + "," + str(proportion_pop_outside_uk[code])  + "," + str(ethnic_diversity[code])+ "\n"
            #manchester
            row = ward.id + "," + str(average_distance_to_work[code]) + "," + str(median_age[code]) + "," + str(average_number_bedrooms[code]) + "," + str(average_household_size[code]) + "," + str(proportion_economic_active[code]) + "," + str(proportion_students[code]) + "," + str(proportion_stem[code]) +  "," + str(proportion_bohemian[code]) + "," + str(proportion_qual4[code]) + "," + str(proportion_household_dep_children[code])+ ","  + str(proportion_nonenglish_household[code]) + "," + str(proportion_pop_outside_uk[code])  + "," + str(ethnic_diversity[code])+ "," + str(deprivation_index[code]) + "\n"
            csv.write(row)

    print(len(wards_list))
    print(len(average_household_size))


moveToCSV()
