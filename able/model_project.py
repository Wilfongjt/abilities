import os
import json
import able
#from able import NormalString,Stack, JSONString, Level, IsArray, IsObject


#### The Idea

## Reference tree branch with github stack
##
## eg markdown
##
##```
### A
##1. B
##    1. C
##    1. D
##1. E
##    1. F
##```
##
## Convert markdown line into github stack
##
##| line | level (lv) | size (sz) | (sz-lv)+1 | ss         | stack   |
##|----|----|----|-----------|------------|---------|
##| "# A"     | 1  | 0  | 0  |  pop(0), push(A)  |  [A]
##| "1. B"    | 2  | 1  | 0  |  pop(0), push(B)  |  [A,B]
##| "----1. C"  | 3  | 2  | 0  |  pop(0), push(C)  |  [A,B,C]
##| "----1. D"  | 3  | 3  | 1  |  pop(1), push(D)  |  [A,B,D]
##| "1. E"    | 2  | 3  | 2  |  pop(2), push(E)  |  [A,E]
##| "----1. F"  | 3  | 2  | 0  |  pop(0), push(F)  |  [A,E,F]
##
## "-" is github placeholder for github space

class ProjectModel(dict):
    ##
    ##__ProjectModel__
    ##
    ## Dictionary that models github project
    ##
    ##* load dictionary from github markdown document


    def __init__(self, md_string):
        #contents = {}
        stack = able.stack.Stack()

        line_list = md_string.split('\n')
        for ln in line_list:

            if ln.startswith('#'):
                stack.pop(count=(stack.size() - able.level.Level(ln)) + 1)
                stack.push(ln.replace('# ', '').replace('#', '').replace(':', ''))
                stack.update(self, {})

            elif ln.startswith('1.'):
                ln = ln.replace('1. ', '')
                ln = able.string_normal.NormalString(ln)
                s = ln.split(' : ', maxsplit=1)

                stack.push(s[0])
                if able.is_array.IsArray(s[1]):
                    s[1] = json.loads(able.string_json.JSONString(s[1]).replace('\'', '"'))
                elif able.is_object.IsObject(s[1]):
                    s[1] = json.loads(able.string_json.JSONString(s[1]).replace('\'', '"'))
                stack.update(self, s[1])
                stack.pop()

def main():
    from pprint import pprint
    from able import StringReader
    from able import TemplateString

    # handle default with github template
    print('cwd                ', os.getcwd())
    md_project_string = str(os.getcwd()).replace('able','able/template/hapi/model/latest').replace('bin','able/template/hapi/model/latest')
    print('A md_project_string',md_project_string)

    md_project_string = '{}/model.project.md.C---.tmpl'.format(md_project_string)
    print('B md_project_string',md_project_string)

    md_project_string = StringReader(md_project_string)
    print('C md_project_string',md_project_string)

    md_project_string += StringReader('{}/model.resource.*.md.C---.tmpl'.format(str(os.getcwd()).replace('able','able/template/hapi/model/latest')))
    print('D md_project_string',md_project_string)

    #print('md_project_string',md_project_string)
    nv_list = [{'name':'<<WS_ORGANIZATION>>', 'value':'testapi-org'},
               {'name':'<<GH_PROJECT>>', 'value':'able'}]
    md_project_string = TemplateString(md_project_string, nv_list)
    print('E md_project_string',md_project_string)
    # handle template values
    #md_project = str(os.getcwd()).replace('able','source/data')
    #md_project = '{}/model.project.md'.format(md_project)
    #print('md_project', md_project)
    #md_string = StringReader(md_project)
    assert (ProjectModel('') == {})

    print(ProjectModel(md_project_string))

    assert(ProjectModel(md_project_string))
    assert(type(ProjectModel(md_project_string) is dict))
    assert ('project' in ProjectModel(md_project_string))
    assert ('audience' in ProjectModel(md_project_string)['project'])
    assert ('claim' in ProjectModel(md_project_string)['project'])
    assert ('issuer' in ProjectModel(md_project_string)['project'])
    assert ('name' in ProjectModel(md_project_string)['project'])
    assert ('owner' in ProjectModel(md_project_string)['project'])
    assert ('resource' in ProjectModel(md_project_string)['project'])
    assert ('subject' in ProjectModel(md_project_string)['project'])

    #print('ProjectModel',ProjectModel(md_project_string))
    pprint(ProjectModel(md_project_string))

if __name__ == "__main__":
    # execute as docker
    main()
