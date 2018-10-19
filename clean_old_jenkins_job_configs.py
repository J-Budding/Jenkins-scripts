# clean_old_jenkins_job_configs.py
#
# The Jenkins job config histrory plugin can keep al lot of files if you don't configure it properly.
# With this script you can do some cleaning.
#
# Walk over the job config history files in Jenkins and clean em up if they are older than the
# retention perios of 30 days. 3 Jobs configs will always be kept as a minimum regardless of their age.
#

import os
import getopt, sys
import shutil
from datetime import datetime, timedelta
from collections import defaultdict

CONST_RETENTION_DAYS = 30
purge_candidates = defaultdict(list)

def process_command_line_options():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hds:", ["help", "dry-run", "start-folder="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
    global start_folder, dry_run
    start_folder, dry_run = None, None
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--dry-run"):
            dry_run = True
        elif o in ("-s", "--start-folder"):
            start_folder = a
        else:
            assert False, "unhandled option"
    if not start_folder:
        print("start-folder is mandatory, use the -s|--start-folder flag")
        usage()


def usage ():
    print("\nUSAGE python clean_old_job_configs.py [-h|--help] -d|--dry-run -s|--start-folder <start folder path> \n")
    print("Clean old config folder utility for Jenkins")
    sys.exit(2)


# Main
process_command_line_options()

print "Starting clean old job configs"

rootDir = start_folder
# '/var/lib/jenkins/config-history/jobs/Build/jobs'

print "Starting clean old job configs"
print "Start dir " + rootDir

for dirName, subdirList, fileList in os.walk(rootDir):
    #print 'Found directory: %s' % dirName
    if "history.xml" in fileList:
        #for fname in fileList:
        #    print 'Directory %s' % dirName
        #    print '\t%s' % fname
        current_dirname = dirName.split(os.path.sep)[-1]
        # 2018-03-22_11-50-40
        current_dirname_date = datetime.strptime( current_dirname[:10], "%Y-%m-%d" )

        #print 'current_dirname_date %s current_dirname %s' % (current_dirname_date, current_dirname)

        if current_dirname_date < datetime.today() - timedelta(days=CONST_RETENTION_DAYS):
            #print 'Config file more then %s days old : %s' % (CONST_RETENTION_DAYS, current_dirname_date)
            parentdir_ofthisdir = '/'.join(dirName.split(os.path.sep)[:-1])
            purge_candidates [ parentdir_ofthisdir ].append(current_dirname)

for parentdir, childdirs_to_purge in purge_candidates.iteritems():
    print parentdir + "  :: "

    for dirName, subdirList, fileList in os.walk(parentdir):
        subdirList.sort(reverse=True)
        if 'jobs' in subdirList:
            subdirList.remove('jobs')
        for idx, sd in enumerate(subdirList):
            if idx not in [0, 1, 2]:  # ALWAYS keep at least 3 configs, delete the rest if it's in the purge list (older then retention days)
                if sd in childdirs_to_purge:
                    if not dry_run:
                        print "Perform delete "  + parentdir + "/" + sd
                        shutil.rmtree(parentdir + "/" + sd)
                    else:
                        print "[Dry run] no delete "  + parentdir + "/" + sd

