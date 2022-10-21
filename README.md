# slack-utils

> The collection of Slack Utilities

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/mrmoneyc/slack-utils/blob/master/LICENSE)

## Requirement

* Python 3
* [Slack App](https://api.slack.com/apps) User / Bot Token with the required scope listed below (refer to **Creating an app**, **Requesting scopes** and **Installing the app to a workspace** sections in this [tutorial](https://api.slack.com/authentication/basics)), and some action needs admin permission.
  * `users:read`
  * `users:read.email`
  * `users.profile:write`

## Prerequisite

```shell
pip install -r requirements.txt
```

## Configuration

Edit `const.py` file:

```python
class Const(metaclass=ConstMeta):
    # Slack App OAuth Tokens
    USER_TOKEN = "xoxp-xxxxx-ooooo"
    BOT_TOKEN = "xoxb-xxxxx-ooooo"

    # Use user token when set True
    USE_USER_TOKEN = True

    # Wait time (sec) for Slack API call
    REQUEST_DELAY = 1.2

    # Log Verbosity
    LOG_LEVEL = logging.INFO
```

## Usage

### Batch update user's email domain

```shell
# Modify email from user@old-domain.com to user@new-domain.com
python ./batch_modify_user_email_domain.py old-domain.com new-domain.com

# Dry run
python ./batch_modify_user_email_domain.py old-domain.com new-domain.com --dryrun
```

For more usage, use `-h` or `--help`
