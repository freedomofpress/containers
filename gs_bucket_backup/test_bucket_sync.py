import unittest.mock
from bucket_sync import GCPBucketBackup


class TestBucketSync(object):
    def setup_class(self):
        self.GENERIC_ARGS = dict(src_bucket="gs://src-bucket/dir/",
                                 backup_bucket="gs://backup-bucket/dir",
                                 encrypt_key="124124213123",
                                 file_suffix="siteapp",
                                 gsutil_path="/usr/local/bin/gsutil")
        self.gen_backup_obj = GCPBucketBackup(**self.GENERIC_ARGS)

    def test_rsync_cmd_cli_str(self):
        """Throw different options against rsync function to determine called command"""

        backup = self.gen_backup_obj

        with unittest.mock.patch("subprocess.check_output") as mock_subp:

            assert_call_skel = [backup.gsutil_path, "-m", "rsync", "-r", "-d",
                                self.GENERIC_ARGS['src_bucket'], self.GENERIC_ARGS['backup_bucket']]
            assert_call_kws = dict(stderr=-2, shell=False)
            # With dry-run
            backup.rsync_cmd(backup.src, backup.dst, dry=True)
            cmd_dry = assert_call_skel[:4] + ["-n"] + assert_call_skel[4:]
            mock_subp.assert_called_with(cmd_dry, **assert_call_kws)

            # Without dry-run
            backup.rsync_cmd(backup.src, backup.dst)
            mock_subp.assert_called_with(assert_call_skel, **assert_call_kws)

            # Lets try swapping out the gsutil config path
            backup.gsutil_path = '/bin/gsutil'
            cmd_binswap = [backup.gsutil_path] + assert_call_skel[1:]
            backup.rsync_cmd(backup.src, backup.dst)
            mock_subp.assert_called_with(cmd_binswap, **assert_call_kws)

    def test_tar_invocation(self):
        """Ensure we are calling tar with the expected path and returning a full tarfile path"""

        with unittest.mock.patch("tarfile.open") as mock_tar:
            tar_action = self.gen_backup_obj.tar_directory("/tmp/dir")
            full_bucket_path = "/tmp/dir/src-bucket.tar.gz"

            assert tar_action == full_bucket_path
            mock_tar.assert_called_once_with(full_bucket_path, 'w:gz')
