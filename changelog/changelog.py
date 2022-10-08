import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List

TEMPLATE = """# Change Log

All notable changes to %(project)s project will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

%(releases)s

%(links)s
"""
RELEASE_TEMPLATE = """## [%(release_version)s] - %(date)s
%(changes)s
"""
DATE_FORMAT = "%y-%m-%d"


class TypeOfChange(Enum):
    ADDED = auto()
    CHANGED = auto()
    DEPRECATED = auto()
    REMOVED = auto()
    FIXED = auto()
    SECURITY = auto()


@dataclass
class Release:
    name: str
    date: datetime
    changes: Dict[TypeOfChange, List[str]]


@dataclass
class TopSection:
    title: str
    description: str


class ChangeLog:
    def __init__(self, repository: str, releases: List[Release]):
        self.repository = repository
        self.releases = releases

    def dumps(self) -> str:
        project_name = "this"
        match = re.match(r"(.*://github.com/[^\/]+\/([^\/]+))", self.repository)
        url = ""
        if match:
            groups = match.groups()
            project_name = groups[1]
            url = ":".join(("https", groups[0].split(":", maxsplit=1)[-1]))
        release_notes = []
        links = []
        for i, release in enumerate(self.releases):
            version = release.name
            date = release.date.strftime(DATE_FORMAT)
            changes = []
            for type_of_change, change in sorted(
                release.changes.items(), key=lambda x: x[0].value
            ):
                type_string = f"### {type_of_change.name.capitalize()}"
                entries = [f"- {entry}" for entry in change]
                changes.append("%s\n%s" % (type_string, "\n".join(entries)))
            release_note = RELEASE_TEMPLATE % dict(
                release_version=version, date=date, changes="".join(changes)
            )
            release_notes.append(release_note)
            try:
                prev = self.releases[i + 1].name
            except IndexError:
                prev = None
            link = ""
            if version == "Unreleased":
                link = "/".join(
                    (
                        url,
                        f"compare/{prev if prev else 'HEAD~1'}...HEAD",
                    )
                )
            elif not prev:
                link = "/".join((url, f"releases/tag/{version}"))
            else:
                link = "/".join((url, f"compare/{prev}...{version}"))
            links.append(f"[{version}]: {link}")

        return TEMPLATE % dict(
            project=project_name,
            releases="\n".join(release_notes),
            links="\n".join(links),
        )
