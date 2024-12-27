from concurrent import futures
import grpc
import glossary_pb2
import glossary_pb2_grpc

TERMS = {}

class GlossaryService(glossary_pb2_grpc.GlossaryServicer):
    def GetTerm(self, request, context):
        term = TERMS.get(request.keyword)
        if not term:
            return glossary_pb2.TermResponse(keyword=request.keyword, description="Not found")
        return glossary_pb2.TermResponse(keyword=request.keyword, description=term)

    def AddTerm(self, request, context):
        TERMS[request.keyword] = request.description
        return glossary_pb2.Status(message="Term added successfully")

    def DeleteTerm(self, request, context):
        if request.keyword in TERMS:
            del TERMS[request.keyword]
            return glossary_pb2.Status(message="Term deleted successfully")
        return glossary_pb2.Status(message="Term not found")

    def ListTerms(self, request, context):
        return glossary_pb2.TermList(terms=[glossary_pb2.Term(keyword=k, description=v) for k, v in TERMS.items()])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServicer_to_server(GlossaryService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
