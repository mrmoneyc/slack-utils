#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Required Scopes:
# - users:read
# - users:read.email
# - users.profile:write

import argparse

from logging import basicConfig, getLogger
from time import sleep

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from const import Const


# Initialize logger
basicConfig(format="%(asctime)s %(name)s: %(lineno)s [%(levelname)s]: " +
            "%(message)s (%(funcName)s)")
logger = getLogger(__name__)
logger.setLevel(Const.LOG_LEVEL)

# Initialize argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--dryrun",
                    action="store_false",
                    help="Don't apply email update")
parser.add_argument("orig_domain",
                    type=str,
                    help="Original domain")
parser.add_argument("new_domain",
                    type=str,
                    help="New domain")
args = parser.parse_args()


def init_slack_client():
    client = None

    if Const.USE_USER_TOKEN:
        logger.info("Use User Token")
        client = WebClient(token=Const.USER_TOKEN)
    else:
        logger.info("Use Bot Token")
        client = WebClient(token=Const.BOT_TOKEN)

    return client


def get_users(client):
    users = []

    try:
        logger.debug("Call users_list (Slack API)")
        users = client.users_list()["members"]
        # logger.debug(users)
        sleep(Const.REQUEST_DELAY)

    except SlackApiError as e:
        logger.error(e)
        sleep(Const.REQUEST_DELAY)

    return users


def get_userid_email_map(users):
    uid_email = [{
        "id": u["id"],
        "email": u["profile"]["email"]
    } for u in users if (
        not u["is_bot"]
        and u["id"] != "USLACKBOT"
        and not u["deleted"]
        and u["profile"]["email"].split("@")[1] == args.orig_domain)]

    return uid_email


def update_user_email(client, uid_emails):
    for u in uid_emails:
        new_email = u['email'].replace(args.orig_domain, args.new_domain)
        logger.info(f"Update {u['id']}: {u['email']} -> {new_email}")

        try:
            if args.dryrun:
                api_response = client.users_profile_set(
                    user=u["id"],
                    profile={"email": new_email})

                logger.debug(api_response)
        except SlackApiError as e:
            logger.error(e)

        sleep(Const.REQUEST_DELAY)


def main():
    logger.info("=== Start Batch Modify User Email Domain ===")
    logger.info(f"Update Email Domain from {args.orig_domain} to " +
                f"{args.new_domain}")

    client = init_slack_client()
    users = get_users(client)
    uid_emails = get_userid_email_map(users)
    update_user_email(client, uid_emails)

    logger.info("=== End Batch Modify User Email Domain ===")


if __name__ == "__main__":
    main()
