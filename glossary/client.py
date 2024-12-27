import grpc
import glossary_pb2
import glossary_pb2_grpc

def run():
    with grpc.insecure_channel("server:50051") as channel:
        stub = glossary_pb2_grpc.GlossaryStub(channel)
        # Добавляем термин
        response = stub.AddTerm(glossary_pb2.Term(keyword="example", description="This is an example term"))
        print(response.message)

        # Получаем термин
        term = stub.GetTerm(glossary_pb2.TermRequest(keyword="example"))
        print(f"Keyword: {term.keyword}, Description: {term.description}")

        # Список всех терминов
        terms = stub.ListTerms(glossary_pb2.Empty())
        for t in terms.terms:
            print(f"Keyword: {t.keyword}, Description: {t.description}")

if __name__ == "__main__":
    run()
