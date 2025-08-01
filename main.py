# from flask import Flask
# from users.handlers import user_bp
# from products.handlers import product_bp
# from category.handlers import category_bp
# from tortoise import Tortoise
# from core.settings import TORTOISE_ORM
# import asyncio

# """
# Backend dasturlashda quyidagi http metodlar bor:
#     GET  - Ma'lumotlarni backenddan olib beradi.
#     POST - Ma'lumotni backendga jo'natadi, ushbu ma'lumot backendni vazifasiga qarab obrabotka boladi
#         Misol uchun:
#             Foydalanuvchi qoshish uchun:
#                 {
#                     "username": "Something",
#                     "password": "9999"
#                 }
#     PATCH  - Ma'lumotni ozgartiradi qisman
#     PUT    - Ma'lumotni ozgartiradi qo'liq
#     DELETE - Ma'lumotni ochirib tashlaydi

# """


# app = Flask(__name__)

# app.register_blueprint(user_bp, url_prefix="/users")
# app.register_blueprint(product_bp, url_prefix="/products")
# app.register_blueprint(category_bp, url_prefix="/category")
# # ORM-ni ishga tushurish
# async def init_orm():
#     await Tortoise.init(config=TORTOISE_ORM)
#     await Tortoise.generate_schemas()


# # ORM-ni yopish
# async def close_orm():
#     await Tortoise.close_connections()


# if __name__ == "__main__":
#     asyncio.run(init_orm())  # ORM ni boshlash
#     try:
#         app.run(debug=True)
#     finally:
#         asyncio.run(close_orm())
