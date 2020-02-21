def get_document_block_bounds(document):
    """Extract from a parsed image document the bounding boxes of BLOCKS.
       Taken nearly verbatim from the quickstart guide.
    """
    bounds = []
    for page in document.pages:
        for block in page.blocks:
            bounds.append(block.bounding_box)

    return bounds
