import time

import authone


def epoch_time_now():
    return int(time.time())


def apply_did_token_nbf_grace_period(timestamp):
    return timestamp - authone.did_token_nbf_grace_period_s
