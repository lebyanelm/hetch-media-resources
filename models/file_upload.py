class FileUploadModel():
    def __init__(self, original_filename:str, filename:str, url:str, uid:str):
        self.original_filename = original_filename
        self.filename = filename
        self.url = url
        self.uid = uid

        self.__schema_version__ = 1.0