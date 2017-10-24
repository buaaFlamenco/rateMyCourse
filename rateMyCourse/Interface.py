'''
Get CourseInfo list from designated school, or from designated department
'''
def getCourseList(str school = None, str department = None):
    pass

'''
Get CourseInfo via course name from designated department
'''
def getCourse(str school, str department, str courseName):
    pass


# Course information displayed to users & can be editted by user in very beginning
class CourseInfo:

    '''
    Init CourseInfo.
    If course doesn't exist in database, create this course
    '''
    def __init__(self, str school, str department, str courseName):
        pass
    
    '''
    Set course name to newName & store it into database
    Manipulated by user
    '''
    def setName(self, str newName):
        pass

    '''
    Set description & store it into database
    Manipulated by user
    '''
    def setDescription(self, str description):
        pass

    '''
    Set website & store into database
    Manipulated by user
    '''
    def setWebsite(self, str website):
        pass

    '''
    Set department that course belongs to & store it into database
    Manipulated by user
    '''
    def setDepartment(self, str department):
        pass

    '''
    Set school that course belongs to & store it into database
    Manipulated by user
    '''
    def setSchool(self, str school):
        pass


'''
Get UserInfo via username
'''
def getUser(str username):
    pass

# User's profile that can be obtained or modified
class UserInfo:
    '''
    Init UserInfo.
    If user doesn't exist in database, create this course
    '''
    def __init__(self, str username, str school, str department):
        pass
    
    '''
    Set school that user attends & modify it in database
    Manipulated by user
    '''
    def setSchool(self, str school):
        pass

    '''
    Set department that user attends & modify it in database
    Manipulated by user
    '''
    def setDepartment(self, str department):
        pass

    '''
    Set grade that user is in
    Manipulated by user
    '''
    def setGrade(self, str grade):
        pass


'''
Get OverallRate via CourseInfo which is already set up with school, department & course name
'''
def getOverallRate(str CourseInfo):
    pass

# Overall rate displayed to users
class OverallRate:

    '''
    rateTable[] contains all sectioned rates from all rated users, with types of whatever back-end like
    totalRate is the overall rate relying on scores in rateTable[], with type of whatever back-end like
    '''
    def __init__(self, dict rateTable, str totalRate):
        pass


'''
Get an array of detailed rates for one course, with type of DetailedRate
'''
def getDetailedRateList(str course):
    pass

# Detailed rate raised by one user & displayed to other users
class DetailedRate:

    '''
    sectionedRates[] is user's rates in different section in rating criteria
    totalRate is the total rate relying on scores in sectionedRates[]
    comment is what user said about this course
    recordTime is when he rated
    semester refers to the semester he attended this course
    tags[] is a group of tags easy for other users to see the main idea of this rate,
    set up by the rating user, contains tags fewer than 4
    teacher is teacher
    countOfLikes is how many likes this rate get
    countOfDislikes is how many dislikes this rate get
    '''
    def __init__(self, str sectoinedRates[], str totalRate, str comment,
                 str recordTime, str semester, str tags[],
                 str teacher, int countOfLikes, int countOfDislikes):

