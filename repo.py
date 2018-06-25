def _get_item_type(self, item):
    item_type = None

    if isinstance(item, Product):
        item_type = 'product'
    elif isinstance(item, Project):
        item_type = 'project'

    if item.is_library():
        item_type = 'library'
    elif item.is_executable():
        item_type = 'package'

    return item_type
