# hugrverse-actions

Reusable workflows for projects in the hugrverse.

To call use workflow in your project, add it to a workflow in your project's `.github/workflows` directory.
See the workflow list below for usage instructions, including the workflow triggers.

Some workflows may require additional inputs, such as a [`GITHUB_PAT`] to
access the GitHub API. For these we [generate fine-grained access
tokens](https://github.com/settings/personal-access-tokens/new) with the
@hugrbot bot account, which must be stored in the repository secrets.

## Workflows

The following workflows are available:

- [`drop-cache`](#drop-cache): Drops the cache for a branch when a pull request is closed.
- [`pr-title`](#pr-title): Checks the title of pull requests to ensure they follow the conventional commits format.
- [`rs-semver-checks`](#rs-semver-checks): Runs `cargo-semver-checks` on a PR against the base branch, and reports back if there are breaking changes.
- [`add-to-project`](#add-to-project): Adds new issues to a GitHub project board when they are created.

### [`drop-cache`](https://github.com/CQCL/hugrverse-actions/blob/main/.github/workflows/drop-cache.yml)

Drops the cache for a branch when a pull request is closed. This helps to avoid
cache pollution by freeing up some of github's limited cache space.

#### Usage
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

### [`pr-title`](https://github.com/CQCL/hugrverse-actions/blob/main/.github/workflows/pr-title.yml)

Checks the title of pull requests to ensure they follow the [conventional
commits](https://www.conventionalcommits.org/en/v1.0.0/) format. If the title
does not follow the conventional commits, a comment is posted on the PR to help
the user fix it.

#### Usage
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

#### Token Permissions

The fine-grained `GITHUB_PAT` secret must include the following permissions:

| Permission | Access |
| --- | --- |
| Pull requests | Read and write |

### [`rs-semver-checks`](https://github.com/CQCL/hugrverse-actions/blob/main/.github/workflows/rs-semver-checks.yml)

Runs `cargo-semver-checks` on a PR against the base branch, and reports back if
there are breaking changes.
Suggests adding a breaking change flag to the PR title if necessary. 

#### Usage
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

#### Token Permissions

The fine-grained `GITHUB_PAT` secret must include the following permissions:

| Permission | Access |
| --- | --- |
| Pull requests | Read and write |


### [`add-to-project`](https://github.com/CQCL/hugrverse-actions/blob/main/.github/workflows/add-to-project.yml)

Adds new issues to a GitHub project board when they are created.

#### Usage
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

#### Token Permissions

The fine-grained `GITHUB_PAT` secret must include the following permissions:

| Permission | Access |
| --- | --- |
| Projects | Read and write |
| Pull requests | Read |

Note that fine-grained access tokens cannot grant permissions to projects and repositories in different organisations simultaneously.
In those cases, you will need an unrestricted _classical_ github token instead. 
