#!/usr/bin/env python3
#
#
#
#
import argparse
import datetime
import logging
import os
import subprocess
import tarfile
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
        file_suffix: str,
        gsutil_path="/google-cloud-sdk/bin",
    ):

        self.src = src_bucket
        self.dst = backup_bucket
        self.encrypt_key = encrypt_key
        self.gsutil_path = gsutil_path
        self.suffix = file_suffix

    def _subprocess_debug_wrap(self, cmd: list, shellmode: bool = False) -> str:
        logger.debug("Calling command {}".format(" ".join(cmd)))
        if shellmode:
            cmd = " ".join(cmd)
        copy_output = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, shell=shellmode).decode('ascii')
        logger.debug(copy_output)

        return copy_output

    def gsutil_encrypt_cp_cmd(self, src: str, dst: str) -> None:
        """ Copy a local file to a bucket with encryption """
        gsutil_base_cmd = [self.gsutil_path,
                           "-o", '"GSUtil:encryption_key={}"'.format(
                               self.encrypt_key),
                           "cp",  src, dst]

        self._subprocess_debug_wrap(gsutil_base_cmd, True)

    def rsync_cmd(self, src: str, dst: str, dry: bool = False) -> None:
        """ Call gsutil rsync against two paths """
        gsutil_base_cmd = [self.gsutil_path,
                           "-m", "rsync", "-r", "-d", src, dst]

        if dry:
            gsutil_base_cmd.insert(4, "-n")

        self._subprocess_debug_wrap(gsutil_base_cmd)

    def rsync_source_bucket(self) -> str:
        """ Pull down a copy of a bucket contents for local comparison"""

        # Start out creating a temporary directory
        self.tmp_dir = tempfile.mkdtemp()
        logger.info(
            "Created local dir {} for bucket manipulation".format(self.tmp_dir))

        self.rsync_cmd(self.src, self.tmp_dir)

        return self.tmp_dir

    def tar_directory(self, tar_dir: str) -> str:
        """ Tar+gzip up a directory and return path to that tar ball """
        tar_file_path = os.path.join(tar_dir, "src-bucket.tar.gz")
        tar = tarfile.open(tar_file_path, 'w:gz')
        tar.add(tar_dir, arcname='')
        tar.close()
        logger.info("Created tar at {} of {}".format(tar_file_path, tar_dir))

        return tar_file_path

    def upload_encrypted_timestamp_file(self, upload_file: str) -> None:
        """ Given a file path upload said file to our backup bucket. File is timestamp'd and includes file prefix. """
        timestamp_name = datetime.datetime.now().strftime(
            '%b-%d-%y-%X-{}.tar.gz'.format(self.suffix))
        backup_bucket_path = os.path.join(self.dst, timestamp_name)

        self.gsutil_encrypt_cp_cmd(upload_file, backup_bucket_path)


if __name__ == "__main__":
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('src', type=str, help="Source bucket")
    args.add_argument('backup', type=str, help="Backup bucket")
    args.add_argument(
        'suffix', type=str,
        help="Backup suffix filename ex: $timestamp-prefix.tar.gz")
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
        parsed_args.src, parsed_args.backup, encrypt_key,
        parsed_args.suffix, parsed_args.gsutil_bin)

    # Local directory filled with rsync'd files
    backup_local_dir = backup.rsync_source_bucket()

    # Create tarfile and grab file location
    local_tar = backup.tar_directory(backup_local_dir)

    # Upload backup to final destination
    backup.upload_encrypted_timestamp_file(local_tar)
