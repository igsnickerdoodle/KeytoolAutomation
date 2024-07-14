#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import os
 
def run_module():
    module_args = dict(
        src=dict(type='str', required=True),
        dest=dict(type='str', required=True)
    )
 
    result = dict(
        changed=False,
        message=''
    )
 
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
 
    src = module.params['src']
    dest = module.params['dest']
 
    if not os.path.exists(src):
        module.fail_json(msg='Source file not found', **result)
 
    if not os.path.exists(dest):
        os.makedirs(dest)
 
    counter = 0
 
    try:
        with open(src, 'r') as infile:
            lines = infile.readlines()
 
        output = ""
        subject = ""
        for line in lines:
            if line.startswith("subject="):
                subject = line.split("CN = ")[-1].strip().split(",")[0].replace(' ', '')
 
            if line.startswith("-----BEGIN CERTIFICATE-----"):
                if not subject:
                    counter += 1
                    output = os.path.join(dest, f"cert_{counter}.cer")
                else:
                    output = os.path.join(dest, f"{subject.lower()}.cer")
                    subject = ""
 
                with open(output, 'w') as outfile:
                    outfile.write(line)
            elif line.startswith("-----END CERTIFICATE-----"):
                with open(output, 'a') as outfile:
                    outfile.write(line)
                    output = ""
            elif output:
                with open(output, 'a') as outfile:
                    outfile.write(line)
 
        result['changed'] = True
        result['message'] = 'Certificates extracted and saved as .cer files successfully'
    except Exception as e:
        module.fail_json(msg=str(e), **result)
 
    module.exit_json(**result)
 
def main():
    run_module()
 
if __name__ == '__main__':
    main()