from typing import Optional, List, Any

from pydantic import BaseModel

from deeploy.enums import ModelType, ExplainerType


class CreateVersion(BaseModel):
    """
    """
    repository_id: str
    branch_name: Optional[str]
    commit: Optional[str]
    commit_message: Optional[str]
    has_example_input: Optional[bool] = False
    example_input: Optional[List[Any]]
    example_output: Optional[Any]
    input_tensor_size: Optional[str]
    output_tensor_size: Optional[str]
    model_type: ModelType
    model_serverless: Optional[bool] = False
    explainer_type: ExplainerType
    explainer_serverless: Optional[bool] = False
