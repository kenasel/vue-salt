# -*- conding: utf-8 -*-
import requests
requests.packages.urllib3.disable_warnings()

class SaltApi(object):
    def __init__(self, username, password, url):
        self.url = url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.post(self.url + "/login", verify=False, json={
        'username': username,
        'password': password,
        'eauth': 'pam',
        })

    def salt_logout(self):
        res = self.session.post(self.url + "/logout", verify=False)
        return res,res.json()


    def salt_minions_get(self, mid):
        res = self.session.get(self.url + "/minions/" + mid, verify=False)
        return res.json()

    def salt_minions_post(self, tgt, fun):
        res = self.session.post(self.url + "/minions/", verify=False, json={
            "tgt": tgt, 
            "fun": fun
        })
        return res.json()['return'][0]['jid']
    
    def salt_jobs(self, jid):
        res = self.session.get(self.url + "/jobs/" + jid, verify=False)
        return res.json()

    def salt_run(self, tgt, fun):
        res = self.session.post(self.url + "/run/" , verify=False, json={
            #"client": "ssh",
            "client": "local",
            "tgt": tgt, 
            "fun": fun,
            "username": self.username,
            "password": self.password,
            "eauth": 'pam'
        })
        return res.json()
          
    def salt_events(self):
        res = self.session.get(self.url + "/events/", verify=False)
        return res.json()

    def salt_hook(self):
        res = self.session.post(self.url + "/hook/", verify=False, json = {
            "foo": "Foo!", 
            "bar": "Bar!"
        })
        return res.json()

    def salt_keys_get(self,mid=None):
        if mid:
            res = self.session.get(f"{self.url}/keys/{mid}", verify=False)
        else:
            res = self.session.get(f"{self.url}/keys/", verify=False)
        return res.json()
    
    def salt_keys_post(self, mid):
        res = self.session.post(self.url + "/keys/", verify=False, json = {
            "mid": mid,
            "username": self.username,
            "password": self.password,
            "eauth": 'pam'
        })
        return res.json()
        
    def salt_ws(self):
        pass

    def salt_stats(self):
        res = self.session.get(self.url + "/stats/", verify=False)
        return res.json()


class SaltManage(object):
    def __init__(self, url, username, password):
        self.url = url
        self._username = username
        self._password = password
        self.get_token()

    def get_token(self, eauth='pam', ):
        token = requests.post(self.url + "/login/", verify=False, json={
            'username': self._username, 
            'password': self._password, 
            'eauth': eauth
            })
        if token.status_code != 200:
            raise Exception(token.status_code)
        self.token = token.json()['return'][0]['token']

    def post(self, json_data=None):
        headers = {'X-Auth-Token': self.token, 'Accept': 'application/json'}
        res = requests.post(self.url, json=json_data, headers=headers, verify=False)
        return res.json()

    def get(self, json_data=None, headers=None):
        headers = {'X-Auth-Token': self.token, 'Accept': 'application/json'}
        res = requests.get(self.url, json=json_data, headers=headers, verify=False)
        return res.json()

    def get_all_key(self):
        json_data = {'client': 'wheel', 'fun': 'key.list_all'}
        res = self.post(json_data=json_data)['return'][0]['data']['return']
        rejected, denied, pre, minions = res['minions_rejected'], res['minions_denied'], res['minions_pre'], res['minions']
        return minions, rejected, denied, pre

    def accept_key(self, mid):
        json_data = {'client': 'wheel', 'fun': 'key.accept', 'match': mid}
        res = self.post(json_data=json_data)
        return res['return'][0]['data']['success']

    def delete_key(self, mid):
        json_data = {'client': 'wheel', 'fun': 'key.delete', 'match': mid}
        res = self.post(json_data=json_data)
        return res['return'][0]['data']['success']

    def module_execute(self, tgt, fun, arg=None):
        json_data = {'client': 'local', 'tgt': tgt, 'fun': fun, }
        if arg:
            json_data.update({'arg': arg})
        res = self.post(json_data=json_data)
        return res['return']

    def group_module_execute(self, tgt, fun, arg=None):
        json_data = {'client': 'local', 'tgt': tgt, 'fun': fun, 'expr_form': 'nodegroup'}
        if arg:
            json_data.update({'arg': arg})
        res = self.post(json_data=json_data)
        return res['return']

    def sls_async(self, tgt, arg):
        json_data = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        res = self.post(json_data=json_data)
        return res['return']

    def group_sls_async(self, tgt, arg):
        json_data = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        res = self.post(json_data=json_data)
        return res['return']

    def host_pillar(self, tgt, arg, **kwargs):
        kwargs = {'pillar': kwargs['kwargs']}
        json_data = {"client": "local", "tgt": tgt, "fun": "state.sls", "arg": arg, "kwarg": kwargs}
        res = self.post(json_data=json_data)
        return res['return']

    def group_pillar(self, tgt, arg, **kwargs):
        kwargs = {'pillar': kwargs['kwargs']}
        json_data = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup', 'kwarg': kwargs}
        res = self.post(json_data=json_data)
        return res['return']

    def get_grains(self, mid):
        data={'client': 'local','tgt': mid, 'fun': 'grains.item','arg':['fqdn', 'virtual', 'num_cpus','os',]}
        res = self.post(json_data=data)
        return res['return']
    
    def jobs_all_list(self):
        json_data = {"client": "runner", "fun": "jobs.list_jobs"}
        res = self.post(json_data=json_data)
        return res['return']
    
    def salt_running_jobs(self):
        json_data = {'client': 'runner', 'fun': 'jobs.active'}
        res = self.post(json_data=json_data)
        return res['return']
        
    def jobs_jid_result(self, jid):
        json_data = {"client": "runner", "fun": "jobs.lookup_jid", "jid": jid}
        res = self.post(json_data=json_data)
        return res['return']
     



def manage_test():
    url = ''
    username, password = 'kenasel','kenasel'
    man = SaltManage(url, username, password)
    #print(man.get_all_key())
    #print(man.module_execute("*", "cmd.run", "uptime"))
    #print(man.remote_execute("*", "status.diskusage"))
    #print(man.jobs_all_list())
    #print(man.jobs_jid_result('20181030164003872815'))
    print(man.get_grains("*"))


if __name__ == '__main__':
    manage_test()
    # url = ''
    # username, password = 'kenasel','kenasel'
    # salt = SaltApi(username,password,url)
    #print(salt.salt_logout())
    #print(salt.salt_minions_get("*"))
    #print(salt.salt_minions_post("*", "status.diskusage"))
    #print(salt.salt_jobs("20181030164331632821"))
    #print(salt.salt_run("*","test.ping"))
    #print(salt.salt_events())
    #print(salt.salt_hook())
    #print(salt.salt_ws())
    #print(salt.salt_stats())
    #print(salt.test("*", 'grains.item'))
