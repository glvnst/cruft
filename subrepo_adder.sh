#!/bin/sh

set -e

TZ_OFFSET="+0100"

usage() {
  printf '%s\n' \
    "Usage: $0 subrepo [...]" \
    "" \
    "This script is for adding the contents of subrepos to the current repo" \
    "while maintaining the GIT_AUTHOR_DATE and GIT_COMMITTER_DATE." \
    "" \
    "Example Steps:" \
    "" \
    "$ git init # if you haven't done this already" \
    "$ git clone some_repo.git" \
    "$ git clone some_other_repo.git" \
    "$ git clone some_third_repo.git" \
    "$ $0 some_repo some_other_repo some_third_repo" \
    "$ git remote add origin some_repo_url_for_this_container_repo.git" \
    "$ git push" \
    ""

  exit 1
}

warn() {
  printf '%s %s\n' "$(date '+%FT%T')" "$*" >&2
}

die() {
  warn "$* EXITING"
  exit 1
}

subrepos() {
  for git_dir in */.git; do
    dirname "$git_dir"
  done
}

subrepo_files() {
  subrepo="$1"; shift

  find "$subrepo" -mindepth 1 -not '(' -name .git -prune ')' -not -type d
}

subrepo_file_date() {
  filename="$1"; shift                # shlibs/examples/rpath_entries.py
  subrepo="${filename%%/*}"           # shlibs
  subrepo_filename="${filename#*/}"   # examples/rpath_entries.py

  ( cd "$subrepo" || die "couldn't cd to ${subrepo}"
    git log -1 --format="%at" -- "$subrepo_filename" || die "couldn't get git log for (${subrepo_filename}) (${filename})"
  ) || exit 1
}

main() {
  # you could automatically add all subdirs with this:
  # subrepos | while read -r repo; do

  [ -n "$*" ] || usage
  for repo in "$@"; do
    subrepo_files "$repo" | while read -r repo_file; do
      subrepo_file_date "$repo_file" | {
        read -r git_date
        export GIT_AUTHOR_DATE="$git_date $TZ_OFFSET"
        export GIT_COMMITTER_DATE="$GIT_AUTHOR_DATE"

        git add "$repo_file" || die "Couldn't git add ${repo_file}"
        git commit -m "adding ${repo_file}" || die "Couldn't git commit ${repo_file}"
      } || exit 1
    done
  done
}

main "$@"