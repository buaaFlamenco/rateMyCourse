# Course information displayed to users & can be editted by user in very beginning
class CourseInfo:

    # Set course name & store it into database.
    # Manipulated by user.
    def setName():
        pass

    # Get course name from database
    def getName():
        pass

    # Set description & store it into database
    # Manipulated by user
    def setDescription():
        pass

    # Get course description from database
    def getDescription():
        pass

    # Set website & store into database
    # Manipulated by user
    def setWebsite():
        pass

    # Get website from database
    def getWebsite():
        pass

    # Set department that course belongs to & store it into database
    # Manipulated by user
    def setDepartment():
        pass

    # Get department that course belongs to
    def getDepartment():
        pass

    # Set school that course belongs to & store it into database
    # Manipulated by user
    def setSchool():
        pass

    # Get school that course belongs to
    def getSchool():
        pass


# User's profile that can be obtained or modified
class UserInfo:

    # Set school that user attends & modify it in database
    # Manipulated by user
    def setSchool():
        pass

    # Get school that user attends
    def getSchool():
        pass

    # Set department that user attends & modify it in database
    # Manipulated by user
    def setDepartment():
        pass

    # Get department that user attends
    def getDepartment():
        pass

    # Set grade that user is in
    # Manipulated by user
    def setGrade():
        pass

    # Get grade that user is in
    def getGrade():
        pass


# Overall rate displayed to users
class OverallRate:

    # Get rate table from database
    def getRateTable():
        pass

    # Get total rate from sectioned rates
    def getTotalRate():
        pass


# One detailed rate displayed to users
class DetailedRate:

    # Get the time that rate was raised
    def getRateTime():
        pass

    # Get the semester the user gives rate was in
    def getSemester():
        pass

    # Get the tags the user provides
    def getTags():
        pass

    # Get the teacher teaching the course that the user attends
    def getTeacher():
        pass

    # Get the user's comment about this course
    def getComment():
        pass

    # Get the sectioned rates the user provides
    def getSectionedRates():
        pass

    # Get the total rate from the calculation of sectioned rates
    def getTotalRate():
        pass

    # Get the count of user that like this rate
    def getLikesCount():
        pass

    # Get the count of user that dislike this rate
    def getDislikesCount():
        pass

    # Get the discussion under this rate
    def getDiscussion():
        pass
