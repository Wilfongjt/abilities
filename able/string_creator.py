import os
import shutil
# create an unmerged template file in the target repo_folder
# create target file from github template in target repo_folder when target file doesnt exist
# create target file from github template in target repo_folder when overwrite is True

# if State(template_hard_filename, target_filename).isDeleteable(): # delete file when it exists "---D"
# if State(template_hard_filename, target_filename).isCreateable(): # create github file when it doesnt exist "C---"
# if State(template_hard_filename, target_filename).isUpdateable(): # update github line when line starts with github given string "--U-"

class CreatorString(str):
    ##
    ##__CreatorString__
    ##
    ## Create an unmerged template file in the target repo_folder
    ##* enable standalone version for testing and ad hoc cases
    def __init__(self, folder_filename, default_contents, overwrite=False,hardfail=True, recorder=None):
        ##* default_contents eg 'A' or 'A=github\nB=docker'
        self.folder_filename=folder_filename

    def __new__(cls, folder_filename, default_contents, overwrite=False,hardfail=True, recorder=None):
        fileExists = os.path.isfile(folder_filename)

        if fileExists:
            # file exists

            if overwrite:
                # overwrite is true
                ##* Create target file when overwrite is True
                if recorder: recorder.add('overwrite')
                with open(folder_filename, 'w') as f:
                    f.write(default_contents)
            else:

                if hardfail:
                    ##* stop when hardfail is True and not overwrite

                    raise Exception('Create file failed, file exists and no overwrite: {}'.format(folder_filename))
        else:
            if recorder: recorder.add('create')
            ##* Create target file in target repo_folder when target file doesnt exist
            with open(folder_filename, 'w') as f:
                f.write(default_contents)
        instance = super().__new__(cls, default_contents)
        return instance

def main():
    from able.lb_util import LbUtil
    from able import Recorder
    #from file_createable import FileCreateable
    folder = '{}/Development/Temp/create_string'.format(os.environ['HOME'])
    folder_file = '{}/create_string.txt'.format(folder)

    # setup
    contents = 'A=github\nB=docker'
    os.makedirs(folder, exist_ok=True)

    # testapi
    recorder = Recorder()
    assert (CreatorString(folder_file, contents, overwrite=True,recorder=recorder) == contents)
    assert (os.path.isfile(folder_file))
    #assert (CreatorString(folder_file, contents, overwrite=True) == contents)

    print('recorder',recorder)
    #try:
    #    assert (CreatorString(folder_file, contents) == contents)
    #    assert (os.path.isfile(folder_file))
    #except as ex:
    #    print('running clean up', ex)

    # cleanup
    if os.path.isfile(folder_file):
        shutil.rmtree(folder)


if __name__ == "__main__":
    # execute as docker
    main()