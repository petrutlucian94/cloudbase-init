# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Cloudbase Solutions Srl
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
import unittest

from cloudbaseinit.metadata.services import base as metadata_services_base
from cloudbaseinit.plugins import base
from cloudbaseinit.plugins.windows import userdata
from cloudbaseinit.osutils import base as osutils_base


class UserDataTest(unittest.TestCase):
    '''testing the userdata module'''

    def setUp(self):
        self.plugin = userdata.UserDataPlugin()
        self.service = metadata_services_base.BaseMetadataService()

    def test_no_user_data(self):
        self.service.get_user_data = mock.MagicMock(return_value = None)
        response = self.plugin.execute(self.service)
        self.service.get_user_data.assert_called_with('openstack')
        self.assertEqual(response, (base.PLUGIN_EXECUTION_DONE, False))

    def test_get_user_data_exception(self):
        self.side_effect = metadata_services_base.NotExistingMetadataException
        self.service.get_user_data = mock.MagicMock(side_effect =
                                                    self.side_effect)
        response = self.plugin.execute(self.service)
        self.service.get_user_data.assert_called_with('openstack')
        self.assertEqual(response, (base.PLUGIN_EXECUTION_DONE, False))

    def test_get_proper_user_data(self):
        self.service.get_user_data = mock.MagicMock(return_value = 'rem cmd')
        self.plugin._process_userdata = mock.Mock()
        response = self.plugin.execute(self.service)
        self.service.get_user_data.assert_called_with('openstack')
        self.assertEqual(response, (base.PLUGIN_EXECUTION_DONE, False))
        self.plugin._process_userdata.assert_called_with('rem cmd')

    def test_process_multipart_userdata(self):
        self.fake_user_data = 'Content-Type: multipart'
        self.plugin._process_part = mock.Mock()
        self.plugin._process_userdata(self.fake_user_data)
        self.plugin._process_part.assert_called_once()

    def test_process_singlepart_userdata(self):
        self.fake_user_data = 'rem cmd'
        userdata.handle = mock.Mock()
        self.plugin._process_userdata(self.fake_user_data)
        userdata.handle.assert_called_with('rem cmd')

    '''def test_process_part(self):'''
