from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.article import Article
from app.models.user import User, UserRole
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse
from app.dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/articles", tags=["articles"])



@router.get(
    "/",
    response_model=List[ArticleResponse],
    summary="Get all articles",
    description="Returns a list of all articles. Supports search by title and content, limit and offset."
)
def get_articles(
    search: str | None = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Article)
    #search across both title and content fields
    if search:
        query = query.filter(
            Article.title.ilike(f"%{search}%") |
            Article.content.ilike(f"%{search}%")
        )
    return query.offset(offset).limit(limit).all()

@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
    summary="Get article by ID",
    description="Returns a single article by ID. Available to any authenticated user."
)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post(
    "/",
    response_model=ArticleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create article",
    description="Creates a new article. The currently authenticated user becomes the author."
)
def create_article(
    article_data: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    #author_id is taken from the token, not from the request body
    article = Article(**article_data.model_dump(), author_id=current_user.id)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

@router.put(
    "/{article_id}",
    response_model=ArticleResponse,
    summary="Update article",
    description="Updates an article. A user can update only their own. Editor and admin can update any."
)
def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    is_owner = article.author_id == current_user.id
    is_editor_or_admin = current_user.role in [UserRole.editor, UserRole.admin]

    if not is_owner and not is_editor_or_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # only update fields that were actually sent in the request
    for field, value in article_data.model_dump(exclude_none=True).items():
        setattr(article, field, value)

    db.commit()
    db.refresh(article)
    return article

@router.delete(
    "/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete article",
    description="Deletes an article. A user can delete only their own. Admin can delete any."
)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    is_owner = article.author_id == current_user.id
    is_admin = current_user.role == UserRole.admin

    if not is_owner and not is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.delete(article)
    db.commit()