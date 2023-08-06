from typing import Dict, Optional
from marshmallow import Schema, fields, validate, validates, ValidationError


class CloudProviderConfigValidator(Schema):
    # TODO: It has to be reworked as soon as we manage multiple cloud provider
    cloud_provider = fields.String(required=True, validate=validate.OneOf(["aws"]))
    region_name = fields.String(required=True)
    aws_access_key_id = fields.String()
    aws_secret_access_key = fields.String()
    endpoint_url = fields.String()
    skip_queue_mapping_verification = fields.Boolean(default=False)

    @validates("endpoint_url")
    def validate_endpoint_url(self, value: Optional[str]):
        if value is None:
            return
        if not value.startswith(("http", "https")):
            raise ValidationError("endpoint url must be in http or https")


class CloudQueueWorkerValidator(Schema):
    queue_mapping = fields.Dict(required=True)
    concurrency = fields.Integer(required=True)
    cloud_provider_config = fields.Nested(CloudProviderConfigValidator, required=True)

    @validates("queue_mapping")
    def validate_queue_mapping(self, value: Dict[str, str]):
        if not value:
            raise ValidationError("queue_mapping parameter is missing or empty in the config")
