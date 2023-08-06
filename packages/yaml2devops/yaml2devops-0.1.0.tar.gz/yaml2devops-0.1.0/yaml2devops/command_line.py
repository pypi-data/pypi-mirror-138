import click

from yaml2devops.core import TestSuite, gen_tasks, get_suite


@click.option("--org", prompt="input azure devops organization name", help="azure devops organization name")
@click.option("--project", prompt="input azure devops project_id", help="azure devops project_id")
@click.option("--pat", prompt="input azure devops personal access token", help="azure devops personal access token")
@click.option("--file", prompt="input yaml file path", help="yaml file path")
@click.command()
def cli(org, project, pat, file):
    test_suite: TestSuite = get_suite(file)
    gen_tasks(test_suite, org, project, pat)
    print("success")


if __name__ == "__main__":
    cli()
