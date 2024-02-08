from fastapi import Depends, HTTPException
from starlette import status

from models.product import ProductModel

from core.token import get_current_user
from sqlalchemy import func
from models.user_has_role import User
from core.database import get_db
from sqlalchemy.orm import Session
from schema.review import ReviewCreate


class ReviewService:
    def get_all(db: Session):
        return db.query(ProductModel).all()

    def create_review(
        request: ReviewCreate,
        productId: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        try:
            # Ambil produk yang akan direview
            product = db.query(ProductModel).filter(ProductModel.id == productId).first()

            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Produk tidak ditemukan.",
                )

            # Cek apakah pengguna sudah memberikan ulasan sebelumnya untuk produk ini
            existing_review = db.query(ProductModel).filter(
                ProductModel.user_id == current_user.id,
                ProductModel.product_id == productId
            ).first()

            if existing_review:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Anda sudah memberikan ulasan untuk produk ini.",
                )

            # Buat ulasan baru
            review_new = ProductModel(
                name=current_user.name,
                user_id=current_user.id,
                rating=request.rating,
                comment=request.comment,
                product_id=productId
            )

            # Tambahkan ulasan ke database
            db.add(review_new)
            db.commit()

            # Hitung total rating dan jumlah ulasan saat ini untuk produk
            total_rating, total_reviews = db.query(
                func.sum(ProductModel.rating), func.count(ProductModel.id)
            ).filter(
                ProductModel.product_id == productId
            ).first()

            if total_rating is None:
                total_rating = 0
            if total_reviews is None:
                total_reviews = 0

            # Hitung rating rata-rata saat ini
            current_average_rating = total_rating / total_reviews

            # Kurangkan rating ulasan baru dari total rating saat ini
            total_rating -= request.rating
            total_reviews -= 1

            # Hitung rating rata-rata yang baru
            new_average_rating = current_average_rating if total_reviews == 0 else total_rating / total_reviews

            # Perbarui rating produk di database dengan rating rata-rata yang baru
            product.rating = int(new_average_rating)
            db.commit()
        except Exception as e:
            db.rollback()  # Batalkan transaksi jika terjadi kesalahan
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Terjadi kesalahan saat menambahkan ulasan.",
            )
