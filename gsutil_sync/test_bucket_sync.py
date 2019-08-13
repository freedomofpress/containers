import unittest.mock
from bucket_sync import GCPBucketBackup

GENERIC_ARGS = dict(src_bucket="gs://src-bucket/dir/",
                    backup_bucket="gs://backup-bucket/dir", encrypt_key="124124213123")


def test_rsync_cmd_cli_str():
    """Throw different options against rsync function to determine called command"""

    backup = GCPBucketBackup(**GENERIC_ARGS)
    with unittest.mock.patch("subprocess.check_call") as mock_subp:
        # With dry-run
        backup.rsync_cmd(backup.src, backup.dst, dry=True)
        mock_subp.assert_called_with(
            [backup.gsutil_path, "-m", "rsync", "-r", "-n", "-d",
                GENERIC_ARGS['src_bucket'], GENERIC_ARGS['backup_bucket']]
        )

        # Without dry-run
        backup.rsync_cmd(backup.src, backup.dst)
        mock_subp.assert_called_with(
            [backup.gsutil_path, "-m", "rsync", "-r", "-d",
                GENERIC_ARGS['src_bucket'], GENERIC_ARGS['backup_bucket']]
        )

        # Lets try swapping out the gsutil config path
        backup.gsutil_path = '/bin/gsutil'
        backup.rsync_cmd(backup.src, backup.dst)
        mock_subp.assert_called_with(
            ['/bin/gsutil', "-m", "rsync", "-r", "-d",
                GENERIC_ARGS['src_bucket'], GENERIC_ARGS['backup_bucket']]
        )
