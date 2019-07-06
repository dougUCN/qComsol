qComsol  
===============  
Many universities/organizations have a comsol license with a limited number
of maximum users at a given moment in time. This presents a problem if
one attempts to submit jobs to a cluster, when one has no control over when
the job starts running  

qComsol submits a comsol job to a Torque queue, and resubmits it if it was
rejected because of a license error  

Getting started
--------------------
Edit comsolJob.pbs so that -tmpdir and -recoverydir both point to
an appropriate directory, and change the email address  

Put qComsol.py, comsolJob.pbs, and check.pbs in the same directory
as your comsol files, then simply run qComsol.py as described in the Usage section  

Your completed comsol job will be a new file titled filename_solved.mph  


Usage  
----------------
<pre>  
usage: qComsol.py [-h] [-d DELAY] [-t TRIES] [-r] filename  

submit comsol job to TORQUE system  

positional arguments:  
  filename              Accepts names w/ or w/o the '.mph' ending  

optional arguments:  
  -h, --help            show this help message and exit  
  -d DELAY, --delay DELAY  
                        Delay time for job resubmission [min]  
  -t TRIES, --tries TRIES  
                        Max # tries for resubmission   
  -r, --removePBS       Removes PBS job submission scripts  
  -nc, --noCheck        Don't submit checking job to queue  
</pre>

comsolJob.pbs  
----------------  
Tells the torque queue to run the comsol file  

Change settings here appropriately. I've currently picked arbitrary values
for vmem and ppn. For configuring multiple node parallelization check out the
"Useful documentation on Torque and Comsol" section  

Please note that $FILENAME, $TRIESLEFT, $DELAY,and $COMSOL_JOB are not
actually environment variables. They are edited by qComsol.py  

check.pbs  
---------------  
Note that the [--delay] flag in qComsol.py is limited by the wall time you set
in this config file

Python version  
------------------  
This script is written for python 2. For compatibility with python 3 you'll
need to comment out the import future print and change iteritems() to items()  

Useful documentation on Torque and Comsol  
-------------------------------------------
*[qsub command](http://docs.adaptivecomputing.com/torque/4-0-2/Content/topics/commands/qsub.htm)*  
*[Torque conditional execution](http://www.arc.ox.ac.uk/content/torque-job-scheduler#PBScondExecution)*  
*[Comsol and torque submission](https://www.hpc.dtu.dk/?page_id=1257)*  

Of particular note is the last link, where they mention that
"the Comsol -np is used only to specify the processes that run on a single node ONLY"  

For use of multiple nodes it seems that the intel-MPI library is necessary
