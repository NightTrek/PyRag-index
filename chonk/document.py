
class Document:
    """
    A Document is a reference to a indexed File. It includes information about its relations to other index documents as well as metadata.
    """
    def __init__(self, title: str, name: str, file_path: str, doc_type: str, chunk_ids: list, summary: str, full_text: str):
        self.name = name
        self.title = title
        self.file_path = file_path
        self.doc_type = doc_type
        self.chunk_ids = chunk_ids
        self.summary = summary

    
    def get_Chunks(self):
        """
        Returns a list of Chunks that are associated with this document.
        """
        return [Chunk(self.chunk_ids[i], self.chunk_ids[i+1]) for i in range(0, len(self.chunk_ids), 2)]
