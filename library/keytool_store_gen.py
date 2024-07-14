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
        dname=dict(type='str', required=True),
        san=dict(type='str', required=False, default=''),
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
    dname = module.params['dname']
    san = module.params['san']
 
    cmd = [
        keytool_location,
        '-genkey',
        '-keyalg', 'RSA',
        '-keysize', '2048',
        '-alias', alias,
        '-dname', dname,
        '-keystore', keystore_location,
        '-storepass', keystore_password
    ]
 
    if storetype:
        cmd.extend(['-storetype', storetype.upper()])
 
    if san:
        cmd.extend(['-ext', f'san={san}'])
 
    try:
        completed_process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_str = completed_process.stdout.decode('utf-8').strip() if completed_process.stdout else ''
        stderr_str = completed_process.stderr.decode('utf-8').strip() if completed_process.stderr else ''
       
        if completed_process.returncode == 0:
            result['changed'] = True
            result['message'] = 'Key generated successfully'
        else:
            module.fail_json(msg=f"Keytool command failed with error code {completed_process.returncode}. stderr: {stderr_str}", **result)
    except subprocess.CalledProcessError as e:
        module.fail_json(msg=f"Keytool command failed: {e.stderr}", **result)
 
    module.exit_json(**result)
 
def main():
    run_module()
 
if __name__ == '__main__':
    main()