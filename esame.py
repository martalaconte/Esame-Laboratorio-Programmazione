# Importing class 'datetime' from 'datetime' module, to avoid form 'datetime.datetime.strptime'
from datetime import datetime as dt 

# Exception class used to raise custom exceptions later in the program
class ExamException(Exception):
    pass

# Creating CSVFile class extension 
# Istantiating the class by calling it as a function 
# Passing the arguments defined by "init" method (lets the class initialize the object's attributes)
class CSVTimeSeriesFile():
    def __init__ (self, name):

        # The "self" keyword represents the instance of the class and accesses the attributes and methods of the class
        # The variable "name" refers to the name of the file 
        self.name = name

    # Defining a "get_data" method to access the data inside the "data.csv" file
    def get_data(self):

        # Creating two lists that will be needed inside the "get_data" method
        # The list "data_list" stores two values: 1. The dates in the %Y-%m format ; 2. The number of passengers
        data_list = []
        # The list of lists "complete_list" stores multiple "data_list" sublists as items 
        complete_list = []

        # Verifying that the file exists by opening it in read mode
        try:
            file = open (self.name, 'r')

        # Raising an exception in case the file does not exist 
        except Exception:
            raise ExamException ('Error: file not found.')
        
        # Every line in the file is ran through the function and then stored in the "data_list" list
        for line in file: 
            
            # Every line gets split where the script encounters a comma 
            list_element = line.split(',')

            # Ensuring that the strings that are not meant to be stored in the "data_list" do not get processed (title) 
            if list_element[0] != 'date': 
                
                # The date is listed as the first item in "data_list"
                date = list_element[0]

                # Checking all 'date' values by using the imported "datetime" class to convert them to YYYY-MM format ("%Y-%m") 
                try:
                    date = dt.strptime(date, "%Y-%m")

                # Should the date format differ from "%Y-%m" the program keeps running
                except Exception:
                    continue

                # Converting 'date' values back to strings 
                date = list_element[0]

                # The (integer) number of passengers is listed as the second item in "data_list" 
                try:
                    passengers = int(list_element[1])

                #Storing "0" in 'passengers' variable in case the value does not exist so that the program can keep running
                except IndexError:
                    passengers = 0

                # Ignoring float values
                except ValueError:
                    continue 
                
                # Ignoring negative values
                if passengers < 0:
                    continue 

                # Checking for duplicates in the timestamps 
                # Checking that the "complete_list" is not empty
                if len(complete_list) > 0:

                    # Eventually cycling through the list
                    for element in complete_list:

                        # The first item of the list "element" (date) is temporarily saved as the value of a variable
                         tmp_date = element[0] 

                        # An exception is raised in case a duplicate is found
                         if tmp_date == date: 
                            raise ExamException('Error: timestamp "{}" is a duplicate.'.format(date))

                    # Checking the order of the timestamps in case there are no duplicates 
                    # The value of the item will be temporarily saved in a variable
                    tmp_date == complete_list[-1][0]

                    # Checking for errors in the order of the timestamps
                    if tmp_date > date:
                        raise ExamException('Error: timestamp "{}" is misplaced.'.format(date))

                # The sublists "data_list" can be filled 
                data_list = [date, passengers]

                # The sublists "data_list" can be added to "complete_list"
                complete_list.append(data_list)

                # The cycle restarts
                
        # Raising an exception in case the file is empty
        if not complete_list:
            raise ExamException('Error: file is empty.')

        # Returning the output
        return  complete_list

# Defining a function that calculates similar variation values between couples of consecutive months in consecutive years 
def detect_similar_monthly_variations(time_series, years):

    # Checking that the list "years" is not empty and raising an exception if so
    if not years:
        raise ExamException('Error: the list is empty.')

    # Checking that the list "years" does not contain less than the two required items to compare and raising an exception if so
    if len(years) != 2:
        raise ExamException('Error: not enough items to make a comparison.')

    # Checking that parameter "time_series" is a list and raising an exception if not 
    if not isinstance(time_series, list):
        raise ExamException('Error: "time_series" is not a list.')

    # Checking that parameter "time_series" is a list of lists and raising an exception if not
    elif not isinstance(time_series[0], list):
        raise ExamException('Error: "time_series" is not a list of lists. ')

    # Checking both the items in the "years" list to ensure they are both integers and raising an exception if not 
    if not isinstance(years[0], int) or not isinstance(years[1], int):
        raise ExamException('Error: the list "years" should only contain integers values. {} type and {} type found instead.'.format(type(years[0]), type(years[1])))

    # Checking that both the items in the list "years" are also items in the list "time_series" and raising an exception if not 
    # Check on the first item
    if years[0] < int(time_series[0][0][:4]):
        raise ExamException('Error: no available data for listed year.')
    
    # Check on the second item
    if years[1] > int(time_series[-1][0][:4]):
        raise ExamException('Error: no available data for listed year.')

    # Checking that the first item in the list "years" is the year prior to the second item and raising an exception if not
    if years[0] > years[1]:
        raise ExamException('Error: the first year listed comes after the second.')

    # Checking that the two years listed are consecutive and raising an exception if not
    if years[1] != years[0] + 1:
        raise ExamException('Error: the listed years are not consecutive.')

    # Checking that the two items are not the same year and raising an exception if so
    if years[0] == years[1]:
        raise ExamException('Error: the listed years cannot be the same.')

    # Creating empty dictionary
    dictionary = {} 

    # Appending "time_series[i][1]" values (number of passengers) to keys "time_series[i][0]"
    for i in range(len(time_series)):
        dictionary[time_series[i][0]] = []
        dictionary[time_series[i][0]].append(time_series[i][1])

    # Creating a list for the keys that are needed (years)
    keys = []

    # Storing "years[0]" value in another variable
    storage_year = years[0]

    # Storing all needed keys in a separate list
    while years[0] <= years[1]:

        # Running through the keys in the dictionary
        for key in dictionary:
            
            # Taking just the first four digits (the year)
            key_year = key[:4] 

            # This is needed to exit the for loop when it has processed every key for the current year
            if int(key_year) > years[0]:
                break
 
            # Every key for the year gets stored in the previous created list
            if int(key_year) == years[0]:
                keys.append(key)
                        
        # When the cycle is done processing a year, it increases so it can pass on to the next one
        years[0] = years[0] + 1
        
    # Restoring "years[0]" to its initial value
    years[0] = storage_year

    # Creating the output list
    complete_list = []

    # Calculating monthly difference 
    # Defining variables
    var = 0
    result = True

    # range(len(keys) - 1) cause i starts from 0
    for i in range(11): 

        # Calculating variation 
        var = (dictionary[keys[i + 1]][0] - dictionary[keys[i]][0]) - (dictionary[keys[(i + 1) + 12]][0] - dictionary[keys[i + 12]][0])

        # If the absolute value of the variation is less or equal than 2, "True" is appended; if not "False"
        if abs(var) <= 2:
            result = True
            
        else:
            result = False
        
        # Appending the result to the output list
        complete_list.append(result)

    # Returning the final result
    return complete_list


