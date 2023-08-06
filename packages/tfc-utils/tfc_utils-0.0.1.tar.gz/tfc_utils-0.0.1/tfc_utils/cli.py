import typer
from terrasnek.api import TFC

from .terraform_cloud import get_workspace_output

app = typer.Typer()
tfc_token_opt = typer.Option(
    default=...,
    envvar=["TFE_TOKEN", "TFC_TOKEN"],
    help="Terraform Cloud access token",
    is_eager=True,
)


@app.command(name="get-output")
def get_output(
    workspace_ref: str = typer.Argument(
        default=...,
        help="Reference to a Terraform Cloud workspace in "
        "'<org_name>/<workspace_name>/<output_name>' format.",
    ),
    tfc_token: str = tfc_token_opt,
):
    """Get the value of a Terraform Cloud workspace output.

    For example: `python -m tfc_utils get-output hashicorp/primary-workspace/instance_ip_addr`
    """
    tfc = TFC(api_token=tfc_token)
    try:
        org, workspace, output = workspace_ref.split("/")
    except ValueError as e:
        raise ValueError(
            "Invalid Terraform output reference, must be in "
            "'<org_name>/<workspace_name>/<output_name>' format"
        ) from e
    output = get_workspace_output(tfc, org, workspace, output)
    typer.echo(output)


@app.callback()
def callback():
    """A CLI helper tool for Terraform Cloud."""
