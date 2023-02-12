#Kyle Mellott


#This program creates a term by document co-occurence matrix and then uses this
#matrix to calculate the pairwise cosine similarity score between every book that's input
#on the command prompt. The number of text files that can be input will be limited by memory,
#and this limit was not reached during program testing. The program will output the total
#number of tokens and types that fall within the token minimum and token maximum range, as
#well as outputting these ranges. It will then output each pair of books along with the
#cosime similarity score, sorted in descending order.

#The first and second inputs are the minimum and maximum allowed counts, respectively.
#Every input after that should be a .txt file that you would like to compare to other files.

#An example use of the program is as follows:
#   In the command prompt:
#   >> books 1 1000000 10byron.txt 1crime.txt  2war.txt
#   The following output is given:
#   >> tokens = 303636, types = 10985, lower = 1, upper = 1000000
#      10byron.txt 10byron.txt 1.0000
#      1crime.txt 1crime.txt 1.0000
#      2war.txt 2war.txt 1.0000
#      1crime.txt 2war.txt 0.9545
#      10byron.txt 2war.txt 0.9488
#      10byron.txt 1crime.txt 0.8889
#The output cosine values have been truncated to 4 decimal places to improve readability.

#The following is a walkthrough of program execution:

#Upon initiating via the command prompt, the first and second inputs are stored in the
#variables token_min and token_max, respectively. Every input after this is added
#to a list called texts. These three inputs are then passed to the main() function so that
#processing may begin.

#Main first creates the necessary variables. total_text is an empty string that will be
#used to concatenate each of the books into one long string. This is done in order to
#calculate token and type counts, as well as get the list of words that should be used
#in the cosine calculation. books is a list that will hold each individual book.
#book_counts is a list that will contain the type counts for individual books. Note that
#book counts is a list of dictionaries, where each entry is a dictionary with the
#types and type counts of a book.

#The first step after variable creation is pre-processing. Each file name is passed
#to toLower(), which opens the file and changes all of the data to lowercase. The book
#is then returned and passed to the remove() function, which removes all non-alphanumeric
#values. The book is then added to books[], in such a way that each index in books contains
#an entire pre-processed book.

#The next step is to create a string that is every book concatenated together. This
#is necessary to get the total type and token count, as well as get the words that
#will be used in the cosine calculation.
#It's necessary to get the words from the total text block because not every book
#will contain every word.

#Next, the token count requirements and the total_text is passed to the count()
#function. The count function creates a dictionary of types with type counts
#for the entire total text corpus. It then filters this dictionary by adding the
#types that meet the token count requirements to a new dictionary, called
#good_types. It sums the number of times that each type occurs in order to
#get the token count. The count function ends by printing out the token and
#type counts, and the minimum and maximum constraints. It then returns the
#good_types dictionary.

#The next is the book_dict function, which creates a dictionary of types and type
#counts for each individual book and adds it to the book_count list.

#THe next step is the creation of the matrix. good_types, which is the total dictionary
#of types that fall within the range, book_counts, which is a dictionary for each individual
#book, and texts, which is a list of the names of the files input, are all passed
#to the matrix_create function.
#matrix_create creates a 2x2 matrix. Each entry in the matrix is a row that corresponds to
#an entire word.
#For example, a row in the matrix would look like:
#   ['byron', 145, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#The matrix first has the word added. A temporary list is created, and a check variable is
#initialized to false. It then iterates through each book in book_counts and retrieves the
#count for that word. If any of the individual counts is not zero, the check variable is set
#to true and the word count is added to the matrix. If all of the individual counts are zero,
#the word is not added to the matrix.
#I'm not sure if this check is necessary after some changes I made to the program, but it was 
#initially necessary so I left it in as insurance.

#The matrix is then passed to the cos_calc() function, which does all of the math required to
#obtain the cosine similarity value.
#cos_calc has nested while loops. The 2 outer while loops are used to iterate through each book in
#the matrix. Setting y=x for each iteration prevents duplicate comparisons. For example,
#this line prevents book 4 from being compared to book 1 after book 1 was already compared
#to book 4.
#The innermost while loop is used to iterate through each word for each book. It keeps a running
#count of the numberator and denomator values for each word. After each word has been iterated through,
#it does some final calculations to compare the two denominator values and calculate the final
#value. It formats to 4 decimal places, adds to a dictionary and sorts in descending order.
#The final step is printing the results by iterating through the sorted list. 


import sys, re, math


#Takes in data and converts everything to lowercase
def toLower(file):
    file = open(file, "r", encoding = "utf-8")
    data = file.read()
    file.close()
    data = data.lower()
    return data


