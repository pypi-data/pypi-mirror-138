import os

from django.test import TestCase
from google.protobuf import json_format

from fakeapp.grpc import fakeapp_pb2
from fakeapp.grpc.fakeapp_pb2_grpc import (
    BasicControllerStub,
    add_BasicControllerServicer_to_server,
)
from fakeapp.services.basic_service import BasicService

from .grpc_test_utils.fake_grpc import FakeGRPC


class TestAsyncModelService(TestCase):
    def setUp(self):
        os.environ["GRPC_ASYNC"] = "True"
        self.fake_grpc = FakeGRPC(
            add_BasicControllerServicer_to_server, BasicService.as_servicer()
        )

    def tearDown(self):
        os.environ["GRPC_ASYNC"] = ""
        self.fake_grpc.close()

    def test_async_fetch_data_for_user(self):
        grpc_stub = self.fake_grpc.get_fake_stub(BasicControllerStub)
        request = fakeapp_pb2.BasicFetchDataForUserRequest(user_name="test")
        response = grpc_stub.FetchDataForUser(request=request)

        self.assertEqual(response.user_name, "test")
        user_data_dict = json_format.MessageToDict(response.user_data)
        self.assertEqual(
            user_data_dict,
            {
                "email": "fake_email@email.com",
                "birth_date": "25/01/1996",
                "slogan": "Do it better",
            },
        )
