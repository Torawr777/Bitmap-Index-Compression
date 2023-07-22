import math
import os.path

# 'input_file' is a file used to create the bitmap index
# 'output_path' is the destination directory for the outputted bitmap file
# 'sorted' is a boolean value that specifies whether the data will be sorted.
def create_index(input_file, output_path, sorted):

     # Use current working directory if no output_path given
    if output_path is None:
        output_path = os.getcwd()

    # Split the directory/path, then take the last element 
    inputFileName = input_file.split('/')[-1]
    
    # Read data in input file 
    with open(input_file, 'r') as f:
        data = f.readlines()

        # If sorted is true, sort the data file lexicographically 
        if sorted == True:
            data.sort()
            inputFileName = inputFileName + "_sorted"

    
    fullDir = os.path.join(output_path, inputFileName)

    # Open the output file
    outputFile = open(fullDir, "w")

    # Initialize bitmap index with 0s
    bitmap = [0] * 16

    # Populate bitmap index
    for data in data:
        row = data.split(',')
        animal = row[0]
        age = row[1]
        adopted = row[2]

        # Set the bit for animal type (0-3)
        if animal == "cat":
            bitmap[0] = 1
        elif animal == "dog":
            bitmap[1] = 1
        elif animal == "turtle":
            bitmap[2] = 1
        elif animal == "bird":
            bitmap[3] = 1

        # Set the bit for the age bin (4-13)
        if int(age) == 1:
            bitmap[4] = 1
        else:
            bin = int((int(age) - 1) / 10) + 4
            bitmap[bin] = 1

        # Set the bit for adopted (14-15)
        if adopted == "True\n":
            bitmap[14] = 1
        elif adopted == "False\n":
            bitmap[15] = 1

        # Change bitmap contents to string type
        strConvert = ""
        for num in bitmap:
            strConvert += str(num)

        # Write converted bitmap to file then reset bitmap to prep for next iteration
        outputFile.write(strConvert + '\n')
        bitmap = [0] * 16

    outputFile.close()

# Adds 0s to the left of a binary until size is reached
def fill_bin(bin_str, size):
    # Convert string to int, then format as a binary 
    return format(int(bin_str, 2), f"0{size}b")


# Adds 0s to the right of a literal until size is reached
def fill_lit(segment, size):
    return "".join(segment).ljust(size, "0")

# 'bitmap_index' is the input file to be used in the compression
# 'output_path' is the destination directory for the output compressed version
# 'compression_method' is a string specifying which bitmap compression method to use (ex: WAH)
# 'word_size' is an int specifying the word size to be used
def compress_index(bitmap_index, output_path, compression_method, word_size):

    # Use current working directory if no output_path given
    if output_path is None:
        output_path = os.getcwd()
   
    # Create the output file name
    outputFileName = bitmap_index.split('/')[-1] + "_" + compression_method + "_" + str(word_size)

    fullDir = os.path.join(output_path, outputFileName)

    # Open the output file
    outputFile = open(fullDir, "w")

    # Read the bitmap index into an array
    array = []
    with open(bitmap_index, 'r') as f:
        for line in f:
            array.append(list(line)[:-1])

    # Convert columns to rows
    data = [list(col) for col in (zip(*array))]   
    rows = len(array)
    cols = len(data)

    literals = 0
    runs = 0
    segment_size = word_size - 1
    
    # Result starts with empty strings so we can add compressed things later
    result = ["" for x in range(cols)]
    for col in range(cols):
        n = 0
        
        # Loop through every element of the column
        while n < len(data[col]):
            # Get the segment from the column
            segment = data[col][n:n + segment_size]
            n = n + segment_size

            # At the end of the row, fill in the rest as a literal
            if n >= rows:
                result[col] += "0" + fill_lit(segment, segment_size)
                literals = literals + 1
                continue

            # Determine if it's a literal (contains 1s and 0s)
            if segment.count('1') > 0 and segment.count('0') > 0:
                result[col] += "0" + "".join(segment)
                literals = literals + 1

            # Otherwise it's a run
            else:
                # Amount of bits in the run
                total_bits = segment_size  
                start = n  
                bit = segment[0]  

                # Count the number of bits
                while n < rows and (total_bits / segment_size) <= 2 ** (word_size - 2) - 1 and data[col][n] == bit:
                    total_bits += 1
                    n += 1
                    
                run_count = math.floor(total_bits / segment_size)          
                n = start + (run_count - 1) * segment_size  
                runs += run_count  
                
                # Add the header here
                runComp = "" 
                if bit == "0":  
                    runComp += "10"
                elif bit == "1":
                    runComp += "11"

                # Convert run to binary and extend the left with 0s until proper size
                runComp += fill_bin(bin(run_count)[2:], word_size - 2)

                # Add it to the result
                result[col] += runComp

    # Write output to a file
    for num in result:
        outputFile.write(num + '\n')
        
    print(f"__Compression Results__\nFile: {fullDir}\nRuns: {runs}\nLiterals: {literals}")


#create_index('mine/animals', 'test/dog', True)
#compress_index('my_mine/animals_sorted', '', 'WAH', 64)
