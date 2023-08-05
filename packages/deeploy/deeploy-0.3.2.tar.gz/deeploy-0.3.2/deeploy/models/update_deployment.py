from typing import Optional, Dict, Any

from pydantic import BaseModel

from deeploy.models.create_deployment import CreateVersion


class UpdateDeployment(BaseModel):
    """Class that contains the options for updating a model
    """  # noqa
    deployment_id: str
    name: Optional[str]
    kfserving_id: Optional[str]
    owner_id: Optional[str]
    public_url: Optional[str]
    description: Optional[str]
    status: Any
    updating_to: Optional[CreateVersion]

    def to_request_body(self) -> Dict:
        return {
            'id': self.deployment_id,
            'name': self.name,
            'kfServingId': self.kfserving_id,
            'ownerId': self.owner_id,
            'publicURL': self.public_url,
            'description': self.description,
            'updatingTo': {
                'repositoryId': self.updating_to.repository_id,
                'branchName': self.updating_to.branch_name,
                'commit': self.updating_to.commit,
                'commitMessage': self.updating_to.commit_message,
                'hasExampleInput': self.updating_to.has_example_input,
                'exampleInput': self.updating_to.example_input,
                'exampleOutput': self.updating_to.example_output,
                'inputTensorSize': self.updating_to.input_tensor_size,
                'outputTensorSize': self.updating_to.output_tensor_size,
                'modelType': self.updating_to.model_type.value,
                'modelServerless': self.updating_to.model_serverless,
                'explainerType': self.updating_to.explainer_type.value,
                'explainerServerless': self.updating_to.explainer_serverless,
            }
        }
