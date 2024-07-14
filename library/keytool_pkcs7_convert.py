#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess
 
def run_module():
    module_args = dict(
        keytool_location=dict(type='str', required=True),
        src_keystore=dict(type='str', required=True),
        src_storepass=dict(type='str', required=True, no_log=True),
        dest_keystore=dict(type='str', required=True),
        dest_storepass=dict(type='str', required=True, no_log=True),
        dest_storetype=dict(type='str', required=True, choices=['pkcs12'])
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
    src_keystore = module.params['src_keystore']
    src_storepass = module.params['src_storepass']
    dest_keystore = module.params['dest_keystore']
    dest_storepass = module.params['dest_storepass']
    dest_storetype = module.params['dest_storetype']
 
    cmd = [
        keytool_location,
        '-importkeystore',
        '-srckeystore', src_keystore,
        '-srcstorepass', src_storepass,
        '-destkeystore', dest_keystore,
        '-deststoretype', dest_storetype.upper(),
        '-deststorepass', dest_storepass
    ]
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