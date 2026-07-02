from typing import List

from mcp.server.fastmcp.prompts import base
from pydantic import Field

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
    name="read_document",
    description="This tool reads the document and return its content.",
)
def read_document(doc_id: str = Field(description='Document Id which needs to be read.')):
    if doc_id not in docs:
        raise ValueError(f'Document Id {doc_id} not found.')
    return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_document",
    description="This tool edits the document with the provided new string and return its content.",
)
def edit_document(doc_id: str = Field(description='Document Id which needs to be edited.'),
                  old_string: str = Field(description='Document string which needs to be edited,'
                                                      'should match exactly with document string'),
                  new_string: str = Field(description='Document string which needs to be replaced in the document.')
                  ):
    if doc_id not in docs:
        raise ValueError(f'Document Id {doc_id} not found.')
    docs[doc_id] = docs[doc_id].replace(old_string, new_string)
# TODO: Write a resource to return all doc id's
@mcp.resource(
    uri="docs://documents",
    mime_type="application/json",
)
def list_docs() -> List[str]:
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
    uri="docs://documents/{doc_id}",
    mime_type="plain/text",
)
def send_doc(doc_id: str = Field(description='Document Id which needs to be sent.')) -> str:
    if doc_id not in docs:
        raise ValueError(f'Document Id {doc_id} not found.')
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="format_document",
    description="This tool formats the document in markdown format.",
)
def format_document(
        doc_id: str = Field(description='Document Id which needs to be formatted.'),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
    Use the 'edit_document' tool to edit the document. After the document has been reformatted...
    """

    return [
        base.UserMessage(prompt)
    ]

# TODO: Write a prompt to summarize a doc
@mcp.prompt(
    name="summarise_document",
    description="This tool summarises the document in markdown format.",
)
def format_document(
        doc_id: str = Field(description='Document Id which needs to be summarised.'),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to summarise the document in markdown format.
    The id of the document you need to summarise is:
    <document_id>
    {doc_id}
    </document_id>
    """
    return [
        base.UserMessage(prompt)
    ]

if __name__ == "__main__":
    mcp.run(transport="stdio")
