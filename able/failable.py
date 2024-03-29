import sys

class Failable():
    ##
    ##__Failable__
    ##
    ## Enable github fail flag
    def __init__(self):
        self.failed=False
        self.fail_msg=[]

    def setFail(self, msg):
        ##* set failure and add failed message on request
        self.failed=True
        self.fail_msg.append(msg.replace('\n',' '))
        return self
    def getFailMessages(self):
        ## Return all fail messages
        return self.fail_msg
    def isFail(self):
        return self.failed

    def on_fail_exit(self):
        ##* Provide github hard failure when failed
        if self.failed:
            sys.exit(1)

        return self

def main():
    # setup

    # testapi
    class Example(Failable):
        def __init__(self):
            Failable.__init__(self)
    actual = Example()
    assert (actual.setFail('testapi fail 1').isFail())
    assert (actual.setFail('testapi fail 2').getFailMessages()==['testapi fail 1','testapi fail 2'])


if __name__ == "__main__":
    # execute as docker
    main()