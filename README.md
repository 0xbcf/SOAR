# SOAR
A Python security orchestration and automation system

# Installation
TODO

# Documentation
Events should be fed from an SIEM webhook and passed to a mongodb that the soar system reads (not yet created).
Playbooks/orchestrator.py then reads these events and watches for any match to one of the playbooks that have been defined.
If there is a match, the playbook will execute and issue a mitigation command stored in mongodb.
Mitigation/mitigate.py then reads the mitigation command, executes remediation and marks the mitigationa as complete.