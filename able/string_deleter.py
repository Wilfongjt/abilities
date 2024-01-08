import os
import shutil

class DeleterString(str):
    ##__DeleteString__
    ##* Remove a file and return its contents

    def __new__(cls, folder_filename):
        ##* Fail when file doesnt exist
        fileExists = os.path.isfile(folder_filename)
        if not fileExists:
            raise Exception('File Not Found {}'.format(folder_filename))

        with open(folder_filename, 'r') as f:
            contents = f.read()

        # delete file
        os.remove(folder_filename)
        instance = super().__new__(cls, contents)
        return instance

def main():

    folder = '{}/Development/Temp/deleter_string'.format(os.environ['HOME'])
    folder_filename = '{}/deleter.txt'.format(folder)

    # setup
    contents = 'A=a\nB=b'
    os.makedirs(folder, exist_ok=True)

    # create a file to read
    with open(folder_filename, 'w') as f:
        f.write(contents)

    # test
    actual = DeleterString(folder_filename)
    # print('actual', actual.replace('\n',''))
    assert (actual==contents)

    # cleanup
    fileExists = os.path.isfile(folder_filename)
    if fileExists:
        shutil.rmtree(folder)

if __name__ == "__main__":
    # execute as docker
    main()