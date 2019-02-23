#!/usr/bin/python

import yaml

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''

---
module: read_yaml_with_vault
short_description: Reads a YAML file containing encrypted vault
options:
  path:
    description:
      - The file path to the file that needs to be read
    required:True
  fact_name:
    description:
      - The name of the ansible fact to set
    required:True
'''

EXAMPLES = '''
- read_yaml_with_vault:
    path: ./deployments/default/credentials.yml
    fact_name: encrypted
'''

VAULT_YAML_TAG = "!vault |\n"


def vault_constructor(loader, node):
    return VAULT_YAML_TAG + node.value


def read_yaml_with_vault(path, fact_name):
    with open(path, 'r') as file:
        try:
            yaml.add_constructor(u'!vault', vault_constructor)
            parsed_yaml = yaml.load(file.read())
        except Exception as e:
            msg = "Could not load yaml file %s: %s" % (path, str(e))
            print msg
            module.fail_json(msg=msg)

    module.exit_json(changed=True, ansible_facts={fact_name: parsed_yaml})


arg_spec = dict(
    path=dict(
        required=True,
        type='str'),
    fact_name=dict(
        required=True,
        type='str'))
module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)


def main():
    path = module.params['path']
    fact_name = module.params['fact_name']
    read_yaml_with_vault(path, fact_name)


if __name__ == '__main__':
    main()
