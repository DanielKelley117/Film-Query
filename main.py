import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import shlex
from credentials import *
from datetime import datetime as dt #import for package that compares strings of dates

# Use a service account.
#cred = credentials.Certificate('warmup-project-cs3050-0c4ff5204787.json')
#app = firebase_admin.initialize_app(cred)
#db = firestore.client()
db = get_credentials()

class Film:
    def __init__(self, release, rank, percent_total_gross, num_theaters, max_theaters, open_date, distributor, close_date, open_gross, first_gross, world_gross, inter_gross):
        self.release = release
        self.rank = rank
        self.percent_total_gross = percent_total_gross
        self.num_theaters = num_theaters
        self.max_theaters = max_theaters
        self.open_date = open_date
        self.distributor = distributor
        self.close_date = close_date
        self.open_gross = open_gross
        self.first_gross = first_gross
        self.world_gross = world_gross
        self.inter_gross = inter_gross
    
    def __str__(self):
        return f"{self.release}"

    def __eq__(self, other):
        return self.release == other.release

def parse_query(user_input):
    query = shlex.split(user_input)
    
    fields = ["distributor", "rank", "maxTheaters", "open", "percentTotalGross", "openingTheaters", "gross", "OpenGross", "WorldGross", "InterGross"]
    operators = ["<", ">", "<=", ">=", "==", "of"]
    logic_operators = ["and"]

    if len(query) == 3:
        command, compare, value = query
        if command in fields and compare in operators:
            if command != "distributor" and command != "gross" and (not value.isnumeric() and compare != "of"):
                print("Error: Value must be numeric")
                return None
            if command != "distributor" and command != "gross" and value.isnumeric() :
                value = int(value)
            if command == "distributor" and compare != "==" and compare != "of":
                print("Error: distributor must use == or of operator")
                return None
            if command == "gross" and compare != "of":
                print("Error: gross must use of operator")
                return None
            if compare != "of":
                #return equal_inequality_query(command, compare, value)
                compareFilms = equal_inequality_query(command, compare, value)
                for film in compareFilms:
                    print(film)
                return compareFilms
            if compare == "of":
                value = str(value)
                if value.isnumeric():
                    print("Error: Movie name must be a string.")
                    return None
                else:
                    #return of_query(value, command)
                    ofFilms = of_query(value, command)

                    if command != "gross":
                        print(ofFilms)
                        return ofFilms
                    else:
                        for i in range(0, 3):
                            print(ofFilms[i])
        else: 
            print("Error: Fields or Operators not valid")
            return None
    elif len(query) == 7:
        
        field1, operator1, value1, logic_operator, field2, operator2, value2 = query
        if logic_operator in logic_operators:
            if field1 in fields and field2 in fields and operator1 in operators and operator2 in operators:
                if field1 == field2 and operator1 == operator2 and value1 == value2:
                    print("Error: Duplicate commands")
                    return None
                if (field1 != "distributor" and field1 != "gross" and (not value1.isnumeric()and operator1 != "of")) or (field2 != "distributor" and field2 != "gross" and (not value2.isnumeric() and operator2 != "of")):
                    print("Error: Value must be numeric")
                    return None
                if (field1 != "distributor" and field1 != "gross" and value1.isnumeric()):
                    value1 = int(value1)
                if (field2 != "distributor" and field2 != "gross" and value2.isnumeric()):
                    value2 = int(value2)
                if (field1 == "distributor" and operator1 != "==" and operator1 != "of") or (field2 == "distributor" and operator2 != "==" and operator2 != "of"):
                    print("Error: distributor must use == or of operator")
                    return None
                if (field1 == "gross" and operator1 != "of") or (field2 == "gross" and operator2 != "of"):
                    print("Error: gross must use of operator")
                    return None
                conjunction1 = "conjunction1"
                compare1 = False
                if operator1 != "of":
                    conjunction1 = equal_inequality_query(field1, operator1, value1)
                    compare1 = True

                if operator1 == "of":
                    value1 = str(value1)
                    if value1.isnumeric():
                        print("Error: Movie name must be a string.")
                        return None
                    else:
                        conjunction1 = of_query(value1, field1)

                conjunction2 = "conjunction2"
                compare2 = False
                if operator2 != "of":
                    conjunction2 = equal_inequality_query(field2, operator2, value2)
                    compare2 = True

                if operator2 == "of":
                    value2 = str(value2)
                    if str(value1).isnumeric():
                        print("Error: Movie name must be a string.")
                        return None
                    else:
                        conjunction2 = of_query(value2, field2)

                if compare1 and compare2:
                    if field1 != "gross" and field1 != "OpenGross" and field1 != "WorldGross" and field1 != "InterGross" and field2 != "gross" and field2 != "OpenGross" and field2 != "WorldGross" and field2 != "InterGross":
                        newList = find_matches(conjunction1, conjunction2)
                        for film in newList:
                            print(film)
                    else:
                        print("No Gross Values Available")

                        if field1 == "gross" or field1 == "OpenGross" or field1 == "WorldGross" or field1 == "InterGross":

                            for film in conjunction2:
                                print(film)

                        elif field2 == "gross" or field2 == "OpenGross" or field2 == "WorldGross" or field2 == "InterGross":

                            for film in conjunction1:
                                print(film)

                else:
                    print("Results of left command: ")
                    if compare1:
                        for film in conjunction1:
                            print(film)
                    else:

                        if field1 != "gross":
                            print(conjunction1)
                        else:
                            for i in range(0, 3):
                                print(conjunction1[i])

                    print("End of left command")

                    print("Results of right command: ")
                    if compare2:
                        for film in conjunction2:
                            print(film)
                    else:

                        if field2 != "gross":
                            print(conjunction2)

                        else:
                            for i in range(0, 3):
                                print(conjunction2[i])

                    print("End of right command")

                return (field1, operator1, value1, logic_operator, field2, operator2, value2)
            else:
                print("Error: Fields or Operators not valid")
                return None
    else:
        print("Error: Length of string is incorrect")
        return None

