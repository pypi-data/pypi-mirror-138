#!/usr/bin/env python

# Copyright 2015-2020 Earth Sciences Department, BSC-CNS
# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.

import json
from autosubmitAPIwu.history.utils import get_current_datetime_if_none

class ExperimentRun(object):
  """
  Class that represents an experiment run
  """
  def __init__(self, run_id, created=None, modified=None, start=0, finish=0, chunk_unit="NA", chunk_size=0, completed=0, total=0, failed=0, queuing=0, running=0, submitted=0, suspended=0, metadata=""):
    self.run_id = run_id
    self.created = get_current_datetime_if_none(created) 
    self.modified = get_current_datetime_if_none(modified) # Added on DB 16
    self.start = start
    self.finish = finish
    self.chunk_unit = chunk_unit
    self.chunk_size = chunk_size
    self.submitted = submitted
    self.queuing = queuing
    self.running = running
    self.completed = completed
    self.failed = failed
    self.total = total
    self.suspended = suspended
    self.metadata = metadata    

  def get_wrapper_type(self):
    if self.metadata:              
      data = json.loads(self.metadata)                        
      wrapper_section = data["conf"].get("wrapper", None)
      if wrapper_section:      
        wrapper_type = wrapper_section.get("TYPE", None)
        if wrapper_type:
          return wrapper_type
    return None

  @classmethod
  def from_model(cls, row):
    """ Build ExperimentRun from ExperimentRunRow """
    experiment_run = cls(0)
    experiment_run.run_id = row.run_id
    experiment_run.created = get_current_datetime_if_none(row.created)
    experiment_run.modified = get_current_datetime_if_none(row.modified)
    experiment_run.start = row.start
    experiment_run.finish = row.finish
    experiment_run.chunk_unit = row.chunk_unit
    experiment_run.chunk_size = row.chunk_size
    experiment_run.completed = row.completed
    experiment_run.total = row.total
    experiment_run.failed = row.failed
    experiment_run.queuing = row.queuing
    experiment_run.running = row.running
    experiment_run.submitted = row.submitted
    experiment_run.suspended = row.suspended
    experiment_run.metadata = row.metadata
    return experiment_run
  