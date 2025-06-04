# class Article:
#     def __init__(self, author, magazine, title):
#         self.author = author
#         self.magazine = magazine
#         self.title = title
        
# class Author:
#     def __init__(self, name):
#         self.name = name

#     def articles(self):
#         pass

#     def magazines(self):
#         pass

#     def add_article(self, magazine, title):
#         pass

#     def topic_areas(self):
#         pass

# class Magazine:
#     def __init__(self, name, category):
#         self.name = name
#         self.category = category

#     def articles(self):
#         pass

#     def contributors(self):
#         pass

#     def article_titles(self):
#         pass

#     def contributing_authors(self):
#         pass


class Article:
    all = []

    def __init__(self, author, magazine, title):
        self.author = author  # validated by property setter
        self.magazine = magazine  # validated by property setter
        self.title = title  # validated by property setter
        Article.all.append(self)

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise Exception("author must be an instance of Author")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise Exception("magazine must be an instance of Magazine")
        self._magazine = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Title cannot be changed once set
        if hasattr(self, "_title"):
            raise Exception("title cannot be changed")
        if not (isinstance(value, str) and 5 <= len(value) <= 50):
            raise Exception("title must be a string between 5 and 50 characters")
        self._title = value


class Author:
    def __init__(self, name):
        if not (isinstance(name, str) and len(name) > 0):
            raise Exception("name must be a non-empty string")
        if hasattr(self, "_name"):
            raise Exception("name cannot be changed")
        self._name = name

    @property
    def name(self):
        return self._name

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        # Unique magazines the author has articles in
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        # Creates and returns a new Article linked to self and magazine
        return Article(self, magazine, title)

    def topic_areas(self):
        mags = self.magazines()
        if mags:
            return list({mag.category for mag in mags})
        return None


class Magazine:
    all = []

    def __init__(self, name, category):
        self.name = name  # uses setter for validation
        self.category = category  # uses setter for validation
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not (isinstance(value, str) and 2 <= len(value) <= 16):
            raise Exception("name must be a string 2 to 16 characters long")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not (isinstance(value, str) and len(value) > 0):
            raise Exception("category must be a non-empty string")
        self._category = value

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        # Unique authors who have written for this magazine
        return list({article.author for article in self.articles()})

    def article_titles(self):
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        from collections import Counter

        author_counts = Counter(article.author for article in self.articles())
        authors = [author for author, count in author_counts.items() if count > 2]
        return authors if authors else None

    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        # Find magazine with most articles
        return max(
            cls.all, key=lambda mag: len([a for a in Article.all if a.magazine == mag])
        )
