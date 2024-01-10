from console_gfx import ConsoleGfx
#A function to print the menu
def main():

       print('''\nRLE Menu
--------
0. Exit
1. Load File
2. Load Test Image
3. Read RLE String
4. Read RLE Hex String
5. Read Data Hex String
6. Display Image
7. Display RLE String
8. Display Hex RLE Data
9. Display Hex Flat Data

Select a Menu Option:''')

#Looks through the list and changes it to a string that checks for hex string values
def to_hex_string(data):
    Result = ''
    for num in data:
        #Char_hex converts the numbers that are above 10 and below 15 into letters
        Result += char_hex(num)
    return Result
#Char_hex converts the numbers that are above 10 and below 15 into letters
def char_hex(data):
    if data == 10:
        return 'a'
    elif data == 11:
        return 'b'
    elif data == 12:
        return 'c'
    elif data == 13:
        return 'd'
    elif data == 14:
        return 'e'
    elif data == 15:
        return 'f'
    else:
        return str(data)

def count_runs(flat_data):
    runs = 0
    uniqueNumsList = []
    for myNum in flat_data:
        #Checks to see if a number had been repeated and if it hasnt it adds it
        if myNum not in uniqueNumsList:
            uniqueNumsList.append(myNum)
    for i in range(len(flat_data)):
        #Checks to see if the value is the same as the one in front of it and if it does it
        #Adds another run
        if flat_data[i] != flat_data[i-1]:
            runs +=1
    for num in uniqueNumsList:
        #The flat_data.count > mulitples of 15 is to add runs if the number is over 15
        #runs long
        if int(flat_data.count(num)) > 60:
            runs +=4
        elif int(flat_data.count(num)) > 45:
            runs += 3
        elif int(flat_data.count(num)) > 30:
            runs +=2
        elif int(flat_data.count(num)) > 15:
            runs +=1
    return runs

def encode_rle(flat_data):
    result = []
    count = 0
    #To account for value 0
    previous_data = -1
    #Loops through the list
    for num in flat_data:
        #Skips the first iteration
        if num != previous_data and previous_data != -1:
            #Checks for strings longer than 15 and appends it as many times needed
            while count>15:
                result.append(15)
                result.append(previous_data)
                count -=15
            #Checks if the string is exactly 15 or 30 of the same numbers and if its not it appends what it its supposed to be
            #So that it doesnt keep appending if the count is already 0
            if count != 0:
                result.append(count)
                count = 0
                result.append(previous_data)
        #Makes previous data check the last data
        previous_data = num
        #Adds to the count
        count += 1
    #The last number in the list doesnt get added without this
    while count > 15:
        result.append(15)
        result.append(previous_data)
        count -= 15
    if count != 0:
        result.append(count)
        result.append(previous_data)
    return result


def get_decoded_length(rle_data):
    sum = 0
    for i in range(len(rle_data)):
        #This checks even list numbers because those numbers are the one that has the run
        #length and it adds them together to create sum
        if i % 2 == 0:
            sum += rle_data[i]
    return sum

def decode_rle(rle_data):
    sum = 0
    Result = []
    #Counts by even numbers to get it odds and evens formatted in rle_data[i] and rle_data[i+1]
    for i in range(0,len(rle_data),2):
        #The count is the even number in list because that is the one that has run length
        count = rle_data[i]
        #Num is the number that the count dictates too
        num = rle_data[i+1]
        times = 0
        #Adds a the number for count amount of times
        while times < count:
            Result.append(num)
            times += 1
    return Result

# Converts the number from hex values a-f into digits
def decode_string_to_data(data_string):
    data_string = data_string.lower()
    if data_string == 'f':
        return 15
    if data_string == 'e':
        return 14
    if data_string == 'd':
        return 13
    if data_string == 'c':
        return 12
    if data_string == 'b':
        return 11
    if data_string == 'a':
        return 10
    else:
        return data_string

def string_to_data(data_string):
    result = []
    #looks through each number in the string
    for num in data_string:
        #Adds the value into a list
        result.append(int((decode_string_to_data(num))))
    return result




def to_rle_string(rle_data):
    result = ''
    #looks through even numbers to assigne a value to all odds and evens
    for i in range(0,len(rle_data),2):
        #Assigns digit 1 to even numbers
        digit1 = rle_data[i]
        #Assigns digit 2 to odd numbers
        digit2 = rle_data[i+1]
        #Keeps the even number as is
        result += str(digit1)
        #Turns odd number into the respected a-f hex value and adds a colon
        result += str(char_hex(digit2)) + ':'
    #doesnt return the last colon
    result = result[:-1]
    return result



def string_to_rle(rle_string):
    #Converts capital letters to lowercase ones
    rle_string = rle_string.lower()
    #Splits string at the colons into lists
    result = rle_string.split(':')
    result2= []
    #Used to help go through each iteration of char in result
    temp = ''
    for char in result:
        #Checks if the list has 3 letters or if the last digit is a letter
        if len(char) > 2 or char[-1].isalpha():
            # Checks to see if the last number in 2 digit list is a letter and converts it to its value and adds it to the list in order
            if char[-1] == 'a':
                temp = char.replace('a', "")
                result2.append(int(temp))
                result2.append(10)
            elif char[-1]  == 'b':
                temp = char.replace('b', "")
                result2.append(int(temp))
                result2.append(11)

            elif char[-1]  == 'c':
                temp = char.replace('c', "")
                result2.append(int(temp))
                result2.append(12)

            elif char[-1]  == 'd':
                temp = char.replace('d', "")
                result2.append(int(temp))
                result2.append(13)

            elif char[-1]  == 'e':
                temp = char.replace('e', "")
                result2.append(int(temp))
                result2.append(14)

            elif char[-1]  == 'f':
                temp = char.replace('f',"")
                result2.append(int(temp))
                result2.append(15)

            #Adds things like 151 as 15,1
            else:
                result2.append(int(char[0:2]))
                result2.append(int(char[2]))


        else:
            #just adds it as a number incase it is not a letter
            for num in char:
                result2.append(int(num))

    return result2


if __name__ == '__main__':
   image_data = None
   print("Welcome to the RLE image encoder!\n")
   print("Displaying Spectrum Image:")
   ConsoleGfx.display_image(ConsoleGfx.test_rainbow)
   while True:
       main()
       Choice = input()
       if Choice == '1':
           File = input('Enter name of file to load: ')
           image_data = ConsoleGfx.load_file(File)
       elif Choice == '2':
           image_data = ConsoleGfx.test_image
           print('Test image data loaded.')
       elif Choice == '3':
           hexString = input("Enter an RLE string to be decoded: ")
           #Gets image_data ready for displaying image
           image_data = decode_rle(string_to_rle(hexString))
       elif Choice == '4':
           hexString = input("Enter the hex string holding RLE data: ")
           image_data = decode_rle(string_to_data(hexString))
       elif Choice == '5':
            image_data = input("Enter the hex string holding flat data: ")
            image_data = string_to_data(image_data)
       elif Choice == '6':
           print("Displaying image...")
           ConsoleGfx.display_image(image_data)
           print(image_data)
       elif Choice == '7':
           #Undos the decode_rle and shows the data as intended
           print(f"RLE representation: {to_rle_string(encode_rle(image_data))}")
       elif Choice == '8':
           print(f'RLE hex values: {to_hex_string(encode_rle(image_data))}')
       elif Choice == '9':
           #Changes value to flat string
           print("Flat hex values:", (to_hex_string(image_data)))
       elif Choice == '0':
           break
3