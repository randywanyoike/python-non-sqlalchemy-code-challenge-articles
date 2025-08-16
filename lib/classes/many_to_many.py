# lib/classes/many_to_many.py

class Author:
    def __init__(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise Exception("Author name must be a non-empty string")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Immutable: ignore attempts to change
        pass

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        if not self.articles():
            return None
        return list({magazine.category for magazine in self.magazines()})


class Magazine:
    all = []

    def __init__(self, name, category):
        if isinstance(name, str) and 2 <= len(name) <= 16:
            self._name = name
        else:
            raise Exception("Magazine name must be a string between 2–16 characters")

        if isinstance(category, str) and len(category) > 0:
            self._category = category
        else:
            raise Exception("Magazine category must be a non-empty string")

        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Only update if valid, otherwise ignore
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        # else: ignore invalid assignment

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        # Only update if valid, otherwise ignore
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        # else: ignore invalid assignment

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list({article.author for article in self.articles()})

    def article_titles(self):
        if not self.articles():
            return None
        return [article.title for article in self.articles()]

    def contributing_authors(self):
        authors = []
        for author in self.contributors():
            count = len([a for a in self.articles() if a.author == author])
            if count > 2:
                authors.append(author)
        return authors if authors else None

    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        return max(cls.all, key=lambda mag: len(mag.articles()))

class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise Exception("Author must be an Author instance")
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be a Magazine instance")
        if not (isinstance(title, str) and 5 <= len(title) <= 50):
            raise Exception("Title must be a string between 5–50 characters")

        self._author = author
        self._magazine = magazine
        self._title = title
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Immutable: ignore attempts to change
        pass

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value
        else:
            raise Exception("Author must be an Author instance")

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value
        else:
            raise Exception("Magazine must be a Magazine instance")
