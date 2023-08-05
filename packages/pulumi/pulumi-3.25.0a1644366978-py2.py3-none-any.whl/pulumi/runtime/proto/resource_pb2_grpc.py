# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import provider_pb2 as provider__pb2
from . import resource_pb2 as resource__pb2


class ResourceMonitorStub(object):
    """ResourceMonitor is the interface a source uses to talk back to the planning monitor orchestrating the execution."""

    def __init__(self, channel):
        """Constructor.

        Args:
          channel: A grpc.Channel.
        """
        self.SupportsFeature = channel.unary_unary(
            "/pulumirpc.ResourceMonitor/SupportsFeature",
            request_serializer=resource__pb2.SupportsFeatureRequest.SerializeToString,
            response_deserializer=resource__pb2.SupportsFeatureResponse.FromString,
        )
        self.Invoke = channel.unary_unary(
            "/pulumirpc.ResourceMonitor/Invoke",
            request_serializer=provider__pb2.InvokeRequest.SerializeToString,
            response_deserializer=provider__pb2.InvokeResponse.FromString,
        )
        self.StreamInvoke = channel.unary_stream(
            "/pulumirpc.ResourceMonitor/StreamInvoke",
            request_serializer=provider__pb2.InvokeRequest.SerializeToString,
            response_deserializer=provider__pb2.InvokeResponse.FromString,
        )
        self.Call = channel.unary_unary(
            "/pulumirpc.ResourceMonitor/Call",
            request_serializer=provider__pb2.CallRequest.SerializeToString,
            response_deserializer=provider__pb2.CallResponse.FromString,
        )
        self.ReadResource = channel.unary_unary(
            "/pulumirpc.ResourceMonitor/ReadResource",
            request_serializer=resource__pb2.ReadResourceRequest.SerializeToString,
            response_deserializer=resource__pb2.ReadResourceResponse.FromString,
        )
        self.RegisterResource = channel.unary_unary(
            "/pulumirpc.ResourceMonitor/RegisterResource",
            request_serializer=resource__pb2.RegisterResourceRequest.SerializeToString,
            response_deserializer=resource__pb2.RegisterResourceResponse.FromString,
        )
        self.RegisterResourceOutputs = channel.unary_unary(
            "/pulumirpc.ResourceMonitor/RegisterResourceOutputs",
            request_serializer=resource__pb2.RegisterResourceOutputsRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )


class ResourceMonitorServicer(object):
    """ResourceMonitor is the interface a source uses to talk back to the planning monitor orchestrating the execution."""

    def SupportsFeature(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Invoke(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def StreamInvoke(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Call(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ReadResource(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def RegisterResource(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def RegisterResourceOutputs(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_ResourceMonitorServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "SupportsFeature": grpc.unary_unary_rpc_method_handler(
            servicer.SupportsFeature,
            request_deserializer=resource__pb2.SupportsFeatureRequest.FromString,
            response_serializer=resource__pb2.SupportsFeatureResponse.SerializeToString,
        ),
        "Invoke": grpc.unary_unary_rpc_method_handler(
            servicer.Invoke,
            request_deserializer=provider__pb2.InvokeRequest.FromString,
            response_serializer=provider__pb2.InvokeResponse.SerializeToString,
        ),
        "StreamInvoke": grpc.unary_stream_rpc_method_handler(
            servicer.StreamInvoke,
            request_deserializer=provider__pb2.InvokeRequest.FromString,
            response_serializer=provider__pb2.InvokeResponse.SerializeToString,
        ),
        "Call": grpc.unary_unary_rpc_method_handler(
            servicer.Call,
            request_deserializer=provider__pb2.CallRequest.FromString,
            response_serializer=provider__pb2.CallResponse.SerializeToString,
        ),
        "ReadResource": grpc.unary_unary_rpc_method_handler(
            servicer.ReadResource,
            request_deserializer=resource__pb2.ReadResourceRequest.FromString,
            response_serializer=resource__pb2.ReadResourceResponse.SerializeToString,
        ),
        "RegisterResource": grpc.unary_unary_rpc_method_handler(
            servicer.RegisterResource,
            request_deserializer=resource__pb2.RegisterResourceRequest.FromString,
            response_serializer=resource__pb2.RegisterResourceResponse.SerializeToString,
        ),
        "RegisterResourceOutputs": grpc.unary_unary_rpc_method_handler(
            servicer.RegisterResourceOutputs,
            request_deserializer=resource__pb2.RegisterResourceOutputsRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "pulumirpc.ResourceMonitor", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
