from deeploy.models.create_version import CreateVersion
from typing import Optional

from pydantic import BaseModel


class CreateDeployment(BaseModel):
    """Class that contains the options for creating a deployment
    """ # noqa
    name: str
    description: Optional[str]
    updating_to: CreateVersion

    def to_request_body(self):
        return {
            'name': self.name,
            'description': self.description,
            'updatingTo:': {
                'repositoryId': self.updating_to.repository_id,
                'exampleInput': self.updating_to.example_input,
                'exampleOutput': self.updating_to.example_output,
                'modelType': self.updating_to.model_type.value,
                'modelServerless': self.updating_to.model_serverless,
                'explainerType': self.updating_to.explainer_type.value,
                'explainerServerless': self.updating_to.explainer_serverless,
                'branchName': self.updating_to.branch_name,
                'commit': self.updating_to.commit,
            }
        }
