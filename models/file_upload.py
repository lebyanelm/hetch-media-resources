from random_utilities.models import DataModel

class FileUploadModel(DataModel):
    def __init__(self, data):
        super().__init__()

        self.original_filename = data.get("original_name")
        self.filename = data.get("filename")
        self.alternate_name = data.get("alternate_name")
        self.credits_name = data.get("credits_name")
        self.file_path = data.get("file_path")
        self.file_size = data.get("file_size")
        self.url_link = data.get("url_link")
        self.uploader_id = data.get("uploader_id")
        self.mime_type = data.get("mime_type")
        self.is_virus_safe = None
        self.scan_results = None

        self.key = self.filename

        self.__schema_version__ = 1.0