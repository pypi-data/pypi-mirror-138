"""
    MastodonAmnesia - deletes old Mastodon toots
    Copyright (C) 2021  Mark S Burgunder

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import argparse
import time
from logging import Logger
from math import ceil
from typing import Any
from typing import cast

import arrow
import httpx
from mastodon import MastodonRatelimitError
from rich import traceback

from mastodonamnesia import CODE_VERSION_MAJOR
from mastodonamnesia import CODE_VERSION_MINOR
from mastodonamnesia import CODE_VERSION_PATCH
from mastodonamnesia.control import Configuration

traceback.install(show_locals=True)


def main() -> None:
    """Main logic to run MastodonAmnesia."""

    parser = argparse.ArgumentParser(description="Delete old toots.")
    parser.add_argument(
        "-c", "--config-file", action="store", default="config.json", dest="config_file"
    )
    args = parser.parse_args()

    config = Configuration(config_file_name=args.config_file)

    logger = config.bot.logger
    mastodon = config.mastodon_config.mastodon

    now = arrow.now()
    oldest_to_keep = now.shift(seconds=-config.mastodon_config.delete_after)

    logger.info("Welcome to MastodonAmnesia")
    check_updates(logger)
    logger.info(
        "We are removing toots older than %s from %s@%s",
        oldest_to_keep,
        config.mastodon_config.base_url,
        config.mastodon_config.user_info.user_name,
    )

    max_toot_id, toots = skip_toots_to_keep(config, oldest_to_keep)

    # Delete toots
    toots_deleted = 0
    while True:
        if len(toots) == 0:
            break

        for toot in toots:
            try:
                toot_created_at = arrow.get(cast(int, toot.get("created_at")))
                logger.debug(
                    "Oldest to keep vs toot created at %s > %s (%s)",
                    oldest_to_keep,
                    toot_created_at,
                    bool(oldest_to_keep > toot_created_at),
                )
                if toot_created_at < oldest_to_keep:
                    mastodon.status_delete(toot.get("id"))
                    logger.info(
                        "Deleted toot %s from %s", toot.get("url"), toot_created_at
                    )
                    toots_deleted += 1

            except MastodonRatelimitError:
                need_to_wait = ceil(
                    mastodon.ratelimit_reset - mastodon.ratelimit_lastcall
                )
                logger.info("Deleted a total of %s toots", toots_deleted)
                logger.info(
                    'Need to wait %s seconds (until %s) to let server "cool down"',
                    need_to_wait,
                    arrow.get(mastodon.ratelimit_reset),
                )
                time.sleep(need_to_wait)

        # Get More toots
        toots = mastodon.account_statuses(
            id=config.mastodon_config.user_info.account_id,
            limit=10,
            max_id=max_toot_id,
        )

    logger.info("All old toots deleted! Total of %s toots deleted", toots_deleted)


def skip_toots_to_keep(
    config: Configuration, oldest_to_keep: arrow.Arrow
) -> tuple[int, list[dict[str, Any]]]:
    """Method to skip over toots that should not yet be deleted.

    :param config: Configuration object for MastodonAmnesia
    :param oldest_to_keep: arrow object of date of oldest toot we want to keep
    :return: tuple consisting of that toot id of the oldest toot to keep and
    List of toots
    """
    logger = config.bot.logger
    mastodon = config.mastodon_config.mastodon
    toots = mastodon.account_statuses(
        id=config.mastodon_config.user_info.account_id, limit=10
    )
    max_toot_id = toots[-1].get("id") if len(toots) > 0 else None
    # Find first toot that needs to be deleted
    logger.info("Finding first toot old enough to delete.")
    while True:
        if len(toots) == 0:
            break

        last_toot_created_at = arrow.get(toots[-1].get("created_at"))
        logger.debug("Oldest toot in this batch is from %s", last_toot_created_at)
        if last_toot_created_at < oldest_to_keep:
            break

        try:
            toots = mastodon.account_statuses(
                id=config.mastodon_config.user_info.account_id,
                limit=10,
                max_id=max_toot_id,
            )
            max_toot_id = toots[-1].get("id") if len(toots) > 0 else None

        except MastodonRatelimitError:
            need_to_wait = ceil(mastodon.ratelimit_reset - mastodon.ratelimit_lastcall)
            logger.info(
                'Need to wait %s seconds (until %s) to let server "cool down"',
                need_to_wait,
                arrow.get(mastodon.ratelimit_reset),
            )
            time.sleep(need_to_wait)
    return max_toot_id, toots


def check_updates(logger: Logger) -> None:
    """Check of there is a newer version of MastodonAmnesia available on
    gitlab.

    :param logger: Logger object to be able to send message to log
    :return: None
    """
    try:
        response = httpx.get(
            "https://codeberg.org/MarvinsMastodonTools/mastodonamnesia"
            "/raw/branch/main/update-check/release-version.txt"
        )
        response.raise_for_status()
        repo_version = response.content.decode("utf-8").strip().partition(".")
        repo_version_major = int(repo_version[0].strip())
        repo_minor_version_to_check = repo_version[2].strip().partition(".")
        repo_version_minor = int(repo_minor_version_to_check[0].strip())
        repo_version_patch = int(repo_minor_version_to_check[2].strip())

        code_version_numeric = CODE_VERSION_MAJOR * 1000000
        code_version_numeric += CODE_VERSION_MINOR * 1000
        code_version_numeric += CODE_VERSION_PATCH
        repo_version_numeric = repo_version_major * 1000000
        repo_version_numeric += repo_version_minor * 1000
        repo_version_numeric += repo_version_patch

        if code_version_numeric >= repo_version_numeric:
            logger.info(
                "MastodonAmnesia v%s.%s.%s is up to date.",
                CODE_VERSION_MAJOR,
                CODE_VERSION_MINOR,
                CODE_VERSION_PATCH,
            )
        else:
            logger.warning(
                "New version of MastodonAmnesia  (v%s.%s.%s) is available!",
                repo_version_major,
                repo_version_minor,
                repo_version_patch,
            )
            logger.warning(
                "(You have v%s.%s.%s)",
                CODE_VERSION_MAJOR,
                CODE_VERSION_MINOR,
                CODE_VERSION_PATCH,
            )
            logger.warning(
                "Latest available at: https://codeberg.org/MarvinsMastodonTools"
                "/mastodonamnesia"
            )
    except (httpx.ConnectError, httpx.HTTPError) as update_check_error:
        logger.warning(
            "Encountered error while checking for updates: %s", update_check_error
        )


# run main programs
if __name__ == "__main__":
    main()
