import os

def main():
    print("Hello world!")   

    #out =!python -m site --user-site


    #out2 = listToString(out)

    #filename =  os.path.join(out2, "finailab_install", "jupyter_notebook_config.py")

    #filename2 = filename.replace(os.sep, '/')

    #type(filename2)

    #!jupyter lab --config={filename2}
    !jupyter lab --config=D:/Hub/jupyter_notebook_config.py	

if __name__ == "__main__":
    main()


def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 

