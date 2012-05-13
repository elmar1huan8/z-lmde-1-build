#! /usr/bin/env python

# Check for root user login
import os, sys
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")

# Get your username (not root)
import pwd
uname=pwd.getpwuid(1000)[0]

# The remastering process uses chroot mode.
# Check to see if this script is operating in chroot mode.
# /home/mint directory only exists in chroot mode
is_chroot = os.path.exists('/home/mint')
dir_develop=''
if (is_chroot):
	dir_develop='/usr/local/bin/develop'
	dir_user = '/home/mint'
else:
	dir_develop='/home/' + uname + '/develop'
	dir_user = '/home/' + uname

# Everything up to this point is common to all Python scripts NOT called by shared-* scripts
# ==========================================================================================
import shutil

def elim_dir (dir_to_elim): 
	if (os.path.exists(dir_to_elim)):
		shutil.rmtree (dir_to_elim)

def create_dir (dir_to_create):
    if not (os.path.exists(dir_to_create)):
        os.mkdir (dir_to_create)

# Obtain the LMDE ISO file
os.system ('mount -t vboxsf guest /mnt/host')
base_iso = '/mnt/host/linuxmint-201204-mate-cinnamon-dvd-32bit.iso'
while not (os.path.isfile (base_iso)):
    print ('Could not find your ' + base_iso + 'file.')
    print ('Please go to your host OS and copy the appropriate file into')
    print ('the /home/(username)/guest directory.')
    print ('Press Enter when you are finished')
    var_dummy = raw_input ('TEST')
    os.system ('mount -t vboxsf guest /mnt/host')

print (base_iso + ' file found, ready to proceed')

# Prepare the remastering script
os.system ('sh ' + dir_develop + '/remaster/main.sh')

# Execute the remastering script
os.system ('echo EXECUTING THE REMASTERING SCRIPT')
command_remaster = 'python /usr/lib/linuxmint/mintConstructor/mintConstructor.py '
os.system (command_remaster)

