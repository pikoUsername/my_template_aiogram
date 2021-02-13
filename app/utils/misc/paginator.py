class InvalidPage(Exception):
    pass


class Paginator:
    __slots__ = ("object_list", "per_page", "current_page")
    """
    Created like django paginator
    """
    def __init__(self, object_list: list, per_page: int = 5):
        self.object_list = object_list
        self.per_page = per_page
        self.current_page = 0

    def __iter__(self):
        for page_number in self.page_range:
            yield self.page(page_number)

    @property
    def page_range(self) -> range:
        return range(0, len(self.object_list))

    def page(self, page: int):
        result = self.object_list[page]
        if not result:
            raise InvalidPage("Invalid Page")
        return result

    def page_number(self):
        return len(self.object_list)

    def next(self):
        if self.has_next():
            return self.object_list[self.current_page + 1]
        self.current_page += 1
        return self.object_list[self.current_page]

    def has_next(self):
        try:
            return bool(self.page(self.current_page + 1))
        except IndexError:
            return False

    def has_previous(self):
        try:
            return bool(self.page(self.current_page - 1))
        except IndexError:
            return False

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.current_page + 1

    def previous_page_number(self):
        if self.current_page == len(self.object_list):
            return 1
        return self.current_page - 1