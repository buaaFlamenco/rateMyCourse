from unittest import skipIf, skip
import json

from django.test import TestCase, Client, tag
import django.db

from rateMyCourse.models import User, Teacher, Course, Comment, MakeComment, TeachCourse

from db_checker import DBChecker
from test_logger import log


class BackBasicTestCase(TestCase):
    # Prepare the database by using fixture.
    fixtures = ["fixture.json"]


class BackPostCheckDBTC(BackBasicTestCase):
    def setUp(self):
        self.checker = DBChecker(
            django.db.connection,
            "rateMyCourse",
            self
        )

    def postContainTest(self, url, form, text=""):
        # Send Request
        #   Specify the interface to test by assigning the url.
        #   With the form attached.
        response = self.client.post(url, form)
                    
        # Response Check
        #   Check the status code(default 200) 
        #   and whether contain text in body.
        try:
            body = json.loads(response.content)
            self.assertEqual(body["status"], 1)
            self.assertContains(response, text)
        except Exception as e:
            log.error("Error when checking response. The response is %s", response.content)
            raise e

    def postAndCheck(self, url, model_name, prop_dict, text=""):
        # Send Request & Response Check
        self.postContainTest(url, prop_dict, text=text)
        # Side Effect Check
        #   Check whether the side effects take place.
        self.checker.check(model_name, prop_dict)

    def autoTest(self, testcase_file):
        # Read Testcases from json
        testcases = None
        with open(testcase_file, "r", encoding="utf-8") as fd:
            testcases = json.load(fd)

        for case in testcases:
            # Load json data
            case_name = case[0]
            url = case[1]
            model_name = case[2]
            prop_dict = case[3]
            text = ""
            if len(case) > 4:
                text = case[4]

            # Do Test
            with self.subTest(case_name=case_name):
                try:
                    self.postAndCheck(
                        url,
                        model_name,
                        prop_dict,
                        text
                    )
                except Exception as e:
                    log.error("(%s) Test Fail.", case_name)
                    raise e


class BackGetCheckBodyTC(BackBasicTestCase):
    def getJsonBody(self, url, form=None):
        response = self.client.get(url, form)
        try:
            self.assertEqual(response.status_code, 200)
            body = json.loads(response.content)
            self.assertEqual(body["status"], 1)
            retlist = body["body"]
        except Exception as e:
            log.error("Error when checking response. The response is %s", response.content)
            raise e
        return (body, retlist)

    def checkDictEntry(self, dicta, dictb):
        for key, value in dictb.items():
            if not key in dicta.keys():
                return False
            if dicta[key] != dictb[key]:
                return False
        return True

    def assertDictEntry(self, dicta, dictb):
        for key, value in dictb.items():
            self.assertTrue(key in dicta.keys())
            self.assertEquals(dicta[key], dictb[key])

    def getAndCheck(self, url, prop_dict, length, exp_list=[]):
        body, retlist = self.getJsonBody(url, prop_dict)
        self.assertDictEntry(
            body,
            {
                "length": length
            }
        )
        for i in range(len(exp_list)):
            exist = False
            for j in range(len(retlist)):
                if self.checkDictEntry(retlist[j], exp_list[i]):
                    exist = True
                    break
            self.assertTrue(exist)


    def autoTest(self, testcase_file):
        # Read Testcases from json
        testcases = None
        with open(testcase_file, "r", encoding="utf-8") as fd:
            testcases = json.load(fd)

        for case in testcases:
            # Load json data
            case_name = case[0]
            url = case[1]
            prop_dict = case[2]
            length = case[3]
            exp_list = []
            if len(case) > 4:
                exp_list = case[4]

            # Do Test
            with self.subTest(case_name=case_name):
                try:
                    self.getAndCheck(
                        url,
                        prop_dict,
                        length,
                        exp_list
                    )
                except Exception as e:
                    log.error("(%s) Test Fail. [%s]", case_name, str(e))
                    raise e

# Test Cases
@tag("back")
class BackCreateTC(BackPostCheckDBTC):
    @tag("auto")
    def test_auto(self):
        self.autoTest("test/test_create.pd.json")

    @tag("foreign")
    def test_add_teach_course(self):
        self.postContainTest(
            "/addTeachCourse/",
            {
                "teacher_list": ["rbq"],
                "course": "rbq",
                "department": "rbq"
            }
        )
        self.assertTrue(
            TeachCourse.objects.filter(
                teachers__name="rbq",
                course__name="rbq",
                department__name="rbq"
            ).exists()
        )

    @tag("foreign")
    def test_make_comment(self):
        self.postContainTest(
            "/makeComment/",
            {
                "username": "hong",
                "course_ID": "0",
                "content": "hong test comment"
            }
        )
        self.assertTrue(
            Comment.objects.filter(
                content="hong test comment",
            ).exists()
        )
        self.assertTrue(
            MakeComment.objects.filter(
                user__username="hong",
                course__course_ID="0",
                comment__content="hong test comment"
            ).exists()
        )


@tag("back")
class BackUpdateTC(BackPostCheckDBTC):
    @tag("auto")
    def test_auto(self):
        self.autoTest("test/test_update.pd.json")

    @tag("foreign")
    def test_edit_comment(self):
        comment_ID = Comment.objects.get(content="rbq").id
        self.postContainTest(
            "/editComment/",
            {
                "comment_ID": comment_ID,
                "content": "changed"
            }
        )
        self.assertTrue(
            MakeComment.objects.filter(
                comment__content="changed"
            ).exists()
        )


@tag("back")
class BackSearchTC(BackGetCheckBodyTC):
    @tag("auto")
    def test_auto(self):
        self.autoTest("test/test_search.gb.json")


@tag("back")
class BackAuthTC(BackBasicTestCase):
    def test_sign_in(self):
        pass