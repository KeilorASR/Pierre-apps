# -*- coding: utf-8 -*-
######################################################################################################
#
# Copyright (C) B.H.C. sprl - All Rights Reserved, http://www.bhc.be
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# This code is subject to the BHC License Agreement
# Please see the License.txt file for more information
# All other rights reserved
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied,
# including but not limited to the implied warranties
# of merchantability and/or fitness for a particular purpose
######################################################################################################

import time
import math
from odoo.osv import expression
from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT,DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo import api, fields, models, _
import logging
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from operator import itemgetter
_logger = logging.getLogger(__name__)
from xml.dom.minidom import Node
from xml.dom.minidom import parse, parseString
import xml.dom.minidom
import ssl
import socket
import httplib
import ftplib
import os
import os.path
import csv, math
import thread
import smtplib
import sys
import re

class launch_map(models.Model):
    _inherit = "res.partner"

    @api.multi
    def open_map(self):
        for partner in self:
            url="http://maps.google.com/maps?oi=map&q="
            if partner.street:
                url+=partner.street.replace(' ','+')
            if partner.city:
                url+='+'+partner.city.replace(' ','+')
            if partner.state_id:
                url+='+'+partner.state_id.name.replace(' ','+')
            if partner.country_id:
                url+='+'+partner.country_id.name.replace(' ','+')
            if partner.zip:
                url+='+'+partner.zip.replace(' ','+')
        return {'type': 'ir.actions.act_url','target': 'new','url':url}