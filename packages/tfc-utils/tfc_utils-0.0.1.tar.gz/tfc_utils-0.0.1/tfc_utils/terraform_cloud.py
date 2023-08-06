from terrasnek.api import TFC


def get_workspace_output(tfc: TFC, org_name: str, workspace_name: str, output_name: str) -> str:
    tfc.set_org(org_name=org_name)
    response = tfc.workspaces.show(workspace_name=workspace_name)
    current_state_version = response["data"]["relationships"]["current-state-version"]
    current_state_version_id = current_state_version["data"]["id"]
    response = tfc.state_versions.list_state_version_outputs(current_state_version_id)
    for output in response["data"]:
        attrs = output["attributes"]
        if attrs["name"] == output_name:
            return attrs["value"]
    raise LookupError(
        f"Failed to find output in workspace: {org_name}/{workspace_name}/{output_name}"
    )
