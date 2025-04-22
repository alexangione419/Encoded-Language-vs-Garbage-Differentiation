import re

# function to read data from a file
# returns a list of strings containing atmost 5k words each. 
def prepareAndObfuscateText(filename, flux = False):
    
    result_strings = []

    with open(filename, 'r', encoding='utf-8') as file:
        full_string = "" 

        lineCounter = 0
        for line in file:
            pattern = r'^\s*\d+\s*«?\s*'
            line = re.sub(pattern, '', line)
            line = line.strip()
            
            if (flux):
                # remove the first word from the line if the data is solar flux data
                line = ' '.join(line.split()[1:])
        
            processed_bytes = line.encode('utf-8')
            processed_binary_string = ' '.join(format(byte, '08b') for byte in processed_bytes)
            full_string += processed_binary_string + ' '
            # print(processed_bytes[-1])


            # break up the text into lists of ~2k lines
            if lineCounter >= 1999:
                result_strings.append(full_string)
                lineCounter = 0
                full_string = ""
            else:
                lineCounter += 1
        
    return result_strings

        



# frenchText = prepareAndObfuscateText("./data/solarFluxData.txt", flux=True)
# # function to obfuscate text by encoding it into binary
# def obfuscate(line):

