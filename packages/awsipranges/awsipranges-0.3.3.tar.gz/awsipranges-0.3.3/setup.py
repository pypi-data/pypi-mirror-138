# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsipranges', 'awsipranges.models']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'awsipranges',
    'version': '0.3.3',
    'description': 'Work with the AWS IP address ranges in native Python.',
    'long_description': '# awsipranges\n\n*Work with the AWS IP address ranges in native Python.*\n\n[![License](https://img.shields.io/github/license/aws-samples/awsipranges)](https://github.com/aws-samples/awsipranges/blob/main/LICENSE)\n[![PyPI](https://img.shields.io/pypi/v/awsipranges.svg)](https://pypi.org/project/awsipranges/)\n[![Code Coverage](https://img.shields.io/codecov/c/github/aws-samples/awsipranges)](https://app.codecov.io/github/aws-samples/awsipranges/)\n[![Build](https://img.shields.io/github/workflow/status/aws-samples/awsipranges/tests)](https://github.com/aws-samples/awsipranges/actions/workflows/tests.yml)\n[![Docs](https://img.shields.io/github/workflow/status/aws-samples/awsipranges/publish-docs?label=docs)](https://aws-samples.github.io/awsipranges/)\n\n---\n\nAmazon Web Services (AWS) publishes its [current IP address ranges](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html) in [JSON](https://ip-ranges.amazonaws.com/ip-ranges.json) format. Python v3 provides an [ipaddress](https://docs.python.org/3/library/ipaddress.html) module in the standard library that allows you to create, manipulate, and perform operations on IPv4 and IPv6 addresses and networks. Wouldn\'t it be nice if you could work with the AWS IP address ranges like native Python objects?\n\n## Features\n\n- Work with the AWS IP prefixes as a simple `AWSIPPrefixes` collection.\n- Quickly check if an IP address, interface, or network is contained in the AWS IP address ranges.\n- Get the AWS IP prefix that contains an IP address, interface, or network.\n- See what services are served from an IP prefix.\n- Filter the AWS IP prefixes by _region_, _network border group_, _service_, and IP prefix _version_.\n- Use the AWS prefix data in your app or automation scripts in the format required by your infrastructure.\n- Easily validate the TLS certificate presented by the IP ranges server.\n- awsipranges has _no third-party dependencies_ and is compatible with CPython v3.7+.\n\n```python\n>>> import awsipranges\n\n>>> aws_ip_ranges = awsipranges.get_ranges(cafile="amazon_root_certificates.pem")\n\n>>> \'52.94.5.15\' in aws_ip_ranges\nTrue\n\n>>> aws_ip_ranges[\'52.94.5.15\']\nAWSIPv4Prefix(\'52.94.5.0/24\', region=\'eu-west-1\', network_border_group=\'eu-west-1\', services=(\'AMAZON\', \'DYNAMODB\'))\n\n>>> aws_ip_ranges.filter(services=\'CODEBUILD\')\n{\'create_date\': datetime.datetime(2021, 8, 24, 1, 31, 14, tzinfo=datetime.timezone.utc),\n \'ipv4_prefixes\': (AWSIPv4Prefix(\'3.26.127.24/29\', region=\'ap-southeast-2\', network_border_group=\'ap-southeast-2\', services=(\'CODEBUILD\',)),\n                   AWSIPv4Prefix(\'3.38.90.8/29\', region=\'ap-northeast-2\', network_border_group=\'ap-northeast-2\', services=(\'CODEBUILD\',)),\n                   AWSIPv4Prefix(\'3.68.251.232/29\', region=\'eu-central-1\', network_border_group=\'eu-central-1\', services=(\'CODEBUILD\',)),\n                   AWSIPv4Prefix(\'3.98.171.224/29\', region=\'ca-central-1\', network_border_group=\'ca-central-1\', services=(\'CODEBUILD\',)),\n                   AWSIPv4Prefix(\'3.101.177.48/29\', region=\'us-west-1\', network_border_group=\'us-west-1\', services=(\'CODEBUILD\',)),\n                   ...),\n \'ipv6_prefixes\': (),\n \'sync_token\': \'1629768674\'}\n\n>>> for prefix in aws_ip_ranges.filter(regions=\'eu-west-1\', services=\'DYNAMODB\'):\n...     print(prefix.network_address, prefix.netmask)\n...\n52.94.5.0 255.255.255.0\n52.94.24.0 255.255.254.0\n52.94.26.0 255.255.254.0\n52.119.240.0 255.255.248.0\n```\n\n## Installation\n\nInstalling and upgrading `awsipranges` is easy:\n\n**Install via PIP**\n\n```shell\n❯ pip install awsipranges\n```\n\n**Upgrade to the latest version**\n\n```shell\n❯ pip install --upgrade awsipranges\n```\n\n## Documentation\n\nExcellent documentation is now available at: https://aws-samples.github.io/awsipranges/\n\nCheck out the [Quickstart](https://aws-samples.github.io/awsipranges/quickstart.html) to dive in and begin using awsipranges.\n\n## Contribute\n\nSee [CONTRIBUTING](https://github.com/aws-samples/awsipranges/blob/main/CONTRIBUTING.md) for information on how to contribute to this project.\n\n## Security\n\nSee [CONTRIBUTING](https://github.com/aws-samples/awsipranges/blob/main/CONTRIBUTING.md#security-issue-notifications) for information on how to report a security issue with this project.\n\n## License\n\nThis project is licensed under the [Apache-2.0 License](https://github.com/aws-samples/awsipranges/blob/main/LICENSE).\n',
    'author': 'Chris Lunsford',
    'author_email': 'cmluns@amazon.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://aws-samples.github.io/awsipranges/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
