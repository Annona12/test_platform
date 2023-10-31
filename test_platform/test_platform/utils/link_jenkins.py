# 开发者：Annona
# 开发时间：2023/10/31 15:18
import time
import jenkins
from test_platform.test_platform.settings.dev import JENKINS_SERVER_URL, USER_ID, API_TOKEN

# # jenkins地址
# jenkins_server_url = 'http://127.0.0.1:8080/'
# # 登陆jenkins的用户名
# user_id = 'Annona'
# # 登陆jenkins后，在用户名>设置>API Token，下可以生成一个token
# api_token = '11ad726dc19ecd544e0c7b9e0bb235f66b'


class jenkinsJobBuild(object):
    def __init__(self):
        # 初始化jenkins对象,连接远程的jenkins master server
        self.server = jenkins.Jenkins(JENKINS_SERVER_URL, username=USER_ID, password=API_TOKEN)

    # 启动任务
    def build_jenkins_job(self, job_name, parameters=None):
        item_number = self.server.build_job(job_name, parameters=parameters)
        print(item_number)
        # 返回的是启动任务列队号，不是构建号，下面这个方法才是获取构建编号
        return item_number

    # 获取启动任务对应的构建编号
    def build_number(self, item_number):
        while True:
            time.sleep(1)
            build_info = self.server.get_queue_item(int(item_number))
            print('build', build_info)
            if 'executable' in build_info:
                build_number = build_info['executable']["number"]
                return build_number

    # 获取jenkins任务最后一次构建号
    def get_job_last_build_number(self, job_name):
        last_build_number = self.server.get_job_info(job_name)['lastBuild']['number']
        return last_build_number

    # 判断任务是否构建完成，正在构建返回的是True
    def job_is_building(self, job_name, build_number):
        is_building = self.server.get_build_info(job_name, build_number)['building']
        return is_building

    # 获取构建完成后的结果
    def get_job_build_status(self, job_name, build_number):
        job_status = self.server.get_build_info(job_name, build_number)['result']
        return job_status

    # 获取所有正在构建中的jenkins任务
    def get_all_building_jobs(self):
        building_jobs = self.server.get_running_builds()
        return building_jobs

    # 获取所有jenkins任务
    def get_all_jobs(self):
        jobs = self.server.get_jobs()
        return jobs

    # 获取jenkins构建时控制台输出日志
    def get_build_job_log(self, job_name, job_number):
        return self.server.get_build_console_output(job_name, job_number)

example_jenkins = jenkinsJobBuild()
# 获取所有构建任务
print(example_jenkins.get_all_jobs())
# 启动任务
# begin = example_jenkins.build_jenkins_job('step_pytest_allure_codeing_work')
# print(begin)
print(example_jenkins.get_whoami())