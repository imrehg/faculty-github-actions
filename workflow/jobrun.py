import faculty
import sys
from time import sleep
import os
import random

from faculty.clients.job import RunState

COMPLETED_RUN_STATES = {
    RunState.COMPLETED,
    RunState.FAILED,
    RunState.CANCELLED,
    RunState.ERROR,
}

profile = faculty.config.resolve_profile()
dashboard_url = f"{profile.protocol}://{profile.domain.replace('services.', '')}"

project_id = os.getenv("FACULTY_PROJECT_ID")
jobname = os.getenv("FACULTY_JOB_NAME")
# https://help.github.com/en/actions/configuring-and-managing-workflows/using-environment-variables
# GITHUB_SHA is the most relevant value, but that doesn't seem reliable at the moment, thus we are checking
# things out by reference.
commit = os.getenv("GITHUB_HEAD_REF")

job_client = faculty.client("job")

jobs = job_client.list(project_id)
try:
    myjob = [j for j in jobs if j.metadata.name == jobname][0]
except IndexError:
    sys.exit(
        f"Error: Couldn't find job {jobname} in project {project_id}, please check the name."
    )

# Trigger run
parameter_value_sets = [
    {"COMMIT": commit, "MESSAGE": "automating", "CYCLES": "10"},
    {"COMMIT": commit, "MESSAGE": "automating", "CYCLES": "15"},
]
print(f"Parameters: {parameter_value_sets}")
run_id = job_client.create_run(project_id, myjob.id, parameter_value_sets)
print(f"Run triggered with id {run_id}")
run_data = job_client.get_run(project_id, myjob.id, run_id)
print(f"Run number: {run_data.run_number}")
print("Waiting for job to finish...")
while run_data.state not in COMPLETED_RUN_STATES:
    run_data = job_client.get_run(project_id, myjob.id, run_id)
    sleep(1)

# job_link = join(str(dashboard_url), "project", str(project_id), "jobs", "manage", str(myjob.id), "history")
# print(f"Check results at {job_link}")
if run_data.state == RunState.COMPLETED:
    print("Job completed successfully.")
else:
    sys.exit(f"Job has not not finished correctly: {run_data.state}")
