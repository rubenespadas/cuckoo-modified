# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import codecs
import time
import json
import logging
import os
from datetime import datetime

from lib.cuckoo.core.database import Database
from lib.cuckoo.common.abstracts import Processing
from lib.cuckoo.common.constants import CUCKOO_VERSION
from lib.cuckoo.common.exceptions import CuckooProcessingError

log = logging.getLogger(__name__)


class AnalysisInfo(Processing):
    """General information about analysis session."""

    def had_timeout(self):
        """ Test if the analysis had a timeout
        """
        if os.path.exists(self.log_path):
            try:
                analysis_log = codecs.open(self.log_path, "rb", "utf-8").read()
            except ValueError as e:
                raise CuckooProcessingError("Error decoding %s: %s" %
                                            (self.log_path, e))
            except (IOError, OSError) as e:
                raise CuckooProcessingError("Error opening %s: %s" %
                                            (self.log_path, e))
            else:
                if "INFO: Analysis timeout hit, terminating analysis" in analysis_log:
                    return True
        return False

    def get_options(self,optstring):
        """Get analysis options.
        @return: options dict.
        """
        # The analysis package can be provided with some options in the
        # following format:
        #   option1=value1,option2=value2,option3=value3
        #
        # Here we parse such options and provide a dictionary that will be made
        # accessible to the analysis package.
        options = {}
        if optstring:
            try:
                # Split the options by comma.
                fields = optstring.split(",")
            except ValueError as e:
                pass
            else:
                for field in fields:
                    # Split the name and the value of the option.
                    try:
                        key, value = field.split("=", 1)
                    except ValueError as e:
                        pass
                    else:
                        # If the parsing went good, we add the option to the
                        # dictionary.
                        options[key.strip()] = value.strip()

        return options

    def run(self):
        """Run information gathering.
        @return: information dict.
        """
        self.key = "info"

        try:
            started = time.strptime(self.task["started_on"], "%Y-%m-%d %H:%M:%S")
            started = datetime.fromtimestamp(time.mktime(started))
            ended = time.strptime(self.task["completed_on"], "%Y-%m-%d %H:%M:%S")
            ended = datetime.fromtimestamp(time.mktime(ended))
        except:
            log.critical("Failed to get start/end time from Task.")
            duration = -1
        else:
            duration = (ended - started).seconds

        db = Database()

        # Fetch sqlalchemy object.
        task = db.view_task(self.task["id"], details=True)

        if task and task.guest:
            # Get machine description ad json.
            machine = task.guest.to_dict()
            # Remove useless task_id.
            del(machine["task_id"])
            # Save.
            self.task["machine"] = machine

        return dict(
            version=CUCKOO_VERSION,
            started=self.task["started_on"],
            ended=self.task.get("completed_on", "none"),
            duration=duration,
            id=int(self.task["id"]),
            category=self.task["category"],
            custom=self.task["custom"],
            machine=self.task["machine"],
            package=self.task["package"],
            timeout=self.had_timeout(),
            options=self.get_options(self.task["options"])
        )
