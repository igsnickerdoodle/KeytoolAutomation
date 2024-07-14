#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess
import datetime
 
def run_module():
    module_args = dict(
        keytool_location=dict(type='str', required=True),
        keystore_location=dict(type='str', required=True),
        keystore_password=dict(type='str', required=True, no_log=True),
        storetype=dict(type='str', required=True, choices=['pkcs12', 'pkcs7']),
        alias=dict(type='str', required=True),
        san=dict(type='str', required=False, default=''),
        csr_output_dir=dict(type='str', required=True),
        var_host=dict(type='str', required=True),
        host_var_map=dict(type='dict', required=True)
    )
 
    result = dict(
        changed=False,
        message='',
        csr_file=''
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
    san = module.params['san']
    csr_output_dir = module.params['csr_output_dir']
    var_host = module.params['var_host']
    host_var_map = module.params['host_var_map']
 
    csr_filename = f"{host_var_map[var_host]}_{datetime.datetime.now().strftime('%Y-%m-%d')}.csr"
    csr_filepath = f"{csr_output_dir}/{csr_filename}"
 
    cmd = [
        keytool_location,
        '-certreq',
        '-keystore', keystore_location,
        '-storetype', storetype.upper(),
        '-storepass', keystore_password,
        '-alias', host_var_map[var_host],
        '-file', csr_filepath
    ]
 
    if san:
        cmd.extend(['-ext', f'san="{san}"'])
 
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