def remove(data):
    #Removes all non-word characters except for spaces. This is my way to
    #remove punctuation
    data = re.sub("[^\w\s]", "", data)
    #The regex above doesn't remove underscores, so I added this one too
    data = re.sub("_", "", data)
    return data

def count(data, token_min, token_max):
    #Types is all types in the combined text of each book
    types = {}
    #Good_types is a dictionary of all types that satisfy the
    #requirement of being within the range
    good_types = {}
    tokens = 0
    data = data.split()
    #Uses a dictionary to find the total type count, because
    #dictionaries do not allow duplicates
    for word in data:
        types[word] = int(0)
    #This counts the total number of times that each type occurs.
    #These numbers will then be summed to get the token count
    for word in data:
        types[word] += 1
    #This filters out the types that do not meet the range requirements
    for word in types:
        if ((types.get(word) > int(token_min))
            and
            (types.get(word) < int(token_max))):
            good_types[word] = types.get(word)
    types = len(good_types)
    #The following for loop counts the number of times each type occurs
    #in order to get the total token count
    for word in good_types:
        tokens += good_types.get(word)
    print("tokens = " + str(tokens) + ", types = " + str(types) + ", lower = " +
          str(token_min) + ", upper = " + str(token_max))
    return good_types


#This function creates a dictionary of types for each specific book that's input
#It works basically the same way as the count function, without the filtering
#since it has already been done. 
def book_dict(data, token_min, token_max):
    types = {}
    good_types = {}
    data = data.split()
    for word in data:
        types[word] = int(0)
    for word in data:
        types[word] += 1
    return types


#Creates a term by document co-occurrence matrix
#The following are examples of what the matrix looks like when a row is printed:
#   ['works', 65, 0, 0, 0, 29, 7, 0, 0, 0, 8]
#   ['lord', 99, 9, 0, 22, 111, 32, 9, 0, 0, 40]
#   ['byron', 145, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#The first is the word that's being counted, and the numbers correspond
#to each book in the order that they were entered on the command prompt.
#The first line of the matrix has the labels and looks like this:
#   ['Word', '10byron.txt', '1crime.txt', '2war.txt', '3tale2.txt', '4passages.txt',
#   '5donq.txt', '6pride.txt', '7emma.txt', '8donqesp.txt', '9holmes.txt']
def matrix_create(good_types, book_counts, texts):
    matrix = [[]]
    matrix[0].append("Word")
    for word in texts:
        matrix[0].append(word)
    for word in good_types:
        temp = []
        check = False
        temp.append(word)
        for book in book_counts:
            if(book.get(word) == None):
                temp.append(0)
            else:
                temp.append(book.get(word))
                check = True
        #This prevents adding words if the numbers are all 0
        if check == True:
            matrix.append(temp)
    return matrix
    
def cos_calc(matrix):
    answers = {}
    x = 1
    while x <= len(matrix[0]):
        y = x
        while y <= len(matrix[0]) - 1:
            numerator = 0
            denom1 = 0
            denom2 = 0
            denom = 0
            word = 1
            while word < len(matrix) - 1:
                #The following is just the cosine calculation for each relation
                numerator += (int(matrix[word][x]) * int(matrix[word][y]))
                denom1 += (int(matrix[word][x]) * int(matrix[word][x]))
                denom2 += (int(matrix[word][y])* int(matrix[word][y]))
                word += 1
            denom = (math.sqrt(denom1) * math.sqrt(denom2))
            cos = numerator / denom
            
            #Formats the cosign value to 4 decimal places and adds
            #to a dictionary
            answers[matrix[0][x], matrix[0][y]] = str("%.4f" % cos)
            
            #This is the sorting algorithm I've used in previous assignments that I got
            #from Stack Overflow
            sorted_answers = sorted(answers.items(), key = lambda key:key[1], reverse = True)
            y += 1
        x += 1
    for each in sorted_answers:
        print(str(each[0][0]) + " " + str(each[0][1]) + " " + str(each[1]))
    
   
def main(token_min, token_max, texts):
    total_text = ""
    books = []
    book_counts = []
    for book in texts:
        data = toLower(book)
        data = remove(data)
        books.append(data)
    for book in books:
        total_text += book
    good_types = count(total_text, token_min, token_max)
    for book in books:
        book_counts.append(book_dict(book, token_min, token_max))
    matrix = matrix_create(good_types, book_counts, texts)
    cos_calc(matrix)
    

if __name__ == '__main__':
    texts = []
    token_min = sys.argv[1]
    token_max = sys.argv[2]
    for x in sys.argv[3:]:
        texts.append(x)
    main(token_min, token_max, texts)
