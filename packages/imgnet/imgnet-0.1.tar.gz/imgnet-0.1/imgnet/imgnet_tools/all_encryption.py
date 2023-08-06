import base64


def decodeFile(fileString, filePath):
    """Decode an image from a base64 string and write it to a file.
    Args:
        imgstring ([string]): [Image path to be decode]
        fileName ([string]): [Name of the file]
    """
    print(filePath)
    zipFile = base64.b64decode(fileString)
    # return zipFile
    with open(filePath, 'wb') as f:
        f.write(zipFile)
        f.close()
        print("file closed")


def encodeImageIntoBase64(croppedImagePath):
    """Decode an image from a base64 string and write it to a file.
    Args:
        croppedImagePath ([string]): [Image path to be decode]

    """
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())


def encodeModel(modelPath):
    """Encode a file from base64 and return it

    Args:
        modelPath ([String]): [Model path to be encode]
    """
    with open(modelPath, "rb") as f:
        return base64.b64decode(f.read())