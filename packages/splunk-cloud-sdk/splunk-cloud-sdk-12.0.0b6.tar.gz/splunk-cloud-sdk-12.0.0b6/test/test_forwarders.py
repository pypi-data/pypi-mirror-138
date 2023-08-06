# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import pytest

from splunk_sdk.base_client import BaseClient
from splunk_sdk.forwarders import SplunkForwarderService, Certificate
from test.fixtures import get_test_client as test_client  # NOQA


PEM = '''-----BEGIN CERTIFICATE-----
MIIC1TCCAb2gAwIBAgIJAIOAwz2qyz1FMA0GCSqGSIb3DQEBCwUAMBoxGDAWBgNV
BAMMD3d3dy5leGFtcGxlLmNvbTAeFw0yMTA4MjcxOTAwNTVaFw0yNjA4MjYxOTAw
NTVaMBoxGDAWBgNVBAMMD3d3dy5leGFtcGxlLmNvbTCCASIwDQYJKoZIhvcNAQEB
BQADggEPADCCAQoCggEBANHY9Uc+AJL17z6GkJ9VoiPU0TDF3+rVjp2CLxcc2Upt
BgX//F+MFNwY6bK3HEXE3AQPvuOtp7FQQYX+2BgLQwMiyKThKg5V4KcmsDR3zvqQ
Rdrd4lXm5KAt8kLSF+VFFO+Fm0eJG7fQgERsBFuyHg16511dh1JC2cAu6E2IaFw2
nUWyYsvjKCl3hcPqvmVl8MIFexhPw7cyUlq68PyEgYpDXzfgE1DIiu1BGQ5z/UZ2
XzBTQKg7/+iVfdMjftYbRqLk3MKwaM0yuohVBLkkBKuY8H+93G4qizYGAs+Ae5Hi
EYPUkkmQMYfOXhSF7cV2aDPcCAY9oJWDaQNBk3rx4v8CAwEAAaMeMBwwGgYDVR0R
BBMwEYIPd3d3LmV4YW1wbGUuY29tMA0GCSqGSIb3DQEBCwUAA4IBAQC5mqAoFR1t
tYR558EYxn91VVmFFeUdXtAbkWQ6LLLQPTbWz8bQW5qoj9mYF7r2AAKnJvJoAtUX
ZYfVlHhEenGG9x8U/he/4L8IubHySMrksmoGVC5vS/0ecSD0pjObcNa6ZZH+ELbf
O1Fm1vP/QzOZeQoH2C4tdtDNXS9JV0F4ZGOHQALEBNkO5CfOVXd3YhmGGLFxkgjs
I135CtslJTR3+GpPHg44/Lo7VvwuSp0gJIzgLayM8Hcb7fKpZ0D2FsRkc4dDIwuR
wDYojnaUIAuni1Dd8oguYvm5+S56XOOO9BNDorxNzqqHuwEsqszG86VBEkMAB5v+
AQ86ecyUH90A
-----END CERTIFICATE-----
'''

@pytest.mark.usefixtures("test_client")  # NOQA
def test_cert_crud(test_client: BaseClient):
    forwarders = SplunkForwarderService(test_client)
    forwarders.delete_certificates()

    certs = forwarders.list_certificates()
    current_cert_count = len(certs)

    forwarders.add_certificate(Certificate(pem=PEM))

    certs = forwarders.list_certificates()
    assert(len(certs) == current_cert_count + 1)

    forwarders.delete_certificates()
    certs = forwarders.list_certificates()
    assert(len(certs) == 0)
