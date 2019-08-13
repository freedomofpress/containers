#!/usr/bin/env python3
#
#
#
#
import argparse
import logging
import os
import subprocess
import tempfile
import sys

"""
Takes a source bucket, a backup bucket, encryption key as args. Will rsync down the source,
tar those files up, grab the latest tar-ball from the backup bucket, if there are changes
the local tar ball will be backed up.
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class GCPBucketBackup(object):
    def __init__(
        self,
        src_bucket: str,
        backup_bucket: str,
        encrypt_key: str,
        gsutil_path="/google-cloud-sdk/bin",
    ):

        self.src = src_bucket
        self.dst = backup_bucket
        self.encrypt_key = encrypt_key
        self.gsutil_path = gsutil_path

    def rsync_cmd(self, src: str, dst: str, dry: bool = False) -> None:
        """ Thin wrapper around gsutil rsync command """
        gsutil_base_cmd = [self.gsutil_path,
                           "-m", "rsync", "-r", "-d", src, dst]

        if dry:
            gsutil_base_cmd.insert(4, "-n")

        rsync_output = subprocess.check_output(
            gsutil_base_cmd, stderr=subprocess.STDOUT).decode('ascii')
        logger.debug(rsync_output)

    def rsync_source_bucket(self) -> str:
        """ Pull down a copy of a bucket contents for local comparison"""

        # Start out creating a temporary directory
        self.tmp_dir = tempfile.mkdtemp()
        logger.info(
            "Created local dir {} for bucket manipulation".format(self.tmp_dir))

        self.rsync_cmd(self.src, self.tmp_dir)

        return self.tmp_dir


if __name__ == "__main__":
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('src', type=str, help="Source bucket")
    args.add_argument('backup', type=str, help="Backup bucket")
    args.add_argument('-v', action='store_true', default=False,
                      required=False, help='Increase verbosity')
    args.add_argument('-gsutil_bin', type=str, required=False,
                      help="Full path to gsutil binary on disk", default="/google-cloud-sdk/bin")
    parsed_args = args.parse_args()

    # Set verbose output
    if parsed_args.v:
        logger.setLevel(logging.DEBUG)

    logger.debug("ARGS piped in: {}".format(parsed_args))

    try:
        encrypt_key = os.environ['GBACKUP_ENV_KEY']
    except KeyError:
        logging.error("Must expose an env var called GBACKUP_ENV_KEY")
        args.print_help()
        sys.exit(1)

    backup = GCPBucketBackup(
        parsed_args.src, parsed_args.backup, encrypt_key, parsed_args.gsutil_bin)
    backup.rsync_source_bucket()
