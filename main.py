from flask import Flask
# from users.handlers import user_bp
from blogs.handlers import blog_bp
# from category.handlers import category_bp

"""
Backend dasturlashda quyidagi http metodlar bor:
    GET  - Ma'lumotlarni backenddan olib beradi.
    POST - Ma'lumotni backendga jo'natadi, ushbu ma'lumot backendni vazifasiga qarab obrabotka boladi
        Misol uchun:
            Foydalanuvchi qoshish uchun:
                {
                    "username": "Something",
                    "password": "9999"
                }
    PATCH  - Ma'lumotni ozgartiradi qisman
    PUT    - Ma'lumotni ozgartiradi qo'liq
    DELETE - Ma'lumotni ochirib tashlaydi

"""


app = Flask(__name__)

# app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(blog_bp, url_prefix="/blogs")
# app.register_blueprint(category_bp, url_prefix="/category")

if __name__ == "__main__":
    app.run(debug=True)
