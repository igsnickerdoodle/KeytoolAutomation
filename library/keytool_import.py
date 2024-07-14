#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import subprocess
 
def run_module():
    module_args = dict(
        keytool_location=dict(type='str', required=True),
        keystore_location=dict(type='str', required=True),
        keystore_password=dict(type='str', required=True, no_log=True),
        storetype=dict(type='str', required=False, choices=['pkcs12', 'pkcs7']),
        alias=dict(type='str', required=True),
        target_file=dict(type='list', elements='dict', required=True),
    )
 
    result = dict(
        changed=False,
        message=''
    )
 
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
 
    keytool_location = module.params['keytool_location']
    keystore_location = module.params['keystore_location']
    keystore_password = module.params['keystore_password']
    storetype = module.params['storetype']
    alias = module.params['alias']
    target_files = module.params['target_file']
 
    for file_info in target_files:
        target_file = file_info['path']
 
        cmd = [
            keytool_location,
            '-import',
            '-trustcacerts',
            '-alias', alias,
            '-file', target_file,
            '-keystore', keystore_location,
            '-storepass', keystore_password,
            '-noprompt',
        ]
 
        if storetype:
            cmd.extend(['-storetype', storetype.upper()])
 
        try:
            completed_process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout_str = completed_process.stdout.decode('utf-8').strip() if completed_process.stdout else ''
            stderr_str = completed_process.stderr.decode('utf-8').strip() if completed_process.stderr else ''
           
            if completed_process.returncode == 0:
                result['changed'] = True
                result['message'] = 'Key Successfully Imported'
            else:
                module.fail_json(msg=f"Keytool command failed with error code {completed_process.returncode}. stderr: {stderr_str}", **result)
        except subprocess.CalledProcessError as e:
            module.fail_json(msg=f"Keytool command failed: {e.stderr}", **result)
 
    module.exit_json(**result)
 
def main():
    run_module()
 
if __name__ == '__main__':
    main()