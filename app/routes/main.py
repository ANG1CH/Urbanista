from venv import logger
from flask import Blueprint, render_template, request

from ..models.post import Post


main = Blueprint('main', __name__)

@main.route('/', methods=['POST', 'GET'])
def index():
    best_posts = Post.query.filter_by(category='best').all()
    recommended_posts = Post.query.filter_by(category='recommended').all()
    return render_template('main/index.html', best_posts=best_posts, recommended_posts=recommended_posts)

@main.route('/about')
def about():
    return render_template('main/about.html')

@main.route('/terms-of-use')
def terms_of_use():
    return render_template('main/terms_of_use.html')

@main.route('/privacy-policy')
def privacy_policy():
    return render_template('main/privacy_policy.html')