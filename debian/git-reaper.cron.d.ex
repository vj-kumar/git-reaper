#
# Regular cron jobs for the git-reaper package
#
0 4	* * *	root	[ -x /usr/bin/git-reaper_maintenance ] && /usr/bin/git-reaper_maintenance
