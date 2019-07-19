'''
Module containing all cusstom exceptions used by the package. All exceptions related to this package
has the PCD prefix.

Please, if you used one of our methods and it raised an exception that doesn't have our PCD prefix
**and** it came from inside our files send us a ticket in this link:
https://github.com/Cerberus1746/PandaCoreData/issues

:author: Leandro (Cerberus1746) Benedet Garcia
'''


class PCDTypeGroupNotFound(Exception):
    """
    Exception raised if the ~Model or ~Template Group is not found.
    """


class PCDTypeNotFound(Exception):
    """
    Exception raised if the ~Model or ~Template Group is not found.
    """


class PCDDuplicatedTypeName(Exception):
    """
    Exception raised if a ~Model or ~Template Type already exists with the same name inside the
    group.
    """


class PCDFolderNotFound(Exception):
    """
    Exception raised if the folder is invalid.
    """

class PCDCannotInstanceTemplateDirectly(Exception):
    """
    Exception raised if the user attempts to instance a ~Template directly.
    """
