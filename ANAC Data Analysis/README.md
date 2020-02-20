# ANAC Testing Script and Data Extraction Pipeline

In order to run the automatically generated report, make sure to be in negotiation-agent location (eg. cd one level before) and run the following command from terminal:

```cmd
python analysis/automation.py <agent name> <opponent list txt file location> <domain list txt file location> 
```

Example:

```cmd
python analysis/automation.py agents.anac.y2011.IAMhaggler2011.IAMhaggler2011 analysis/opponents_list.txt analysis/domains_list.txt
```

Example using BOA agent:

```
python analysis/automation.py out/production/agent/boa/Atlas.class analysis/opponents_list.txt analysis/domains_list.txt
```

Example using not BOA agent:

```
py -3.6 analysis/automation.py out/production/agent/group27/Agent27.class analysis/opponents_list.txt analysis/domains_list.txt
```

Once run this command in terminal, the results will be available in a folder called log (which will be created at the location from which the program was run) inside a folder named with the name of the agent under examination and the run time (eg. Atlas_2019-11-20_2029).