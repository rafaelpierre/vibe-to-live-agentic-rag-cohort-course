import click
from .evals.pipeline import run_synthetic_relevance_pipeline


@click.group()
def cli():
    """CLI for running evaluation pipelines."""
    pass


@cli.command()
@click.option(
    "--max-queries",
    default=20,
    type=int,
    help="Maximum number of queries to generate (default: 20)",
)
def relevance(max_queries: int):
    """Run the synthetic relevance evaluation pipeline."""
    click.echo(f"Running synthetic relevance pipeline with max_queries={max_queries}")
    results = run_synthetic_relevance_pipeline(max_queries=max_queries)
    click.echo(f"Pipeline completed. Generated {len(results)} results.")
    for idx, result in enumerate(results, 1):
        click.echo(f"{idx}. {result}")


if __name__ == "__main__":
    cli()
