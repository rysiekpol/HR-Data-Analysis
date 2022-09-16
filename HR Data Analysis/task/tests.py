import ast
from hstest.stage_test import List
from hstest import *

answer = {('Work_accident', 'mean'): {0: 0.18, 1: 0.04},
          ('last_evaluation', 'mean'): {0: 0.72, 1: 0.72},
          ('last_evaluation', 'std'): {0: 0.16, 1: 0.2},
          ('number_project', 'count_bigger_5'): {0: 207, 1: 339},
          ('number_project', 'median'): {0: 4.0, 1: 4.0},
          ('time_spend_company', 'mean'): {0: 3.4, 1: 3.91},
          ('time_spend_company', 'median'): {0: 3.0, 1: 4.0}}


class AggTest(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase(time_limit=15000)]

    def check(self, reply: str, attach):

        reply = reply.strip()

        if len(reply) == 0:
            return CheckResult.wrong("No output was printed")

        if reply.count('{') < 1 or reply.count('}') < 1:
            return CheckResult.wrong('Print output as a dictionary')

        index_from = reply.find('{')
        index_to = reply.rfind('}')
        dict_str = reply[index_from: index_to + 1]

        try:
            user_dict = ast.literal_eval(dict_str)
        except Exception as e:
            return CheckResult.wrong(f"Seems that output is in wrong format.\n"
                                     f"Make sure you use only the following Python structures in the output: string, int, float, list, dictionary")

        if not isinstance(user_dict, dict):
            return CheckResult.wrong('Print output as a dictionary')

        if len(answer.keys()) != len(user_dict.keys()):
            return CheckResult.wrong(f'Output should contain {len(answer.keys())} dict elements, found {len(user_dict.keys())}')

        for key in answer.keys():
            if key not in user_dict.keys():
                return CheckResult.wrong(f'Output should contain \"{key}\" as a key')

        for key in user_dict.keys():
            curr_user_dict = user_dict[key]
            curr_answer_dict = answer[key]
            for key_curr in curr_user_dict.keys():
                if key_curr not in curr_answer_dict.keys():
                    return CheckResult.wrong(f'Output should not contain \"{key_curr}\" as a key for the employement status')
                curr_user_val = curr_user_dict[key_curr]
                curr_answer_val = curr_answer_dict[key_curr]
                error = abs(curr_answer_val * 0.02)
                if not curr_user_val - error < curr_answer_val < curr_user_val + error:
                    return CheckResult.wrong(
                        f'Wrong value of the element with \"{key}\" key with left status \"{key_curr}\"')

        return CheckResult.correct()


if __name__ == '__main__':
    AggTest().run_tests()
