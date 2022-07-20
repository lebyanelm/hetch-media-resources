from hetch_utilities.models.data import DataModel

class FileUploadModel(DataModel):
    def __init__(self, data):
        super().__init__()

        self.original_filename = data.get("original_name")
        self.filename = data.get("filename")
        self.alt_name = data.get("alt_name")
        self.credits_name = data.get("credits_name")
        self.fpath = data.get("fpath")
        self.url_link = data.get("url_link")
        self.uploader_uid = data.get("uploader_uid")
        self.mime_type = data.get("mime_type")
        self.is_virus_safe = None

        self.key = self.filename

        self.__schema_version__ = 1.0