def equal_inequality_query(command, compare, value):
    #Be sure to wrap long distributor names in quotes "" 
    # ex: distributor == "Paramount Pictures"
    # ex: rank == 100

    if command == "gross" or command == "OpenGross" or command == "WorldGross" or command == "InterGross":
        return ["Gross values cannot be used with compare operators."]

    docs = (
        db.collection("Movies")
        .where(filter=FieldFilter(command, compare, value))
        .stream()
    )
    filmsList = []
    for doc in docs:
        ref = doc.to_dict()
        film_object = Film(
                release=ref.get("release"),
                rank=ref.get("rank"),
                percent_total_gross=ref.get("percentTotalGross"),
                num_theaters=ref.get("openingTheaters"),
                max_theaters=ref.get("maxTheaters"),
                open_date=ref.get("openDate"),
                distributor=ref.get("distributor"),
                close_date=ref.get("closeingDate"),
                open_gross=ref.get("open"),
                first_gross=ref.get("gross")[0],
                world_gross=ref.get("gross")[2],
                inter_gross=ref.get("gross")[1]
            )
        filmsList.append(film_object)
        #print(f"{doc.id}")

    if len(filmsList) == 0:
        print("None Found")
    return filmsList


def of_query(film_id, attribute):
    ref = db.collection("Movies").document(film_id)

    ref_mem = ref.get()

    if ref_mem.exists:
        ref_third = ref_mem.to_dict()
        film_object = Film(
                release=ref_third.get("release"),
                rank=ref_third.get("rank"),
                percent_total_gross=ref_third.get("percentTotalGross"),
                num_theaters=ref_third.get("openingTheaters"),
                max_theaters=ref_third.get("maxTheaters"),
                open_date=ref_third.get("openDate"),
                distributor=ref_third.get("distributor"),
                close_date=ref_third.get("closeingDate"),
                open_gross=ref_third.get("open"),
                first_gross=ref_third.get("gross")[0],
                world_gross=ref_third.get("gross")[2],
                inter_gross=ref_third.get("gross")[1]
                )
        if attribute == "release" or attribute == "Release":
            #print(film_object.release)
            return film_object.release

        elif attribute == "rank" or attribute == "Rank":
            #print(film_object.rank)
            return film_object.rank
        elif attribute == "percentTotalGross":
            #print(film_object.percent_total_gross)
            return film_object.percent_total_gross

        elif attribute == "openingTheaters":
            #print(film_object.num_theaters)
            return film_object.num_theaters

        elif attribute == "maxTheaters":
            #print(film_object.max_theaters)
            return film_object.max_theaters

        elif attribute == "openDate":
            #print(film_object.open_date)
            return film_object.open_date

        elif attribute == "Distributor" or attribute == "distributor":
            #print(film_object.distributor)
            return film_object.distributor

        elif attribute == "closingDate":
            #print(film_object.close_date)
            return film_object.close_date

        elif attribute == "open" or attribute == "Open":
            #print(film_object.open_gross)
            return film_object.open_gross

        elif attribute == "gross":
            grossList = [film_object.first_gross, film_object.world_gross, film_object.inter_gross]
            return grossList

        elif attribute == "OpenGross":
            #print(film_object.gross array values)
            return film_object.first_gross

        elif attribute == "WorldGross":
            return film_object.world_gross

        elif attribute == "InterGross":
            return film_object.inter_gross

    else:
        return "No Data Available"



def find_matches(list1, list2):
    commonList = []
    for i in list1:
        for j in list2:
            if i == j and not(i in commonList):
                commonList.append(i)

    return commonList

def main():
    menu = "--------------------\nCOMMANDS\nFields: distributor, rank, maxTheaters, openingTheaters, percentTotalGross, gross, OpenGross, WorldGross, InterGross\nOperators: <, >, <=, >=, ==, of\nSTRUCTURES\nAttribute Operator Value (ex. distributor == \"Paramount Pictures\")\nAttribute of MovieName (ex. maxTheaters of Uncharted)\nAttribute Operator Value and Attribute Operator Value (ex. rank < 5 and openDate <= 2022-05-27)\nEnter quit to exit\n--------------------"
    print("Welcome to the Top 200 Movies of 2022 query parser.\nEnter help for more information.")
    while True:
        user_input = input("> ")
        # quit option
        if user_input.lower() == "quit" or user_input.lower() == "exit":
            break
        # help option should print out help text about the commands
        elif user_input.lower() == "help":
            print(menu)
        else:
            parsed_query = parse_query(user_input)
            if parsed_query == None:
                print(menu)
            

main()
