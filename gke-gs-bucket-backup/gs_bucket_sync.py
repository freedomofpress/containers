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
Takes a source bucket, a backup bucket, encryption key as args.
Will rsync down the source,
tar those files up,
grab the latest tar-ball from the backup bucket.

If you provide a service account key path, script will call out to gcloud to initialize it
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class ChattyArgParser(argparse.ArgumentParser):
    """ArgumentParser that prints full help instead of short usage on argument error"""
    def error(self, message):
        logger.error('{}: {}\n'.format(self.prog, message))
        self.print_help(sys.stderr)
        self.exit(2)


class GCPBucketBackup(object):
    def __init__(
        self,
        src_bucket: str,
        backup_bucket: str,
        encrypt_key: str,
        filename: str,
        gsutil_path: str,
    ):

        self.src = src_bucket
        self.dst = backup_bucket
        self.encrypt_key = encrypt_key
        self.gsutil_path = gsutil_path
        self.filename = filename

    def _subprocess_debug_wrap(self,
                               cmd: list,
                               shellmode: bool = False) -> str:

        # Sanitize out potential output of encryption key
        debug_cmd_str = "Calling command {}".format(
            " ".join(cmd)).replace(self.encrypt_key, "X"*10)
        logger.debug(debug_cmd_str)

        if shellmode:
            cmd = " ".join(cmd)

        try:
            copy_output = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, shell=shellmode).decode('ascii')
            logger.debug(copy_output)
        except subprocess.CalledProcessError as e:
            logger.error("command {} failed with status {}, output = {}".format(
                e.cmd, e.returncode, e.output.decode('utf-8')))
            sys.exit(1)

        return copy_output

    def initialize_svc_acct(self, acct_key_path: str) -> None:
        """ Initilize gcloud tooling using a GCP service account key """
        gcloud_auth_cmd = [
            "gcloud", "auth", "activate-service-account", "--key-file",
            acct_key_path]
        self._subprocess_debug_wrap(gcloud_auth_cmd)

    def gsutil_encrypt_cp_cmd(self, src: str, dst: str) -> None:
        """ Copy a local file to a bucket with encryption """
        gsutil_base_cmd = [self.gsutil_path,
                           "-o", '"GSUtil:encryption_key={}"'.format(
                               self.encrypt_key),
                           "cp",  src, dst]

        self._subprocess_debug_wrap(gsutil_base_cmd, True)
        logger.info('Uploaded to encrypted bucket destination {}'.format(dst))

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
        logger.debug(
            "Created local dir {}"
            " for bucket manipulation".format(self.tmp_dir))

        self.rsync_cmd(self.src, self.tmp_dir)

        return self.tmp_dir

    def tar_directory(self, tar_dir: str) -> str:
        """ Tar+gzip up a directory and return path to that tar ball """
        tar_file_path = os.path.join(tar_dir, "src-bucket.tar.gz")
        tar = tarfile.open(tar_file_path, 'w:gz')
        tar.add(tar_dir, arcname='')
        tar.close()
        logger.debug("Created tar at {} of {}".format(tar_file_path, tar_dir))

        return tar_file_path

    def upload_encrypted_timestamp_file(self, upload_file: str) -> None:
        """ Given a file path upload said file to our backup bucket.
            File is timestamp'd and includes file prefix. """
        timestamp = datetime.datetime.now().strftime('%F-%R-%s')
        backup_bucket_path = os.path.join(self.dst, '{}-{}'.format(timestamp, self.filename))

        self.gsutil_encrypt_cp_cmd(upload_file, backup_bucket_path)


if __name__ == "__main__":
    default_src = os.environ.get("GS_BACKUP_SRC")
    default_dest = os.environ.get("GS_BACKUP_DEST")
    default_name = os.environ.get("GS_BACKUP_FILENAME")

    encryption_key = os.environ.get("GS_ENCRYPTION_KEY")

    args = ChattyArgParser(description=__doc__)
    args.add_argument('-f', '--from-bucket', type=str,
                      help="Source bucket URL prefix (e.g. gs://files.example.org/stuff); or set GS_BACKUP_SRC",
                      default=default_src,
                      required=default_src is None)
    args.add_argument('-t', '--to-bucket', type=str,
                      help="Destination bucket URL prefix (e.g. gs://example-org-backups/files); or set GS_BACKUP_DEST",
                      default=default_dest,
                      required=default_dest is None)
    args.add_argument('-n', '--filename', type=str,
                      help="Object name to create, will be prefixed with timestamp (e.g. stuff.tar.gz); or set GS_BACKUP_FILENAME",
                      default=default_name,
                      required=default_name is None)
    args.add_argument('-e', '--encryption-key-path', type=str,
                      help="File containing key ('CMEK') for uploaded object; or set GS_ENCRYPTION_KEY to value of key",
                      required=encryption_key is None)
    args.add_argument('-g', '--gsutil', type=str,
                      help="Path to gsutil binary on disk",
                      default="/usr/bin/gsutil",
                      required=False)
    args.add_argument('-s', '--svc-acct-key', type=str,
                      help="Full path to GCP service account key",
                      required=False)
    args.add_argument('-v', '--verbose', action='store_true',
                      help='Increase verbosity',
                      default=False,
                      required=False)

    parsed_args = args.parse_args()

    # Set verbose output
    if parsed_args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.debug("ARGS piped in: {}".format(parsed_args))

    if parsed_args.encryption_key_path is not None:
        try:
            with open(parsed_args.encryption_key_path) as f:
                encryption_key = f.read()
        except:
            logger.error("Could not read encryption key from {}".format(parsed_args.encryption_key_path))
            sys.exit(1)

    backup = GCPBucketBackup(
        parsed_args.from_bucket,
        parsed_args.to_bucket,
        encryption_key,
        parsed_args.filename,
        parsed_args.gsutil,
    )

    # If a service account key is provided lets initialize gcloud first
    if parsed_args.svc_acct_key:
        backup.initialize_svc_acct(parsed_args.svc_acct_key)

    # Local directory filled with rsync'd files
    backup_local_dir = backup.rsync_source_bucket()

    # Create tarfile and grab file location
    local_tar = backup.tar_directory(backup_local_dir)

    # Upload backup to final destination
    backup.upload_encrypted_timestamp_file(local_tar)
