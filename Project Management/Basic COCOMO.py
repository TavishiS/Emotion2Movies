import math
def findTypeOfProject(kloc):
    projectType=""
    if kloc>0:
        if kloc<2:
            projectType="Small project"
        if kloc>=2 and kloc<=50:
            projectType="Organic"
        elif kloc>50 and kloc<=300:
            projectType="Semi-detached"
        elif kloc>300:
            projectType="Embedded"

    return projectType


def findDetails(projectType):
    details = {}

    if projectType == "Organic":

        fineDetails = {"complexity":"Low",
        "teamExperience":"Highly experienced",
        "env":"Flexible, fewer constraints",
        "a":2.4, "b":1.05, "c":2.5, "d":0.38}        


    elif projectType == "Semi-detached":

        fineDetails = {"complexity" : "Medium",
        "teamExperience" : "Some experienced, some inexperienced",
        "env":"Somewhat flexible, moderate constraints",
        "a":3.0, "b":1.12, "c":2.5, "d":0.35}

        details.update({projectType: fineDetails})


    elif projectType == "Embedded":
        
        fineDetails = {"complexity" : "High",
        "teamExperience" : "Mixed, includes experts",
        "env" : "Highly rigorous, strict requirements",
        "a":3.6, "b":1.20, "c":2.5, "d":0.32}


    else:
        print("Invalid Project Type")

    details.update({projectType: fineDetails})
    return details


def findEquation(kloc, projectType):
    if projectType == "Small project":
        return 0, 0, 1, "Very Low", "Not applicable", "Minimal constraints"
    
    details=findDetails(projectType)

    values = details[projectType]

    a = values["a"]
    b = values["b"]
    c = values["c"]
    d = values["d"]

    complexity, teamExperience, env = values["complexity"], values["teamExperience"], values["env"]

    effort = a * pow(kloc, b)

    time = c * pow(effort, d)

    persons = effort/time

    return effort, time, math.ceil(persons), complexity, teamExperience, env


def measureComplexity(program):
    with open(program, "r") as f:
        lines = len(f.readlines())
    
    kloc=lines/1000.0

    projectType=findTypeOfProject(kloc)
    valid=True
    if len(projectType)>0:
        print("Project Type = ", projectType)

    else:
        print("Project type could not be decided :(")
        valid=False

    if valid:
        # if projectType == "Small Project":
        #     print("This project is too small for COCOMO estimation !!")
        # else:        
            effort, time, persons, complexity, teamExperience, env = findEquation(kloc, projectType)
            print("kLOC = ", kloc)
            print("Complexity of project = ", complexity)
            print("Team experience = ", teamExperience)
            print("Environment = ", env)
            print("Effort = ", effort, " Person-Months")
            print("Time = ", time, " months")
            print("Persons required = ", persons)
    else:
        print("Can't make calculations regarding project complexity !!")


if __name__ == "__main__":
    measureComplexity("add.py") # write the name of the desired file here



    




