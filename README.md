# hugrverse-actions

Reusable workflows for projects in the hugrverse.

To call use workflow in your project, add it to a workflow in your project's `.github/workflows` directory.
See the workflow list below for usage instructions, including the workflow triggers.

Some workflows may require additional inputs, such as a [`GITHUB_TOKEN`] to
access the GitHub API. For these we [generate fine-grained access
tokens](https://github.com/settings/personal-access-tokens/new) with the
@hugrbot bot account, which must be stored in the repository secrets.

## Workflows

The following workflows are available:

### [`drop-cache`](https://github.com/CQCL/hugrverse-actions/blob/main/.github/workflows/drop-cache.yml)

Drops the cache for a branch when a pull request is closed. This helps to avoid
cache pollution by freeing up some of github's limited cache space.

Usage:
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

### [`pr-title`]()

Checks the title of pull requests to ensure they follow the [conventional
commits](https://www.conventionalcommits.org/en/v1.0.0/) format. If the title
does not follow the conventional commits, a comment is posted on the PR to help
the user fix it.

Usage:
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
            GITHUB_TOKEN: ${{ secrets.HUGRBOT_PAT }}
```

#### Token Permissions

The fine-grained `GITHUB_TOKEN` secret must include the following permissions:

| Permission | Access |
| --- | --- |
| Pull requests | Read and write |

If you do not want to generate a new token, you can have `github-actions` post the comments instead.
This requires giving additional permissions to the included github token:

```yaml
permissions:
  pull-requests: write
```