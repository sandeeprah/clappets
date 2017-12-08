from clappets import mongo


def getProjectTitle(projectID):
    try:
        projects = mongo.db["projects"]
        project = projects.find_one({"_id": projectID})
        name = project['title']
    except:
        name = ""
        raise
    return name
