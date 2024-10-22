# hugrverse-actions

Reusable workflows for projects in the hugrverse.

To call use workflow in your project, add it to a workflow in your project's `.github/workflows` directory.
See the workflow list below for usage instructions, including the workflow triggers.

Some workflows may require additional inputs, such as a [`GITHUB_PAT`] to
access the GitHub API. For these we [generate fine-grained access
tokens](https://github.com/settings/personal-access-tokens/new) with the
@hugrbot bot account, which must be stored in the repository secrets.

The following workflows are available:

- [`add-to-project`](#add-to-project): Adds new issues to a GitHub project board when they are created.
- [`coverage-trend`](#coverage-trend): Checks the coverage trend for the project, and produces a summary that can be posted to slack.
- [`drop-cache`](#drop-cache): Drops the cache for a branch when a pull request is closed.
- [`pr-title`](#pr-title): Checks the title of pull requests to ensure they follow the conventional commits format.
- [`rs-semver-checks`](#rs-semver-checks): Runs `cargo-semver-checks` on a PR against the base branch, and reports back if there are breaking changes.

## [`add-to-project`](https://github.com/CQCL/hugrverse-actions/blob/main/.github/workflows/add-to-project.yml)

Adds new issues to a GitHub project board when they are created.

### Usage
```yaml
name: Add issues to project board
on:
  issues:
    types:
      - opened

jobs:
    add-to-project:
        uses: CQCL/hugrverse-actions/.github/workflows/add-to-project.yml@main
        with:
            project-url: https://github.com/orgs/{your-org}/projects/{project-id}
        secrets:
            GITHUB_PAT: ${{ secrets.ADD_TO_PROJECT_PAT }}
```

### Token Permissions

The fine-grained `GITHUB_PAT` secret must include the following permissions:

| Permission | Access |
| --- | --- |
| Projects | Read and write |
| Pull requests | Read |

Note that fine-grained access tokens cannot grant permissions to projects and repositories in different organisations simultaneously.
In those cases, you will need an unrestricted _classical_ github token instead. 

## [`coverage-trend`](https://github.com/CQCL/hugrverse-actions/blob/main/.github/workflows/coverage-trend.yml)

Compares the project coverage on [Codecov](https://codecov.io/) against the last workflow run,
and produces a summary of the changes that can be posted to slack.

If the project didn't have new commits that changed the coverage since the last run,
the `should_notify` output will be set to `false` and the `msg` output will be empty.

### Usage
```yaml
name: Notify coverage changes
on:
  schedule:
    # 04:00 every Monday
    - cron: '0 4 * * 1'
  workflow_dispatch: {}

jobs:
    coverage-trend:
        uses: CQCL/hugrverse-actions/.github/workflows/coverage-trend.yml@main
        secrets:
            CODECOV_GET_TOKEN: ${{ secrets.CODECOV_GET_TOKEN }}
    # Post the result somewhere.
    notify-slack:
      needs: coverage-trend
      runs-on: ubuntu-latest
      if: needs.coverage-trend.outputs.should_notify == 'true'
      steps:
        - name: Send notification
          uses: slackapi/slack-github-action@v1.27.0
          with:
            channel-id: "SOME CHANNEL ID"
            slack-message: ${{ needs.coverage-trend.outputs.msg }}
          env:
            SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

### Outputs

- `should_notify`: Whether there has been a change in coverage since the last run, which we can post about.
- `msg`: A message summarising the coverage changes. This is intended to be posted to slack.

### Token Permissions

`CODECOV_GET_TOKEN` is a token generated by Codecov to access the repository's coverage data.

## [`drop-cache`](https://github.com/CQCL/hugrverse-actions/blob/main/.github/workflows/drop-cache.yml)

Drops the cache for a branch when a pull request is closed. This helps to avoid
cache pollution by freeing up some of github's limited cache space.

### Usage
```yaml
name: cleanup caches by a branch
on:
  pull_request:
    types:
      - closed

jobs:
    drop-cache:
        uses: CQCL/hugrverse-actions/.github/workflows/drop-cache.yml@main
```

## [`pr-title`](https://github.com/CQCL/hugrverse-actions/blob/main/.github/workflows/pr-title.yml)

Checks the title of pull requests to ensure they follow the [conventional
commits](https://www.conventionalcommits.org/en/v1.0.0/) format. If the title
does not follow the conventional commits, a comment is posted on the PR to help
the user fix it.

### Usage
```yaml
name: Check Conventional Commits format
on:
  pull_request_target:
    branches:
      - main
    types:
      - opened
      - edited
      - synchronize
      - labeled
      - unlabeled
  merge_group:
    types: [checks_requested]

jobs:
    check-title:
        uses: CQCL/hugrverse-actions/.github/workflows/pr-title.yml@main
        secrets:
            GITHUB_PAT: ${{ secrets.GITHUB_PAT }}
```

### Token Permissions

The fine-grained `GITHUB_PAT` secret must include the following permissions:

| Permission | Access |
| --- | --- |
| Pull requests | Read and write |

## [`rs-semver-checks`](https://github.com/CQCL/hugrverse-actions/blob/main/.github/workflows/rs-semver-checks.yml)

Runs `cargo-semver-checks` on a PR against the base branch, and reports back if
there are breaking changes.
Suggests adding a breaking change flag to the PR title if necessary. 

### Usage
```yaml
name: Rust Semver Checks
on:
  pull_request:
    branches:
      - main

jobs:
    rs-semver-checks:
        uses: CQCL/hugrverse-actions/.github/workflows/rs-semver-checks.yml@main
        secrets:
            GITHUB_PAT: ${{ secrets.GITHUB_PAT }}
```

The workflow compares against the base branch of the PR by default. Use the `baseline-rev` input to specify a different base commit.

### Token Permissions

The fine-grained `GITHUB_PAT` secret must include the following permissions:

| Permission | Access |
| --- | --- |
| Pull requests | Read and write |

