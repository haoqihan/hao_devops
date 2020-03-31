import json
import shutil
from collections import namedtuple
from ansible.inventory.host import Host, Group  # 操作单个主机或者主机组信息
from ansible.parsing.dataloader import DataLoader  # 用于读取yaml、json格式的文件
from ansible.vars.manager import VariableManager  # 用于存储各类变量信息
from ansible.inventory.manager import InventoryManager  # 用于导入inventory 文件
from ansible.playbook.play import Play  # 存储执行hosts的角色信息
from ansible.executor.task_queue_manager import TaskQueueManager  # ansible底层用到的任务队列
from ansible.executor.playbook_executor import PlaybookExecutor  # 核心类执行playbook剧本
from ansible.plugins.callback import CallbackBase  # 状态回调，各种成功失败的状态
import ansible.constants as C
from ansible import context
from optparse import Values
from ansible.utils.sentinel import Sentinel


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleApi(object):
    def __init__(self):
        self.options = {'verbosity': 0, 'ask_pass': False, 'private_key_file': None, 'remote_user': None,
                        'connection': 'smart', 'timeout': 10, 'ssh_common_args': '', 'sftp_extra_args': '',
                        'scp_extra_args': '', 'ssh_extra_args': '', 'force_handlers': False, 'flush_cache': None,
                        'become': False, 'become_method': 'sudo', 'become_user': None, 'become_ask_pass': False,
                        'tags': ['all'], 'skip_tags': [], 'check': False, 'syntax': None, 'diff': False,
                        'inventory': './test_hosts',
                        'listhosts': None, 'subset': None, 'extra_vars': [], 'ask_vault_pass': False,
                        'vault_password_files': [], 'vault_ids': [], 'forks': 5, 'module_path': None, 'listtasks': None,
                        'listtags': None, 'step': None, 'start_at_task': None, 'args': ['fake']}
        self.ops = Values(self.options)
        self.loader = DataLoader()
        self.passwords = dict()
        self.results_callback = ResultCallback()
        self.inventory = InventoryManager(loader=self.loader, sources=[self.options['inventory']])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        context._init_global_context(self.ops)

    def runansible(self, host_list, task_list):

        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=task_list
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                # options=self.ops,
                passwords=self.passwords,
                stdout_callback=self.results_callback,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
                # shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def playbookrun(self, playbook_path):

        # self.variable_manager.extra_vars = {'customer': 'test', 'disabled': 'yes'}
        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, passwords=self.passwords)
        playbook._tqm._stdout_callback = self.results_callback
        playbook.run()

        rest = self._callback()
        print(rest)

        return

    def _callback(self):
        results_raw = {}
        results_raw['success'] = {}
        results_raw['failed'] = {}
        results_raw['unreachable'] = {}
        for host, result in self.results_callback.host_ok.items():
            results_raw['success'][host] = json.dumps(result._result)

        for host, result in self.results_callback.host_failed.items():
            results_raw['failed'][host] = result._result

        for host, result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result

        return results_raw


if __name__ == "__main__":
    a = AnsibleApi()
    host_list = ['106.13.54.147']
    tasks_list = [
        dict(action=dict(module='command', args='touch xxxx1')),
        # dict(action=dict(module='shell', args='python sleep.py')),
        # dict(action=dict(module='synchronize', args='src=/home/op/test dest=/home/op/ delete=yes')),
    ]
    # a.runansible(host_list, tasks_list)
    a.playbookrun(playbook_path=['./test.yml'])

    # loader = DataLoader()
    # inventory = InventoryManager(loader,['./test_hosts'])
    # variable_manager = VariableManager(loader,inventory)
    # print(variable_manager.get_vars())
