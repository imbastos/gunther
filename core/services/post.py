from uuid import UUID

import utils
from core.exceptions.post import NotFoundPostError
from core.models import Post
from core.repositories import PostRepo


class PostService:
    """Serviço responsável pelo gerenciamento de publicações."""

    def __init__(self, post_repo: PostRepo):
        self.post_repo = post_repo

    def get_all(self) -> list[Post]:
        return self.post_repo.get_all()

    def get_by_id(self, post_id: UUID | str) -> Post:
        post = self.post_repo.get_by_id(post_id)

        if post is None:
            raise NotFoundPostError()

        return post

    def get_highlighted(self) -> Post | None:
        return self.post_repo.get_highlighted()

    def create(self, post: Post) -> Post:
        return self.post_repo.create(post)

    def update(self, post: Post) -> Post:
        self.get_by_id(post.id)

        post.updated_at = utils.date_now()
        return self.post_repo.update(post)

    def delete(self, post_id: UUID | str) -> None:
        self.get_by_id(post_id)
        self.post_repo.delete(post_id)
